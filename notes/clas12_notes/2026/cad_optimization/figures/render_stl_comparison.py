#!/usr/bin/env python3
"""Render the LTCC STL comparison directly from the baseline and current repository data.

Requires NumPy and Matplotlib. No mesh repair, decimation, smoothing, or geometry edits are applied.
Run with --repo /opt/projects/gemc/clas12Tags; the default baseline is ea3625f.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'ltcc-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

FRAME = ['S1-BB', 'S1-BLB', 'S1-BRB', 'S1-BW', 'S1-LW', 'S1-RW', 'S1-TB', 'S1-TLB', 'S1-TRB']
NOSE = ['NFrame', 'FrontPlate', 'Mount', 'Nose', 'BottomPlate', 'Epoxy']
NEW_FRAME = ['backwall', 'leftwall', 'rightwall']
CONES = ['WC_S', 'WC_M', 'WC_L']
COLORS = {'back': '#4c84b5', 'left': '#65a57d', 'right': '#66a6be', 'nose': '#ce9551', 'cone': '#9a77ad'}
DTYPE = np.dtype([('normal', '<f4', (3,)), ('vertices', '<f4', (3, 3)), ('attribute', '<u2')])


def git_bytes(repo, ref, path):
    return subprocess.check_output(['git', '-C', str(repo), 'show', f'{ref}:{path}'])


def numbers(spec):
    scales = {'mm': 1., 'cm': 10., 'm': 1000., 'deg': 1.}
    return np.array([float(s.split('*')[0]) * scales[s.split('*')[1]] for s in spec.split()])


def active_rotation(spec):
    x, y, z = np.deg2rad(numbers(spec))
    cx, cy, cz = np.cos([x, y, z])
    sx, sy, sz = np.sin([x, y, z])
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    # GEMC applies CLHEP rotateX, rotateY, rotateZ, then passes the passive matrix to G4PVPlacement.
    return (rz @ ry @ rx).T


def group(name):
    if name in NOSE or name == 'nose':
        return 'nose'
    if name.startswith('WC_'):
        return 'cone'
    if name in ['S1-BLB', 'S1-LW', 'S1-TLB', 'leftwall']:
        return 'left'
    if name in ['S1-BRB', 'S1-RW', 'S1-TRB', 'rightwall']:
        return 'right'
    return 'back'


def draw(ax, meshes, bounds, camera, edges, zoom=1.):
    light = np.array([-.3, -.6, .75])
    light /= np.linalg.norm(light)
    for name, triangles in meshes.items():
        normal = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
        norm = np.linalg.norm(normal, axis=1)
        normal /= np.where(norm == 0, 1, norm)[:, None]
        shade = .56 + .44 * np.abs(normal @ light)
        color = shade[:, None] * np.array(to_rgb(COLORS[group(name)]))[None, :]
        collection = Poly3DCollection(triangles, facecolors=color, zsort='average',
                                     edgecolors=(.1, .16, .22, .65) if edges else 'none',
                                     linewidths=.13 if edges else 0, rasterized=True)
        ax.add_collection3d(collection)
    low, high = bounds
    span = high - low
    center = (high + low) / 2
    span *= 1.08
    for setter, value, extent in zip([ax.set_xlim, ax.set_ylim, ax.set_zlim], center, span):
        setter(value - extent / 2, value + extent / 2)
    ax.set_box_aspect(span, zoom=zoom)
    ax.set_proj_type('ortho')
    ax.view_init(elev=camera[0], azim=camera[1])
    ax.set_axis_off()
    ax.set_facecolor('white')


def common_bounds(*bundles):
    vertices = np.concatenate([v.reshape(-1, 3) for d in bundles for v in d.values()])
    return vertices.min(axis=0), vertices.max(axis=0)


def save(fig, output, name):
    fig.savefig(output / (name + '.png'), dpi=240, facecolor='white')
    fig.savefig(output / (name + '.pdf'), dpi=300, facecolor='white')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--baseline-ref', default='ea3625f')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    original, optimized, provenance = {}, {}, {}
    for case, names in [('original', FRAME + NOSE + CONES), ('optimized', NEW_FRAME + ['nose'] + CONES)]:
        bundle = original if case == 'original' else optimized
        provenance[case] = {}
        for name in names:
            if case == 'original':
                directory = 'cadTempRemoved' if name in NOSE + ['S1-BW', 'S1-LW', 'S1-RW', 'S1-TRB'] else 'cad'
                path = f'geometry_source/ltcc/{directory}/{name}.stl'
                raw = git_bytes(args.repo, args.baseline_ref, path)
            else:
                path = f'experiments/clas12/ltcc/cad/{name}.stl'
                raw = (args.repo / path).read_bytes()
            count = int.from_bytes(raw[80:84], 'little')
            assert len(raw) == 84 + 50 * count, (name, 'Not a binary STL')
            bundle[name] = np.frombuffer(raw[84:], DTYPE)['vertices'].astype(float)
            provenance[case][name] = {
                'path': path, 'triangles': count, 'sha256': hashlib.sha256(raw).hexdigest()}
    assert sum(len(v) for v in original.values()) == 134618
    assert sum(len(v) for v in optimized.values()) == 8146
    # Read the sector mother and active CAD placements from the actual ported files.
    text = (args.repo / 'experiments/clas12/ltcc/ltcc__geometry_default.txt').read_text()
    mother = next(line.split('|') for line in text.splitlines() if line.split('|')[0].strip() == 'ltccS3')
    mother_r, mother_p = active_rotation(mother[4].strip()), numbers(mother[3].strip())
    attributes = {v.attrib['name']: v.attrib for v in ET.parse(
        args.repo / 'experiments/clas12/ltcc/cad/cad_default.gxml').getroot()}
    old_hardware, new_hardware = {}, {}
    transforms = {}
    for name in FRAME + NOSE:
        r = active_rotation('180*deg 0*deg ' + ('120*deg' if name in NOSE else '60*deg'))
        p = np.array([0., 0., 1273.7])
        old_hardware[name] = (original[name] @ r.T + p) / 1000.
        transforms[name] = {'rotation': r.tolist(), 'translation_mm': p.tolist()}
    for name in NEW_FRAME + ['nose']:
        attr = attributes[name]
        r = mother_r @ active_rotation(attr['rotation'])
        p = mother_r @ numbers(attr['position']) + mother_p
        reference = transforms['NFrame' if name == 'nose' else 'S1-BB']
        assert np.allclose(r, reference['rotation']) and np.allclose(p, reference['translation_mm'])
        new_hardware[name] = (optimized[name] @ r.T + p) / 1000.
        transforms[name] = {'rotation': r.tolist(), 'translation_mm': p.tolist()}
    bounds = common_bounds(old_hardware, new_hardware)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    fig = plt.figure(figsize=(10, 9.1))
    for row, camera in enumerate([(18, -68), (20, 112)]):
        for col, bundle in enumerate([old_hardware, new_hardware]):
            ax = fig.add_subplot(2, 2, row * 2 + col + 1, projection='3d')
            draw(ax, bundle, bounds, camera, edges=row == 1, zoom=1.35)
            if row == 0:
                ax.set_title(('Complete original\n15 hardware meshes; 124,652 triangles' if col == 0 else
                              'Optimized\n4 hardware meshes; 3,646 triangles'), fontsize=13, pad=8)
            ax.text2D(.03, .05, 'Front oblique' if row == 0 else 'Rear oblique + triangle edges',
                      transform=ax.transAxes)
    legend = [Patch(color=COLORS[x], label=x.capitalize()) for x in ['back', 'left', 'right', 'nose']]
    fig.legend(handles=legend,
               loc='lower center', ncol=4, frameon=False, bbox_to_anchor=(.5, .037))
    fig.text(.5, .017, 'Sector 3 STL hardware only · identical camera and scale in each row',
             ha='center', fontsize=10)
    fig.subplots_adjust(left=0, right=1, top=.92, bottom=.10, wspace=0, hspace=.01)
    save(fig, args.output, 'hardware_stl_comparison')
    # Nose consolidation in the shared engineering coordinates, not independently recentered.
    nose_old = {k: original[k] for k in NOSE}
    nose_new = {'nose': optimized['nose']}
    nose_bounds = common_bounds(nose_old, nose_new)
    fig = plt.figure(figsize=(10, 5.2))
    for col, bundle in enumerate([nose_old, nose_new]):
        ax = fig.add_subplot(1, 2, col + 1, projection='3d')
        draw(ax, bundle, nose_bounds, (10, -35), edges=True)
        ax.set_title('Original nose\n6 meshes; 12,012 triangles' if col == 0 else
                     'Consolidated nose\n1 mesh; 1,986 triangles', fontsize=13)
    fig.text(.5, .035, 'Original STL coordinates (mm) · identical orthographic camera, bounds, and scale',
             ha='center', fontsize=10)
    fig.subplots_adjust(left=0, right=1, top=.90, bottom=.06, wspace=0)
    save(fig, args.output, 'nose_stl_comparison')
    fig = plt.figure(figsize=(10, 10))
    for row, name in enumerate(CONES):
        left, right = {name: original[name]}, {name: optimized[name]}
        cone_bounds = common_bounds(left, right)
        for col, bundle in enumerate([left, right]):
            ax = fig.add_subplot(3, 2, row * 2 + col + 1, projection='3d')
            draw(ax, bundle, cone_bounds, (22, -65), edges=True, zoom=1.06)
            ax.set_title(f'{name}: {len(bundle[name]):,} triangles', fontsize=12, pad=0)
    fig.text(.26, .967, 'Original Winston cones', ha='center', fontsize=14)
    fig.text(.75, .967, 'Optimized Winston cones', ha='center', fontsize=14)
    fig.text(.5, .020, 'Triangle edges shown · identical camera and scale within each row',
             ha='center', fontsize=10)
    fig.subplots_adjust(left=0, right=1, top=.91, bottom=.07, wspace=0, hspace=.04)
    save(fig, args.output, 'cones_stl_comparison')
    metadata = {'baseline_ref': args.baseline_ref, 'stl_files': provenance,
                'hardware_transforms': transforms, 'hardware_bounds_m': [v.tolist() for v in bounds],
                'projection': 'orthographic', 'hardware_cameras_elevation_azimuth_deg': [[18, -68], [20, 112]],
                'nose_camera': [10, -35], 'cone_camera': [22, -65],
                'rendering': 'Unmodified stored triangles; flat shading; no geometry repair or smoothing',
                'numpy_version': np.__version__, 'matplotlib_version': matplotlib.__version__}
    (args.output / 'stl_comparison_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(args.output)


if __name__ == '__main__':
    main()
