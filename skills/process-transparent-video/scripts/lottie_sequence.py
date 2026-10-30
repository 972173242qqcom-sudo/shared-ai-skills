#!/usr/bin/env python3
"""Build and verify embedded lossless PNG-sequence Lottie (this exporter subset)."""
import argparse, base64, hashlib, io, json, math
from pathlib import Path
from PIL import Image, ImageChops


def sources(folder):
    files=sorted(Path(folder).glob('*.png'))
    if not files: raise ValueError('No PNGs; use zero-padded names')
    return files


def verify(path, files=None, max_mb=None):
    path=Path(path); doc=json.loads(path.read_text())
    if doc.get('meta',{}).get('generator')!='transparent-raster-v1':
        raise ValueError('Verifier supports this exporter subset only')
    if doc['fr']<=0 or doc['op']<=0: raise ValueError('Invalid timeline')
    if files and len(files)!=doc['op']: raise ValueError('Frame count mismatch')
    assets={a['id']:a for a in doc['assets']}; cache={}
    for a in assets.values():
        if not a['p'].startswith('data:image/png;base64,'): raise ValueError('Expected embedded PNG')
        im=Image.open(io.BytesIO(base64.b64decode(a['p'].split(',',1)[1],validate=True))).convert('RGBA')
        if im.size!=(a['w'],a['h']): raise ValueError('Asset size mismatch')
        cache[a['id']]=im
    for n in range(doc['op']):
        active=[l for l in doc['layers'] if l['ip']<=n<l['op']]
        if len(active)>1: raise ValueError('Overlapping layers')
        out=Image.new('RGBA',(doc['w'],doc['h']))
        if active:
            l=active[0]; x,y,_=l['ks']['p']['k']
            out.paste(cache[l['refId']],(x,y))
        if files:
            with Image.open(files[n]) as src: src=src.convert('RGBA')
            if src.size!=out.size: raise ValueError('Canvas mismatch')
            if ImageChops.difference(src.getchannel('A'),out.getchannel('A')).getbbox():
                raise ValueError(f'Alpha mismatch frame {n}')
            diff=ImageChops.difference(src.convert('RGB'),out.convert('RGB'))
            mask=src.getchannel('A').point(lambda a:255 if a else 0)
            if ImageChops.multiply(diff,Image.merge('RGB',[mask]*3)).getbbox():
                raise ValueError(f'Visible RGB mismatch frame {n}')
    size=path.stat().st_size
    if max_mb is not None and size>max_mb*1_000_000: raise ValueError(f'Over budget: {size} bytes')
    return dict(bytes=size,frames=doc['op'],duration_seconds=doc['op']/doc['fr'],dimensions=[doc['w'],doc['h']],assets=len(assets),structure='PASS',source_comparison='PASS' if files else 'not_requested',target_player='not_tested',kind='embedded-raster-sequence')


def build(args):
    files=sources(args.frames)
    with Image.open(files[0]) as first: w,h=first.size
    assets=[]; layers=[]; unique={}
    for n,f in enumerate(files):
        with Image.open(f) as im: im=im.convert('RGBA')
        if im.size!=(w,h): raise ValueError('Inconsistent canvas')
        box=im.getchannel('A').getbbox()
        if box is None: continue
        x,y,r,b=box; box=max(0,x-2),max(0,y-2),min(w,r+2),min(h,b+2)
        crop=im.crop(box); buf=io.BytesIO(); crop.save(buf,format='PNG',optimize=True)
        data=buf.getvalue(); key=hashlib.sha256(data).hexdigest()
        if key not in unique:
            ref='image_'+str(len(assets)); unique[key]=ref
            assets.append(dict(id=ref,w=crop.width,h=crop.height,u='',p='data:image/png;base64,'+base64.b64encode(data).decode(),e=1))
        ref=unique[key]; pos=[box[0],box[1],0]
        if layers and layers[-1]['refId']==ref and layers[-1]['ks']['p']['k']==pos and layers[-1]['op']==n:
            layers[-1]['op']=n+1; continue
        layers.append(dict(ddd=0,ind=len(layers)+1,ty=2,nm=f'Frame {n}',refId=ref,sr=1,
            ks={k:dict(a=0,k=v) for k,v in dict(o=100,r=0,p=pos,a=[0,0,0],s=[100,100,100]).items()},
            ao=0,ip=n,op=n+1,st=0,bm=0))
    doc=dict(v='5.7.4',fr=len(files)/args.duration,ip=0,op=len(files),w=w,h=h,nm='Transparent raster sequence',ddd=0,assets=assets,layers=layers,markers=[],meta={'generator':'transparent-raster-v1'})
    out=Path(args.output)
    if out.exists(): raise ValueError('Output exists; choose a new filename')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(doc,separators=(',',':')))
    return verify(out,files,args.max_mb)


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build'); b.add_argument('frames'); b.add_argument('output'); b.add_argument('--duration',type=float,required=True); b.add_argument('--max-mb',type=float)
    v=sub.add_parser('verify');v.add_argument('input');v.add_argument('--frames');v.add_argument('--max-mb',type=float)
    a=p.parse_args()
    try:
        if a.command=='build' and (not math.isfinite(a.duration) or a.duration<=0): raise ValueError('Duration must be positive and finite')
        print(json.dumps(build(a) if a.command=='build' else verify(a.input,sources(a.frames) if a.frames else None,a.max_mb),indent=2))
    except (ValueError,KeyError,OSError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
