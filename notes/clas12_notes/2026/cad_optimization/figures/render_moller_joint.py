"""Render actual triangle sections through the Moller-cone/FT-shield joint."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import vtk


def section(path, offset=0):
    reader=vtk.vtkSTLReader();reader.SetFileName(str(path));reader.Update()
    plane=vtk.vtkPlane();plane.SetOrigin(0,0,0);plane.SetNormal(0,1,0)
    cut=vtk.vtkCutter();cut.SetInputData(reader.GetOutput());cut.SetCutFunction(plane);cut.Update()
    poly=cut.GetOutput();segments=[]
    for i in range(poly.GetNumberOfCells()):
        cell=poly.GetCell(i)
        for j in range(cell.GetNumberOfPoints()-1):
            a=poly.GetPoint(cell.GetPointId(j));b=poly.GetPoint(cell.GetPointId(j+1))
            if a[0]>=0 and b[0]>=0:segments.append([(a[0],a[2]+offset),(b[0],b[2]+offset)])
    return segments


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('/private/tmp/moller-cone-study'))
    args=parser.parse_args()
    repo=Path('/opt/projects/gemc/clas12-systems')
    sources=[repo.parent/'clas12Tags/geometry_source/beamline/cad_original/main-cone.stl',
             repo/'geometry_src/beamline/stls/moller_cone.stl',
             repo/'geometry_src/beamline/stls/FTInnerShield.stl']
    fig,axes=plt.subplots(1,2,figsize=(9,4.8),layout='constrained')
    colors=['#bb4037','#285caa','#23874b']
    labels=['Original cone','Optimized cone','Unchanged FT shield']
    for path,color,label,offset in zip(sources,colors,labels,(0,0,-53.73)):
        segments=section(path,offset)
        for ax in axes:
            ax.add_collection(LineCollection(segments,colors=color,linewidths=1.5,label=label))
    for ax in axes:
        ax.set_xlabel('Radius in y = 0 plane (mm)');ax.set_ylabel('Local cone z (mm)')
        ax.grid(alpha=.2)
    axes[0].set_xlim(34,42);axes[0].set_ylim(-172,-50)
    axes[0].set_title('Counterbore section')
    axes[0].legend(loc='lower left',fontsize=8)
    axes[1].set_xlim(37,40.6);axes[1].set_ylim(-57,-53)
    axes[1].set_title('Shield tip / cone shoulder')
    axes[1].annotate('',xy=(37.6,-53.73),xytext=(37.6,-53.53),
                     arrowprops={'arrowstyle':'<->','color':'black'})
    axes[1].annotate('0.2 mm axial allowance',xy=(37.6,-53.63),xytext=(38.2,-54.7),fontsize=8,
                     arrowprops={'arrowstyle':'->','color':'black'})
    for suffix in ('png','pdf'):
        fig.savefig(args.output/('moller_cone_joint.'+suffix),dpi=220)
    metadata={'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              'shield_offset_in_cone_mm':-53.73,'method':'Actual triangulated intersections with y = 0 plane'}
    (args.output/'moller_cone_joint_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':main()
