#!/usr/bin/env python3
"""Synthetic regression fixtures; no user media or external services."""
import argparse, importlib.util, json, tempfile, subprocess, contextlib, io
from pathlib import Path
from PIL import Image


def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def main():
    lot=module('lottie_sequence'); gif=module('gif_timeline')
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp);frames=root/'frames';frames.mkdir()
        # Repeated asset, changed position, partial Alpha, black detail, empty frame.
        for n in range(5):
            im=Image.new('RGBA',(40,32))
            if n<4:
                x=2 if n<2 else 15
                im.paste((15,128,250,127),(x,5,x+5,12));im.putpixel((x+1,6),(0,0,0,255))
            im.save(frames/f'{n:06d}.png')
        out=root/'animation.json'
        report=lot.build(argparse.Namespace(frames=str(frames),output=str(out),duration=3,max_mb=1))
        assert report['frames']==5 and report['assets']==1 and report['source_comparison']=='PASS'
        assert report['duration_seconds']==3
        doc=json.loads(out.read_text());assert len(doc['layers'])==2
        doc['layers'][0]['ks']['p']['k'][0]+=1
        broken=root/'broken.json';broken.write_text(json.dumps(doc))
        try:lot.verify(broken,lot.sources(frames))
        except ValueError:pass
        else:raise AssertionError('Placement corruption accepted')
        try:lot.verify(out,max_mb=.000001)
        except ValueError:pass
        else:raise AssertionError('Budget violation accepted')
        # Variable delay: red for 20ms, blue for 980ms. Midpoint must be blue.
        a=Image.new('RGBA',(16,16),(255,0,0,255));b=Image.new('RGBA',(16,16),(0,0,255,255))
        src=root/'variable.gif';a.save(src,save_all=True,append_images=[b],duration=[20,980],loop=0,disposal=2)
        assert sum(s[1] for s in gif.timeline(src)[2])==1000
        merged=root/'merged.gif';assert gif.merge(src,merged)['lossless']
        video=module('transparent_video');qc=root/'qc';video.qc_frames(src,qc)
        samples=list(qc.glob('*0.500_alpha.png'));assert len(samples)==1
        # Exact production QC must select blue at 0.5s, not frame 0 by average FPS.
        composite=Image.open(next(qc.glob('*0.500_light.png'))).convert('RGB')
        r,g,bl=composite.getpixel((8,8));assert bl>200 and r<30,(r,g,bl)
        sequence=root/'colors';sequence.mkdir()
        for n in range(10):
            Image.new('RGBA',(32,32),(20*n,30,100,128)).save(sequence/f'{n:03d}.png')
        source=root/'source.mov'
        subprocess.run([video.FFMPEG,'-v','error','-y','-framerate','10','-i',str(sequence/'%03d.png'),
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-frames:v','10','-t','1',
                        '-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-c:a','pcm_s16le',str(source)],check=True)
        for duration in (.5,.37,2):
            output=root/f'retimed_{duration}.mov'
            args=video.parser().parse_args(['encode',str(source),str(output),'--format','prores4444','--duration',str(duration)])
            with contextlib.redirect_stdout(io.StringIO()):video.encode_cmd(args)
            raw=subprocess.run([video.FFMPEG,'-v','error','-i',str(output),'-f','rawvideo','-pix_fmt','rgba','-'],check=True,capture_output=True).stdout
            assert len(raw)==10*32*32*4
            for n in range(10):
                center=n*32*32*4+(16*32+16)*4
                assert abs(raw[center]-20*n)<8,(duration,n,raw[center])
            detail=video.probe(output)
            for stream in detail['streams']:
                assert abs(float(stream['duration'])-duration)<.03,(duration,stream['duration'])
    print('PASS: Lottie RGBA/crop/dedup/empty/timing/budget/corruption; GIF variable-delay QC/merge; MOV full-frame integer/fractional/slow retime + audio')
if __name__=='__main__':main()
