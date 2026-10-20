#!/usr/bin/env python3
"""Compare the engineering adjuster assembly with its volume-matched replacement."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def load_stl(path):
    data=path.read_bytes()
    count=struct.unpack_from('<I',data,80)[0]
    if len(data)!=84+count*50:
        raise ValueError('Expected binary STL: '+str(path))
    dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attribute','<u2')])
    triangles=np.frombuffer(data,dtype=dtype,offset=84)['vertices'].astype(float)
    return triangles,{'sha256':hashlib.sha256(data).hexdigest(),'triangles':count}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originals',type=Path,
        default=Path('/opt/projects/gemc/clas12Tags/geometry_source/beamline/cad_original'))
    parser.add_argument('--optimized',type=Path,
        default=Path('/opt/projects/gemc/clas12-systems/geometry_src/beamline/stls'))
    parser.add_argument('--output',type=Path,default=Path('/private/tmp/adjuster-study'))
    args=parser.parse_args()
    originals=[load_stl(args.originals/(n+'.stl')) for n in ('adjuster1','adjuster2','adjuster3')]
    final=load_stl(args.optimized/'ft_adjuster.stl')
    meshes=[np.vstack([r[0] for r in originals]),final[0]]
    points=np.concatenate([t.reshape(-1,3) for t in meshes])
    low,high=points.min(0),points.max(0)
    centre,extent=(low+high)/2,high-low
    fig=plt.figure(figsize=(9,6),layout='constrained')
    for column,triangles in enumerate(meshes):
        ax=fig.add_subplot(1,2,column+1,projection='3d')
        collection=Poly3DCollection(triangles,facecolors='#a7c7d5',edgecolors='#425761',linewidths=0.1)
        collection.set_rasterized(True)
        ax.add_collection3d(collection)
        for setter,c,e in zip((ax.set_xlim,ax.set_ylim,ax.set_zlim),centre,extent):
            setter(c-e*0.55,c+e*0.55)
        ax.set_box_aspect(extent.copy())
        ax.view_init(elev=12,azim=-65)
        ax.set_proj_type('ortho')
        ax.set_title(('Original trio' if column==0 else 'ft_adjuster')+
                     f'\n{len(triangles):,} triangles',fontsize=11)
        ax.text2D(0.02,-0.02,f'Local z: {low[2]:.1f} to {high[2]:.1f} mm',
                  transform=ax.transAxes,fontsize=9)
        ax.set_axis_off()
    args.output.mkdir(exist_ok=True,parents=True)
    for suffix in ('png','pdf'):
        fig.savefig(args.output/('adjuster_stl_comparison.'+suffix),dpi=230,bbox_inches='tight')
    metadata={'originals':{n:r[1] for n,r in zip(('adjuster1','adjuster2','adjuster3'),originals)},
              'final':final[1],'bounds_mm':[low.tolist(),high.tolist()],'elevation':12,'azimuth':-65,
              'coordinate_frame':'Original STL coordinates; common CAD placement not baked into vertices'}
    (args.output/'adjuster_figure_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':
    main()
