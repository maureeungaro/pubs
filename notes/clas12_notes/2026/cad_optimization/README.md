# CAD optimization technical note

Author: Maurizio Ungaro, Jefferson Lab. LTCC measurements: October 1, 2026; beamline: October 12--16.
Note updated October 21, 2026.

The note covers LTCC, the October 12--16 beamline CAD studies, the October 19 HTCC transfer, and the
October 21 removal of duplicate magnets shielding.
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

## Magnets duplicate shielding removal

Section 26 records removal of nine DSShield meshes and apex from all three magnets configurations in GEMC2 and
GEMC3: 61 to 51 meshes and 148,940 to 132,230 triangles (11.22% fewer). The beamline retains the shielding.
Repeated loading and four-particle tracking results, remaining geometry warnings, and all-run validation are
reported separately. data/magnets_dedup/ and magnets_dedup_archive.zip retain the complete evidence.

## Downstream shielding plate and vacuum jacket

Section 27 optimizes the two original volumes separately: 1,380 to 508 plate triangles and 2,392 to 556 jacket
triangles (71.79% fewer together), with fourteen fastener features filled. Main rims, apertures, bounds, and
the gap are retained. The signed volume increase, repeated final-model tracking results, clean isolated
construction, and residual assembly warnings are explicit. data/magnets_plate/ and magnets_plate_archive.zip
retain all evidence.

## Upstream shielding plate and vacuum jacket

Section 28 keeps the original two upstream names and placements, fills fourteen fastener features, and reduces
4,256 triangles to 1,512 (64.47%). The outer rounded jacket features, stepped bore, bounds, and gap are
retained. Independent probes, material changes, repeated tracking results, and residual diagnostics are
explicit. data/magnets_upstream/ and magnets_upstream_archive.zip retain the evidence.

## DC region-1 back membranes

Section 29 moves the six membranes to DC and replaces six STL builds with one shared solid and five copies.
Unique facets fall from 120 to 20 (83.33%). Integer angles pass the dense assembly overlap comparison. The
note reports submillimetre displacements, signed Kapton-volume changes, repeated startup/tracking
measurements, and remaining assembly warnings. data/dc_back/ and dc_back_archive.zip retain the evidence.

## DC region-1 supports

Section 30 moves the six aluminum support assemblies to DC, with one unchanged STL and five copies. Unique
facets fall from 6,036 to 1,006 (83.33%). Integer angles pass dense overlap checks. The note reports the small
signed-volume change, accepted millimetre-scale displacements, repeated startup and tracking measurements, and
remaining assembly warnings. data/dc_support/ and dc_support_archive.zip retain the evidence.

## Vacuum jackets with all holes retained

Section 31 renames shell1a to vacuumJacket and shares compatible jackets while retaining two different
families, all holes, and four original exports needed for distinct details or plate contacts. Six sources
supply twelve placements, with 48.86% fewer unique facets. The note records repeated timing, material changes,
and no added sampled assembly overlaps. Evidence is retained in data/magnets_vacuum/ and
magnets_vacuum_archive.zip.

## Jacket naming follow-up

All active shell placements and source STLs now use vacuumJacket names with sector/side suffixes, retaining
the original vacuumJacket base name. Existing study archives preserve their measured inputs.
data/magnets_vacuum_naming/ and magnets_vacuum_naming_archive.zip record the mapping and validation; this
changes neither geometry nor the measured performance.

## Torus coils

Section 32 shares one unchanged copper coil across six sectors, with all openings retained and 83.33% fewer
unique facets. Repeated timing, the dense overlap comparison, and both-engine validation are retained in
data/magnets_coils/ and magnets_coils_archive.zip. Duplicate-isotope failures also affect the original
geometry; tracking statistics include only completed pairs.

## Hub covers

Section 33 shares two unchanged hub-cover STLs across six sectors, retaining every hole and reducing unique
facets by 53.45%. Repeated timing and memory measurements, both-engine construction checks, and the
naming-controlled dense overlap comparison are retained in data/magnets_hub_covers/ and
magnets_hub_covers_archive.zip.

## Hub shields

Section 34 shares the five matching middle hub shields while retaining the two different ends and every hole
and reducing unique facets by 61.55%. Repeated timing and memory measurements, both-engine construction
checks, and the naming-controlled dense overlap comparison are retained in data/magnets_hub_shields/ and
magnets_hub_shields_archive.zip.

## Cold hub

Section 35 repairs the cold hub while retaining every opening and reducing unique facets by 0.41%. Repeated
timing and memory measurements, both-engine construction checks, and the naming-controlled dense overlap
comparison are retained in data/magnets_cold_hub/ and magnets_cold_hub_archive.zip.

## Bore tubes

Section 36 records the bore-tube audit and BoreCenterTube rename. All 1,130 facets remain to preserve the
original profiles and holes; no speedup is claimed. Evidence is in data/magnets_bore_tubes/ and
magnets_bore_tubes_archive.zip.

## HTCC Moller repair

The October 23 revision of Section 25 resolves the Moller-cone orientation warning in both engines, restores a
conical section lost during curing, and retains its bore and bounds. Evidence is in data/htcc_moller_repair/
and htcc_moller_repair_archive.zip; the prior entry-cone/window contact remains.

## Detector bank consolidation

Section 37 consolidates DC and magnets copy placements into their main banks, retaining the physical solenoid
name and all meshes. Twenty construction checks and repeated-generation evidence are retained in
data/detector_banks/ and detector_banks_archive.zip. No new speedup is claimed.
