#!/usr/bin/env python3
"""Render the FT inner shield with matched bounds/cameras and retain source hashes."""

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
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    if len(data) != 84 + count * 50:
        raise ValueError('Expected binary STL: ' + str(path))
    dtype = np.dtype([('normal', '<f4', (3,)), ('vertices', '<f4', (3, 3)), ('attribute', '<u2')])
    triangles = np.frombuffer(data, dtype=dtype, offset=84)['vertices'].astype(float)
    return triangles, {'sha256': hashlib.sha256(data).hexdigest(), 'triangles': count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originals', type=Path,
                        default=Path('/opt/projects/gemc/clas12Tags/geometry_source/beamline/cad_original'))
    parser.add_argument('--optimized', type=Path,
                        default=Path('/opt/projects/gemc/clas12-systems/geometry_src/beamline/stls'))
    parser.add_argument('--output', type=Path, default=Path('/private/tmp/ft-shield-study'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(10, 7), layout='constrained')
    metadata = {}
    pairs = [('FT inner shield', 'taggerInnerShield', 'FTInnerShield')]
    for row, (title, old, new) in enumerate(pairs):
        meshes = [load_stl(args.originals / (old + '.stl')),
                  load_stl(args.optimized / (new + '.stl'))]
        points = np.concatenate([t.reshape(-1, 3) for t, _ in meshes])
        low, high = points.min(0), points.max(0)
        centre, extent = (low + high) / 2, high - low
        metadata[new] = {'original': meshes[0][1], 'optimized': meshes[1][1],
                         'bounds_mm': [low.tolist(), high.tolist()], 'elevation': 12, 'azimuth': 90}
        for column, (triangles, information) in enumerate(meshes):
            ax = fig.add_subplot(1, 2, row * 2 + column + 1, projection='3d')
            collection = Poly3DCollection(triangles, facecolors='#a7c7d5',
                                          edgecolors='#425761', linewidths=0.07, alpha=1)
            collection.set_rasterized(True)
            ax.add_collection3d(collection)
            for setter, c, e in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), centre, extent):
                setter(c - e * 0.55, c + e * 0.55)
            ax.set_box_aspect(extent.copy())
            ax.view_init(elev=12, azim=90)
            ax.set_proj_type('ortho')
            ax.set_title(f'{title}: {"original" if column == 0 else "optimized"}\n'
                         f'{information["triangles"]:,} triangles', fontsize=11)
            ax.set_zticks([])
            ax.text2D(0.02, -0.02, f'Local z: {low[2]:.1f} to {high[2]:.1f} mm',
                      transform=ax.transAxes, fontsize=9)
            ax.tick_params(labelsize=7)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            ax.set_axis_off()
    for suffix in ('png', 'pdf'):
        fig.savefig(args.output / ('ft_shield_stl_comparison.' + suffix), dpi=230, bbox_inches='tight')
    (args.output / 'ft_shield_figure_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')


if __name__ == '__main__':
    main()
