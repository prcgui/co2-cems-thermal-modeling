#!/usr/bin/env python3
"""Caracteriza os indicadores horários e os planos de monitoramento de CO2.

Lê os insumos locais e grava tabelas descritivas; não modifica as amostras.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
REPO = BASE.parent
SOURCES = REPO / "references/monitoramento"
CATEGORIES = ("measured_only", "mixed_measured_substitute", "substitute_only",
              "calculated", "missing", "other")
LABELS = {
    "measured": "measured_only",
    "measured and substitute": "mixed_measured_substitute",
    "substitute": "substitute_only",
    "calculated": "calculated",
}
PLAN_GROUPS = {
    "method": "monitoringMethodData",
    "formula": "monitoringFormulaData",
    "system": "monitoringSystemData",
    "component": "componentData",
    "span": "monitoringSpanData",
}
FIELDS = {
    "method": ["parameterCode", "monitoringMethodCode", "substituteDataCode", "bypassApproachCode"],
    "formula": ["parameterCode", "formulaId", "formulaCode", "formulaText"],
    "system": ["monitoringSystemId", "systemTypeCode", "systemDesignationCode", "fuelCode"],
    "component": ["componentId", "componentTypeCode", "sampleAcquisitionMethodCode",
                  "basisCode", "manufacturer", "modelVersion", "serialNumber"],
    "span": ["componentTypeCode", "spanScaleCode", "spanMethodCode", "mpcValue", "mpfValue",
             "spanValue", "fullScaleRange", "spanUnitsOfMeasureCode",
             "flowSpanValue", "flowFullScaleRange"],
    "system_component": ["componentId"],
    "analyzer_range": ["analyzerRangeCode", "dualRangeIndicator"],
}
INTERVAL_FIELDS = ["beginDate", "beginHour", "endDate", "endHour"]
COMMON_KEY_FIELDS = sorted(set(sum(FIELDS.values(), [])) | {"begin", "end"})


def norm_key(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def get(record, name, default=None):
    wanted = norm_key(name)
    for k, v in record.items():
        if norm_key(k) == wanted:
            return v
    return default


def norm_id(x):
    if x is None or pd.isna(x):
        return None
    s = str(x).strip().upper()
    if re.fullmatch(r"\d+(?:\.0+)?", s):
        return str(int(float(s)))
    return s


def canon(x):
    if x is None or (not isinstance(x, (list, dict)) and pd.isna(x)):
        return ""
    if isinstance(x, pd.Timestamp):
        return x.isoformat()
    s = str(x).strip()
    if re.fullmatch(r"-?\d+\.0+", s):
        return str(int(float(s)))
    return s


def timestamp_from_date_hour(date, hour, *, is_end=False):
    """EndHour is the last effective hour, so comparisons use <= end."""
    if date is None or not str(date).strip():
        if is_end:
            return None, ""
        raise ValueError("missing beginDate")
    d = pd.to_datetime(str(date), errors="raise")
    if d.tzinfo is not None:
        # Plan date/hour fields are local reporting dates, not UTC instants.
        d = d.tz_localize(None)
    d = d.normalize()
    note = ""
    if hour is None or str(hour).strip() == "":
        hour = 23 if is_end else 0
        note = "endHour_assumed_23" if is_end else "beginHour_assumed_0"
    n = float(hour)
    if not n.is_integer() or n < 0 or n > 23:
        raise ValueError("hour outside 0..23")
    return d + pd.Timedelta(hours=int(n)), note


def interval(record):
    try:
        start, note1 = timestamp_from_date_hour(get(record, "beginDate"), get(record, "beginHour"))
        end, note2 = timestamp_from_date_hour(get(record, "endDate"), get(record, "endHour"), is_end=True)
        if end is not None and end < start:
            raise ValueError("end before begin")
        return start, end, "valid", ";".join(x for x in (note1, note2) if x)
    except (ValueError, TypeError, OverflowError):
        return None, None, "invalid", "invalid_or_missing_interval"


def xml_record(element):
    result = {}
    for child in element:
        tag = child.tag.split("}")[-1]
        if len(child) == 0:
            result[tag] = child.text
        else:
            value = xml_record(child)
            result.setdefault(tag, []).append(value)
    return result


def list_value(record, key):
    v = get(record, key, [])
    return v if isinstance(v, list) else ([] if v is None else [v])


def plan_documents(path):
    """Lê planos JSON/XML ou os membros XML de um arquivo compactado."""
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as z:
            for name in sorted(z.namelist()):
                if name.lower().endswith(".xml"):
                    yield name, xml_record(ET.fromstring(z.read(name))), "xml"
    elif path.suffix.lower() == ".xml":
        yield path.name, xml_record(ET.parse(path).getroot()), "xml"
    else:
        doc = json.loads(path.read_text(encoding="utf-8"))
        plans = doc if isinstance(doc, list) else doc.get("items", [doc])
        for i, plan in enumerate(plans):
            yield f"{path.name}#{i}", plan, "json"


def flatten_plan(path, facility, unit):
    rows = []
    source = path.stem
    for member, plan, fmt in plan_documents(path):
        oris = norm_id(get(plan, "orisCode", get(plan, "facilityId")))
        if oris != norm_id(facility):
            continue
        locations = list_value(plan, "monitoringLocationData")
        for loc in locations:
            if norm_id(get(loc, "unitId")) != norm_id(unit) or get(loc, "stackPipeId"):
                continue
            # Legacy EPA XML nests the unit's plan sections under UnitData,
            # whereas the current JSON schema places them on the location.
            sections = dict(loc)
            unit_data = list_value(loc, "unitData")
            if len(unit_data) > 1:
                raise ValueError(f"Ambiguous UnitData blocks in {path.name}: {member}")
            if unit_data:
                sections.update(unit_data[0])
            components = {
                canon(get(c, "componentId")): c for c in list_value(sections, "componentData")
            }

            def add(kind, item, parent=None):
                row = {"source": source, "source_member": member, "kind": kind,
                       "facility_id": str(facility), "unit_id": str(unit)}
                row.update({key: get(item, key) for key in FIELDS[kind]})
                row.update({key: get(item, key) for key in INTERVAL_FIELDS})
                if kind != "component":
                    row["begin"], row["end"], row["interval_status"], row["interval_note"] = interval(item)
                if parent:
                    row.update(parent)
                rows.append(row)

            for kind, group in PLAN_GROUPS.items():
                for item in list_value(sections, group):
                    add(kind, item)
                    if kind == "system":
                        parent = {k: get(item, k) for k in FIELDS["system"]}
                        for assoc in list_value(item, "monitoringSystemComponentData"):
                            c = components.get(canon(get(assoc, "componentId")), {})
                            detail = {k: get(c, k) for k in FIELDS["component"]}
                            add("system_component", assoc, {**parent, **detail})
                    elif kind == "component":
                        for ar in list_value(item, "analyzerRangeData"):
                            add("analyzer_range", ar, {
                                "componentId": get(item, "componentId"),
                                "componentTypeCode": get(item, "componentTypeCode"),
                            })
    if not rows:
        raise ValueError(f"No direct Unit {unit}, Facility {facility} in plan {path.name}")
    if not any(r["kind"] == "method" and r.get("parameterCode") in ("CO2", "CO2M") for r in rows):
        raise ValueError(f"No CO2 monitoring-method section parsed in {path.name}")
    return rows


def indicator_category(value):
    if value is None or pd.isna(value) or not str(value).strip():
        return "missing"
    return LABELS.get(str(value).strip().casefold(), "other")


def pct(n, denominator):
    return 100.0 * int(n) / int(denominator) if denominator else None


def sum_mass(values):
    return float(values.sum(min_count=1)) if values.notna().any() else None


def summarize(frame, period):
    op = frame["_op"]
    on, off = op.gt(0), op.eq(0)
    mass, load, cat = frame["_co2"], frame["_load"], frame["_category"]
    result = {
        "period": period, "n_rows": len(frame), "n_on": int(on.sum()), "n_off": int(off.sum()),
        "n_operating_time_missing": int(op.isna().sum()),
        "n_operating_time_outside_0_1": int(((op < 0) | (op > 1)).sum()),
        "n_co2_missing_on": int((on & mass.isna()).sum()),
        "n_co2_negative_on": int((on & mass.lt(0)).sum()),
        "n_load_missing_on": int((on & load.isna()).sum()),
        "n_load_zero_on": int((on & load.eq(0)).sum()),
        "n_co2_positive_off": int((off & mass.gt(0)).sum()),
        "n_indicator_missing_off": int((off & cat.eq("missing")).sum()),
        "co2_mass_sum_on_short_tons": sum_mass(mass[on]),
    }
    for category in CATEGORIES:
        selected = on & cat.eq(category)
        result[f"n_{category}_on"] = int(selected.sum())
        result[f"pct_{category}_of_on"] = pct(selected.sum(), on.sum())
        result[f"co2_mass_in_{category}_on_hours_short_tons"] = sum_mass(mass[selected])
    any_sub = on & cat.isin(["mixed_measured_substitute", "substitute_only"])
    result["n_any_substitute_on"] = int(any_sub.sum())
    result["pct_any_substitute_of_on"] = pct(any_sub.sum(), on.sum())
    legacy = frame["_indicator"].fillna("").astype(str).str.strip().str.lower().str.contains("measured", regex=False)
    result["n_legacy_contains_measured_on"] = int((on & legacy).sum())
    result["pct_legacy_contains_measured_of_on"] = pct((on & legacy).sum(), on.sum())
    return result


def mask_for_intervals(times, records):
    mask = np.zeros(len(times), dtype=bool)
    for record in records:
        if record.get("interval_status") != "valid":
            continue
        selected = times.ge(record["begin"])
        if record["end"] is not None and not pd.isna(record["end"]):
            selected &= times.le(record["end"])
        mask |= selected.fillna(False).to_numpy()
    return mask


def coverage_summary(source, methods, year, hourly):
    calendar = pd.Series(pd.date_range(f"{year}-01-01", f"{year}-12-31 23:00:00", freq="h"))
    co2 = [r for r in methods if r.get("parameterCode") in ["CO2", "CO2M"]]
    cem = [r for r in co2 if r.get("parameterCode") == "CO2" and r.get("monitoringMethodCode") == "CEM"]
    covered = mask_for_intervals(calendar, co2)
    cem_covered = mask_for_intervals(calendar, cem)
    signatures = {}
    for record in co2:
        key = (canon(record.get("parameterCode")), canon(record.get("monitoringMethodCode")))
        signatures.setdefault(key, []).append(record)
    number_active = np.zeros(len(calendar), dtype=int)
    for recs in signatures.values():
        number_active += mask_for_intervals(calendar, recs)
    on = hourly["_op"].gt(0).to_numpy()
    hourly_cem = mask_for_intervals(hourly["_timestamp"], cem)
    return {
        "source": source, "year": year, "expected_calendar_hours": len(calendar),
        "co2_cem_declared_hours": int(cem_covered.sum()),
        "pct_calendar_with_co2_cem": pct(cem_covered.sum(), len(calendar)),
        "co2_method_declared_hours": int(covered.sum()),
        "hours_without_co2_method": int((~covered).sum()),
        "hours_with_multiple_co2_method_signatures": int((number_active > 1).sum()),
        "n_on": int(on.sum()), "n_on_with_declared_cem": int((on & hourly_cem).sum()),
        "n_on_without_declared_cem": int((on & ~hourly_cem).sum()),
        "invalid_co2_intervals": sum(r["interval_status"] != "valid" for r in co2),
    }


def component_coverage_summary(source, records, year, hourly):
    """Describe association continuity; no claim of calibration or accuracy."""
    calendar = pd.Series(pd.date_range(f"{year}-01-01", f"{year}-12-31 23:00:00", freq="h"))
    relevant = [r for r in records if r["kind"] == "system_component" and r.get("systemTypeCode") in ("CO2", "FLOW")]
    groups = {}
    for record in relevant:
        key = (canon(record.get("monitoringSystemId")), record.get("systemTypeCode"), record.get("componentTypeCode"))
        groups.setdefault(key, []).append(record)
    output = []
    for (system_id, system_type, component_type), associations in sorted(groups.items()):
        by_component = {}
        for record in associations:
            by_component.setdefault(canon(record.get("componentId")), []).append(record)
        active = np.zeros(len(calendar), dtype=int)
        for same_component in by_component.values():
            active += mask_for_intervals(calendar, same_component)
        hourly_covered = mask_for_intervals(hourly["_timestamp"], associations)
        on = hourly["_op"].gt(0).to_numpy()
        observed_ids = [cid for cid, recs in by_component.items() if mask_for_intervals(calendar, recs).any()]
        output.append({
            "source": source, "year": year, "monitoringSystemId": system_id,
            "systemTypeCode": system_type, "componentTypeCode": component_type,
            "expected_calendar_hours": len(calendar),
            "hours_with_declared_component": int((active > 0).sum()),
            "hours_without_declared_component": int((active == 0).sum()),
            "hours_with_multiple_component_ids": int((active > 1).sum()),
            "component_ids_active_in_year": ";".join(sorted(observed_ids)),
            "n_on_without_declared_component": int((on & ~hourly_covered).sum()),
            "invalid_association_intervals": sum(r["interval_status"] != "valid" for r in associations),
        })
    return output


def contiguous_ranges(times, **extra):
    ordered = pd.DatetimeIndex(times).dropna().unique().sort_values()
    if len(ordered) == 0:
        return []
    groups = pd.Series(ordered).diff().ne(pd.Timedelta(hours=1)).cumsum()
    return [{**extra, "begin": x.min().isoformat(), "end": x.max().isoformat(), "n_hours": len(x)}
            for _, x in pd.Series(ordered).groupby(groups)]


def load_year(path, year, facility, unit):
    df = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
    required = ["Facility ID", "Unit ID", "Date", "Hour", "Operating Time",
                "Gross Load (MW)", "CO2 Mass (short tons)"]
    absent = sorted(set(required) - set(df.columns))
    if absent:
        raise ValueError(f"{path.name}: required columns missing: {absent}")
    target = df["Facility ID"].map(norm_id).eq(norm_id(facility)) & df["Unit ID"].map(norm_id).eq(norm_id(unit))
    if not target.all():
        raise ValueError(f"{path.name}: contains records outside the target unit; no rows silently removed")
    dates = pd.to_datetime(df["Date"], errors="coerce").dt.normalize()
    hours = pd.to_numeric(df["Hour"], errors="coerce")
    valid_hour = hours.notna() & hours.between(0, 23) & hours.mod(1).eq(0)
    ts = dates + pd.to_timedelta(hours.where(valid_hour), unit="h")
    df["_timestamp"] = ts
    df["_op"] = pd.to_numeric(df["Operating Time"], errors="coerce")
    df["_co2"] = pd.to_numeric(df["CO2 Mass (short tons)"], errors="coerce")
    df["_load"] = pd.to_numeric(df["Gross Load (MW)"], errors="coerce")
    has_indicator = "CO2 Mass Measure Indicator" in df
    df["_indicator"] = df["CO2 Mass Measure Indicator"] if has_indicator else None
    df["_category"] = df["_indicator"].map(indicator_category)
    in_year = ts.dt.year.eq(year)
    # A agregação anual não modifica as amostras dos experimentos.
    frame = df.loc[in_year].copy()
    expected = pd.date_range(f"{year}-01-01", f"{year}-12-31 23:00:00", freq="h")
    present = pd.DatetimeIndex(frame["_timestamp"]).unique()
    missing = expected.difference(present)
    stored_ts_mismatch = None
    if "timestamp" in df:
        stored = pd.to_datetime(df["timestamp"], errors="coerce")
        stored_ts_mismatch = int((~(stored.eq(ts) | (stored.isna() & ts.isna()))).sum())
    summary = summarize(frame, str(year))
    summary.update({
        "year": year, "file_name": path.name, "input_rows": len(df),
        "expected_calendar_hours": len(expected), "reported_unique_hours": len(present),
        "calendar_gap_hours": len(missing), "pct_calendar_coverage": pct(len(present), len(expected)),
        "duplicate_extra_rows": int(frame["_timestamp"].duplicated().sum()),
        "rows_in_duplicate_timestamps": int(frame["_timestamp"].duplicated(keep=False).sum()),
        "invalid_timestamp_rows": int(ts.isna().sum()),
        "timestamp_outside_file_year_rows": int((ts.notna() & ~in_year).sum()),
        "stored_timestamp_disagreement_rows": stored_ts_mismatch,
        "indicator_column_present": has_indicator,
    })
    return frame, summary


def raw_label_counts(frame, year):
    work = frame.copy()
    work["_raw_label"] = work["_indicator"].fillna("<missing>").astype(str)
    records = []
    for (label, cat), group in work.groupby(["_raw_label", "_category"], dropna=False):
        on = group["_op"].gt(0)
        records.append({
            "year": year, "raw_indicator": label, "indicator_category": cat,
            "n_all": len(group), "n_on": int(on.sum()), "n_off": int(group["_op"].eq(0).sum()),
            "co2_mass_in_on_hours_short_tons": sum_mass(group.loc[on, "_co2"]),
        })
    return records


def write_csv(path, rows):
    if isinstance(rows, pd.DataFrame):
        rows.to_csv(path, index=False)
    else:
        pd.DataFrame(rows).to_csv(path, index=False)


def snapshot_comparison(rows, sources):
    relevant = [r for r in rows if
                (r["kind"] in ["method", "formula"] and str(r.get("parameterCode", "")).startswith("CO2"))
                or (r["kind"] in ["system", "system_component"] and r.get("systemTypeCode") in ["CO2", "FLOW"])
                or (r["kind"] in ["component", "span", "analyzer_range"] and r.get("componentTypeCode") in ["CO2", "FLOW"])]
    def fingerprint(r):
        return tuple([r["kind"]] + [canon(r.get(k)) for k in COMMON_KEY_FIELDS])
    sets = {source: {fingerprint(r) for r in relevant if r["source"] == source} for source in sources}
    output = []
    for i, a in enumerate(sources):
        for b in sources[i + 1:]:
            output.append({"source_a": a, "source_b": b, "relevant_unique_rows_a": len(sets[a]),
                           "relevant_unique_rows_b": len(sets[b]), "common_rows": len(sets[a] & sets[b]),
                           "only_in_a": len(sets[a] - sets[b]), "only_in_b": len(sets[b] - sets[a]),
                           "equivalent_on_compared_fields": sets[a] == sets[b]})
    return output


def run(args):
    out = Path(args.output_dir).resolve()
    hourly_dir = Path(args.hourly_dir).resolve()
    if out == hourly_dir or hourly_dir in out.parents:
        raise ValueError("A pasta de resultados deve ser diferente da pasta dos dados horários.")
    plan_rows = []
    for path in args.plan:
        plan_rows += flatten_plan(Path(path).resolve(), args.facility, args.unit)
    source_names = sorted({row["source"] for row in plan_rows})
    frames, annual, monthly, counts, coverage, component_coverage = [], [], [], [], [], []
    for year in range(args.start_year, args.end_year + 1):
        paths = [hourly_dir / f"iatan_unit2_{year}{suffix}" for suffix in (".parquet", ".csv")]
        paths = [path for path in paths if path.exists()]
        if len(paths) != 1:
            raise ValueError(f"Esperado exatamente um arquivo anual de {year}; encontrados {len(paths)}.")
        frame, summary = load_year(paths[0], year, args.facility, args.unit)
        frames.append(frame)
        annual.append(summary)
        counts += raw_label_counts(frame, year)
        for month, group in frame.groupby(frame["_timestamp"].dt.to_period("M")):
            monthly.append(summarize(group, str(month)))
        for source in source_names:
            methods = [row for row in plan_rows if row["source"] == source and row["kind"] == "method"]
            coverage.append(coverage_summary(source, methods, year, frame))
            component_coverage += component_coverage_summary(
                source, [row for row in plan_rows if row["source"] == source], year, frame)
    all_hourly = pd.concat(frames, ignore_index=True).sort_values("_timestamp").reset_index(drop=True)
    cohorts = []
    for name, years in [("2011-2022", range(2011, 2023)), ("2023-2024", [2023, 2024]),
                        ("2025", [2025]), ("all_years", range(args.start_year, args.end_year + 1))]:
        cohorts.append(summarize(all_hourly[all_hourly["_timestamp"].dt.year.isin(years)], name))
    any_sub = all_hourly["_op"].gt(0) & all_hourly["_category"].isin(["mixed_measured_substitute", "substitute_only"])
    episodes = []
    if all_hourly["_timestamp"].duplicated().any():
        raise ValueError("Há horários duplicados; resolva a origem antes de calcular os episódios de substituição.")
    for episode in contiguous_ranges(all_hourly.loc[any_sub, "_timestamp"]):
        selected = all_hourly["_timestamp"].between(pd.Timestamp(episode["begin"]), pd.Timestamp(episode["end"]))
        episode.update(summarize(all_hourly[selected], episode["begin"] + "/" + episode["end"]))
        episodes.append(episode)
    tables = {
        "annual_measurement_summary.csv": annual,
        "monthly_measurement_summary.csv": monthly,
        "cohort_measurement_summary.csv": cohorts,
        "indicator_raw_counts.csv": counts,
        "monitoring_plan_coverage.csv": coverage,
        "component_coverage.csv": component_coverage,
        "substitution_episodes.csv": episodes,
        "snapshot_comparison.csv": snapshot_comparison(plan_rows, source_names),
    }
    for kind in FIELDS:
        tables[f"plan_{kind}_history.csv"] = [row for row in plan_rows if row["kind"] == kind]
    instrument = [row for row in plan_rows if row["kind"] == "system_component" and row.get("systemTypeCode") in ("CO2", "FLOW")]
    tables["co2_flow_component_changes.csv"] = [row for row in instrument if row.get("begin") is not None and args.start_year <= row["begin"].year <= args.end_year]
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write_csv(out / name, rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hourly-dir", default=str(REPO / "data/interim/03A04_multiyear"), help="Pasta com arquivos anuais Parquet ou CSV.")
    parser.add_argument("--plan", action="append", help="Plano XML/JSON; repita para comparar fontes.")
    parser.add_argument("--output-dir", default=str(REPO / "outputs/tables/monitoramento"))
    parser.add_argument("--facility", default="6065")
    parser.add_argument("--unit", default="2")
    parser.add_argument("--start-year", type=int, default=2011)
    parser.add_argument("--end-year", type=int, default=2025)
    args = parser.parse_args()
    if args.start_year > args.end_year:
        parser.error("O ano inicial deve ser menor ou igual ao ano final.")
    if args.plan is None:
        args.plan = [str(SOURCES / "original_plan_unit2.xml"), str(SOURCES / "current_plan_unit2.json")]
    try:
        run(args)
    except (ValueError, OSError, KeyError, RuntimeError):
        print("Não foi possível concluir os cálculos. Confira os arquivos e os argumentos.", file=sys.stderr)
        return 1
    print("Tabelas de monitoramento geradas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
