"""Matched flange views and tube cross-sections of stored FT inner-shield meshes."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from render_ft_shield_comparison import load_stl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import vtk

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--original', type=Path,
                    default=Path('/private/tmp/ft-shield-study/original_engineering/taggerInnerShield.stl'))
parser.add_argument('--optimized', type=Path,
                    default=Path('/opt/projects/gemc/clas12-systems') /
                    'geometry_src/beamline/stls/FTInnerShield.stl')
parser.add_argument('--output', type=Path, default=Path('/private/tmp/ft-shield-study'))
args = parser.parse_args()
study = args.output
study.mkdir(parents=True, exist_ok=True)
paths = [args.original, args.optimized]
fig = plt.figure(figsize=(10, 8), layout='constrained')
metadata = {}
for column, path in enumerate(paths):
    triangles, info = load_stl(path)
    name = 'Original' if column == 0 else 'Optimized'
    metadata[name] = info
    ax = fig.add_subplot(2, 2, column+1, projection='3d')
    flange = triangles[(triangles[:, :, 2] >= -635.001).all(1)
                       & (triangles[:, :, 2] <= -594.999).all(1)]
    collection = Poly3DCollection(flange, facecolors='#a7c7d5', edgecolors='#425761', linewidths=.08)
    collection.set_rasterized(True)
    ax.add_collection3d(collection)
    ax.set_xlim(-105, 105); ax.set_ylim(-105, 105); ax.set_zlim(-637, -593)
    ax.set_box_aspect(np.array([210, 210, 44])); ax.view_init(elev=-65, azim=90)
    ax.set_proj_type('ortho'); ax.set_axis_off(); ax.set_title(name+' flange underside')
    reader = vtk.vtkSTLReader(); reader.SetFileName(str(path)); reader.Update()
    plane = vtk.vtkPlane(); plane.SetOrigin(0, 0, -100); plane.SetNormal(0, 0, 1)
    cutter = vtk.vtkCutter(); cutter.SetInputData(reader.GetOutput()); cutter.SetCutFunction(plane)
    cutter.Update(); poly = cutter.GetOutput()
    ax = fig.add_subplot(2, 2, column+3)
    for i in range(poly.GetNumberOfCells()):
        cell = poly.GetCell(i)
        points = np.array([poly.GetPoint(cell.GetPointId(j)) for j in range(cell.GetNumberOfPoints())])
        ax.plot(points[:, 0], points[:, 1], color='#245770', linewidth=.9)
    ax.set_xlim(-43, 43); ax.set_ylim(-43, 43); ax.set_aspect('equal')
    ax.set_xlabel('Local x (mm)'); ax.set_ylabel('Local y (mm)')
    ax.set_title(name+' tube section at z = -100 mm')
    ax.grid(alpha=.2)
metadata['views'] = {'flange_elevation': -65, 'flange_azimuth': 90, 'tube_section_z_mm': -100}
for suffix in ('png', 'pdf'):
    fig.savefig(study/('ft_shield_details.'+suffix), dpi=220, bbox_inches='tight')
(study/'ft_shield_details_metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
