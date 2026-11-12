"""Portable paths and publication metadata for the project deliverables."""
from pathlib import Path
import os, re, sys, io

def project_root():
    override=os.environ.get('CO2_PROJECT_ROOT') or os.environ.get('PROJECT_ROOT')
    if override:
        root=Path(override).expanduser().resolve()
        if not (root/'notebooks').is_dir():
            raise FileNotFoundError('A raiz informada precisa conter notebooks/.')
        return root
    for root in (Path.cwd(), *Path.cwd().parents):
        if (root/'notebooks').is_dir() and (root/'pipeline').is_dir():return root
    raise FileNotFoundError('Abra o notebook dentro do projeto ou defina CO2_PROJECT_ROOT.')


def get_epa_api_key():
    value=os.environ.get('EPA_API_KEY','').strip()
    if value:return value
    try:
        from google.colab import userdata
        return str(userdata.get('EPA_API_KEY') or '').strip()
    except (ImportError,KeyError):return ''

def relative_path(value,root):
    path=Path(value)
    try:return path.resolve().relative_to(Path(root).resolve()).as_posix() or '.'
    except ValueError:return path.name

def public_text(value,root):
    text=str(value)
    urls=[]
    def hide(m):urls.append(m.group());return f'URLTOKEN{len(urls)-1}END'
    text=re.sub(r'https?://[^\s\"\'<>]+',hide,text)
    roots=[str(Path(root).resolve()),str(Path.home())]
    for prefix in sorted(roots,key=len,reverse=True):
        for variant in {prefix,prefix.replace('\\','/'),prefix.replace('\\','\\\\')}:
            text=text.replace(variant,'.')
    text=re.sub(r'(?i)[a-z]:[\\/]+[^\n\r\"\'<>]*',lambda m:m.group().replace('\\','/').split('/')[-1],text)
    text=re.sub(r'(?<![:\w])/(?:[\w.~-]+/)+[\w.~+-]+',lambda m:Path(m.group()).name,text)
    for i,url in enumerate(urls):text=text.replace(f'URLTOKEN{i}END',url)
    return text

def public_value(value,root):
    if isinstance(value,str):return public_text(value,root)
    if isinstance(value,dict):return {public_text(k,root):public_value(v,root) for k,v in value.items()}
    if isinstance(value,list):return [public_value(v,root) for v in value]
    return value

class _Output(io.TextIOBase):
    def __init__(self,target,root):self.target=target;self.root=root
    def write(self,text):self.target.write(public_text(text,self.root));return len(text)
    def flush(self):return self.target.flush()
    @property
    def encoding(self):return self.target.encoding
    def isatty(self):return self.target.isatty()

def configure_output(root):
    for name in ['stdout','stderr']:
        target=getattr(sys,name)
        if not isinstance(target,_Output):setattr(sys,name,_Output(target,root))

def save_figure(figure,path,*args,**kwargs):
    suffix=Path(path).suffix.lower()
    metadata=dict(kwargs.pop('metadata',{}) or {})
    if suffix=='.png':metadata.update(Software=None)
    elif suffix=='.svg':metadata.update(Creator=None,Date=None)
    elif suffix=='.pdf':metadata.update(Creator=None,Producer=None,CreationDate=None,ModDate=None)
    if suffix in ['.png','.svg','.pdf']:kwargs['metadata']=metadata
    return figure.savefig(path,*args,**kwargs)

def prepare_notebook(nb,root):
    nb['metadata']={k:v for k,v in nb.get('metadata',{}).items() if k in ['kernelspec','language_info','projeto','reproduction']}
    for cell in nb.get('cells',[]):
        cell['metadata']={}
        for output in cell.get('outputs',[]):
            output.pop('transient',None)
            if 'metadata' in output:output['metadata']={}
            if 'text' in output:output['text']=public_value(output['text'],root)
            if 'traceback' in output:output['traceback']=public_value(output['traceback'],root)
            if 'data' in output:
                for key in list(output['data']):
                    if key.startswith('text/') or key=='application/json':output['data'][key]=public_value(output['data'][key],root)
                if 'text/html' in output['data']:
                    value=output['data']['text/html']
                    value=''.join(value) if isinstance(value,list) else value
                    value=re.sub(r'<(script|style|button)\b[^>]*>.*?</\1>','',value,flags=re.I|re.S)
                    value=re.sub(r'\s+(?:class|id|data-[\w-]+)="[^"]*"','',value)
                    output['data']['text/html']=value
    return nb
