# CAD optimization technical note

Author: Maurizio Ungaro, Jefferson Lab. LTCC measurements: October 1, 2026; beamline: October 12--16.
Note updated October 20, 2026.

The note covers LTCC, the October 12--16 beamline CAD studies, and the October 19 HTCC transfer.
Beamline measurements use GEMC3 and separate matched-primary workloads; engine timings are not pooled.

The LaTeX project follows the `simgrid_osg_portal` note structure and the CLAS12 house style.
`cad_optimization.tex` is the main source; `chapters/` holds the scientific discussion.
The compiled note is `cad_optimization.pdf`. The Markdown draft is retained for review.

Build with installed Meson, latexmk, and TeX Live:

```shell
meson setup /private/tmp/cad-note-build .
meson compile -C /private/tmp/cad-note-build
meson install -C /private/tmp/cad-note-build
```

The install step copies the PDF into this source directory. Auxiliary build files stay in the build directory.
`figures/transport_comparison.tex` is the standalone PGFPlots source; rebuild it with `latexmk -pdf`.

The primary benchmark restores all ten original `cadTempRemoved` meshes and their sector copies.
`REPRODUCE.md` documents execution; `data/` stores results and provenance. `study_archive.zip` retains
raw logs, time reports, input fixtures, and analysis scripts. No executable is redistributed.

The full port changes materials and mothers as well as meshes. It improves loading, memory, and
nonoptical electron throughput, while hadron and optical electron workloads use more CPU time.
Higher CPU use may reflect more complete transport after navigation defects are removed; lower original
CPU time does not establish faster correct transport. Remaining overlap reports and detector-response
equivalence require separate studies.

## STL image comparisons

`figures/` includes paired hardware, nose, and Winston-cone views as PNG and PDF files.
Rebuild them directly from the owning `clas12Tags` repository with Python, NumPy, and Matplotlib:

```shell
python3 figures/render_stl_comparison.py --repo /opt/projects/gemc/clas12Tags --baseline-ref ea3625f
```

The script reads original meshes from Git and optimized meshes from the current repository. It checks
triangle counts and placement transforms, and retains STL hashes and camera settings in the figure metadata.
Matched cameras and common bounds preserve the scale within each pair. These images render unmodified
stored triangles, including facets rejected by Geant4; they are not screenshots of Geant4-accepted solids.
The hardware views show one sector's frame and nose, while separate panels show individual cone sources.

## Beamline apex progress

The measured apex dataset is in `data/beamline_apex/`; `beamline_apex_archive.zip` retains the raw logs,
time reports, fixtures, scripts, and original/optimized meshes. The scientific discussion is in
`chapters/beamline.tex`, with mesh quality checks and a matched-camera STL comparison.

## Downstream tube progress

The October 12 downstream study is in `chapters/downstream.tex` and `data/beamline_downstream/`.
`beamline_downstream_archive.zip` retains fixtures, logs, time reports, original/optimized meshes,
and scripts. Triangle reduction is modest; the main repair closes annular seams without blocking the bore.
Measured surface differences, retained placement overlaps, and navigation warnings are reported explicitly.

## Adapter and exit shield progress

The October 13 study is in `chapters/exit_shield.tex` and `data/beamline_exit/`.
`beamline_exit_archive.zip` retains fixtures, logs, time reports, originals, and reproduction scripts.
The adapter is renamed `Beamline_Adapter_1`; the already-coarse group is reduced by only 0.434%, with
432 casing mating faces protected and the lead fill retained byte for byte. The measured timings do
not establish a substantial performance gain. Diagnostics and remaining full-beamline warnings are explicit.

## FT adjuster progress

The October 13 material-model study is in `chapters/ft_adjuster.tex` and `data/beamline_adjuster/`.
`beamline_adjuster_archive.zip` retains the original trio, both fixtures, timing/diagnostic records, and
reproduction scripts. The simplified model has 48 triangles and matches the estimated sealed reference
union volume within 0.00003%. Original openings, overlapping material, and response limitations are explicit.

## FT inner shield progress

The October 13 study is in `chapters/ft_inner_shield.tex` and `data/beamline_inner_shield/`.
`beamline_inner_shield_archive.zip` retains the original, fixtures, raw logs/time reports, component
validation, and reproduction scripts. The renamed mesh has 22,000 triangles, unchanged bounds and
pocket geometry, and sampled differences below 0.05 mm. The isolated and full-beamline diagnostics
are retained separately; loading and transport figures apply only to this workload.

## FT inner-shield bolt progress

The October 13 bolt study is in `chapters/ft_bolts.tex` and `data/beamline_bolts/`.
`beamline_bolts_archive.zip` retains all nine engineering originals, both timed fixtures, matched primaries,
raw logs, model dimensions, surface clearance checks, and the shield-plus-bolts overlap fixture.
Tracking times and ratios are reported alongside the earlier five beamline studies in their own sections.

## FT outer flange progress

The October 13--14 study is in `chapters/ft_outer_flange.tex` and `data/beamline_outer_flange/`.
The separate `beamline_outer_flange_archive.zip` retains the original and hole-filled reference, optimized
fixtures, tracking results, executable hash, raw diagnostics, and repeated assembly overlap checks.
The note records all nine independent beamline studies without pooling their performance results.

## Outer-flange control at fixed material volume

The October 14 follow-up compares the 2,084-triangle hole-filled reference with the 836-triangle simplified
flange. Five repetitions use 2,000 events per particle and the same fixed executable, material, and placement.
Section 12.1 and Table 26 report this control separately from the earlier drilled-versus-filled comparison.
`data/beamline_outer_flange_control/` and the control entries in the outer-flange archive retain all results.

## FT outer mount progress

The October 14 study is in `chapters/ft_outer_mount.tex` and `data/beamline_outer_mount/`.
`beamline_outer_mount_archive.zip` retains the original mesh, sealed and relieved references, unchanged
flange, clearance proofs, original/optimized assembly fixtures, raw transport logs, and reproduction scripts.
The previously reported flange/mount interference is removed in the optimized 10,000-point assembly check.

## FT inner shield progress

The October 14 study is in `chapters/ft_shield.tex` and `data/beamline_ft_shield/`.
`beamline_ft_shield_archive.zip` retains the engineering input, reconstructed hole-filled reference,
both repeated tracking comparisons, feature probes, assembly/full construction logs, and reproduction scripts.
The two longitudinal grooves and blind flange recesses are retained; existing shield/cone interference remains.

## FT inner-shield smooth-flange revision

Section 14.1 supersedes the initial shield mesh with a 6,500-triangle smooth-flange version.
The original chapter, figures, measurements, and archive remain as historical evidence.
`data/beamline_ft_shield_smooth/` and `beamline_ft_shield_smooth_archive.zip` retain both new tracking
comparisons, the previous mesh, the smooth reference, flange-surface proofs, and validation logs.

## Moller cone

Section 15 adds the renamed 5,000-triangle cone with surface holes filled and a widened shield opening.
The cone/shield joint passes independent checks and the 10,000-point Geant4 overlap test.
`data/beamline_moller_cone/` and `beamline_moller_cone_archive.zip` retain the raw-input and clean-reference
tracking comparisons, material references, all nine placements, and validation evidence.

## Downstream socket clearance revision

Section 16 resolves the adapter and downstream tube contacts with local relief in Segment 1.
The previous study archives remain unchanged. `data/beamline_downstream_joints/` and
`beamline_downstream_joints_archive.zip` retain the previous and relieved meshes, all raw benchmark
runs, independent clearance checks, full default construction, and reproduction inputs.

## Beamline run selection

Section 17 records the October 15 database-selection fix. All beamline SQLite geometry and material banks
use `default`, selected by run number. Run 16000 loads ten native and 22 CAD volumes. All 17 configured
runs pass construction, with unchanged physical geometry and successful GEMC2 semantic comparisons.
`data/beamline_run_selection/` retains before/after fixtures, construction/comparison logs, and provenance.

## Moller cone tip

Section 18 adds the renamed 5,000-triangle tip in all four applicable run configurations. Protected sharp
faces, openings, bounds, and near-identical tungsten volume are retained. Five-seed isolated tracking
benchmarks are clean and faster for all four particles; the pre-existing main-cone/tip assembly overlap
remains and is reported with complete-configuration warnings. `data/beamline_cone_tip/` and
`beamline_cone_tip_archive.zip` retain mesh checks, raw measurements, fixtures, and reproduction evidence.

## FT flange

Section 19 records the `FTFlange` rename and conservative 552-to-540 triangle reduction in four runs.
Five repetitions of 2,000 matched events per particle show no meaningful tracking-speed gain. Existing
inner/outer assembly contacts and open-surface warnings remain. `data/beamline_ft_flange/` and
`beamline_ft_flange_archive.zip` retain the mesh checks, raw results, assembly fixtures, and provenance.

## Inner Moller-cone extension

Section 20 records the `moller-cone-extension-inner` rename, missing radial-port wall repair, and
30.77% triangle reduction. Passages remain open, protected faces and bounds are retained, and separate
raw-input and repaired-reference tracking comparisons distinguish repair from decimation.
`data/beamline_extension_inner/` and `beamline_extension_inner_archive.zip` retain all raw measurements,
mesh/feature checks, placed assembly diagnostics, complete configurations, and reproducibility inputs.


Sections 21 and 22 record the renamed Moller cone extension lead fill and case, mesh checks, repeated tracking
timings, and existing assembly overlaps. The corresponding data directories and separate archives retain
reproducible fixtures and provenance.

## Moller-cone extension tungsten add-on

Section 23 records the `moller-cone-extension-tungsten-addon` rename, missing radial-port wall repair, and
56.80% triangle reduction. Passages remain open, protected faces and bounds are retained, and separate
raw-input and repaired-reference tracking comparisons distinguish repair from decimation.
`data/beamline_extension_tungsten/` and `beamline_extension_tungsten_archive.zip` retain all raw measurements,
mesh/feature checks, placed assembly diagnostics, complete configurations, and reproducibility inputs.


Section 24 records the final FT/cone interface clearances, material changes, and tracking comparison. All
corrected interfaces and affected complete configurations pass their stated checks. data/beamline_ft_joints/
and the separate archive retain the final evidence and excluded cap trial.

## HTCC cone transfer

Section 25 records the three HTCC cone meshes transferred into GEMC2: 49.20% fewer triangles, six successful
TEXT/CAD and SQLite/CAD initialization checks, and matching native/CAD rows in three runs. The Moller cone
retains 24 non-manifold edges, and the cured entry cone has an unresolved 0.053 mm entry-window contact. No
loading or transport-speed gain is measured. The chapter is in chapters/htcc.tex; data/htcc/ and
htcc_archive.zip retain the supporting evidence.
