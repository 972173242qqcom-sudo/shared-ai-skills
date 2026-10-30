#!/usr/bin/env python3
"""Inspect GIF variable delays or merge identical consecutive RGBA states losslessly."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image


def timeline(path):
    states=[]; size=None; loop=None
    with Image.open(path) as gif:
        size=gif.size; loop=gif.info.get('loop')
        for n in range(gif.n_frames):
            gif.seek(n); delay=gif.info.get('duration',0)
            if delay<=0: raise ValueError('Missing/zero frame duration')
            im=gif.convert('RGBA'); raw=bytearray(im.tobytes())
            # Invisible RGB is irrelevant to visual equivalence.
            for i in range(0,len(raw),4):
                if raw[i+3]==0: raw[i:i+3]=b'\0\0\0'
            digest=hashlib.sha256(raw).hexdigest()
            if states and states[-1][0]==digest: states[-1][1]+=delay
            else: states.append([digest,delay])
    return size,loop,states


def merge(src,dst):
    if Path(dst).exists(): raise ValueError('Output exists')
    frames=[];delays=[];last=None
    with Image.open(src) as gif:
        loop=gif.info.get('loop')
        for n in range(gif.n_frames):
            gif.seek(n); im=gif.convert('RGBA'); delay=gif.info.get('duration',0)
            if delay<=0: raise ValueError('Missing/zero delay')
            # Compare complete decoded states, not compressed frame rectangles.
            key=im.tobytes()
            if key==last and delays[-1]+delay<=655350:delays[-1]+=delay
            else:frames.append(im.copy());delays.append(delay);last=key
    kw={'loop':loop} if loop is not None else {}
    frames[0].save(dst,save_all=True,append_images=frames[1:],duration=delays,disposal=2,optimize=False,**kw)
    if timeline(src)!=timeline(dst):
        Path(dst).unlink()
        raise ValueError('RGBA/timing comparison failed; candidate removed. Use palette-preserving block merge instead')
    return {'bytes':Path(dst).stat().st_size,'visual_timeline':'PASS','lossless':True}


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('input');p.add_argument('--merge-to');a=p.parse_args()
    try:
        if a.merge_to:report=merge(a.input,a.merge_to)
        else:
            size,loop,states=timeline(a.input)
            report=dict(dimensions=size,loop=loop,visual_states=len(states),duration_ms=sum(s[1] for s in states),bytes=Path(a.input).stat().st_size)
        print(json.dumps(report,indent=2))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
