# Reproducing the LTCC CAD optimization study

The primary comparison enables all original hardware from `cadTempRemoved/` before benchmarking.
The `old` and `cones_only` labels therefore denote complete original hardware, not disabled production.
The `new` label denotes the full optimized implementation ported from meson.

Run from the owning `clas12Tags` repository after loading the same local `gemc/dev` module:

```shell
export LTCC_DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH"
python3 ci/ltcc_cad_benchmark.py --baseline-ref ea3625f \
    --ccdb geometry_source/coatjava/etc/data/sqlite/ccdb.sqlite \
    --output /private/tmp/ltcc-optical --restore-baseline-hardware --fixed-primaries \
    --events 1000 --repeats 5 --overlaps --timeout 1800
```

For each of `e-`, `proton`, `pi+`, and `neutron`, use a fresh output directory and add
`--physics nonoptical --transport-only --events 10000 --particle <particle>`, omitting `--overlaps`.
For CAD-only loading use `--cad-only-loading --restore-baseline-hardware --repeats 5`.
For tracking diagnostics use `--physics nonoptical --transport-only --events 100 --repeats 1`
with `--track-verbosity 1`, the restoration flag, and either electrons or protons.
Use one benchmark process at a time. Keep event output and the GUI disabled.

`data/` retains the primary comparison results, commands, hashes, and metadata. The archive includes
all raw primary-comparison and supplementary logs, time reports, the input fixtures, and the analysis
scripts used to produce the note. Supplementary datasets omit the restoration flag and represent the
previously disabled production configuration. Failed pilots are excluded from quantitative results.

Each primary comparison uses identical LUND inputs for a given seed. The archived fixture holds the
last input file used; the benchmark deterministically regenerates all five seeds. The supplementary
optical dataset used internal generation, so its primary sequences are not identical across geometries.

The original executable and the local CCDB path are recorded in metadata; the executable is not
redistributed. Match its SHA-256 hash for exact binary reproduction. The original STL files remain
byte-for-byte unchanged in the complete baseline, including invalid facets reported by Geant4.
The optimized geometry also changes materials and mothers, so the full-port transport ratio includes
those changes. The cone-only case isolates the substituted Winston-cone meshes.

Timing medians use runs with normal process exit and a timing footer. The cone-only optical and
nonoptical electron samples each contain one GeomNav0003 event-abort request; a timing footer does
not guarantee complete transport of every event. These timings describe the defective configuration. A controller interruption left one unrecorded run; that run
was repeated and the interrupted log retained. Timings are machine- and workload-specific. The
one-event SQLite smoke tests verify all six run-dependent configurations; the geometry comparison
summary records the corresponding TEXT/SQLite row counts.

## Beamline apex pair: GEMC3

Run from the owning `clas12-systems` repository with an existing GEMC3 executable:

```shell
build/subprojects/pygemc/python_env/bin/python3 geometry_src/beamline/beamline.py \
  -f sqlite -sql /tmp/beamline.sqlite
python3 scripts/beamline_cad_benchmark.py --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/apex-benchmark --events 200 --repeats 5
```

The October 12 dataset uses five seeds, 200 events per electron/proton/pion/neutron run, and an isolated
two-mesh fixture. It measures elapsed wall transport time, whole-process CPU, loading time, and peak RSS.
Its GEMC3/Geant4 stack and acceptance differ from the LTCC dataset; do not pool their absolute timings.
The benchmark alternates case order, checks requested event counts and completion footers, and retains
separate zero-event overlap diagnostics. All input fixtures and exact executable/STL hashes are retained.
`beamline_apex_archive.zip` also includes the mesh builder and original engineering meshes. Mesh sampling
is not a proven global Hausdorff bound, and this small transport sample is not detector-response validation.

## Downstream tube pair: GEMC3

Use the same beamline SQLite generation command, then select the downstream pair:

```shell
python3 scripts/beamline_cad_benchmark.py --pair downstream --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/downstream-benchmark --events 200 --repeats 5
```

The pair uses 0.1--1.3-degree matched 5 GeV primaries, five seeds, and separate loading, transport,
memory, and overlap diagnostics. Regenerate meshes with `build_cad_meshes.py --pair downstream` in
the owning `clas12-systems` repository. Both segment names and placement rows remain unchanged.
The mesh-health report distinguishes Segment 1's invalid original volume from its repaired reference.
Original and optimized geometries have different diagnostics; do not treat a timing footer as proof of
complete correct transport. Retained data record stuck tracks and placement overlaps explicitly.

## Adapter and exit shield group: GEMC3

Generate the beamline SQLite database as above, then select the three-volume exit group:

```shell
python3 scripts/beamline_cad_benchmark.py --pair exit --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/exit-benchmark --events 200 --repeats 5
```

Matched 5 GeV primaries cover 0.25--2.6 degrees and full azimuth. Regenerate the meshes with
`build_cad_meshes.py --pair exit` in the owning `clas12-systems` repository. Archived originals retain
the reducer's former name; final CAD placements and fixtures use `Beamline_Adapter_1`. The builder
protects casing mating faces and retains the original lead-fill bytes. The small triangle reduction
must not be equated with a significant performance improvement.

## FT adjuster material model: GEMC3

Use the generated beamline database from either geometry state; the benchmark reconstructs the original
trio or the merged replacement from their common physical placement attributes:

```shell
python3 scripts/beamline_cad_benchmark.py --pair adjuster --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/adjuster-benchmark --events 200 --repeats 5
```

Primaries cover 2.5--3.3 degrees and azimuth -95-- -85 degrees. Regenerate with
`build_cad_meshes.py --pair adjuster` in the owning `clas12-systems` repository. The reference uses small
sealing patches and Boolean union of imperfect originals, with an inclusion-exclusion volume check.
Only the clean, volume-matched prism is published; reference meshes are diagnostic material-budget inputs.

## FT inner shield and flange: GEMC3

Regenerate from the owning `clas12-systems` repository with `build_cad_meshes.py --pair inner_shield`.
The archived original keeps its old stem; both benchmark fixtures use `FTInnerShieldAndFlange`:

```shell
python3 scripts/beamline_cad_benchmark.py --pair inner_shield --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/inner-shield-benchmark --events 200 --repeats 5
```

The benchmark accepts the database before or after the rename, uses 0.25--3.0-degree primaries over
full azimuth, and retains the alloy and placement. The original has a wrong-orientation import warning;
all measured diagnostics are retained rather than treating a completion footer as sufficient validation.

## FT inner-shield bolts: GEMC3

Regenerate in the owning `clas12-systems` repository using the archived original nut stems:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair bolts
/Users/ungaro/venv/pygemc/bin/python scripts/beamline_bolt_clearance.py --output /tmp/clearance.json
python3 scripts/beamline_cad_benchmark.py --pair bolts --executable /path/to/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/bolt-benchmark --events 200 --repeats 5
```

The benchmark accepts the database before or after renaming. It isolates the nine bolts and samples
1.3--3.0 degrees over full azimuth. The archived shield-plus-bolts fixture supplies the unchanged shield
for separate clearance verification. Its archived `stls` directory contains all ten meshes:

```shell
/path/to/gemc smoke.yaml -check_overlaps=10000
```

The archived builder reproduces the nine saved STLs byte for byte. The collision validator requires VTK
in the mesh-enabled environment. Reproduce geometry rather than asserting bitwise-identical stochastic
showers or wall timings on another machine.

## FT outer flange: GEMC3

The mesh-enabled environment provides pygemc's bolt-hole removal utility. From `clas12-systems`:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair outer_flange
python3 scripts/beamline_cad_benchmark.py --pair outer_flange --executable /path/to/fixed/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/outer-flange-benchmark --events 200 --repeats 5
```

The benchmark accepts the database before or after renaming and uses 1.9--2.8-degree primaries over full
azimuth. Use a fixed executable throughout; the retained metadata identifies the measured snapshot hash.
The standalone snapshot used here requires a sibling `lib` directory to satisfy GEMC's layout check.
The archive excludes the executable. Its original and optimized assembly fixtures can be run with their
included meshes using `gemc smoke.yaml`; each requests a 10,000-point overlap check. Their residual mount
overlaps are reported. The archived hole-removal utility source records the dependency used for this study.

## Outer-flange control with both bolt-hole patterns filled

Extract `hole_filled_reference/filled.stl` from the outer-flange archive, or regenerate it from the archived
engineering STL with pygemc's `remove_holes.py` and a 40 mm cutoff. From `clas12-systems`, compare it with the
optimized mesh using the same fixed executable as the original flange study:

```shell
python3 scripts/beamline_cad_benchmark.py --pair outer_flange \
  --filled-reference /tmp/filled.stl --executable /path/to/fixed/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/flange-filled-control --events 2000 --repeats 5
```

Here `original` means the unreduced hole-filled flange. The two fixture geometry and material tables are
identical. The archived control contains all matched primary files, timings, logs, executable hash, and
seed-paired ratios. Its 2,000-event results are independent of the earlier 200-event comparison.

## FT outer mount: GEMC3

The builder requires the archived original mount and the unchanged optimized flange in the owning
`clas12-systems` mesh directory. Its report retains that flange hash; all ten placements keep the same
verified 0.5 mm relative z translation. From `clas12-systems`:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair outer_mount
/Users/ungaro/venv/pygemc/bin/python scripts/beamline_mount_clearance.py --output /tmp/mount-clearance.json
python3 scripts/beamline_cad_benchmark.py --pair outer_mount --executable /path/to/fixed/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/mount-benchmark --events 200 --repeats 5
```

The unchanged fixed executable and 1.5--2.4-degree acceptance are recorded in the metadata. Separate
assembly fixtures include the flange, inner shield, and nine bolts; their cards request 10,000-point checks.
The archive also retains the sealed and relieved references, with hashes matching the builder report.
The repaired reference defines volume comparisons because the engineering mesh is open.

## Downstream FT inner shield: initial revision

Use the archived scripts in beamline_ft_shield_archive.zip for this historical 13,500-triangle revision. The
current owning builder generates the smooth-flange revision documented below.

From `clas12-systems`, use the archived engineering mesh. Generate the reference separately from runtime
assets:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair ft_inner_shield --reference /tmp/ft-inner-shield-reference.stl
python3 scripts/beamline_cad_benchmark.py --pair ft_inner_shield --executable /path/to/fixed/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/ft-inner-shield-engineering --events 200 --repeats 5
```

Repeat with `--filled-reference /tmp/ft-inner-shield-reference.stl` and a fresh output directory for the
separate reconstructed-reference control. Both acceptances are 0.7--2.7 degrees with full azimuth. The
reference has the same closed holes, blind flange recesses, and two longitudinal grooves as the optimized
mesh; the report retains its small further decimation volume change and sampled distances. The archive
includes the two-volume assembly with unchanged cone, full-construction and comparator logs, measured source
profiles, independent containment probes, matched primaries, executable hashes, and all timing/diagnostic
reports. The open engineering mesh has no defined solid volume; the reconstructed material reference is not
a certified mass.

## Downstream FT inner shield: smooth-flange revision

The current builder fills all flange recesses and protects both flat flange faces:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair ft_inner_shield --reference /tmp/ft-inner-shield-smooth-reference.stl
python3 scripts/beamline_cad_benchmark.py --pair ft_inner_shield \
  --filled-reference /tmp/ft-inner-shield-smooth-reference.stl --executable /path/to/fixed/gemc \
  --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/ft-inner-shield-smooth-control --events 200 --repeats 5
```

For the incremental upgrade workload, use `previous/FTInnerShield.stl` from the revision archive as
`--filled-reference` and pass `--baseline-description` describing the previous retained-recess mesh.
Both comparisons use the unchanged fixed executable and matched 0.7--2.7-degree primaries. The archive
contains the engineering input, smooth reference, previous mesh and code, every primary/time/log file,
surface/containment proofs, unchanged-cone assembly checks, and full-construction/comparator evidence.

## Moller cone

Rebuild the cone and retain both references for material and repaired-reference timing comparisons:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair moller_cone --reference /tmp/moller-clearance-reference.stl \
  --repair-reference /tmp/moller-hole-filled-reference.stl
/Users/ungaro/venv/pygemc/bin/python scripts/beamline_cone_clearance.py \
  --output /tmp/moller-clearance.json
python3 scripts/beamline_cad_benchmark.py --pair moller_cone \
  --executable /path/to/fixed/gemc --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/moller-upgrade --events 200 --repeats 5
python3 scripts/beamline_cad_benchmark.py --pair moller_cone \
  --filled-reference /tmp/moller-clearance-reference.stl \
  --executable /path/to/fixed/gemc --database /tmp/beamline.sqlite \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/moller-reference-control --events 200 --repeats 5
```

The builder reads the owning GXML placements and the current smooth-flange FTInnerShield. The archive
retains that unchanged shield, all placement inputs, both references, final and reproduced meshes,
geometry database fixtures, raw logs/time reports/primaries, and archived scripts. The original cone is
open and emits solid and stuck-track warnings; only the repaired-reference control isolates decimation.
The binary itself is not redistributed; its SHA-256 is recorded in both benchmark metadata files.

## Downstream socket clearance revision

The current downstream builder includes both socket reliefs. Use the previous optimized meshes from
the new revision archive as the three-part benchmark baseline; the older downstream archive retains
the historical 5,000-triangle Segment 1 and its original two-volume benchmark.

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair downstream
/Users/ungaro/venv/pygemc/bin/python scripts/beamline_downstream_clearance.py \
  --output /tmp/downstream-clearance.json
python3 scripts/beamline_cad_benchmark.py --pair downstream_joints \
  --executable /path/to/fixed/gemc --database /tmp/beamline.sqlite \
  --originals /path/to/archive/previous --output /tmp/downstream-joint-benchmark --events 200 --repeats 5
```

## Beamline run selection

All beamline SQLite banks now use `default`. From the owning `clas12-systems` repository, regenerate a
database and check every configured beamline run with the local Python environment and installed GEMC:

```shell
PY=build/subprojects/pygemc/python_env/bin/python3
$PY geometry_src/beamline/beamline.py -f sqlite -sql /private/tmp/beamline-run-check.sqlite
$PY scripts/check_geometry_gemc.py /path/to/fixed/gemc /path/to/plugin/lib \
  geometry_src/beamline /private/tmp/beamline-run-check.sqlite
$PY scripts/compare_ascii_databases.py beamline --workdir /private/tmp/beamline-ascii-check --keep
```

For the interactive example, regenerate the database used by the card, then run
`gemc beamline.yaml -gui -runno=16000` from `geometry_src/beamline`. The transverse card selects run
10000204 by default; `-runno=10000206` and `-runno=10000207` select forward and midpoint wedges.

`data/beamline_run_selection/` retains the old and new SQLite fixtures, the headless card used for the
matched run-16000 check, logs, validation, and executable/source/STL hashes. To replay the before/after
construction, use a scratch directory with a `stls` symlink to the owning beamline meshes and run the
retained card with `-sql=/path/to/before.sqlite` or `-sql=/path/to/after.sqlite`, plus `-runno=16000`.
The tested executable is identified by SHA-256; it is not redistributed. Existing benchmark archives
are unchanged and keep their historical variation labels.

## Moller cone tip

The October 15 tip study is independent of the earlier main-cone study. Reproduce from the owning
`clas12-systems` repository using the archived original and current builder:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair cone_tip
python3 scripts/beamline_cad_benchmark.py --pair cone_tip --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/cone-tip-benchmark --events 200 --repeats 5
```

The source variation is `rgk_winter2018`, mapped to run 5874 in the beamline run table. Select that run
with `default`; this tip is absent from run 11. Both fixture databases and the benchmark card retain the
selected run. `beamline_cone_tip_archive.zip` contains all 52 isolated process logs/time reports, matched
primaries, original and final STL bytes, unchanged assembly cone, both assembly checks, eight complete
construction logs, code snapshots, generation/comparison checks, and executable/source hashes.
The executable is not redistributed. Earlier study archives are unchanged. The tip/main-cone assembly
overlap remains; isolated tracking performance does not validate the complete beamline geometry.

## FT flange

The October 15 flange study selects `rgk_winter2018`, run 5874, with `default`; the flange is absent
from run 11. From the owning `clas12-systems` repository:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py --pair ft_flange
python3 scripts/beamline_cad_benchmark.py --pair ft_flange --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/ft-flange-benchmark --events 2000 --repeats 5
```

`beamline_ft_flange_archive.zip` retains both database fixtures, original and optimized meshes, the
unchanged neighboring meshes and assembly fixtures, all 52 isolated process logs/time reports, matched
primaries, eight complete-configuration logs, code snapshots, and provenance hashes. It includes the
pre-change manifests and GEMC2 database backup used for integrity checks. The tested executable is
identified by SHA-256 and is not redistributed. All earlier study archives remain unchanged.
The isolated timings show no meaningful speed gain, and existing assembly defects remain.

## Inner Moller-cone extension

Select `rgk_winter2018`, run 5874, with `default`. The extension is absent from run 11.
From the owning `clas12-systems` repository:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair extension_inner --reference /tmp/inner-extension-reference.stl
python3 scripts/beamline_cad_benchmark.py --pair extension_inner --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/inner-extension-upgrade --events 200 --repeats 5
python3 scripts/beamline_cad_benchmark.py --pair extension_inner --runno 5874 \
  --filled-reference /tmp/inner-extension-reference.stl --executable /path/to/fixed/gemc \
  --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/inner-extension-control --events 200 --repeats 5
```

Run only one benchmark at a time. macOS process timing requires access to kernel resource statistics.
The archive retains one sandbox-denied timing attempt separately; it is excluded from all reported
measurements. `beamline_extension_inner_archive.zip` retains both complete repeated comparisons,
matched primaries, original/repaired/optimized meshes, assembly fixtures and probes, all four affected
complete configurations, database backups, code snapshots, and provenance. The executable is identified
by SHA-256 and is not redistributed. Earlier study archives remain unchanged. Raw-input timing includes
defects; the repaired-reference comparison measures decimation after restoring the port wall.

## Moller-cone extension lead fill

Select run 5874 with the default variation. Run only one benchmark at a time. The macOS time utility requires
kernel process-statistic access. From the owning clas12-systems repository:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair extension_lead
python3 scripts/beamline_cad_benchmark.py --pair extension_lead --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/extension_lead-benchmark --events 200 --repeats 5
```

The extension_lead archive retains matched primaries, all 52 process logs and time reports, original and
optimized meshes, both database snapshots, assembly fixtures, complete construction fixtures, code snapshots,
and provenance hashes. The executable is identified by SHA-256 and is not redistributed. Earlier study
archives remain unchanged.

## Moller-cone extension lead case

Select run 5874 with the default variation. Run only one benchmark at a time. The macOS time utility requires
kernel process-statistic access. From the owning clas12-systems repository:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair extension_case
python3 scripts/beamline_cad_benchmark.py --pair extension_case --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/extension_case-benchmark --events 200 --repeats 5
```

The extension_case archive retains matched primaries, all 52 process logs and time reports, original and
optimized meshes, both database snapshots, assembly fixtures, complete construction fixtures, code snapshots,
and provenance hashes. The executable is identified by SHA-256 and is not redistributed. Earlier study
archives remain unchanged.

## Moller-cone extension tungsten add-on

The October 16 study selects run 5874 with `default`. From the owning `clas12-systems` repository:

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair extension_tungsten --reference /tmp/tungsten-reference.stl
python3 scripts/beamline_cad_benchmark.py --pair extension_tungsten --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/tungsten-upgrade --events 200 --repeats 5
python3 scripts/beamline_cad_benchmark.py --pair extension_tungsten --runno 5874 \
  --filled-reference /tmp/tungsten-reference.stl --executable /path/to/fixed/gemc \
  --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original \
  --output /tmp/tungsten-control --events 200 --repeats 5
```

Run only one benchmark at a time. macOS process timing requires kernel resource-statistic access.
`beamline_extension_tungsten_archive.zip` retains both complete five-seed comparisons, matched
primaries, raw/repaired/optimized meshes, feature probes, the exact repair audit, placed assembly
checks, all four complete affected configurations, database snapshots, code, and provenance hashes.
The executable is identified by SHA-256 and is not redistributed. Earlier archives remain unchanged.
Raw-input timing includes defects; the repaired-reference control measures decimation alone.

## FT/cone joint clearances

Select run 5874 with the default variation. From the owning clas12-systems repository, run the final clearance
pass after the earlier individual builders. The archived optimized inputs preserve the exact baseline; the
historical tungsten add-on builder uses their main cone for its pinned dependency.

```shell
/Users/ungaro/venv/pygemc/bin/python geometry_src/beamline/build_cad_meshes.py \
  --pair ft_joints --reference /tmp/ft-joint-case-reference.stl
python3 scripts/beamline_cad_benchmark.py --pair ft_joints --runno 5874 \
  --executable /path/to/fixed/gemc --database geometry_src/beamline/gemc.db \
  --originals ../clas12Tags/geometry_source/beamline/cad_original/ft_joint_inputs_20261016 \
  --output /tmp/ft-joints-benchmark --events 200 --repeats 5
```

The separate beamline_ft_joints_archive.zip retains the pre-clearance and corrected meshes, both database
fixtures, all final benchmark logs/time reports and matched primary files, the excluded cap-triangulation
trial, independent geometry checks, full affected run fixtures, code snapshots, and provenance. The executable
is identified by hash and is not redistributed. All earlier archives remain unchanged.

## HTCC cone transfer and validation

The October 19 checks use GEMC 6.2 and Geant4 10.7.4 with the local CCDB SQLite database. The HTCC
dataset contains construction and overlap validation only; no repeated performance benchmark was run.
The dedicated `htcc_archive.zip` includes raw/cured STLs, fixtures, code, and all retained validation logs.
`data/htcc/mesh_health.json`, `validation.json`, and `provenance.json` describe the inspected inputs.

Extract the archive to a writable scratch directory. Its `code/` directory contains the mesh inspector,
initialization/database checker, cone/window overlap checker, original GEMC3 curing recipe, and the
documentation collection script. The validation scripts use the owning repositories at
`/opt/projects/gemc/clas12Tags` and `/opt/projects/gemc/clas12-systems`; they write fixtures under
`/private/tmp/htcc-stl-validation`. Do not run the original GEMC3 builder against the now-cured GEMC2 input:
use the archived raw inputs in `geometry_source/htcc/cad_original/` to reproduce the curing recipe.

After loading the GEMC2 module, run with a Python environment containing PyMeshLab and NumPy:

```shell
source /opt/homebrew/opt/modules/init/zsh
module use /opt/projects/ceInstall/modules
module load gemc/dev
export CCDB_CONNECTION=sqlite:///opt/projects/gemc/clas12Tags/geometry_source/coatjava/etc/data/sqlite/ccdb.sqlite
/Users/ungaro/venv/pygemc/bin/python code/inspect_htcc_meshes.py
/Users/ungaro/venv/pygemc/bin/python code/validate_htcc_stls.py
/Users/ungaro/venv/pygemc/bin/python code/check_htcc_entry_overlap.py
```

The archived inspector reads the archived raw source directory and the active GEMC3 meshes. The driver
resolves run mappings through `ci/env.sh`, compares row counts before individual native rows, checks CAD
placements separately, and initializes the three variations through both factories with `N=0`.
For full default SQLite assembly diagnostics, run the generated fixture with `CHECK_OVERLAPS=2`:

```shell
export GEMC_DATA_DIR=/opt/projects/gemc/clas12Tags
cd /private/tmp/htcc-stl-validation/11-sqlite
/opt/projects/gemc/clas12Tags/source/gemc check.gcard -USE_GUI=0 -N=0 -CHECK_OVERLAPS=2 -GEO_VERBOSITY=2
```

The isolated raw/cured window check fixes `RANDOM=12345` and requests `CHECK_OVERLAPS=1000`. It reproduces
the cured entry cone's approximately 0.053 mm contact; the matched raw-cone fixture reports none.
Retain that warning and the Moller cone's remaining 24 non-manifold edges as unresolved limitations.
Executable and dependency hashes captured when documenting the study are identified separately from the
original validation logs; an exact validation-time executable hash was not recorded by the original driver.
