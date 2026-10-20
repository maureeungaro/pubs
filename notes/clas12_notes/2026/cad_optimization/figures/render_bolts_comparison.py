#!/usr/bin/env python3
"""Compare representative regular and long FT bolts with matched bounds and cameras."""
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

def load(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    dtype = np.dtype([('normal', '<f4', (3,)), ('vertices', '<f4', (3, 3)), ('attribute', '<u2')])
    assert len(data) == 84 + 50 * count
    return np.frombuffer(data, dtype=dtype, offset=84)['vertices'].astype(float), {
        'sha256': hashlib.sha256(data).hexdigest(), 'triangles': count}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', type=Path,
                    default=Path('/opt/projects/gemc/clas12Tags/geometry_source/beamline/cad_original'))
parser.add_argument('--optimized', type=Path,
                    default=Path('/opt/projects/gemc/clas12-systems/geometry_src/beamline/stls'))
parser.add_argument('--output', type=Path, default=Path('/private/tmp/bolts-study'))
args = parser.parse_args()
fig = plt.figure(figsize=(10, 7), layout='constrained')
metadata = {}
for row, i in enumerate((1, 4)):
    name = f'FTInnerShieldAndFlange_Bolt{i}'
    meshes = [load(args.originals / f'nut{i}.stl'), load(args.optimized / (name + '.stl'))]
    axis = 0 if i == 1 else 1
    transverse = [j for j in range(3) if j != axis]
    order = [axis, *transverse]
    original = meshes[0][0]
    centre = (original.reshape(-1, 3).min(0) + original.reshape(-1, 3).max(0)) / 2
    transformed = [(triangles - centre)[:, :, order] for triangles, _ in meshes]
    points = np.concatenate([t.reshape(-1, 3) for t in transformed])
    low, high = points.min(0), points.max(0)
    extent = high-low
    midpoint = (low+high)/2
    metadata[name] = {'original': meshes[0][1], 'optimized': meshes[1][1],
                      'coordinate_permutation': order, 'origin_mm': centre.tolist(),
                      'elevation': 20, 'azimuth': -55}
    for column, (triangles, info) in enumerate(zip(transformed, [m[1] for m in meshes])):
        ax = fig.add_subplot(2, 2, row*2+column+1, projection='3d')
        surface = Poly3DCollection(triangles, facecolors='#d9a074', edgecolors='#664a37', linewidths=.15)
        surface.set_rasterized(True)
        ax.add_collection3d(surface)
        for setter, c, e in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), midpoint, extent):
            setter(c-e*.55, c+e*.55)
        ax.set_box_aspect(extent.copy())
        ax.view_init(elev=20, azim=-55)
        ax.set_proj_type('ortho')
        label = 'original' if column == 0 else 'smooth'
        ax.set_title(f'Bolt {i}: {label}\n{info["triangles"]:,} triangles', fontsize=11)
        ax.set_axis_off()
for suffix in ('png', 'pdf'):
    fig.savefig(args.output / ('bolts_stl_comparison.'+suffix), dpi=230, bbox_inches='tight')
(args.output / 'bolts_figure_metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
