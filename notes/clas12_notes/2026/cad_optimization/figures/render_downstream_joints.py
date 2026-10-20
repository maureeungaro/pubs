"""Plot actual socket and neighboring tube polygons at the two downstream joints."""
from pathlib import Path
import hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pymeshlab as ml

study=Path('/private/tmp/downstream-joints-study')
health=json.loads((study/'optimized/downstream_mesh_health.json').read_text())['Downstream_Beam_tube_Segment_1']

def vertices(path):
    ms=ml.MeshSet();ms.load_new_mesh(str(path));return ms.current_mesh().vertex_matrix()

old=vertices(study/'previous/Downstream_Beam_tube_Segment_1.stl')
new=vertices(study/'optimized/Downstream_Beam_tube_Segment_1.stl')
fig,axes=plt.subplots(1,2,figsize=(10,4.3),layout='constrained')
metadata={}
for ax,row in zip(axes,health['joint_relief']):
    neighbor=row['neighbor'];before=row['radius_before_mm'];after=row['radius_after_mm']
    rings=[]
    for v,r in ((old,before),(new,after)):
        ids=abs(np.linalg.norm(v[:,:2],axis=1)-r)<1e-4
        z=v[ids,2].min();points=v[ids&(abs(v[:,2]-z)<.001),:2]
        angle=np.mod(np.arctan2(points[:,1],points[:,0]),2*np.pi)
        rings.append(points[np.argsort(angle)])
    male=vertices(study/'previous'/(neighbor+'.stl'))
    z=male[:,2].max() if neighbor=='Beamline_Adapter_1' else male[:,2].min()
    ring=male[abs(male[:,2]-z)<.001,:2];r=np.linalg.norm(ring,axis=1)
    ring=ring[r>r.max()-1e-4]
    ring=ring[np.argsort(np.mod(np.arctan2(ring[:,1],ring[:,0]),2*np.pi))]
    edges=np.roll(rings[0],-1,axis=0)-rings[0]
    normals=np.column_stack([edges[:,1],-edges[:,0]]);normals/=np.linalg.norm(normals,axis=1)[:,None]
    offsets=(normals*rings[0]).sum(1)
    gaps=offsets-(ring@normals.T).max(0);i=int(gaps.argmin())
    n=normals[i];t=np.array([n[1],-n[0]]);origin=offsets[i]
    for points,color,label,style in zip([*rings,ring],['#bb4037','#285caa','#23874b'],
        ['Previous socket','Relieved socket','Unchanged neighbor'],['--','-','-']):
        points=np.vstack([points,points[0]])
        ax.plot(points@t,points@n-origin,color=color,label=label,linestyle=style,linewidth=1.6)
    ax.set_xlim(-9,9);ax.set_ylim(-.25,.72);ax.grid(alpha=.2)
    ax.set_title('Adapter / Segment 1' if neighbor=='Beamline_Adapter_1' else 'Segment 2 / Segment 1')
    ax.set_xlabel('Along socket face (mm)');ax.set_ylabel('Normal distance from previous face (mm)')
    ax.legend(fontsize=8,loc='upper right')
    metadata[neighbor]={'old_plane_gap_mm':float(gaps.min()),'new_radius_mm':after,
        'neighbor_sha256':row['neighbor_sha256']}
for suffix in ('png','pdf'):fig.savefig(study/('downstream_joint_clearance.'+suffix),dpi=220)
(study/'downstream_joint_figure_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
