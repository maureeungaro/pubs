"""Plot matched meridian sections through the corrected interfaces using the placed STL surfaces."""
from pathlib import Path
import hashlib,json
import numpy as np
import pyvista as pv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
s=Path('/private/tmp/beamline-joints-study');out=s/'figures';out.mkdir(exist_ok=True)
rows=[
 ('Shield / inner extension','FTInnerShield','moller-cone-extension-inner',142,(-372,-369.2),(35,42)),
 ('Inner extension / lead fill','moller-cone-extension-inner','moller-cone-extension-lead-fill',
  55.75,(-474,-468),(46,49)),
 ('FT flange / lead case','FTFlange','moller-cone-extension-lead-case',70.4,(-523.8,-519.3),(116.8,118.3)),
 ('Inner extension / main cone','moller-cone-extension-inner','moller_cone',37.7,(-171,-169),(39.5,48.2)),
 ('Main cone / cone tip','moller_cone','moller_cone_tip',-45.8,(711.35,712.25),(34.4,38.6)),
 ('Main cone / tungsten add-on','moller_cone','moller-cone-extension-tungsten-addon',
  -155.4,(-122,-105),(72.4,74.6)),
]
short={'FTInnerShield':'FT inner shield','moller-cone-extension-inner':'Inner extension',
 'moller-cone-extension-lead-fill':'Lead fill','FTFlange':'FT flange',
 'moller-cone-extension-lead-case':'Lead case',
 'moller_cone':'Main cone','moller_cone_tip':'Cone tip',
 'moller-cone-extension-tungsten-addon':'Tungsten add-on'}
metadata={'mesh_sha256':{},'sections':[]}
for page in range(2):
 fig,axes=plt.subplots(3,2,figsize=(10,9),layout='constrained')
 for k,(title,a,b,phi,zrange,rrange) in enumerate(rows[page*3:page*3+3]):
  angle=np.deg2rad(phi);radial=np.array([np.cos(angle),np.sin(angle),0])
  normal=np.array([-np.sin(angle),np.cos(angle),0])
  metadata['sections'].append({'title':title,'phi_degrees':phi,'local_z_mm':zrange,'r_mm':rrange})
  for col,case in enumerate(['before','optimized']):
   ax=axes[k,col]
   for name,color in [(a,'#18577c'),(b,'#bc4a21')]:
    path=s/case/(name+'.stl')
    metadata['mesh_sha256'][case+'/'+name]=hashlib.sha256(path.read_bytes()).hexdigest()
    mesh=pv.read(path)
    if name=='FTInnerShield':mesh.translate([0,0,-369.73],inplace=True)
    cut=mesh.slice(normal=normal,origin=(0,0,0));points=cut.points;segments=[];lines=cut.lines;index=0
    while index<len(lines):
     n=int(lines[index]);ids=lines[index+1:index+1+n];index+=n+1
     for u,v in zip(ids[:-1],ids[1:]):
      p=points[[u,v]];r=p@radial
      if r.max()>0:segments.append(np.column_stack([p[:,2],r]))
    ax.add_collection(LineCollection(segments,colors=color,linewidths=1.3,label=short[name]))
   ax.set_xlim(*zrange);ax.set_ylim(*rrange);ax.set_xlabel('Local z (mm)');ax.set_ylabel('Radius (mm)')
   ax.set_title(title+'\n'+('Before' if col==0 else 'Corrected'),fontsize=11)
   ax.tick_params(labelsize=9);ax.ticklabel_format(useOffset=False);ax.grid(alpha=.2)
   ax.legend(fontsize=8,loc='best')
 for ext in ['png','pdf']:fig.savefig(out/f'ft_joint_sections_{page+1}.{ext}',dpi=220,bbox_inches='tight')
 plt.close(fig)
(out/'ft_joint_sections_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
