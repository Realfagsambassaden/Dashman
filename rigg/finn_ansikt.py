# Finner øyne og munn i hver positur (komponenter i strekene) -> rigg.json
from PIL import Image; import numpy as np, json, glob, os
from scipy import ndimage
R={}
for f in sorted(glob.glob('ut/*.png')):
    n=os.path.basename(f)[:-4]
    a=np.asarray(Image.open(f))[...,3]>40; H,W=a.shape
    if H<400: continue
    lab,k=ndimage.label(a,structure=np.ones((3,3))); obj=ndimage.find_objects(lab)
    K=[dict(i=i+1,bb=[s[1].start,s[0].start,s[1].stop,s[0].stop],n=int((lab[s]==i+1).sum())) for i,s in enumerate(obj)]
    oy=[c for c in K if 45<c['bb'][2]-c['bb'][0]<150 and 40<c['bb'][3]-c['bb'][1]<130 and c['bb'][1]<0.45*H and c['n']>300]
    oy=sorted(oy,key=lambda c:c['bb'][1])[:1]
    r={'str':[W,H]}
    if oy:
        e=oy[0]['bb']; pup=[c for c in K if c['n']<200 and e[0]<=c['bb'][0] and c['bb'][2]<=e[2] and e[1]<=c['bb'][1] and c['bb'][3]<=e[3]]
        r['oyne']=e; r['oyne_komp']=[oy[0]['i']]+[c['i'] for c in pup]
        cx=(e[0]+e[2])/2
        mu=[c for c in K if 50<c['n']<600 and c['bb'][1]>e[3]+5 and c['bb'][1]<e[3]+110 and abs((c['bb'][0]+c['bb'][2])/2-cx)<90 and c['bb'][3]-c['bb'][1]<45 and 15<c['bb'][2]-c['bb'][0]<80]
        if mu: m=min(mu,key=lambda c:c['bb'][1]); r['munn']=m['bb']; r['munn_komp']=[m['i']]
    R[n]=r; print(n,r)
json.dump(R,open('rigg.json','w'),indent=1)
