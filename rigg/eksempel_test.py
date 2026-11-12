# Test: animert Dashman med lærerens stemme (11 s fra Energibevaring). Leppesynk fra lyden, blunking, pust, poser.
import json, numpy as np, soundfile as sf, subprocess, os
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from scipy import ndimage
H='/home/claude/work/rigg'; R=json.load(open(f'{H}/rigg.json'))
FPS=30; T0,T1=27.9,39.0
x,sr=sf.read('/home/claude/work/eb/tale.wav',dtype='float32'); x=x[int(T0*sr):int(T1*sr)]
sf.write(f'{H}/test/lyd.wav',x,sr)
N=int((T1-T0)*FPS)
# --- munnform per bilde: lydstyrke + spektral tyngdepunkt
form=[]
for i in range(N):
    s=x[int(i/FPS*sr):int((i+1)/FPS*sr)]
    d=20*np.log10(np.sqrt((s**2).mean())+1e-9)
    if d<-38: form.append('lukket'); continue
    X=np.abs(np.fft.rfft(s*np.hanning(len(s)))); f=np.fft.rfftfreq(len(s),1/sr); m=(f>100)&(f<5000)
    c=(X[m]*f[m]).sum()/(X[m].sum()+1e-9)
    form.append('o' if c<700 else 'aapen' if c<1500 else 'smil_tenner')
for i in range(1,N-1):   # ikke bytt for ofte
    if form[i-1]==form[i+1]!=form[i]: form[i]=form[i-1]
MUNN={k:Image.open(f'{H}/ut/munn_{k}.png') for k in ('lukket','o','aapen','smil_tenner')}
OYNE_L=Image.open(f'{H}/ut/oyne_lukket_v.png')
def tykk(im,k=3):
    a=im.split()[3].filter(ImageFilter.MaxFilter(k)); out=Image.new('RGBA',im.size,(236,239,230,0)); out.putalpha(a); return out
POSER={}
def pose(n,munn,blunk):
    key=(n,munn,blunk)
    if key in POSER: return POSER[key]
    im=Image.open(f'{H}/ut/{n}.png').convert('RGBA'); a=np.asarray(im).copy(); r=R[n]
    lab,_=ndimage.label(a[...,3]>40,structure=np.ones((3,3)))
    def fjern(komp):
        for k in komp: a[lab==k,3]=0
    if 'munn' in r and munn!='orig':
        fjern(r['munn_komp'])
    if blunk and 'oyne' in r: fjern(r['oyne_komp'])
    im=Image.fromarray(a)
    if 'munn' in r and munn!='orig':
        m=MUNN[munn]; x0,y0,x1,y1=r['munn']; w=int((x1-x0)*(1.0 if munn=='lukket' else 0.9 if munn=='smil_tenner' else 0.55 if munn=='o' else 0.8))
        w=max(w,10); m=m.resize((w,max(4,int(m.height*w/m.width))),Image.LANCZOS)
        im.alpha_composite(m,(int((x0+x1)/2-m.width/2),int((y0+y1)/2-m.height/2)))
    if blunk and 'oyne' in r:
        x0,y0,x1,y1=r['oyne']; o=OYNE_L.resize((int((x1-x0)*0.45),int(OYNE_L.height*(x1-x0)*0.45/OYNE_L.width)))
        for cx in (x0+(x1-x0)*0.27,x0+(x1-x0)*0.73): im.alpha_composite(o,(int(cx-o.width/2),int((y0+y1)/2-o.height/3)))
    im=tykk(im)
    POSER[key]=im; return im
# --- manus: (start, slutt, positur, speil)
MANUS=[(0,2.25,'noytral',False),(2.25,4.0,'peker_tavla',True),(4.0,8.9,'noytral_kopp',False),(8.9,11.2,'armer_opp',False)]
BLUNK=[1.3,5.6,7.9]
HOYDE=680; BUNN=1050; MIDT=1560
fnt=ImageFont.truetype('/home/claude/videoer/_verktoy/ArchitectsDaughter-Norsk.ttf',64)
fnt2=ImageFont.truetype('/home/claude/videoer/_verktoy/ArchitectsDaughter-Norsk.ttf',96)
bg=Image.new('RGBA',(1920,1080),(13,17,16,255))
try:
    tb=Image.open('/home/claude/videoer/_verktoy/tavle-bakgrunn.webp').convert('RGBA').resize((1920,1080)); tb.putalpha(23); bg.alpha_composite(tb)
except Exception as e: print(e)
logo=Image.open('/home/claude/videoer/_verktoy/drnormann-logo.png').convert('RGBA'); logo=logo.resize((int(logo.width*90/logo.height),90))
bg.alpha_composite(logo,(1920-30-logo.width,30))
os.makedirs(f'{H}/test/b',exist_ok=True)
for i in range(N):
    t=i/FPS; fr=bg.copy(); d=ImageDraw.Draw(fr)
    d.text((120,120),'Energien forsvinner ikke …',font=fnt,fill=(236,239,230,255))
    if t>2.3:
        d.text((160,300),'E',font=fnt2,fill=(86,215,184,255)); d.text((215,350),'p',font=fnt,fill=(86,215,184,255))
        d.text((290,315),'→',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',80),fill=(236,239,230,255))
        d.text((430,300),'E',font=fnt2,fill=(241,156,44,255)); d.text((485,350),'k',font=fnt,fill=(241,156,44,255))
        d.text((600,320),'den bytter form!',font=fnt,fill=(238,228,98,255))
    if t>9.3:
        s=min(1,(t-9.3)/0.15)*1.0+0.15*max(0,1-abs(t-9.45)/0.15)
        f3=ImageFont.truetype('/home/claude/videoer/_verktoy/ArchitectsDaughter-Norsk.ttf',int(110*s))
        d.text((140,560),'ENERGIBEVARING!',font=f3,fill=(110,240,74,255))
    st,sl,n,sp=next(m for m in MANUS if m[0]<=t<m[1])
    bl=any(0<=t-b<0.13 for b in BLUNK)
    im=pose(n,form[i] if 'munn' in R[n] else 'orig',bl)
    if sp: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    sk=HOYDE/max(im.height,540)*(1+0.006*np.sin(2*np.pi*t/3.1))   # pust
    if n in('armer_opp',): sk*=1.0
    hopp=-18*max(0,1-(t-st)/0.18) if t-st<0.18 and st>0 else 0          # lite hopp ved ny positur
    im2=im.resize((int(im.width*sk),int(im.height*sk)),Image.LANCZOS).rotate(1.2*np.sin(2*np.pi*t/4.3),resample=Image.BICUBIC,expand=True)
    fr.alpha_composite(im2,(int(MIDT-im2.width/2),int(BUNN-im2.height+hopp)))
    fr.convert('RGB').save(f'{H}/test/b/{i:04d}.png')
subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',f'{H}/test/b/%04d.png','-i',f'{H}/test/lyd.wav','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',f'{H}/test/dashman_test.mp4'])
print('ok', N, {k:form.count(k) for k in set(form)})
