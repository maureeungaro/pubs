# Performance and geometry validation of optimized CLAS12 CAD models

Maurizio Ungaro

Jefferson Lab, 12,000 Jefferson Avenue, 23606 Newport News, VA, USA

## Abstract

This study compares LTCC CAD optimization and sixteen separate GEMC3 beamline mesh studies with original
engineering STL files. The complete optimized LTCC model contains 93.9% fewer triangles and bytes, with
median initialization CPU time reduced by 63.5% and startup peak memory by 56.8%. Nonoptical LTCC electron
transport is 1.29 times faster by CPU time, while hadron and optical workloads require 1.35--1.53 and 1.73
times as much CPU time; material and hierarchy changes and more complete transport after defect repairs may
contribute. The apex, downstream, and adapter/exit-shield studies reduce triangles by 45.4%, 3.75%, and
0.434%, respectively, with apex startup wall time and peak memory reduced by 15.7% and 17.4%. The FT
adjuster consolidation reduces triangles by 98.74% while matching an estimated reference union volume, and
the FT inner shield and flange assembly is reduced by 36.14% with its enclosed pocket retained exactly and
sampled surface differences below 0.05 mm; the nine FT inner-shield bolts have 89.38% fewer triangles,
matched copper volumes, and explicit clearance from the shield; the FT outer flange retains its rims with
60.79% fewer triangles and twelve bolt holes filled; the repaired outer mount clears the flange with 11.44%
fewer triangles. These independent workloads do not establish detector-response equivalence or complete
overlap freedom, and remaining geometry and navigation diagnostics are reported explicitly. The downstream
FT inner shield is rebuilt with closed through-holes and retained longitudinal grooves and fully smooth
flange faces. The Moller cone has 68.32% fewer triangles, filled surface holes, and a widened opening that
clears the FT inner shield; repaired-reference tracking separates decimation from source defects.

The separate HTCC transfer reduces three cone meshes by 49.20% in triangles; six initialization checks pass,
with remaining non-manifold edges and a 0.053 mm entry-window contact recorded.

## 1. Scope and geometry changes

The question is how much the optimized LTCC CAD implementation changes loading cost, memory use, particle-
transport cost, and geometry diagnostics. This is a software and geometry study, not a background-rate
prediction or a measurement of LTCC photon yield. No experimental data were collected.

The original data are taken from main revision ea3625f. The port uses the LTCC CAD changes in meson revision
4c7c6af. The later PMT absorption change in revision 3472ede is excluded, so PMT optical properties remain the
same in the compared geometries. The unrelated Meson build-system changes are also excluded; the same installed
executable runs every case.

The primary comparison restores all ten files from main's cadTempRemoved directory: S1-BW, S1-LW, S1-RW, S1-TRB,
NFrame, FrontPlate, Mount, Nose, BottomPlate, and Epoxy. Source volumes are placed in sector 3 and the disabled
frame and six-part nose copies are enabled in the other five sectors. The benchmark preserves the legacy
placement formulas and material assignments from ltcc_frame.pl: source frame volumes are aluminum, copied frames
are stainless steel, nose pieces are aluminum, and Epoxy is G4_CR39. No STL facet is repaired or removed in the
original baseline. This gives 90 frame/nose physical placements, compared with 24 in the consolidated
implementation, excluding the Winston cones.

The previous production configuration had this hardware disabled. Comparing it directly with the complete meson
model changes the amount of simulated hardware and answers a different question. Those initial measurements are
retained as supplementary context; the headline optimization results in this note compare the complete original
and consolidated models.

The consolidated implementation uses four hardware source volumes: backwall, rightwall, leftwall, and nose.
Sector 3 contains the source volumes; enabled sectors reuse them through CopyOf placements inside their LTCC
mothers. The port restores walls and nose hardware that were disabled in the original geometry, changes the
frame hierarchy and some materials, and replaces the previous chain of mother-volume subtractions with a fitted,
planar G4Trap intersection. The unmodified engineering drawings remain archived in the geometry source
repository. The restored original baseline keeps the legacy mothers and hierarchy unchanged.

The consolidated nose uses the implementation's effective material at density 3.86 g/cm³, with mass fractions
0.9464 stainless steel, 0.0408 carbon, 0.0043 hydrogen, and 0.0085 oxygen. This study does not establish
material-budget or detector-response equivalence to the original model.

Three cases separate part of the optimization: Original uses the old data; Cones only replaces only WC_S, WC_M,
and WC_L while retaining the restored original frame, mothers, and materials; Full port uses the new geometry
and all its optimized meshes. Cones only is a diagnostic configuration, not an implementation proposed for
deployment. Frame consolidation and mother changes remain combined in the Full port case and cannot be assigned
independent transport speedups from this comparison.

Figures 1–3 compare renderings of the original and optimized STL files directly. The original includes all
restored CAD hardware. Paired panels use identical orthographic cameras, common bounds, and the same scale; no
mesh repair, smoothing, or additional decimation is applied. The hardware view applies the sector-3 placements,
including the sector mother transform for the optimized model. The resulting hardware transforms are checked
against the restored original placements. Nose and cone close-ups use their stored STL coordinate systems.
Colors identify functional hardware groups, not materials. The images expose simplification and changes in
shape; they do not establish volume, material-budget, or detector-response equivalence.

![Hardware STL comparison](figures/hardware_stl_comparison.png)

Figure 1. Sector-3 STL frame and nose hardware: complete original on the left and optimized on the right. Upper
panels show shaded front oblique views; lower panels show rear oblique views with triangle edges. The same
camera and scale are used within each row. The 15 original meshes contain 124,652 triangles; the four optimized
meshes contain 3,646. Winston cones, native LTCC mirrors, PMTs, mothers, and other sector copies are omitted.

![Nose STL comparison](figures/nose_stl_comparison.png)

Figure 2. Nose consolidation in the stored engineering coordinates, with identical camera and scale: six
original meshes and 12,012 triangles on the left; one optimized mesh and 1,986 triangles on the right. Triangle
edges are shown; simplified details and differences in the rendered envelope are visible.

![Cones STL comparison](figures/cones_stl_comparison.png)

Figure 3. Winston-cone meshes with triangle edges: WC_S, WC_M, and WC_L from top to bottom; original on the
left and optimized on the right. The camera, bounds, and scale match within each row. Original triangle counts
are 4,312, 3,076, and 2,578; each optimized mesh contains 1,500 triangles. These are individual source meshes,
not all physical cone placements.

## 2. Simulation and measurement configuration

All runs use the local gemc/dev module, which reports GEMC 6.2, and Geant4 10.7.4 on macOS arm64. A local CCDB
SQLite database prevents remote calibration access. Executable and STL SHA-256 hashes, the complete gcard,
commands, and platform information are retained with the results.

The physics list is STD + FTFP_BERT, with Optical enabled only for the optical electron workload. Only LTCC is
present. RUNNO is explicitly 11 with the default geometry variation, enabling six LTCC sectors. The primary
momentum is 5 GeV/c, the vertex is at the origin, the polar angle spans 15–35 degrees, and the azimuth spans the
full circle. Both magnets are off; polarity is therefore not applicable. There is no target, no imposed beam
current, no luminosity normalization, no bunch-time window, and no background pileup. Each event contains one
primary particle. FTOn/FTOff and shielding configurations are not applicable to this isolated detector test.

Initialization runs use N=0. Optical electron runs use 1,000 events; electron, proton, positive-pion, and
neutron runs without optical processes use 10,000 events each. Each timing workload has five repetitions with
seeds 12345–12349, rotating the order of the three geometry cases. The nonoptical tests use matched LUND files:
every geometry receives identical primary tracks for a given seed. The corrected optical study also uses matched
LUND primaries. Random histories of secondary particles can differ because the geometries and ensuing transport
differ.

Event output and the GUI are disabled. The benchmark applies identical default production cuts; no obsolete
frame-specific cut is used. No readout threshold or detector rate is evaluated. GEMC reports process CPU time
and its events-only CPU time separately. Its events-only timer excludes the first warmup event and scales the
remaining time to the full event count. The macOS time utility records wall time and maximum resident-set size.
Medians summarize five runs; observed ranges are provided where useful and are not confidence intervals. The
machine was not dedicated to the study, so wall time includes scheduling and system-load variation.

A separate CAD-only loading test removes the TEXT detector hierarchy and loads the active STL solids directly
into the world with standard aluminum, no sensitivities, no field, and N=0. The same executable and physics
selection are used. This artificial configuration measures loading of the mesh bundle without native LTCC
mothers, copies, or custom-material definitions; its coincident world placements are not a physical simulation
and are not overlap-checked.

Construction diagnostics use CHECK_OVERLAPS=1, N=0, and seed 12345. GEMC performs placement construction checks
and invokes /geometry/test/run without overriding its sampling resolution. One diagnostic run per case counts
each G4Exception by code. Geant4 caps overlap reports per volume, and some warnings concern ineffective
sampling; the number of reports is not the number of all intersecting pairs. Runtime navigation warnings are
counted separately during event transport. No warning count is interpreted as proof of overlap-free geometry.

## 3. Mesh size and loading performance

Table 1 compares the active mesh inventory. Counts refer to unique STL source meshes selected by the CAD gxml,
not to repeated physical placements. All ten previously disabled meshes are active in the original comparator.
Nine frame meshes with 112,640 triangles become three meshes with 1,660 triangles (98.5% fewer). Six nose meshes
with 12,012 triangles become one mesh with 1,986 triangles (83.5% fewer). The three Winston cones shrink from
9,966 to 4,500 triangles (54.8% fewer), retaining three source meshes.

Table 1. Active CAD inventory for default LTCC geometry.

| Quantity | Original | Cones only | Full port |
| --- | --- | --- | --- |
| STL source meshes | 18 | 18 | 7 |
| Frame triangles | 112,640 | 112,640 | 1,660 |
| Nose triangles | 12,012 | 12,012 | 1,986 |
| Winston-cone triangles | 9,966 | 4,500 | 4,500 |
| All triangles | 134,618 | 129,152 | 8,146 |
| STL bytes | 6,732,412 | 6,459,112 | 407,888 |
| Frame/nose placements | 90 | 90 | 24 |
| TEXT geometry rows | 2,438 | 2,438 | 2,377 |
| Component rows | 668 | 668 | 662 |

Table 2 separates full-detector initialization from the artificial CAD-only loading test. LTCC initialization
CPU time decreases from 1.874 to 0.684 s (63.5%); startup memory decreases from 176.75 to 76.31 MiB (56.8%).
CAD-only loading CPU time decreases by 92.6%, demonstrating a loading benefit of the simplified mesh bundle
independently of the native mother redesign.

Table 2. Median initialization measurements over five N=0 runs; 1 MiB = 1,048,576 bytes.

| Measurement | Original | Cones only | Full port |
| --- | --- | --- | --- |
| LTCC CPU time (s) | 1.874 | 1.816 | 0.684 |
| LTCC wall time (s) | 2.592 | 2.530 | 1.388 |
| LTCC peak RSS (MiB) | 176.75 | 175.53 | 76.31 |
| CAD-only CPU time (s) | 1.321 | 1.271 | 0.098 |
| CAD-only wall time (s) | 2.066 | 2.027 | 0.835 |
| CAD-only peak RSS (MiB) | 165.97 | 162.89 | 66.22 |

## 4. Electron and hadronic transport

Table 3 gives median events-only CPU time per 1,000 primaries. The nonoptical entries divide the measured
10,000-event times by ten. Throughput factors are Original time divided by comparison time: values above one
indicate faster transport, and values below one indicate slower transport. Figure 4 presents these ratios and
the initialization ratio for direct comparison.

Table 3. CPU seconds per 1,000 events and transport throughput factors; zero magnetic field.

| Workload | Original | Cones only | Full port | Cone factor | Port factor |
| --- | --- | --- | --- | --- | --- |
| Electron + optical | 26.067 | 26.852 | 45.126 | 0.97 | 0.58 |
| Electron | 4.739 | 4.546 | 3.679 | 1.04 | 1.29 |
| Proton | 1.009 | 0.958 | 1.490 | 1.05 | 0.68 |
| Positive pion | 1.084 | 1.055 | 1.467 | 1.03 | 0.74 |
| Neutron | 0.575 | 0.601 | 0.877 | 0.96 | 0.66 |

Optical electron transport: the cone-only substitution has a throughput factor of 0.97; the full port has a
factor of 0.58. Original per-1,000-event CPU times range from 25.549 to 29.228 s, and full-port times range from
39.580 to 56.916 s.

Nonoptical electron transport: the cone-only substitution has a throughput factor of 1.04; the full port has a
factor of 1.29. Original per-1,000-event CPU times range from 4.207 to 6.261 s, and full-port times range from
3.476 to 6.536 s.

Proton transport: the cone-only substitution has a throughput factor of 1.05; the full port has a factor of
0.68. Original per-1,000-event CPU times range from 0.987 to 1.034 s, and full-port times range from 1.477 to
1.580 s.

Positive-pion transport: the cone-only substitution has a throughput factor of 1.03; the full port has a factor
of 0.74. Original per-1,000-event CPU times range from 1.060 to 1.170 s, and full-port times range from 1.444 to
1.546 s.

Neutron transport: the cone-only substitution has a throughput factor of 0.96; the full port has a factor of
0.66. Original per-1,000-event CPU times range from 0.543 to 0.651 s, and full-port times range from 0.842 to
0.908 s.

The cone-only comparison isolates the three substituted meshes. The full port additionally changes gas
containment, hardware coverage, placements, and materials. Optical paths and particle showers can therefore
differ, and faster loading does not imply faster transport or unchanged response. The measured changes include
both mesh-navigation cost and changes in physical transport; these data do not identify a unique cause. PMT
absorption was held fixed and cannot account for the difference between these cases.

Cone-only throughput ratios close to one represent small measured differences within the observed run variation;
these five repetitions do not establish a statistically significant speedup of the Winston-cone substitution.
The full-model timing also includes the revised materials and mothers, and does not separately measure CPU cost
per navigation query.

A separate matched 100-event electron diagnostic at seed 12345 enables tracking verbosity 1 and counts the
printed trace (Original: 18,271 track headers and 123,928 step rows; Cones only: 17,025 track headers and
115,895 step rows; Full port: 24,164 track headers and 203,087 step rows). Step rows include the initial row for
each track; they are not a direct count of navigation queries. These counts characterize the amount of transport
work in this sample. Verbose-run times are excluded from the timing tables, and this sample does not isolate the
contribution of each geometry change.

A separate matched 100-event proton diagnostic at seed 12345 enables tracking verbosity 1 and counts the printed
trace (Original: 6,135 track headers and 50,512 step rows; Cones only: 7,794 track headers and 62,163 step rows;
Full port: 9,566 track headers and 99,568 step rows). Step rows include the initial row for each track; they are
not a direct count of navigation queries. These counts characterize the amount of transport work in this sample.
Verbose-run times are excluded from the timing tables, and this sample does not isolate the contribution of each
geometry change.

The increased CPU time is consistent with more complete transport in the optimized geometry. The original model
has invalid or rejected facets and repeated stuck tracks requiring corrective navigation pushes; these defects
may alter material crossings and suppress expected particle histories. In the matched diagnostic samples, the
optimized model prints 1.64 times as many electron step rows and 1.97 times as many proton step rows. Lower CPU
time in the defective original model may therefore reflect incorrect or incomplete transport rather than a
lower cost of equivalent physics. These observations support that interpretation but do not establish
causation: materials and mothers also change, and this study does not compare energy balance, particle
survival, or detector response event by event.

![Transport comparison](figures/transport_comparison.png)

Figure 4. Original/comparison CPU-time ratios for initialization and particle transport. Bars use the ratio of
five-run medians. Transport uses the isolated default LTCC at RUNNO=11, 5 GeV/c primary momentum, and zero
magnetic field; only the optical electron workload enables optical processes. No readout threshold or luminosity
normalization applies. Ratios above one mean faster.

## 5. Warnings and geometry validation

Table 4 separates construction diagnostics from transport warnings. GeomVol1002 denotes placement overlap or
mother-containment reports; GeomSolids1001 records invalid-facet or surface-sampling warnings, and
GeomSolids1002 records rejected facets. GeomNav1002 denotes a stuck track for which the navigator attempts a
corrective push. Each exception header is counted once rather than counting repeated wording within the warning.

Table 4. Construction warning counts and total navigation warnings across five transport runs.

| Diagnostic | Original | Cones only | Full port |
| --- | --- | --- | --- |
| GeomVol1002 (construction) | 1505 | 1515 | 1420 |
| GeomSolids1001 (construction) | 857 | 857 | 2 |
| GeomSolids1002 (construction) | 857 | 857 | 0 |
| All construction warning lines | 3219 | 3229 | 1422 |
| Mother containment reports | 792 | 792 | 517 |
| Sibling overlap reports | 713 | 723 | 903 |
| Optical electrons navigation | 405 | 395 | 0 |
| Electrons navigation | 3486 | 3562 | 0 |
| Protons navigation | 1946 | 1959 | 0 |
| Positive pions navigation | 1899 | 1923 | 0 |
| Neutrons navigation | 1810 | 1852 | 1 |
| GeomNav0003 (event-abort requests) | 0 | 2 | 0 |
| GeomVol1002 (transport) | 0 | 4 | 0 |
| HAD_QGSPARTICIPANTS_002 (transport) | 0 | 0 | 1 |

The additional transport exception rows retain other diagnostics across all five workloads. The cone-only case
requests one event abort in optical electron seed 12347 and one in nonoptical electron seed 12349, both
following stuck tracks in the retained original frame geometry. Each reports that the track is abandoned after
25 zero steps. These runs exit normally and print timing footers, but that does not mean every event completed
its intended transport. Their timings are retained as measurements of this defective configuration, not
equivalent completed-event throughput. No GeomNav0003 event-abort request appears in the Original or Full port
cases. These mixed-workload totals are not event-normalized rates.

Original construction produces 3219 warning lines, while Full port produces 1422. Its diagnostic CPU time
changes from 237.66 to 257.80 s. Overlap-check timing is excluded from transport and initialization comparisons.
The stochastic construction check provides evidence of improvement where counts fall, but remaining reports and
unsampled intersections must be assessed separately.

Without overlap checking, each complete original import emits 857 invalid-facet warnings (GeomSolids1001) and
857 rejected-facet warnings (GeomSolids1002). The optimized import emits none of these warnings. Geant4
therefore excludes malformed facets from the original imported solids; the triangle counts in Table 1 describe
the files rather than accepted Geant4 facets.

An independent binary-STL check finds exactly 857 zero-area triangles in the original files: 452 in S1-LW, 396
in S1-RW, six in Epoxy, and three in NFrame. The optimized active meshes contain no exact zero-area triangles.
This check uses the cross product of the stored single-precision vertex differences and tests for an exactly
zero vector; it does not establish that all meshes are watertight or free of near-degenerate facets.

Mother-containment reports change from 792 to 517; sibling-overlap reports change from 713 to 903. The changed
hierarchy alters what is tested, so these are counts of emitted reports rather than a one-to-one comparison of
all physical intersections. Native mirror and PMT/light-guide reports remain, and the new walls and nose also
appear in the diagnostic logs. Resolving the remaining geometry problems is separate from the performance port.

The ported geometry generator reproduces the packaged TEXT data exactly for all six LTCC variations. The shared
CI helpers select runs and variations; a missing mapping for run 4763 was corrected before comparison. For each
run, SQLite geometry and CAD are selected at the latest default row with run less than or equal to RUNNO. Row
counts are checked first, followed by the repository's row-by-row geometry comparison. All comparisons pass, all
CAD mother and mesh references resolve, and the generation preserves all non-LTCC SQLite rows. One-event SQLite
runtime smoke tests also complete for all six runs without G4Exception reports. Table 5 records the effective
configurations and their row counts.

Table 5. Ported model: validated run-dependent TEXT/SQLite geometry and CAD row counts.

| RUNNO | TEXT variation | Geometry rows | CAD rows |
| --- | --- | --- | --- |
| 11 | default | 2377 | 7 |
| 3029 | rga_spring2018 | 1667 | 7 |
| 4763 | rga_fall2018 | 957 | 7 |
| 6150 | rgb_spring2019 | 957 | 7 |
| 11323 | rgb_spring2020 | 957 | 7 |
| 15016 | rgm_fall2021_H | 1667 | 7 |

## 6. Beamline port and validation: October 12 progress

### Current port and validation status

The current GEMC3 port includes all fifteen native beamline geometry and material variations: ten
standard run-mapped configurations and five detector-local configurations. It follows the active GEMC2
beamline dispatch; historical builders and disabled HD-ice daughters are not activated. All published
volumes use passive placement, and this passive system requires no sensitive digitization plugin or
optical surface.

Native geometry is published as beamline. The beamline_cad companion contains the ten standard CAD
configurations plus DDVCS, while beamline_transverse_cad provides noWedges, forwardWedges, and
midpointWedges as separately selectable alternatives. Both native and CAD systems use the SQLite factory;
mesh coordinates remain in millimetres at scale one. The runtime inventory contains 51 STL files: 30
beamline meshes and seven meshes for each transverse alternative. The two apex meshes are optimized as
described below; the remaining 49 retain the original tessellation.

The semantic comparator passes all fifteen native geometry variations, fifteen material variations, and
fourteen CAD placement variations against the GEMC2 TEXT/GXML references. The ten standard runs also
match the named native and CAD entries in the GEMC2 SQLite reference. Seven identical duplicate CAD rows
at run 20000 are represented once per volume name; the DDVCS configuration is also available at its
detector-local run. This preserves the effective geometry without duplicating physical placements.

Saved construction smoke logs show completion for all fifteen native configurations and all three
transverse CAD alternatives with overlap checking enabled. These zero-event checks validate geometry
construction and mesh resolution, not particle transport or detector response. A separate default
beamline check after the apex optimization also exits normally with check_overlaps=2, but records eight
GeomSolids1001 and nineteen GeomVol1002 exception blocks. These counts describe reported solid defects
and overlap/containment warnings, not unique defective meshes or overlapping pairs. The unchanged CAD
meshes still include surface-hole and facet-orientation diagnostics.

The current status is therefore a port with passing semantic comparisons and completed construction
checks, with residual geometry diagnostics retained for follow-up. Full-beamline transport performance,
overlap freedom, material-budget equivalence, magnetic-field operation, and full CLAS12 background
response equivalence have not been established by these checks. The isolated apex measurements below are
reported separately from this broader port validation.

### Apex shielding optimization and isolated benchmark

The next optimization step covers two beamline apex shielding meshes. The lead fill is reduced from 2,880 to
1,440 triangles; the hub is renamed from Apex_Shield_PCAL_Hub to Apex_Shield_Hub and reduced from 36,354 to
20,000 triangles. The two-file total falls from 39,234 to 21,440 triangles, a 45.4% reduction. Stored bytes
fall from 1,961,868 to 1,072,168. All other beamline meshes remain unchanged. Materials, coordinates, and
passive placements are preserved in both repositories; all eleven CAD variations and eleven run-dependent
GEMC2 hub rows use the new name.

Topology-preserving quadric edge collapse keeps the lead opening and both hub components. Faces adjoining
hub edges with dihedral angles above five degrees are protected; no holes are filled and no component is
removed. Both originals and optimized meshes are closed and manifold, with no detected self-intersections or
exact zero-area triangles. Bidirectional checks include every vertex and approximately 200,000 edge/surface
samples in each direction. The largest sampled deviations are 0.0425 mm for the lead fill and 0.0209 mm for
the hub; these are sampled measurements, not proven global Hausdorff bounds. The lead volume changes by
-0.002287%; the hub volume changes by -0.00000100%. The original engineering meshes remain archived, and the
builder reproduces the optimized STL files byte for byte.

Table 6 summarizes the unchanged topology and reduced mesh inventory.

Table 6. Apex engineering and optimized mesh inventory; topology is preserved.

| Mesh | Original triangles | Optimized triangles | Components | Genus |
|------|--------------------|---------------------|------------|-------|
| Lead fill | 2,880 | 1,440 | 1 | 1 |
| Hub | 36,354 | 20,000 | 2 | 2 |

This follow-on benchmark uses one GEMC3 development executable dated October 11, 2026 and Geant4 11.4.3 on
macOS arm64. Its timings are independent of the GEMC2 LTCC measurements above and must not be compared
across engines. Only the apex pair is loaded, in air, with its original lead and carbon-steel materials.
Native beamline geometry and other CAD solids are omitted to isolate the substitution. Both cases use
FTFP_BERT without optical processes, zero magnetic field, one thread, identical default production cuts, and
no GUI or event output. Fixed 5 GeV primaries originate at the target, uniform in solid angle from 0.25 to
3.5 degrees and over full azimuth. This aperture illuminates the forward shielding rather than reusing the
larger LTCC angular acceptance.

There are five alternating-order repetitions per case, with seeds 12345--12349 and matching LUND files for
each seed. Each electron, proton, positive-pion, and neutron run contains 200 events (1,000 events per
particle per geometry). This first beamline sample is smaller than the LTCC sample: showers in the thick
lead dominate its per-event cost. Tables report medians of the five runs. Initialization uses separate
zero-event runs with overlap checking disabled. Transport uses GEMC3's elapsed wall time since beamOn;
unlike the LTCC events-only CPU column, this is a wall-clock measure. Whole-process user plus system CPU
time and peak resident memory are also retained in the dataset. The original/optimized transport ratios are
ratios of medians, with no initialization subtraction.

Table 7 gives initialization, peak memory, and particle-transport measurements for this isolated pair.

Table 7. Median pair-only loading and transport measurements over five repetitions.

| Quantity | Original | Optimized | Original/optimized |
|----------|----------|-----------|--------------------|
| Initialization wall seconds | 1.151 | 0.970 | 1.19 |
| Loading peak RSS (MiB) | 186.09 | 153.64 | 1.21 |
| e- | 36.801 | 18.311 | 2.01 |
| proton | 9.329 | 5.174 | 1.80 |
| pi+ | 12.877 | 6.747 | 1.91 |
| neutron | 8.206 | 4.643 | 1.77 |

Transport entries are wall seconds per 200 events; the final column is a ratio of medians.

Median zero-event simulation wall time decreases by 15.7% and loading peak resident memory decreases by
17.4%. All 52 measured processes exit normally and print completion footers; all forty transport runs report
their 200 requested events. No Geant4 exception blocks are recorded in the pair-only loading, transport, or
separate check_overlaps=2 construction samples. The semantic comparator passes all fifteen native
geometry/material variations and all fourteen CAD variations after the rename. Full beamline construction
checks are retained separately; remaining unoptimized meshes can still produce warnings. These measurements
establish the performance of this isolated sample, not full CLAS12 speed, overlap freedom, or
background-response equivalence. Stochastic shower histories may differ despite matched primaries and seeds.

Figure 5 compares the stored triangulations with matched cameras and bounds.

![Apex STL comparison](figures/apex_stl_comparison.png)

Figure 5. Original (left) and optimized (right) apex lead-fill and hub STL surfaces. The views use identical cameras and millimetre coordinates within each pair; edges show the stored triangulations.

## 7. Downstream beam tube optimization

The next beamline step covers the two downstream tube segments. Their engineering tessellations are already
coarse, so reductions are modest: 5,146 to 5,000 and 672 to 600 triangles. Together they decrease from 5,818
to 5,600 triangles (3.75%) and from 291,068 to 280,168 bytes. Names, stainless-steel materials, coordinate
frames, and placements are retained in GEMC3 and GEMC2; no CAD database row is renamed or moved.

Segment 1 originally contains seven disconnected surface components, 392 boundary edges, fourteen boundary
loops, and 1,021 faces flagged by the mesh self-intersection filter. Generic hole closing caps the bore and
is unsuitable. The repair registers the seven inner/outer boundary-ring pairs on matching angular grids
while preserving their measured radii and axial positions, then adds 392 annular faces. All 392 seam
vertices are protected during decimation. The output is a single closed, manifold tube of genus one; the
passage remains open. Segment 2 retains its original single-component, genus-one topology. Neither output
has detected self-intersections or exact zero-area triangles.

Table 8. Downstream triangle counts and surface-component changes.

| Mesh | Original triangles | Optimized triangles | Original components | Output components |
|------|--------------------|---------------------|---------------------|-------------------|
| Segment 1 | 5,146 | 5,000 | 7 | 1 |
| Segment 2 | 672 | 600 | 1 | 1 |

The largest bidirectionally sampled surface differences are 0.7454 mm and 0.4574 mm, mainly around short
connector and flange features. Bounds change by at most 0.011 mm. The 0.05 mm apex sampling limit does not
apply to these tubes. Every original/output vertex and approximately 200,000 edge/surface samples per
direction are checked; these sampled maxima are not proven global error bounds. Segment 1 has no
well-defined original volume because its surface is open. Decimation changes its annularly repaired
reference volume by -0.01632%; this does not establish original-to-repaired mass equivalence. Segment 2
changes by -0.00170%. The builder reproduces both outputs byte for byte from archived originals.

The pair-only benchmark uses the recorded GEMC3 executable and Geant4 stack, FTFP_BERT without optical
processes, air, zero magnetic field, one thread, and identical default production cuts. GUI and event output
are disabled. Matched 5 GeV LUND primaries start at the target, uniform in solid angle from 0.1 to 1.3
degrees and over full azimuth. The smaller forward aperture illuminates the downstream tubes. Five
alternating-order repetitions use seeds 12345--12349 and 200 events per electron, proton, positive-pion, or
neutron run. Separate zero-event runs measure startup without overlap checking; elapsed wall time since
beamOn measures transport. CPU and peak RSS are retained separately. Absolute timings are not pooled with
the apex or LTCC workloads.

Table 9. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original wall seconds | Optimized wall seconds | Original/optimized |
|----------|-----------------------|------------------------|--------------------|
| e- | 13.008 | 11.401 | 1.14 |
| proton | 2.109 | 1.901 | 1.11 |
| pi+ | 2.318 | 2.161 | 1.07 |
| neutron | 1.340 | 1.204 | 1.11 |

Median startup simulation wall time changes from 0.6924 to 0.6925 s; loading peak RSS changes from 123.27 to
123.06 MiB. These small initialization differences should not be interpreted as a substantial startup or
memory improvement. The original/optimized median transport wall-time ratios range from 1.07 to 1.14. All 52
processes exit normally, and all forty transport runs report their 200 requested events. No event-abort
exception is recorded.

Table 10. Downstream construction and transport warning counts.

| Diagnostic | Original | Optimized |
|------------|----------|-----------|
| Surface-hole warnings, five loading runs | 5 | 0 |
| e- stuck tracks, five runs | 10 | 14 |
| proton stuck tracks, five runs | 0 | 0 |
| pi+ stuck tracks, five runs | 0 | 4 |
| neutron stuck tracks, five runs | 0 | 1 |
| Placement reports, overlap sample | 1 | 3 |

The repair eliminates the original surface-hole import warning. Placement overlap reports and stuck-track
diagnostics remain, as quantified below. A completion footer and requested event count do not prove that
every track followed the intended geometry. The original mesh lacks closed surfaces, and the repaired model
changes the represented material boundaries. Therefore transport timing differences cannot be assigned
solely to triangle-count reduction or used as proof of faster correct transport. The unchanged engineering
placement overlap and the thin, coarsely tessellated connector surfaces require further geometry/navigation
work. Detector response and full-experiment performance are outside this study.

Figure 6 compares the original and optimized meshes with matched cameras and bounds.

![Downstream tube comparison](figures/downstream_stl_comparison.png)

Figure 6. Original (left) and optimized (right) downstream tube segments in millimetre coordinates. Both models retain the through-bore; the paired views use the same camera and scale.

## 8. Adapter and torus exit shield

The third beamline study covers the adapter and torus exit-shield casing and lead fill. The reducer is
renamed Beamline_Adapter_1 in GEMC3 and GEMC2, including all eleven source CAD variations, generated runtime
GXML, and eleven run-dependent SQLite CAD rows. Every other database field, material, coordinate frame, and
placement is retained; custom GXML must use the new adapter name to match the STL filename.

These three meshes are already coarse, closed, manifold, and free of detected self-intersections and
zero-area triangles. The adapter decreases from 528 to 526 triangles and the casing from 1,392 to 1,384. The
lead fill remains byte-identical at 384 triangles, with both closed components retained: even the smallest
trial collapse displaced its surface by more than 1 mm near tight mating clearances. Its exact geometry was
explicitly retained after reviewing this constraint. The group decreases from 2,304 to 2,294 triangles
(0.434%) and from 115,452 to 114,952 bytes.

Table 11. Adapter and exit-shield triangle counts.

| Mesh | Original | Optimized |
| --- | --- | --- |
| Adapter | 528 | 526 |
| Exit casing | 1392 | 1384 |
| Exit lead fill | 384 | 384 |

For the casing, 432 faces having at least one vertex within 1 mm of the lead fill are protected. The saved
output is checked to retain every protected triangle at exactly the original coordinates. All three meshes
retain their bounds, component counts, and genus; no hole filling or reconstruction is used. The adapter and
casing have maximum bidirectionally sampled surface differences of 0.4559 and 0.5002 mm, below the 0.51 mm
sampling guard for this group, and volume changes of +0.000368% and +0.000188%. The guard is specific to
this coarse group and does not establish the apex study's 0.05 mm criterion. Every vertex and approximately
200,000 edge/surface samples per direction are checked; the sampled maxima are not proven global bounds. The
builder reproduces all three outputs byte for byte from the archived originals.

The benchmark isolates these three volumes with their unchanged aluminum, stainless-steel, and lead
materials in air. The recorded GEMC3 executable and Geant4 stack run FTFP_BERT without optical processes,
zero magnetic field, one thread, default production cuts, and no GUI or event output. Matched 5 GeV LUND
primaries start at the target, uniform in solid angle over 0.25--2.6 degrees and full azimuth. Five
alternating-order repetitions use seeds 12345--12349 and 200 events per electron, proton, positive-pion, or
neutron run. Separate zero-event runs measure startup without overlap checking; time since beamOn measures
transport. CPU time and peak RSS are retained separately. Absolute timings are not pooled with either
earlier beamline study or LTCC.

Table 12. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 10.750 | 10.443 | 1.029 |
| proton | 3.451 | 3.398 | 1.016 |
| pi+ | 4.363 | 4.269 | 1.022 |
| neutron | 3.421 | 3.293 | 1.039 |

Median startup simulation wall time changes from 0.8844 to 0.8707 s, and peak loading RSS from 125.23 to
125.16 MiB. The original/optimized median transport wall-time ratios range from 1.016 to 1.039; individual
seed-paired ratios span 1.015--1.052. With only ten removed triangles and five repetitions, these timings do
not establish a substantial performance gain. All 52 processes exit normally, and all forty transport runs
report the 200 requested events.

Table 13. Geant4 exception counts over all 52 isolated group processes.

| Diagnostic | Original | Optimized |
| --- | --- | --- |
| GeomSolids1001 | 0 | 0 |
| GeomNav1002 | 0 | 0 |
| GeomNav0003 | 0 | 0 |
| GeomVol1002 | 0 | 0 |

No Geant4 exceptions are recorded in the isolated loading, transport, or overlap samples for either case.
This is a limited sample, not proof of complete overlap freedom or detector-response equivalence. Full
default beamline construction also completes with the renamed adapter and no missing mesh; its seven solid
warnings and twenty overlap reports are unchanged from the preceding downstream state. All fifteen native
geometry/material variations and fourteen CAD variations pass the semantic comparison against GEMC2.

Figure 7 compares the stored triangulations.

![Adapter and exit shield comparison](figures/exit_stl_comparison.png)

Figure 7. Original (left) and final (right) adapter and torus exit-shield STL surfaces in millimetres. Each pair shares camera and bounds; the lead fill is retained exactly.

## 9. FT adjuster material model

The fourth beamline study replaces adjuster1, adjuster2, and adjuster3 with one ft_adjuster mesh. Here the
intended optimization prioritizes the amount of stainless steel over detailed shape. All three source pieces
share the same material, color, mother, position, and passive rotation; the replacement retains these
physical attributes and merges the three placement rows into one in each of the nine applicable CAD
variations. GEMC2's corresponding 27 SQLite CAD rows become nine rows, with every other CAD row retained.

The originals contain 1,687, 424, and 1,689 triangles. The first and third meshes each lack a nine-edge
surface patch, and the assembled pieces intersect. Their original material volume is therefore not
well-defined directly from the raw shells. Small sealing patches define a reference, followed by Boolean
union to avoid counting overlapping steel twice. These temporary reference meshes retain local
intersections; none is published as runtime geometry. The reference defines an estimated material budget,
not a certified engineering mass.

The sealed parts sum to 25203.967 mm³, and their reference union contains 24922.570 mm³. Pairwise
intersection volumes are 140.391 and 141.004 mm³; the first and third pieces have disjoint longitudinal
bounds. Independent inclusion-exclusion reproduces the union volume within 0.00001%. This subtracts about
1.12% from the sum of overlapping parts. Preserving their unqualified sum would retain double-counted
material.

Table 14. Adjuster material volumes in cubic millimetres.

| Reference or model | Volume |
| --- | --- |
| Sealed parts sum | 25203.966821 |
| Inclusion-exclusion union | 24922.571202 |
| Reference Boolean union | 24922.569617 |
| Final saved STL | 24922.562549 |

The final model is a closed 12-sided prism with radius 7.383895 mm and length 152.370361 mm, centered on the
reference union's centroid. It retains the longitudinal span and approximate off-axis material location. Its
saved float32 STL volume is 24922.562549 mm³, differing from the reference by -0.00002836%. The unchanged
stainless-steel material retains its density, so this relative volume match also matches the reference mass.
The output has one closed manifold component of genus zero, with no detected self-intersections or zero-area
faces, and reproduces byte for byte from archived originals. Shape detail, holes, threads, and the original
material-path distribution are deliberately changed; detector-response equivalence is not established.

The runtime model decreases from three files and 3,800 triangles to one file and 48 triangles (98.74%
fewer). STL bytes decrease from 190,252 to 2,484 (98.69%). One placement replaces three. This is a
material-volume substitution rather than a surface-tolerance decimation.

Table 15. Original adjuster trio and simplified material model.

| Model | Files | Triangles | Bytes |
| --- | --- | --- | --- |
| Original trio | 3 | 3,800 | 190,252 |
| ft adjuster | 1 | 48 | 2,484 |

The benchmark compares the original raw trio with the merged model in air using the recorded GEMC3
executable and Geant4 stack, FTFP_BERT without optical processes, zero magnetic field, one thread, default
production cuts, and no GUI or event output. Fixed 5 GeV LUND primaries start at the target, uniform in
solid angle over 2.5--3.3 degrees and azimuth -95-- -85 degrees. The narrow azimuth targets the off-axis
adjuster instead of diluting the sample over full azimuth. Five alternating-order repetitions use seeds
12345--12349 and 200 events for each particle. Zero-event runs measure startup without overlap checking;
time since beamOn measures transport. Both fixtures share physical placement attributes, while the original
contains three solids and the final contains one. The benchmark accepts a generated database from either
geometry state.

Table 16. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Final | Original/final |
| --- | --- | --- | --- |
| e- | 4.871 | 3.124 | 1.559 |
| proton | 0.882 | 0.784 | 1.126 |
| pi+ | 0.903 | 0.805 | 1.121 |
| neutron | 0.699 | 0.597 | 1.170 |

Median startup simulation wall time changes from 0.6875 to 0.6803 s; peak loading RSS changes from 119.55 to
114.31 MiB. The median original/optimized transport wall-time ratios range from 1.121 to 1.559. CPU time,
process wall time, memory, and raw diagnostics are retained separately. All 52 processes exit normally and
all forty transport runs report the 200 requested events.

Table 17. Geant4 exception counts for the isolated adjuster samples.

| Diagnostic | Original | Final |
| --- | --- | --- |
| GeomSolids1001 | 52 | 0 |
| GeomNav1002 | 40 | 0 |
| GeomNav0003 | 0 | 0 |
| GeomVol1002 | 8 | 0 |

The repeated diagnostic counts are retained explicitly. Full default beamline construction completes with no
missing mesh and 5 solid warnings and 10 overlap reports, compared with seven and twenty before this merge.
These counts describe the check sample, not proof of complete overlap freedom. All fifteen native
geometry/material variations and fourteen CAD variations pass the semantic comparison against GEMC2.
Material redistribution, closure repairs, removal of internal overlaps, and fewer solids all affect
transport; timing changes cannot be assigned solely to triangle count or taken as evidence of unchanged
detector response. A normal completion footer does not certify every track in the original imperfect
geometry.

Figure 8 shows the deliberate shape simplification.

![FT adjuster material model](figures/adjuster_stl_comparison.png)

Figure 8. Engineering adjuster trio (left) and the volume-matched ft_adjuster prism (right). Matched cameras and bounds use original STL coordinates; the common CAD transform is retained.

## 10. FT inner shield and flange

The fifth beamline study renames innerShieldAndFlange to FTInnerShieldAndFlange and optimizes its
engineering tessellation. The same rename applies to ten source and generated runtime CAD variations and ten
GEMC2 SQLite CAD rows. The tungsten-alloy material, density, color, mother, position, passive rotation,
coordinate frame, and overall bounds remain unchanged. Custom CAD placements must use the new name to match
the STL filename.

The original has 34,448 triangles, two closed manifold surface components, aggregate genus 17, and no
detected self-intersections or exact zero-area faces. The small inward-oriented component is an enclosed
pocket with signed volume -9.663980 mm³. All 474 of its triangles are protected and verified in the saved
STL at exactly the original coordinates. Only the larger component is decimated, using topology-preserving
quadric collapse. No holes are filled, components removed, or surfaces reconstructed.

The saved output contains 22,000 triangles (36.14% fewer) and 1,100,084 bytes instead of 1,722,484. It
retains both components, aggregate genus, and bounds; no self-intersections or zero-area triangles are
detected. Bidirectional vertex, edge, and surface sampling measures a maximum difference of 0.0481 mm, below
the 0.05 mm guard. Every vertex and approximately 200,000 edge/surface samples per direction are checked;
these sampled maxima are not proven global error bounds. Total signed volume changes by -0.00004391%. A
separate component integration gives -0.00004114% for the main component and no change for the pocket. The
builder reproduces the optimized STL byte for byte from the archived original.

Table 18. Original and optimized FT inner shield and flange.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 34,448 | 22,000 |
| Bytes | 1,722,484 | 1,100,084 |
| Closed surface components | 2 | 2 |
| Aggregate genus | 17 | 17 |
| Protected pocket faces | 474 | 474 |

The benchmark isolates this one CAD volume in air with the recorded GEMC3 executable and Geant4 stack,
FTFP_BERT without optical processes, zero magnetic field, one thread, default production cuts, and no GUI or
event output. Both fixtures use the new volume name, identical physical placement attributes, and the same
alloy definition. Matched 5 GeV LUND primaries start at the target, uniform in solid angle over 0.25--3.0
degrees and full azimuth. Five alternating-order repetitions use seeds 12345--12349 and 200 events per
electron, proton, positive-pion, or neutron run. Separate zero-event runs measure startup without overlap
checking; time since beamOn measures transport. CPU time and peak RSS are retained separately.

Table 19. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 18.565 | 15.048 | 1.234 |
| proton | 2.790 | 2.426 | 1.150 |
| pi+ | 3.655 | 3.292 | 1.110 |
| neutron | 2.504 | 2.425 | 1.033 |

Median startup simulation wall time changes from 0.9492 to 0.8435 s; peak loading RSS changes from 175.23 to
151.28 MiB. Median original/optimized transport wall-time ratios range from 1.033 to 1.234. All 52 processes
exit normally, and all forty transport runs report the 200 requested events. Results describe this isolated
workload and are not pooled with earlier beamline or LTCC benchmarks.

Table 20. Geant4 exception counts for the isolated inner-shield samples.

| Diagnostic | Original | Optimized |
| --- | --- | --- |
| GeomSolids1001 | 26 | 0 |
| GeomNav1002 | 0 | 0 |
| GeomNav0003 | 0 | 0 |
| GeomVol1002 | 0 | 0 |

The diagnostic table records the original wrong-orientation import warning and all other Geant4 exceptions
in the sampled runs. Full default beamline construction completes without a missing mesh, with 4 solid
warnings and 11 overlap reports, compared with five and ten before this change. The full check reports no
overlap involving the optimized inner shield; the listed overlap reports concern other volumes. Their
sampled count can change when CAD loading order and surface tessellation change. All fifteen native
geometry/material variations and fourteen CAD variations pass the semantic comparison against GEMC2. Matched
primaries and seeds do not ensure identical stochastic shower histories, and completion does not establish
detector-response equivalence or complete overlap freedom.

Figure 9 compares the stored triangulations.

![FT inner shield and flange](figures/inner_shield_stl_comparison.png)

Figure 9. Original (left) and optimized (right) FT inner shield and flange STL surfaces. Matched cameras and bounds use original STL coordinates; the small enclosed pocket is retained exactly.

## 11. FT inner shield bolts

The sixth beamline study renames nut1--nut9 to FTInnerShieldAndFlange_Bolt1 through
FTInnerShieldAndFlange_Bolt9. These engineering meshes are solid copper bolts, despite their former names.
The approved simplification removes threads and replaces the hexagonal head details with round heads and
smooth solid shafts. Each surface uses 24 angular sides, an annular shoulder, and closed end caps: 192
triangles per bolt. No hollow bore is introduced. G4_Cu, colors, mothers, and passive placements are
retained across ten applicable CAD variations and ninety GEMC2 SQLite rows; only their names change in the
placement records.

The shaft axes, head shoulders, and outer ends are measured from each original mesh. The head radius is
14.2875 mm, within the original hexagonal across-flats envelope. The original tip caps contact the shield
blind-hole end faces. Shortening each inner tip by 0.15 mm creates an explicit gap; the smooth shaft radius
is then solved from the original signed solid volume. The seven regular shafts have radius approximately
8.5741 mm; the two longer shafts, bolts 4 and 8, have radius approximately 8.3681 mm. Their individual
float32 STL volumes agree with the originals within 0.0001%. This redistributes copper locally and changes
external surfaces rather than preserving the engineering threaded profile.

Combined triangles fall from 16,278 to 1,728 (89.38% fewer), and bytes fall from 814,656 to 87,156. Original
and optimized total copper volumes are 150623.172389 and 150623.196214 mm³, a change of 0.00001582%. All
nine outputs are closed, singly connected, manifold genus-zero surfaces with no detected self-intersections
or zero-area triangles. The archived originals reproduce all nine optimized STLs byte for byte.

Table 21. Individual copper bolt models; radius in mm and volume change in percent.

| Bolt | Original faces | New faces | Shaft radius | Volume change |
| --- | --- | --- | --- | --- |
| 1 | 1,690 | 192 | 8.5741 | 0.0000057 |
| 2 | 1,690 | 192 | 8.5741 | 0.0000107 |
| 3 | 1,690 | 192 | 8.5741 | 0.0000037 |
| 4 | 2,224 | 192 | 8.3681 | 0.0000899 |
| 5 | 1,690 | 192 | 8.5741 | 0.0000037 |
| 6 | 1,690 | 192 | 8.5741 | 0.0000057 |
| 7 | 1,690 | 192 | 8.5741 | 0.0000057 |
| 8 | 2,224 | 192 | 8.3681 | 0.0000029 |
| 9 | 1,690 | 192 | 8.5741 | 0.0000057 |

The optimized FTInnerShieldAndFlange STL is unchanged. Since shield and bolts share the same placement
transform, their collision test uses stored STL coordinates. VTK triangle collision finds zero surface
contacts, and enclosed-point checks in both directions find no bolt vertices inside the shield and no shield
vertices inside any bolt. Minimum bidirectional vertex-to-surface distances are 0.150002 mm for each bolt.
These sampled distances are not a certified global clearance bound; the independent surface and containment
checks address intersection. A ten-volume shield-plus-bolts Geant4 fixture completes without exceptions at
check_overlaps=2 and again with a 10,000-point geometry test. The unchanged shield hash is retained with the
clearance results.

Tracking benchmarks isolate the nine copper bolts in air, excluding the shield from both timed fixtures.
Both cases use the new names, identical materials and placements, the same recorded GEMC3 executable,
FTFP_BERT without optical processes, no magnetic field, one thread, default production cuts, and no GUI or
event output. Matched 5 GeV LUND primaries start at the target and sample solid angle uniformly from 1.3 to
3.0 degrees over full azimuth. Five repetitions with alternating fixture order and seeds 12345--12349 use
200 events per electron, proton, positive-pion, and neutron run. Time since beamOn measures transport;
separate zero-event runs measure startup. All 52 processes complete normally with all forty event counts
correct and no recorded Geant4 exceptions in either case.

Table 22. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 0.551724 | 0.457388 | 1.206 |
| proton | 0.329016 | 0.329104 | 1.000 |
| pi+ | 0.330425 | 0.283490 | 1.166 |
| neutron | 0.133233 | 0.111502 | 1.195 |

Median startup simulation wall time is 0.659214 s originally and 0.623648 s after simplification. Peak
startup RSS falls from 129.34 to 115.31 MiB. The transport wall-time ratios are 1.206 for electrons, 1.000
for protons, 1.166 for positive pions, and 1.195 for neutrons. The proton result shows essentially unchanged
tracking time. These short workloads and five repetitions do not establish a universal speedup; material
redistribution changes stochastic shower histories even for matched primaries and seeds. Full CLAS12
performance and detector-response equivalence are not inferred.

Full default beamline construction completes without missing meshes and with no reported bolt-shield
overlap. Four remaining solid warnings and ten overlap reports concern other volumes, compared with four and
eleven immediately before this study. Sampled counts depend on tessellation and loading order, so this
difference is not claimed as a general overlap repair. All fifteen native geometry/material variations and
fourteen CAD variations pass the semantic comparator against GEMC2. Earlier apex, downstream,
adapter/exit-shield, adjuster, and inner-shield tracking measurements remain in their respective sections
with separate workloads and archives.

Figure 10 compares representative regular and longer bolts.

![Original and smooth FT bolts](figures/bolts_stl_comparison.png)

Figure 10. Original (left) and smooth (right) bolts 1 and 4. Matched bounds and cameras; coordinates are recentered and permuted to put each shaft on the horizontal axis.

## 12. FT outer flange

The seventh beamline study renames outerFlange to FTOuterFlange in ten applicable source and runtime CAD
variations and ten GEMC2 SQLite placement rows. The stainless-steel material, color, mother, and passive
placement are retained, including the original 1272.77 mm z translation. That translation differs by 0.5 mm
from the inner-shield and outer-mount placements and is not rounded to their common value.

The original is a closed manifold annular plate with 2,132 triangles and genus 13. The authorized hole
removal closes twelve bolt tunnels with pygemc's remove_holes utility, leaving the central opening intact
and reducing genus to 1. Flat annular faces are then retriangulated using every original inner and outer rim
coordinate on both z faces. The inner radius is 95.25 mm, the outer radius 127 mm, and the original
thickness approximately 19.049927 mm. Each face retains 97 inner rim vertices and 112 outer rim vertices.
Saved coordinates are verified exactly against those engineering vertices; the original bounds are
unchanged.

Triangles fall to 836 (60.79% fewer), and bytes fall from 106,684 to 41,884. The output remains one closed
manifold surface with no detected self-intersections or zero-area faces. Closing the bolt holes changes
volume from 389837.402125 to 422180.789284 mm³, an increase of 8.296635%. Retriangulation changes the
hole-filled reference volume only at floating-point precision. Bidirectional vertex, edge, and surface
sampling against that reference gives a maximum difference of 0.0000148 mm. This sampled difference
describes retriangulation, not the deliberately closed holes, and is not a proven global error bound. The
archived engineering mesh reproduces the optimized STL byte for byte.

Table 23. Original and optimized FT outer flange.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 2,132 | 836 |
| Bytes | 106,684 | 41,884 |
| Genus | 13 | 1 |
| Volume (mm³) | 389837.402 | 422180.789 |

The isolated tracking fixture contains only this stainless-steel flange in air. Both cases use the new name
and identical material and placement attributes. Matched 5 GeV LUND primaries originate at the target,
uniform in solid angle over 1.9--2.8 degrees and full azimuth. FTFP_BERT runs without optical processes or
magnetic field, with one thread, default production cuts, and no GUI or event output. Five alternating-order
repetitions use seeds 12345--12349 and 200 events for each electron, proton, positive-pion, and neutron run.
Separate zero-event runs measure startup; elapsed time since beamOn measures transport. A fixed executable
snapshot is used for every run, with its hash checked afterward. Earlier runs interrupted by sandbox
resource-timer restrictions or invalidated by a changing shared executable are excluded.

Table 24. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 0.646804 | 0.668927 | 0.967 |
| proton | 0.429432 | 0.425280 | 1.010 |
| pi+ | 0.393231 | 0.377190 | 1.043 |
| neutron | 0.221017 | 0.274356 | 0.806 |

Median startup simulation wall time changes from 0.699890 to 0.693861 s; peak startup RSS changes from
117.83 to 115.67 MiB. Median original/optimized transport ratios are 0.967, 1.010, 1.043, and 0.806 for
electrons, protons, positive pions, and neutrons, respectively. A ratio above one means shorter optimized
tracking time; a ratio below one means longer time. All 52 processes complete normally, and all forty
transport runs report their 200 requested events. These short isolated workloads do not establish a
universal tracking gain. The added stainless steel changes scattering and stochastic shower histories, so
timing differences cannot be attributed solely to triangle reduction or treated as detector-response
equivalence.

Table 25. Geant4 exception counts across the 52 isolated-fixture processes.

| Diagnostic | Original | Optimized |
| --- | --- | --- |
| GeomSolids1001 | 0 | 0 |
| GeomNav1002 | 0 | 0 |
| GeomNav0003 | 0 | 0 |
| GeomVol1002 | 0 | 0 |

A separate twelve-volume assembly fixture includes the flange, unchanged inner shield and outer mount, and
nine copper bolts. Both original and optimized fixtures use the new flange name and the same placements.
Their 10,000-point Geant4 checks report 5 and 5 overlap warnings, respectively; both also retain one
surface-hole import warning from the unchanged outer mount. The retained logs identify the volumes and
micrometre-scale penetrations. Existing outer-mount/flange interference remains a limitation of the
assembly, so no claim of complete overlap freedom is made. Full default construction completes without
missing meshes, with 4 solid warnings and 9 overlap reports. All fifteen native geometry/material variations
and fourteen CAD variations pass the semantic comparison against GEMC2. The earlier six beamline studies
retain their independent timing tables, diagnostic results, and archives.

The subsequent outer-mount study in Section 13 resolves this earlier flange/mount interference.

### 12.1 Tracking at fixed material volume

A follow-up control compares the hole-filled flange before and after retriangulation, removing the added
material as a difference between the cases. The baseline has 2,084 triangles and 104,284 bytes; the
simplified flange has 836 triangles and 41,884 bytes, a 59.88% triangle reduction relative to this filled
reference. Both have the same central opening, bounds, stainless-steel material, placement, and volume of
422180.789284 cubic millimetres to the reported precision. Their sampled surface differences remain below
0.0000148 mm. The fixture label original now denotes the unreduced hole-filled reference, not the drilled
engineering mesh.

The control uses the same fixed executable snapshot and physics settings as the earlier flange study, with 5
GeV primaries uniform in solid angle over 1.9--2.8 degrees and full azimuth. Five alternating-order
repetitions use seeds 12345--12349. Each particle run has 2,000 events, ten times the earlier sample; both
cases have identical primary hashes and geometry/material database records. Separate startup samples retain
the loading and peak-memory measurements. The larger control is reported independently, without pooling its
absolute times or ratios with the earlier 200-event drilled-versus-filled results.

Table 26. Median transport wall seconds per 2,000 events over five repetitions.

| Particle | Filled reference | Simplified | Reference/simplified |
| --- | --- | --- | --- |
| e- | 7.40750 | 6.90088 | 1.073 |
| proton | 4.63719 | 4.56330 | 1.016 |
| pi+ | 4.19454 | 4.05502 | 1.034 |
| neutron | 2.94839 | 2.91016 | 1.013 |

Median baseline/simplified tracking wall-time ratios are 1.073 for electrons, 1.016 for protons, 1.034 for
positive pions, and 1.013 for neutrons. A value above one means shorter tracking time for the simplified
mesh. These measurements quantify retriangulation at fixed material volume. The simplified mesh is faster in
all twenty particle/seed pairs; the individual paired ratios are retained in the control dataset. Matched
primaries and seeds do not guarantee identical subsequent shower histories because tessellated boundary
arithmetic can alter stochastic transport. Five repetitions do not establish a universal speedup or a
precise causal decomposition of the earlier slowdown.

Median startup simulation wall time changes from 0.704797 to 0.692080 s, with peak startup RSS changing from
117.52 to 115.58 MiB. All 52 control processes complete normally, and all forty transport runs report the
requested 2,000 events. Geant4 exception counts, paired seed ratios, fixture hashes, and raw timing reports
are retained in a separate control dataset. Neither case records a Geant4 exception in the sampled control.

Figure 11 compares the original flange and its hole-filled replacement.

![Original and filled flange](figures/outer_flange_stl_comparison.png)

Figure 11. Original flange (left) and optimized flange (right). Matched cameras and bounds; central opening and original rim vertices retained.

## 13. FT outer mount

The eighth beamline study renames outerMount to FTOuterMount across ten source and runtime CAD variations
and ten GEMC2 SQLite rows. The stainless-steel material, color, mother, and passive placement are retained.
The mount remains at z = 1273.27 mm and the unchanged FTOuterFlange at z = 1272.77 mm, both with the
original passive 180-degree y rotation. Their 0.5 mm relative translation is included in every clearance
calculation.

The original mount contains 3,094 triangles, twelve boundary edges forming four triangular surface gaps, and
one manifold surface component. Its open surface has no defined solid volume. Closing these four missing
faces gives a 3,098-triangle sealed reference of genus 11 and volume 3889831.731170 mm³. The central passage
and existing drilled openings are retained. This repaired reference defines the reported material-volume
comparison; the original engineering solid mass is not independently certified.

The original mount/flange check reports small interference at their nominal 95.25 mm radius because the two
cylindrical surfaces have different polygonal sampling. The flange inner polygon has minimum inradius
95.200045 mm. The mount lower outer rim is reduced to 95.150045 mm, approximately 0.100 mm of radial relief.
Adjacent sidewall facets interpolate toward unchanged upper vertices. All 883 facets adjoining the relieved
end are protected at their saved float32 coordinates during topology-preserving quadric simplification. The
flange STL is unchanged, and no placement is shifted to conceal the interference.

The final mount contains 2,740 triangles, 11.44% fewer than the raw engineering mesh, and 137,084 bytes
rather than 154,784. It is one closed manifold component of genus 11 with no detected self-intersections or
zero-area triangles. Bidirectional sampling against the relieved reference gives a maximum difference of
0.042078 mm, below the 0.05 mm guard. These are sampled differences rather than proven global error bounds.
Volume changes by -0.249235% against the sealed reference; simplification alone changes the relieved
reference volume by 0.00011056%. The axial bounds are retained, with at most about 0.00065 mm change in the
transverse bounding coordinates. The builder reproduces the final STL byte for byte from the archived
original.

Table 27. Original and optimized FT outer mount.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 3,094 | 2,740 |
| Bytes | 154,784 | 137,084 |
| Boundary edges | 12 | 0 |
| Surface components | 1 | 1 |
| Solid volume (mm³) | Undefined | 3880136.906 |

Placed-mesh verification finds zero triangle contacts and no contained vertices in either direction between
mount and flange. In mount coordinates, the flange is shifted by +0.5 mm along z. Each mount triangle is
clipped to the flange z interval, and convexity of the radial norm bounds its radius by the clipped polygon
vertices. The maximum is 95.164071 mm, giving at least 0.035974 mm radial separation from the flange inner
polygon throughout their common axial interval. The minimum bidirectional vertex-to-surface distance is
0.085929 mm; this latter value is sampled and is not presented as a global surface-clearance bound. All ten
placement variants retain the same verified relative transform.

A twelve-volume assembly fixture includes the mount, unchanged inner shield and flange, and nine copper
bolts. With both original and optimized fixtures using the new mount name and identical placements, a
10,000-point Geant4 test gives five flange/mount overlap reports and one surface-hole warning for the
original mount. The optimized assembly completes with no Geant4 exceptions or overlap reports, resolving the
joint interference documented in the preceding flange study. Full default beamline construction also
completes without missing meshes or a mount/flange overlap. Its three solid warnings and eight overlap
reports concern other geometry, so this study does not establish complete beamline overlap freedom. All
fifteen native geometry/material variations and fourteen CAD variations pass the semantic comparison against
GEMC2.

The tracking benchmark isolates this one mount in air. Both cases use the new name, the same material and
placement, and the unchanged fixed GEMC3 executable snapshot from the flange study. Matched 5 GeV LUND
primaries begin at the target and sample solid angle uniformly over 1.5--2.4 degrees and full azimuth.
FTFP_BERT runs without optical processes or magnetic field, using one thread, default production cuts, and
no GUI or event output. Five alternating-order repetitions use seeds 12345--12349 and 200 events per
electron, proton, positive-pion, and neutron run. Elapsed time since beamOn measures transport; separate
zero-event samples measure startup and peak RSS.

Table 28. Median transport wall seconds per 200 events over five repetitions.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 15.97580 | 15.51250 | 1.030 |
| proton | 2.13591 | 2.10357 | 1.015 |
| pi+ | 2.93950 | 2.85889 | 1.028 |
| neutron | 1.83088 | 1.93090 | 0.948 |

Median original/optimized transport wall-time ratios are 1.030 for electrons, 1.015 for protons, 1.028 for
positive pions, and 0.948 for neutrons. A ratio below one denotes longer optimized tracking time. All 52
processes complete normally, and all forty transport runs report the requested 200 events. Startup
simulation wall time changes from 0.705080 to 0.693238 s, and peak startup RSS changes from 120.12 to 119.38
MiB. Closure repairs and relief change material boundaries, so these short workload timings are not
attributed solely to triangle reduction. They do not establish detector-response equivalence or full CLAS12
speedup. The preceding flange control at fixed material volume remains separately reported.

Table 29. Geant4 exception counts in all 52 isolated-mount processes.

| Diagnostic | Original | Optimized |
| --- | --- | --- |
| GeomSolids1001 | 26 | 0 |
| GeomNav1002 | 0 | 0 |
| GeomNav0003 | 0 | 0 |
| GeomVol1002 | 0 | 0 |

Figure 12 compares the original and optimized mount.

![Original and optimized mount](figures/outer_mount_stl_comparison.png)

Figure 12. Original (left) and optimized (right) mount. Matched cameras and bounds in original STL coordinates; existing drilled openings retained.

## 14. FT inner shield

The shield/cone interference recorded below is resolved by the subsequent cone revision in Section 15.

The initial revision below is retained with its original measurements. The final smooth-flange configuration
supersedes it; see Section 14.1.

The ninth beamline study renames taggerInnerShield to FTInnerShield in all nine source and runtime CAD
variations that contain it and in nine GEMC2 SQLite CAD rows. The tungsten-alloy material beamline_W, color,
mother, and original passive placement are retained: z = 1643.00 mm with a 180-degree y rotation. This
downstream grooved tube is distinct from the previously optimized FTInnerShieldAndFlange at z = 1273.27 mm.

The original contains 44,122 triangles, 7,404 boundary edges, 67 surface components, 351 non-manifold
vertices, and 1,750 faces selected by the intersection check. Its open and non-manifold surface has no
defined solid volume. Routine welding and generic hole filling do not establish a sound surface. A
deterministic reconstruction uses the measured tube cross-section, chamfers, flange fillets, and feature
positions, without Poisson reconstruction. The central bore remains 60 mm in diameter, nominal tube outer
diameter 80 mm, length 665 mm, and flange outer radius 100 mm. The flange occupies local z = -625 to -605
mm.

Two longitudinal grooves at local azimuths 45 and 135 degrees are retained after the flange. Each is 6 mm
wide and 3 mm deep, extending from local z = -575 mm to the tube end at z = 0. A 6 mm axial end radius
blends its floor into the tube. All 26 flange through-holes and the single radial tube hole are closed. The
requested 0.5 mm recess threshold is applied to axial depth: eight 5.75 mm deep conical recesses, sixteen
0.6 mm face chamfers, and two 10 mm deep counterbores remain as blind features. The conical mouths
originally touch the flange outer rim exactly; reducing each mouth radius from 10.00 to 9.95 mm removes that
tangency while retaining their depths and 4.25 mm bottom radii.

The reference uses 128 angular segments for the main profile, sampled fillet/end curves, and Boolean cuts
for the grooves and retained recesses. A 0.000001 mm weld removes near-coincident Boolean vertices and their
sliver facets before saving the reference. Its 15,100 triangles define a closed manifold component of genus
one with volume 1938424.030371 mm³. Protected quadric simplification retains 9,404 groove, recess, and
corner faces at their saved float32 coordinates and produces 13,500 triangles, a 69.40% reduction from the
engineering mesh. File size decreases from 2,206,184 to 675,084 bytes.

The final mesh remains one closed manifold component of genus one, with no selected self-intersections or
zero-area facets. Bounds remain [-100, -100, -665] to [100, 100, 0] mm apart from negligible source z
rounding. Minimum triangle altitude is 0.000344255 mm. Bidirectional sampling against the rebuilt reference
gives a maximum change of 0.023925 mm, below the 0.05 mm guard. Simplification changes reconstructed volume
by -0.00058479%. These are sampled checks, not proven global surface bounds or a comparison to a certified
original mass.

Independent VTK containment probes verify all 58 requested inside/outside results across groove floors,
blind recesses, filled bolt shafts, the filled tube hole, and the central passage. Outside the removed
drilling walls and flange drilling region, retained source profile vertices lie within 0.050719 mm of the
reconstructed surface. One-way vertex, edge, and face sampling of the retained raw tube/rim subset gives a
larger maximum 0.969091 mm: the reconstruction replaces coarse, disconnected raw facets with the measured
nominal profile. This original-to-final difference is distinct from the much smaller subsequent decimation
error. The original mass change and detector-response equivalence are not established. The builder
reproduces the final STL and reconstructed reference byte for byte from the archived engineering input.

Table 30. Original and optimized downstream FT inner shield.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 44,122 | 13,500 |
| Bytes | 2,206,184 | 675,084 |
| Boundary edges | 7,404 | 0 |
| Surface components | 67 | 1 |
| Solid volume (mm³) | Undefined | 1938412.695 |

A two-volume assembly includes the unchanged main-cone at z = 1589.27 mm and the shield at its original
placement. The 10,000-point Geant4 test reports five shield/cone overlaps in each case, confirming the
pre-existing interference remains. Original construction has three solid warnings; optimized assembly
construction has one warning from the unchanged cone. The isolated optimized shield loads with no Geant4
exceptions. Full default beamline construction completes without missing meshes, with 1 solid warning and 9
overlap reports involving the shield/cone and downstream/adapter geometry. The original placements are
retained rather than adjusted in this study. All fifteen native geometry/material and fourteen CAD
variations pass the semantic comparison against GEMC2.

Two independent tracking comparisons isolate the shield in air. The first uses the defective engineering
mesh as baseline; the second uses the hole-filled, grooved, unreduced reference to measure simplification
after repair. Each uses the fixed GEMC3 executable snapshot from the flange study, matched 5 GeV
target-origin primaries uniform in solid angle over 0.7--2.7 degrees and full azimuth, FTFP_BERT without
optics or magnetic field, one thread, default production cuts, and no GUI or event output. Five
alternating-order repetitions use seeds 12345--12349 and 200 events per electron, proton, positive-pion, and
neutron run. Each comparison contains 52 processes, including zero-event startup and isolated overlap
checks. All 104 processes complete normally and all eighty transport runs report 200 events.

Engineering-original/optimized median transport wall-time ratios are 0.923, 1.007, 0.992, 0.924 for
electrons, protons, positive pions, and neutrons respectively. Ratios below one denote slower optimized
tracking. The engineering surface carries solid and navigation warnings; repair and authorized hole closure
change material boundaries, so this comparison does not attribute timing changes solely to triangle count.
Original material volume is undefined.

Table 31. Median transport wall seconds per 200 events: engineering comparison.

| Particle | Original | Optimized | Original/optimized |
| --- | --- | --- | --- |
| e- | 22.46020 | 24.33720 | 0.923 |
| proton | 2.23604 | 2.22142 | 1.007 |
| pi+ | 2.96617 | 2.99009 | 0.992 |
| neutron | 1.99370 | 2.15824 | 0.924 |

Rebuilt-reference/optimized median ratios are 1.087, 1.075, 1.075, 1.049 in the same particle order. This
comparison retains the same blind recesses, closed holes, grooves, and material, with the recorded small
decimation volume difference. Both isolated reference and optimized fixtures have no Geant4 exceptions.
These short workload results are reported separately from the repair comparison; small ratios are sensitive
to timing variation and stochastic transport. They do not establish full CLAS12 speedup or response
equivalence. The optimized mesh is faster in all 20 matched particle/seed pairs in the reference comparison.
Median startup simulation time changes from 1.063410 to 0.770623 s, with peak startup RSS 199.94 to 136.06
MiB.

Table 32. Median transport wall seconds per 200 events: reconstructed-reference comparison.

| Particle | Reference | Optimized | Reference/optimized |
| --- | --- | --- | --- |
| e- | 26.31760 | 24.21180 | 1.087 |
| proton | 2.37224 | 2.20600 | 1.075 |
| pi+ | 3.16977 | 2.94966 | 1.075 |
| neutron | 2.28295 | 2.17616 | 1.049 |

Table 33. Geant4 exceptions across each isolated 52-process comparison.

| Diagnostic | Original | Optimized | Reference |
| --- | --- | --- | --- |
| GeomSolids1001 | 52 | 0 | 0 |
| GeomSolids1002 | 0 | 0 | 0 |
| GeomNav1002 | 45 | 0 | 0 |
| GeomNav0003 | 0 | 0 | 0 |
| GeomVol1002 | 0 | 0 | 0 |

![FT inner shield comparison](figures/ft_shield_stl_comparison.png)

Figure 13. Original FT inner shield (left) and rebuilt, simplified shield (right). Matched cameras and
bounds use original coordinates; longitudinal grooves are retained.

![FT inner shield comparison](figures/ft_shield_details.png)

Figure 14. Matched flange underside views and tube sections at local z = -100 mm. Flange recesses remain
blind, and both longitudinal grooves remain after through-hole closure.

### 14.1 Smooth flange revision

The shield/cone interference recorded below is resolved by the subsequent cone revision in Section 15.

The smooth-flange FTInnerShield revision fills eight conical recesses, sixteen face chamfers, and two
stepped counterbores retained in the previous 13,500-triangle version. Both flange faces are complete flat
annuli. The large central passage, tube chamfers and flange fillets, and both longitudinal tube grooves
remain. The name, tungsten material, color, and all nine passive placements remain unchanged.

Removing the recess cuts reduces the reconstructed reference to 8,536 triangles. Protected simplification
gives 6,500 triangles, 51.85% fewer than the previous revision and 85.27% fewer than the defective
44,122-triangle engineering input. File size decreases from 675,084 to 325,084 bytes. All 3,148 groove,
flat-flange, and corner faces are protected, including all 512 flange-plane facets. Further trials at 6,300
and 6,200 triangles exceed the shape/quality guard and are not used. The result is one closed manifold
component of genus one with no detected self-intersections or zero-area facets, and unchanged bounds.

The previous closed volume is 1938412.694702 mm³ and the final volume is 1946864.540816 mm³. Filling the
recesses and applying the new simplification changes tungsten volume by +0.436019%. The smooth, unreduced
reference has volume 1946881.004462 mm³; simplification alone changes it by -0.00084564%. Bidirectional
sampling against that reference gives maximum displacement 0.047853 mm, below the 0.05 mm guard. These
sampled limits apply after the authorized recess closure, rather than across the filled cavities. The
original engineering mass remains undefined.

Independent surface checks confirm 256 coplanar triangles at each flange face, with areas matching the
complete 128-sided annuli at local z = -625 and -605 mm. The inner face radii are 45 and 50 mm respectively,
adjoining the retained fillets; outer radius is 100 mm. Every outer flange surface facet belongs to one flat
face or the cylindrical rim, with zero recess-wall facets. All 1,134 independent containment probes pass,
including a dense grid just inside both flange faces, all former bolt and recess centres, tube groove
floors, the filled tube hole, and the central beam passage. The final STL and smooth reference reproduce
byte for byte from the archived raw input.

Table 34. FT inner-shield smooth-flange revision.

| Quantity | Previous | Smooth |
| --- | --- | --- |
| Triangles | 13,500 | 6,500 |
| Bytes | 675,084 | 325,084 |
| Flange recesses | 26 | 0 |
| Boundary edges | 0 | 0 |
| Volume (mm³) | 1938412.695 | 1946864.541 |

Two separate tracking comparisons use the previous closed 13,500-triangle mesh and the new smooth, unreduced
reference as baselines respectively. Both use the same fixed GEMC3 executable snapshot, beamline_W material,
original placement, and matched 5 GeV target-origin primaries over 0.7--2.7 degrees and full azimuth.
FTFP_BERT runs without optics or magnetic field, with one thread, default production cuts, and no GUI or
event output. Five alternating-order repetitions use seeds 12345--12349 and 200 events per electron, proton,
positive-pion, and neutron run. Each comparison has 52 processes including startup and isolated overlap
checks; all 104 complete normally and all eighty transport runs report 200 events, with no Geant4 exceptions
in any fixture.

Previous/smooth median transport ratios are 1.273, 1.152, 1.160, 1.134 for electrons, protons, positive
pions, and neutrons respectively. These incremental upgrade timings include the added tungsten from filling
the blind recesses. Reference/smooth medians are 1.055, 1.023, 1.041, 1.030 in the same particle order,
comparing both cases with fully smooth flange surfaces and the recorded small decimation volume difference.
A ratio above one denotes faster tracking. Both comparisons are retained separately; neither establishes
full CLAS12 speedup or detector-response equivalence. Median startup simulation time changes from 0.776447
to 0.739538 s, with peak startup RSS 135.95 to 124.98 MiB.

Table 35. Median transport wall seconds per 200 events: incremental upgrade.

| Particle | Previous | Smooth | Previous/smooth |
| --- | --- | --- | --- |
| e- | 23.96760 | 18.82900 | 1.273 |
| proton | 2.23387 | 1.93947 | 1.152 |
| pi+ | 2.97310 | 2.56412 | 1.160 |
| neutron | 2.18361 | 1.92635 | 1.134 |

Table 36. Median transport wall seconds per 200 events: smooth-reference control.

| Particle | Reference | Smooth | Reference/smooth |
| --- | --- | --- | --- |
| e- | 20.41750 | 19.34670 | 1.055 |
| proton | 1.98474 | 1.94027 | 1.023 |
| pi+ | 2.68023 | 2.57448 | 1.041 |
| neutron | 1.96960 | 1.91241 | 1.030 |

The unchanged main-cone is included in a separate two-volume 10,000-point assembly check. Both previous and
smooth cases retain five pre-existing shield/cone overlap reports and one solid warning from the cone. Full
default construction completes without missing meshes, with one solid warning and eight overlap reports in
other or pre-existing joints. Smooth flange closure does not resolve that separate cone interference. All
fifteen native geometry/material and fourteen CAD variations continue to pass semantic comparison against
GEMC2. The earlier study archive is retained unchanged; this revision has a separate archive with its
previous mesh, smooth reference, final mesh, complete raw benchmarks, and validation evidence.

![Previous and smooth flange](figures/ft_shield_smooth_comparison.png)

Figure 15. Previous flange with blind recesses (left) and final smooth flange (right), with matched tube
sections showing both longitudinal grooves and the central bore retained.

## 15. Moller cone

The tenth beamline study renames main-cone to moller_cone in nine source and runtime GXML variations and
nine GEMC2 SQLite CAD rows. The beamline_W tungsten material, color, passive 180-degree y rotation, and
run-dependent positions remain unchanged. Five placements use cone z = 1589.27 mm and overlap the
FTInnerShield axial interval; four use z = 1273.27 mm and are already separated from the shield. The current
smooth-flange FTInnerShield is unchanged. The raw engineering cone is archived before replacement.

The original contains 15,782 triangles and 302 boundary edges in eight surface loops: five on the outer
tapered wall and three on the inner cylindrical wall. Its open surface has no valid enclosed material
volume. Filling those openings follows the measured outer cone and inner cylinder profiles, preserving every
original face and vertex before clearance work. The closed hole-filled reference has 16,688 triangles. The
large central beam passage remains open. A full nominal axisymmetric reconstruction is avoided because the
engineering outer rings are coarsely tessellated; their existing bounds and facets provide the shape
reference.

The existing entrance counterbore, about 39.98595 mm radius, is widened with a protected 128-sided
cylindrical cut of radius 40.200001 mm. The cut ends at local cone z = -53.53 mm, 0.2 mm beyond the
overlapping shield tip at -53.73 mm. A 0.2 mm nominal radial allowance above the shield radius accounts for
the polygonal opening. Independent clipped-triangle bounds give a minimum cone opening radius of 40.187892
mm and maximum shield radius 40.000001 mm, proving at least 0.187891 mm radial separation throughout the
shared axial interval. Collision checks and bidirectional vertex containment find no intersection in all
nine placements; the nearest sampled vertex-to-surface distance is 0.199938 mm in the overlapping group and
199.109193 mm in the axially separated group.

The clearance reference has 11,616 triangles; protected simplification retains 1,964 joint, shoulder, and
corner facets and produces 5,000 triangles, 68.32% fewer than the engineering input. File size falls from
789,184 to 250,084 bytes. The final mesh is one closed manifold component of genus one, with no detected
self-intersections or zero-area facets and exactly unchanged outer bounds. Minimum triangle altitude is
0.000380430 mm. Maximum sampled bidirectional displacement from the clearance reference is 0.020048 mm,
below the 0.05 mm shape guard. The original input reproduces the final STL and both reference meshes byte
for byte.

Hole-filled reference volume is 5835559.232219 mm³; final volume is 5825708.437762 mm³. Counterbore relief
and simplification remove 0.168806% tungsten relative to the closed hole-filled reference. Simplification
alone changes clearance-reference volume by -0.0000002660%. No original mass difference is inferred from the
defective open input. Fifty-five independent material probes test the filled opening centres and the
retained central beam passage.

Table 37. Original, repaired clearance reference, and final Moller cone.

| Quantity | Original | Reference | Final |
| --- | --- | --- | --- |
| Triangles | 15,782 | 11,616 | 5,000 |
| Bytes | 789,184 | 580,884 | 250,084 |
| Boundary edges | 302 | 0 | 0 |
| Volume (mm³) | undefined | 5825708.453 | 5825708.438 |

Two tracking comparisons isolate the cone in air: raw engineering input versus final mesh and repaired
clearance reference versus final mesh. They use the same fixed GEMC3 binary, beamline_W material, default
placement, and matched target-origin 5 GeV primaries over 1.1--2.6 degrees and full azimuth. FTFP_BERT runs
without optics or field, with one thread, default production cuts, and no GUI or event output. Each
comparison uses five alternating order repetitions, seeds 12345--12349, and 200 events per electron, proton,
positive-pion, and neutron run. Each has 52 processes including startup and isolated overlap checks. All 104
processes complete normally and all eighty transport runs report 200 events.

Raw/final median transport ratios are 2.200, 1.739, 1.574, 1.552 for electrons, protons, positive pions, and
neutrons respectively. The raw cone emits 26 GeomSolids1001 and 396 GeomNav1002 exception blocks across the
recorded processes. Its stuck-track recovery and invalid solid prevent attributing these ratios solely to
tessellation reduction. The final mesh emits no Geant4 exceptions. The clean repaired-reference/final
comparison gives ratios 1.638, 1.313, 1.402, 1.301 in the same order, with no exceptions in either case.
Ratios above one mean faster tracking. These isolated timings do not establish full CLAS12 speedup or
physics-response equivalence. Median startup simulation time changes from 0.777853 to 0.744276 s; peak
startup RSS changes from 137.08 to 122.14 MiB.

Table 38. Median transport wall seconds per 200 events: raw input versus final cone.

| Particle | Original | Final | Original/final |
| --- | --- | --- | --- |
| e- | 55.95160 | 25.43760 | 2.200 |
| proton | 10.28140 | 5.91253 | 1.739 |
| pi+ | 15.50770 | 9.85140 | 1.574 |
| neutron | 11.84350 | 7.63252 | 1.552 |

Table 39. Median transport wall seconds per 200 events: repaired clearance-reference control.

| Particle | Reference | Final | Reference/final |
| --- | --- | --- | --- |
| e- | 28.23070 | 17.23620 | 1.638 |
| proton | 5.43417 | 4.13941 | 1.313 |
| pi+ | 8.36232 | 5.96464 | 1.402 |
| neutron | 5.71081 | 4.39053 | 1.301 |

A separate cone/shield assembly test uses 10,000-point Geant4 overlap checking. The original cone gives five
overlap reports and one solid warning; the final assembly has no warnings or overlaps. Full default beamline
construction completes with no missing meshes or solid warnings, retaining four overlap reports at the
unrelated downstream tube/adapter joints. The earlier shield studies retain their historical overlap
measurements; this cone revision resolves that interference. Semantic comparisons pass all fifteen native
geometry and material variations and fourteen CAD variations against GEMC2.

![Moller cone comparison](figures/moller_cone_stl_comparison.png)

Figure 16. Original engineering cone (left) and optimized moller_cone (right), with matched cameras and
bounds. Surface openings are filled and the shield counterbore is widened; the central beam passage and
outer envelope remain.

![Moller cone shield joint](figures/moller_cone_joint.png)

Figure 17. Actual triangle sections at y = 0 through the original and final cone with the unchanged FT inner
shield. The enlarged counterbore clears the shield tip; the right panel magnifies the former shoulder
interference. The guaranteed radial gap includes polygon faceting.

## 16. Downstream joint clearance revision

A subsequent revision resolves the remaining contacts between Downstream_Beam_tube_Segment_1 and both
Beamline_Adapter_1 and Downstream_Beam_tube_Segment_2. The nominal cylindrical gaps are 0.0508 and 0.0127
mm, but the mating surfaces use 24-sided polygons with different angular alignments. Both alignments are
present in the engineering inputs. The reported 0.0398313 and 0.0568888 mm Geant4 penetration samples are
not global maxima. Polygon support planes give deficits of 0.342860 and 0.395184 mm at the respective
joints. Independent triangle checks find 240 and 239 contacts in the previous meshes; positive
vertex-distance samples alone would not establish clearance.

Only Segment 1 is changed. Its entrance socket radius increases from 60.325 to 60.771702 mm through nominal
z = 5048.376367 mm, followed by a 1 mm transition back to the original bore. Two additional 24-vertex rings
replace one long wall band with three bands, adding 96 triangles. The downstream socket radius increases
from 70.6628 to 71.162277 mm over its existing downstream wall interval. Both sockets retain their angular
grids. The adapter, Segment 2, all outer bounds, materials, passive placements, and the open beam passage
remain unchanged.

The revised Segment 1 contains 5,096 triangles and 254,884 bytes, compared with 5,000 triangles and 250,084
bytes before relief. It remains one closed manifold genus-one component with no detected self-intersections
or zero-area triangles. Final volume is 6710837.897365 mm3, removing 0.604764% steel relative to the
previous closed mesh. Volume change against the original annularly repaired reference is -0.620987%. The
original engineering surface remains open and has no valid mass. Maximum sampled distance from that source
remains 0.745438 mm, within the existing 0.75 mm guard. The current builder reproduces the relieved STL byte
for byte.

Independent clipping of neighboring triangles to their shared axial intervals gives minimum clearance to all
48 socket-wall triangle planes of 0.100019 mm at the adapter and 0.100022 mm at Segment 2. Triangle
collisions and bidirectional vertex containment are zero for both pairs. All eleven source CAD
configurations containing the three volumes use the same identity placements, so the same joint checks apply
to each. The separate 10,000-point Geant4 assembly test gives eight overlap reports before relief and no
exceptions afterward. Full default beamline construction now finishes without missing meshes, solid
warnings, or overlap reports. These checks cover the tested configuration and do not certify every possible
complete detector assembly.

Table 40. Segment 1 before and after socket relief.

| Quantity | Previous | Relieved | Change |
| --- | --- | --- | --- |
| Triangles | 5,000 | 5,096 | +96 |
| Bytes | 250,084 | 254,884 | +4,800 |
| Boundary edges | 0 | 0 | 0 |
| Volume (mm3) | 6751669.593 | 6710837.897 | -0.604764% |

A new tracking comparison includes the adapter and both downstream segments in air. Its baseline is the
previous optimized closed meshes, not the original engineering inputs. The fixed GEMC3 executable,
materials, identity placements, matched 5 GeV target-origin primaries over 0.1--1.3 degrees and full
azimuth, FTFP_BERT, no optics or field, one thread, default production cuts, and disabled GUI/event output
are identical. Five alternating-order repetitions use seeds 12345--12349 and 200 events per electron,
proton, positive-pion, and neutron run. All 52 processes finish normally and all forty transport runs report
200 events.

Previous/relieved median transport ratios are 0.981, 1.000, 1.008, 0.960 for electrons, protons, positive
pions, and neutrons respectively. Ratios above one denote faster tracking. The previous assembly produces 18
GeomNav1002, 4 GeomVol1002 exception blocks across the recorded processes; the relieved assembly produces 15
GeomNav1002 blocks. The remaining navigation warnings occur in the unchanged bellows region rather than
either relieved joint. Their z coordinates lie between 10177.906421 and 10281.864247 mm; all 1,741 triangles
intersecting the combined before/after warning interval are identical. Clean overlap checks therefore do not
establish warning-free tracking. These timings include overlap removal, local steel removal, and 96
additional facets. They measure the repair workload rather than a pure decimation gain, and do not establish
full CLAS12 performance or physics-response equivalence. The earlier study chapters and archives retain
their historical measurements.

Table 41. Median transport wall seconds per 200 events: three-part downstream assembly.

| Particle | Previous | Relieved | Previous/relieved |
| --- | --- | --- | --- |
| e- | 11.25010 | 11.46960 | 0.981 |
| proton | 1.75729 | 1.75794 | 1.000 |
| pi+ | 1.93580 | 1.92101 | 1.008 |
| neutron | 1.09550 | 1.14060 | 0.960 |

![Downstream socket clearance](figures/downstream_joint_clearance.png)

Figure 18. Actual socket and neighboring tube polygons projected onto the most restrictive socket face at
each joint. The previous socket cuts into its neighbor; the relieved socket provides at least 0.1 mm face
clearance while the neighboring tube remains unchanged.

## 17. Beamline database run selection

The beamline SQLite generator previously stored source labels such as `rgc_summer2022` in the
variation column. The steering card selected `default`, so requesting run 16000 matched no geometry rows
and constructed only the world. The corrected generator publishes all beamline geometry and material
banks under `default`, indexed by run number. Source labels remain authoring selectors and ASCII reference
filenames; they are not additional SQLite variations.

With the regenerated local database, `gemc beamline.yaml -gui -runno=16000` selects the summer-2022
configuration: ten native volumes and 22 CAD volumes. A matched headless construction changes from one
Geant4 volume before the fix to 33 afterward, including the world. The CLI and steering card need no
variation override. Existing databases require regeneration.

The three transverse CAD choices now use distinct run keys: 10000204 for `noWedges`, 10000206 for
`forwardWedges`, and 10000207 for `midpointWedges`. Each uses `default` and has its own copies of the same
two native pipe volumes and their materials. The dedicated transverse card selects the companion CAD
system. Regeneration replaces only the beamline systems in the selected experiment and removes stale
named banks; unrelated detector rows in an aggregate database are retained.

All 17 configured beamline runs construct with the expected SQLite row counts. The semantic comparator
passes all 15 native-geometry, 15 material, and 14 CAD comparisons against the GEMC2 source. A direct
database comparison preserves all physical fields, allowing only the transverse run-key changes and
the additional native copies. Repeated generation produces identical rows apart from database IDs,
and an aggregate-database check preserves unrelated rows exactly.

This is a database-selection repair. STL files, placements, material definitions, and the measured mesh
optimizations are unchanged; no new tracking-speed measurement is attributed to it. The retained
`data/beamline_run_selection/` evidence includes before/after database fixtures, the original command's
construction logs, all-run construction and comparator logs, validation results, and provenance hashes.
Historical benchmark archives retain their original inputs and source labels.

## 18. Moller cone tip

The eleventh beamline mesh study renames `cone-tip` to `moller_cone_tip` in all four source,
runtime, and GEMC3 CAD configurations: runs 5874, 11620, 18304, and 20000. The `beamline_W` material,
passive 180-degree y rotation, and 1273.27 mm z translation remain unchanged. SQLite banks continue to use
`default`, indexed by run number. The original is archived; the three installed meshes have identical bytes.

The original is a clean closed manifold solid with one component and genus two. Protected quadric
decimation reduces 13,730 triangles to 5,000 (63.5834% fewer), and 686,584 bytes to 250,084 (63.5756%
fewer). All 1,936 faces adjoining edges above five degrees retain their exact triangle coordinates.
The original bounds, central passage, and other opening are retained; no hole filling or reconstruction
is applied. The result has no boundary edges, non-manifold elements, detected self-intersections, or
zero-area triangles. The current builder reproduces the saved STL byte for byte.

Volume changes from 196511.847100 to 196510.892015 mm³, a change of -0.000486019%. Bidirectional vertex,
edge, and surface sampling gives a maximum deviation of 0.032396 mm, below the 0.05 mm guard. This is a
sampled maximum, not a proven global error bound. More aggressive protected trials distort the geometry
and are rejected. Table 42 gives the retained mesh properties.

Table 42. Moller cone tip before and after protected decimation.

| Quantity | Original | Optimized |
|----------|----------|-----------|
| Triangles | 13,730 | 5,000 |
| Bytes | 686,584 | 250,084 |
| Boundary edges | 0 | 0 |
| Components / genus | 1 / 2 | 1 / 2 |
| Volume (mm³) | 196511.847100 | 196510.892015 |
| Detected intersecting faces | 0 | 0 |

The isolated benchmark selects the run-5874 CAD row with `default`; the tip is absent from run 11.
The benchmark runner now accepts `--runno` so it can select such components without remapping their run
keys. Both fixtures use matched 5 GeV electron, proton, positive-pion, and neutron primaries from the
target, uniform in solid angle over 2.5--4.8 degrees and full azimuth. Physics is FTFP_BERT with no
magnetic field or optical processes, one thread, default production cuts, and no GUI or event output.
Five alternating-order repetitions use 200 events per particle and seeds 12345--12349. The fixed GEMC3
executable and its SHA-256 match the recent beamline studies; all primary hashes match within seed pairs.

Table 43 reports median Geant4 beamOn wall times, excluding initialization. Ratios are original/optimized;
values above one mean faster tracking. All five pairs are faster for each particle, and all 52 isolated
benchmark processes complete without Geant4 exceptions. The sample measures this one mesh; it does not
establish complete CLAS12 speedup or detector-response equivalence.

Table 43. Isolated Moller cone tip tracking; five repetitions of 200 events per particle.

| Particle | Original (s) | Optimized (s) | Speedup | Paired ratio range |
|----------|--------------|---------------|---------|--------------------|
| electron | 17.63610 | 10.63150 | 1.659 | 1.658--1.665 |
| proton | 1.84329 | 1.62666 | 1.133 | 1.133--1.211 |
| positive pion | 2.40739 | 2.04576 | 1.177 | 1.173--1.236 |
| neutron | 1.62514 | 1.40266 | 1.159 | 1.159--1.207 |

Median loading process wall time is nearly unchanged, 0.843174 to 0.841411 s, while loading CPU time
falls from 0.80 to 0.76 s. Engine initialization wall time changes from 0.758880 to 0.727224 s. Startup
peak RSS falls from 133.125 to 122.813 MiB (7.75%). Process CPU time, total wall time, memory, seed-paired
ratios, and raw diagnostics are retained separately from the tracking measurements.

The main-cone/tip assembly already overlaps before decimation. Independent surface collisions are present
with both engineering originals as well as with the current main cone. A separate 10,000-point Geant4
assembly check reports five GeomVol1002 exception blocks both before and after the tip change; sampled
penetrations reach about 0.372 mm. This optimization preserves the engineering interfaces and does not
repair that assembly overlap. Collision counts and vertex-containment counts depend on tessellation and
must not be interpreted as overlap volumes or as evidence of improved clearance.

All four complete affected configurations construct 39 Geant4 volumes including the world. Their two
GeomSolids1001 warnings remain, and sampled overlap blocks change from 20 to 21 per construction.
The renamed volume changes construction order and the resulting sampled reports; contacts among unchanged
parts remain. The clean isolated benchmark therefore does not certify the complete assemblies.
All 17 beamline configurations pass volume-count construction checks. All 15 native-geometry, 15 material,
and 14 CAD semantic comparisons pass; direct database checks allow only the four names and STL paths to
change. Every other mesh retains its prior hash. Figure 19 uses matched camera and bounds.

![Moller cone tip comparison](figures/moller_cone_tip_stl_comparison.png)

Figure 19. Original and optimized Moller cone tip meshes with identical bounds and camera. Openings and
sharp features are retained while redundant smooth-surface triangles are removed.

## 19. FT flange

The twelfth beamline mesh study renames `flange-assembly` to `FTFlange` in four configurations:
runs 5874, 11620, 18304, and 20000. The stainless-steel material, passive 180-degree y rotation, and
1273.27 mm z translation remain unchanged. Both repositories and the GEMC2 CAD database use the new
name. GEMC3 SQLite banks remain in `default`, selected by run number. The original is archived, and
all three installed meshes are byte-identical.

The original is already a clean closed annulus with only 552 triangles, one component, and genus one.
Topology-preserving quadric decimation reduces it to 540 triangles (2.1739% fewer); stored bytes fall
from 27,684 to 27,084 (2.1673% fewer). No holes are filled or surfaces reconstructed. The central
passage and overall bounds are retained. After edge collapse, vertices are restored to the two exact
engineering face planes, local z = -526.342956543 and -519.992980957 mm. The resulting STL has no
boundary edges, non-manifold elements, detected self-intersections, or zero-area triangles, and the
builder reproduces it byte for byte.

Steel volume changes from 229348.479344 to 229348.228841 mm³ (-0.000109224%). Bidirectional vertex,
edge, and surface sampling gives a maximum deviation of 0.049822 mm, below the 0.05 mm guard. This
sampled maximum is not a proven global error bound. A 536-triangle trial exceeds that guard; larger
reductions are rejected. The small reduction reflects the already-coarse engineering tessellation.
Table 44 summarizes the mesh changes, and Figure 20 compares the stored triangles with a matched camera.

The isolated benchmark selects run 5874 with `default`, using matched 5 GeV electron, proton,
positive-pion, and neutron primaries from the target, uniform in solid angle over 1.4--3.8 degrees and
full azimuth. Physics is FTFP_BERT with no field or optical processes, one thread, default production
cuts, and no GUI or event output. Five alternating-order repetitions use 2,000 events per particle and
seeds 12345--12349. The executable matches the recent beamline studies, and all primary hashes agree
within seed pairs. Table 45 reports median Geant4 beamOn wall times excluding initialization, with
original/optimized ratios and the ranges of paired ratios.

Tracking is effectively unchanged: median ratios are 1.0018 for electrons, 1.0001 for protons, 1.0003
for positive pions, and 0.9993 for neutrons. Every paired range includes one; only three or four of the
five pairs are faster. These variations do not establish a tracking-speed gain. All 52 isolated
processes complete without Geant4 exceptions. Median loading process wall time changes from 0.784696
to 0.791953 s, CPU time remains 0.72 s, and engine initialization wall time changes from 0.681824 to
0.672900 s. Startup peak RSS is 115.391 versus 115.375 MiB, effectively unchanged. Complete process
CPU, wall time, memory, and per-seed results are retained separately from the transport measurements.

The neighboring inner and outer assemblies already contact or overlap the flange before this change.
Independent triangle collision counts are 449 versus 449 for the inner assembly and 600 versus 583
for the outer assembly; those tessellation-dependent counts are not overlap volumes or clearance
proofs. The unchanged inner assembly is not closed. A separate three-part 10,000-point Geant4 check
reports one GeomSolids1001 and eight GeomVol1002 exception blocks both before and after optimization.
Sampled penetration depths reach about 0.249 mm. This mesh simplification retains the existing
engineering interfaces; the assembly defects remain.

All four complete affected configurations construct 39 Geant4 volumes including the world. Both
versions produce two GeomSolids1001 and 21 GeomVol1002 blocks per complete construction. All 17
beamline configurations pass volume-count construction checks, and the comparator passes 15 native
geometry, 15 material, and 14 CAD comparisons. Direct database checks allow only the four names and
STL paths to change; every other mesh retains its previous hash. The clean isolated benchmark does
not certify complete geometry or detector-response equivalence.

Table 44. FT flange before and after conservative decimation.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 552 | 540 |
| Bytes | 27,684 | 27,084 |
| Boundary edges | 0 | 0 |
| Components / genus | 1 / 1 | 1 / 1 |
| Volume (mm³) | 229348.479344 | 229348.228841 |

Table 45. Isolated FT flange tracking; five repetitions of 2,000 events per particle.

| Particle | Original (s) | Optimized (s) | Ratio | Paired ratio range |
| --- | --- | --- | --- | --- |
| Electron | 2.68847 | 2.68375 | 1.0018 | 0.9998--1.0054 |
| Proton | 3.61487 | 3.61435 | 1.0001 | 0.9957--1.0029 |
| Positive pion | 3.06986 | 3.06909 | 1.0003 | 0.9994--1.0033 |
| Neutron | 1.75223 | 1.75338 | 0.9993 | 0.9986--1.0051 |

![FT flange comparison](figures/ft_flange_stl_comparison.png)

Figure 20. Original and optimized FT flange meshes with identical bounds and camera. The central passage, flat
axial faces, and overall shape are retained; the already-coarse tessellation changes modestly.

## 20. Inner Moller-cone extension

The thirteenth beamline mesh study renames `inner-assembly` to `moller-cone-extension-inner` in runs 5874,
11620, 18304, and 20000. Both repositories, their CAD placements, and the GEMC2 CAD database use the new name.
Stainless steel, the passive 180-degree y rotation, and the 1273.27 mm z translation remain unchanged. GEMC3
SQLite banks remain under `default`, indexed by run number. The engineering original is archived, and the three
installed optimized STLs have identical bytes.

The original has 18,057 triangles, 75 boundary edges in two loops, one connected component, and no detected
self-intersections or zero-area triangles. The two open rims surround one radial port on the positive local-x
side: a 35-vertex rim at tube radius 40 mm and a 40-vertex rim at radius 47.625 mm. They share a nominal 6.35 mm
port radius centered at local z = -418.042413330 mm. The wall between these rims is absent. Stitching their
angularly ordered boundaries adds 75 triangles while retaining every original vertex. The beam passage and both
radial ports remain open; no hole caps or surface reconstruction are applied.

This repair produces an 18,132-triangle closed reference with one manifold component and genus three. Genus
describes the closed solid after restoring the missing tunnel wall; the open original does not define a valid
solid volume. Protected quadric decimation retains all 7,297 sharp-edge and port-adjacent faces at their exact
coordinates and reduces the result to 12,500 triangles. This is 30.7748% fewer than the raw source and 31.0611%
fewer than the repaired reference. Original bounds are retained. The final mesh has no boundary edges,
non-manifold elements, detected self-intersections, or zero-area triangles. The minimum triangle altitude is
0.002261 mm. Rebuilding reproduces the reference and optimized STL bytes exactly. Table 46 gives the mesh
inventory, and Figure 21 compares the stored meshes.

Repaired reference volume is 1431693.961982 mm³ and optimized volume is 1431694.095171 mm³, a +0.000009303%
decimation change. The original open mesh has no valid engineering mass. Maximum bidirectional
vertex/edge/surface sampling between the repaired reference and optimized STL is 0.015669 mm, below the 0.05 mm
guard; this is a sampled measurement, not a global bound or a distance to the incomplete raw surface. Larger
reductions distort the geometry and are rejected. Independent containment probes check 25 points along the beam
passage and six points in and around the repaired port, confirming that the passage and port remain empty and
adjacent steel remains filled.

Two separate isolated benchmarks use run 5874 with `default`, matched 5 GeV electron, proton, positive-pion, and
neutron primaries from the target, uniform in solid angle over 0.8--1.8 degrees and full azimuth. Physics is
FTFP_BERT with no field or optical processes, one thread, default production cuts, and no GUI or event output.
Each benchmark uses five alternating-order repetitions of 200 events per particle with seeds 12345--12349. The
fixed executable matches recent beamline studies; every seed pair has matching primary hashes.

Table 47 compares the defective raw mesh with the upgraded mesh. Table 48 separately compares the closed,
unreduced reference with the optimized mesh, preserving the repaired shape and material volume to the reported
decimation precision. Timings are median Geant4 beamOn wall times excluding initialization; ratios are
baseline/optimized, so values above one indicate faster tracking. Raw timings include surface and navigation
defects and do not establish faster correct transport. Only the repaired-reference control measures tessellation
changes after the missing wall is restored.

Raw-upgrade tracking ratios are 1.138, 1.055, 1.088, 1.043 for electrons, protons, positive pions, and neutrons,
respectively. Loading process wall time changes from 0.937190 to 0.886479 s; loading CPU time is 0.85 versus
0.83 s. Startup peak RSS is 141.844 versus 134.578 MiB. Complete process CPU, memory, wall time, and seed-paired
results are retained independently.

Repaired-reference tracking ratios are 1.261, 1.086, 1.144, 1.095 for electrons, protons, positive pions, and
neutrons, respectively. Loading process wall time changes from 0.892270 to 0.841108 s; loading CPU time is 0.82
versus 0.78 s. Startup peak RSS is 141.031 versus 133.953 MiB. Complete process CPU, memory, wall time, and
seed-paired results are retained independently.

Across the valid raw-input benchmark processes, exception totals are 163 GeomNav1002, 26 GeomSolids1001. All
optimized runs and both sides of the repaired-reference control have no Geant4 exceptions. These are
process-level diagnostic counts, not unique physical overlaps or counts of affected events.

A separate six-part 10,000-point assembly check includes the extension, FT flange, FT inner shield, main cone,
lead shield, and outer assembly. Exception blocks are original: 1 GeomSolids1001, 15 GeomVol1002; reference: 15
GeomVol1002; optimized: 15 GeomVol1002. The restored wall removes the extension surface-hole warning;
engineering overlaps remain. Independent surface collisions use the actual CAD transforms, including the FT
inner shield offset. Collision counts depend on tessellation and are not overlap volumes or clearance proofs.

All four complete affected configurations construct 39 Geant4 volumes including the world. Per-configuration
exception blocks are original: 2 GeomSolids1001, 21 GeomVol1002; optimized: 1 GeomSolids1001, 20 GeomVol1002.
All 17 beamline configurations pass volume-count construction checks. All 15 native geometry, 15 material, and
14 CAD semantic comparisons pass. Direct database checks allow only the four names and STL paths to change;
every other mesh retains its prior hash. These checks do not establish complete overlap freedom, full CLAS12
speed gains, or detector-response equivalence.

Table 46. Inner extension raw input, repaired reference, and optimized mesh.

| Quantity | Raw | Repaired | Optimized |
| --- | --- | --- | --- |
| Triangles | 18,057 | 18,132 | 12,500 |
| Bytes | 902,934 | 906,684 | 625,084 |
| Boundary edges | 75 | 0 | 0 |
| Closed components / genus | undefined | 1 / 3 | 1 / 3 |
| Volume (mm³) | undefined | 1431693.961982 | 1431694.095171 |

Table 47. Raw versus optimized inner extension; five repetitions of 200 events per particle.

| Particle | Raw (s) | Optimized (s) | Ratio | Paired ratio range |
| --- | --- | --- | --- | --- |
| Electron | 26.50810 | 23.28480 | 1.138 | 1.117--1.145 |
| Proton | 2.90723 | 2.75559 | 1.055 | 1.034--1.058 |
| Positive pion | 4.34586 | 3.99316 | 1.088 | 1.065--1.113 |
| Neutron | 2.63253 | 2.52499 | 1.043 | 1.035--1.068 |

Table 48. Repaired versus optimized inner extension; five repetitions of 200 events per particle.

| Particle | Repaired (s) | Optimized (s) | Ratio | Paired ratio range |
| --- | --- | --- | --- | --- |
| Electron | 29.39720 | 23.31290 | 1.261 | 1.214--1.275 |
| Proton | 3.00190 | 2.76398 | 1.086 | 1.082--1.116 |
| Positive pion | 4.56824 | 3.99481 | 1.144 | 1.130--1.144 |
| Neutron | 2.76308 | 2.52386 | 1.095 | 1.091--1.118 |

![Inner extension comparison](figures/extension_inner_stl_comparison.png)

Figure 21. Original and optimized inner Moller-cone extension meshes with matched bounds and camera. The beam
passage and both radial ports remain open; the missing wall of the lower port is restored.

## 21. Moller-cone extension lead fill

This study renames `lead-shield` to `moller-cone-extension-lead-fill` in runs 5874, 11620, 18304, and 20000 in
both repositories. The lead material, passive 180-degree y rotation, and 1273.27 mm z translation are
retained. SQLite banks remain in `default`, selected by run number. The original is archived, and all three
installed optimized meshes are byte-identical.

The original is already a closed manifold solid with 10,594 triangles, one component, and genus two. Protected
quadric decimation reduces it to 8,000 triangles (24.4856% fewer), with 529,784 versus 400,084 stored bytes.
All 7,156 faces adjoining sharp edges above five degrees or any vertex within radius 48 mm retain their exact
triangle coordinates. This protects the full inner mating surface and adjacent end faces. The beam passage,
radial opening, and exact bounds remain. There is no hole filling or surface reconstruction. The result
retains its topology and has no boundary edges, non-manifold elements, detected intersections, or zero-area
triangles. Independent rebuilding reproduces its bytes.

Material volume changes from 11950334.138104 to 11950334.137844 mm³ (-0.0000000022%). Maximum bidirectional
vertex, edge, and surface sampled deviation is 0.00001998 mm, below the 0.05 mm guard. This sampled maximum is
not a proven global bound. Trials exceeding the shape, bounds, or volume guards are rejected.

The isolated benchmark selects run 5874 with `default`. It uses matched 5 GeV electrons, protons, positive
pions, and neutrons from the target, uniform in solid angle over 1.6--4.5 degrees and full azimuth. Physics is
FTFP_BERT with no field or optical processes, one thread, default production cuts, and no GUI or event output.
Five alternating-order repetitions use 200 events per particle and seeds 12345--12349. The fixed executable
matches the recent beamline studies, and primary hashes agree within each seed pair.

Tracking tables report median Geant4 beamOn wall time excluding initialization. Ratios are original/optimized;
values above one indicate faster tracking. Median ratios are 1.0826, 1.0795, 1.1226, 1.0882 for electrons,
protons, positive pions, and neutrons, respectively; faster-pair counts are 5/5, 5/5, 5/5, 5/5. Every paired
measurement improves in this sample. All 52 isolated processes complete without Geant4 exceptions. These
measurements describe this isolated workload and do not establish complete CLAS12 performance or
detector-response equivalence.

Loading medians, in seconds, are process wall time: 0.896672 versus 0.844312; process CPU time: 0.850000
versus 0.810000; engine initialization wall time: 0.803922 versus 0.767714. Startup peak RSS is 137.297 versus
133.859 MiB. Process wall time includes launch and initialization; it is separate from beamOn transport.
Complete process CPU, wall time, peak memory, per-seed timings, and provenance are retained.

The separate four-part, 10,000-point assembly check uses the fill, casing, inner extension, and FT flange.
Existing assembly overlaps remain. Original and optimized exception counts are 10 GeomVol1002 and 10
GeomVol1002. Independent triangle-contact counts are moller-cone-extension-inner: 10273 versus 10273;
outer-assembly: 15473 versus 11052; FTFlange: 819 versus 819. These counts depend on tessellation and are
neither penetration volumes nor clearance proofs. Protected mating faces prevent this optimization from moving
those interfaces; retaining an interface does not repair pre-existing interference.

All four complete affected configurations construct 39 Geant4 volumes including the world. Run 5874
exception-block counts are original: 1 GeomSolids1001, 20 GeomVol1002; optimized: 1 GeomSolids1001, 21
GeomVol1002. The archive reports all four runs individually. All 17 beamline configurations pass volume-count
construction checks, and semantic comparisons pass 15 native geometry, 15 material, and 14 CAD comparisons.
Direct database checks allow only four names and STL paths to change; every other mesh retains its previous
hash. Existing complete-assembly warnings are separate from the clean isolated timings. A separate rename-only
control retains the original fill STL under the new name and path and produces the same 1 GeomSolids1001 and
21 GeomVol1002 blocks as the optimized configuration. The count increase from 20 to 21 also occurs without
decimation; overlap-check ordering and sampling change after the rename.

Table 49. Moller-cone extension lead fill mesh inventory.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 10,594 | 8,000 |
| Bytes | 529,784 | 400,084 |
| Boundary edges | 0 | 0 |
| Components / genus | 1 / 2 | 1 / 2 |
| Volume (mm³) | 11950334.138104 | 11950334.137844 |

Table 50. Moller-cone extension lead fill tracking; five repetitions of 200 events per particle.

| Particle | Before (s) | After (s) | Ratio | Paired range |
| --- | --- | --- | --- | --- |
| Electron | 23.76520 | 21.95230 | 1.0826 | 1.0810--1.1063 |
| Proton | 4.70122 | 4.35507 | 1.0795 | 1.0672--1.0912 |
| Positive pion | 7.60341 | 6.77309 | 1.1226 | 1.0457--1.1318 |
| Neutron | 5.23546 | 4.81107 | 1.0882 | 1.0729--1.1069 |

![Moller-cone extension lead fill](figures/extension_lead_stl_comparison.png)

Figure 22. Moller-cone extension lead fill before and after optimization, with identical bounds and camera.
The bore and radial opening remain.

## 22. Moller-cone extension lead case

This study renames `outer-assembly` to `moller-cone-extension-lead-case` in runs 5874, 11620, 18304, and 20000
in both repositories. The stainless steel material, passive 180-degree y rotation, and 1273.27 mm z
translation are retained. SQLite banks remain in `default`, selected by run number. The original is archived,
and all three installed optimized meshes are byte-identical.

The original is already a closed manifold solid with 17,360 triangles, one component, and genus two. Protected
quadric decimation reduces it to 10,000 triangles (42.3963% fewer), with 868,084 versus 500,084 stored bytes.
All 9,105 faces adjoining sharp edges above five degrees or any vertex within radius 118 mm retain their exact
triangle coordinates. This protects the full inner mating surface and adjacent end faces. The beam passage,
radial opening, and exact bounds remain. There is no hole filling or surface reconstruction. The result
retains its topology and has no boundary edges, non-manifold elements, detected intersections, or zero-area
triangles. Independent rebuilding reproduces its bytes.

Material volume changes from 817759.770060 to 817759.420845 mm³ (-0.0000427038%). Maximum bidirectional
vertex, edge, and surface sampled deviation is 0.00678680 mm, below the 0.05 mm guard. This sampled maximum is
not a proven global bound. Trials exceeding the shape, bounds, or volume guards are rejected.

The isolated benchmark selects run 5874 with `default`. It uses matched 5 GeV electrons, protons, positive
pions, and neutrons from the target, uniform in solid angle over 3.7--4.8 degrees and full azimuth. Physics is
FTFP_BERT with no field or optical processes, one thread, default production cuts, and no GUI or event output.
Five alternating-order repetitions use 200 events per particle and seeds 12345--12349. The fixed executable
matches the recent beamline studies, and primary hashes agree within each seed pair.

Tracking tables report median Geant4 beamOn wall time excluding initialization. Ratios are original/optimized;
values above one indicate faster tracking. Median ratios are 1.0529, 1.0377, 1.0098, 1.0198 for electrons,
protons, positive pions, and neutrons, respectively; faster-pair counts are 5/5, 5/5, 5/5, 2/5. Some paired
ranges include one; those particle samples do not establish a consistent gain. All 52 isolated processes
complete without Geant4 exceptions. These measurements describe this isolated workload and do not establish
complete CLAS12 performance or detector-response equivalence.

Loading medians, in seconds, are process wall time: 1.000175 versus 0.838249; process CPU time: 0.920000
versus 0.760000; engine initialization wall time: 0.882605 versus 0.724002. Startup peak RSS is 137.469 versus
127.516 MiB. Process wall time includes launch and initialization; it is separate from beamOn transport.
Complete process CPU, wall time, peak memory, per-seed timings, and provenance are retained.

The separate four-part, 10,000-point assembly check uses the fill, casing, inner extension, and FT flange.
Existing assembly overlaps remain. Original and optimized exception counts are 9 GeomVol1002 and 9
GeomVol1002. Independent triangle-contact counts are moller-cone-extension-inner: 0 versus 0;
moller-cone-extension-lead-fill: 10990 versus 10990; FTFlange: 583 versus 583. These counts depend on
tessellation and are neither penetration volumes nor clearance proofs. Protected mating faces prevent this
optimization from moving those interfaces; retaining an interface does not repair pre-existing interference.

All four complete affected configurations construct 39 Geant4 volumes including the world. Run 5874
exception-block counts are original: 1 GeomSolids1001, 21 GeomVol1002; optimized: 1 GeomSolids1001, 21
GeomVol1002. The archive reports all four runs individually. All 17 beamline configurations pass volume-count
construction checks, and semantic comparisons pass 15 native geometry, 15 material, and 14 CAD comparisons.
Direct database checks allow only four names and STL paths to change; every other mesh retains its previous
hash. Existing complete-assembly warnings are separate from the clean isolated timings.

Table 51. Moller-cone extension lead case mesh inventory.

| Quantity | Original | Optimized |
| --- | --- | --- |
| Triangles | 17,360 | 10,000 |
| Bytes | 868,084 | 500,084 |
| Boundary edges | 0 | 0 |
| Components / genus | 1 / 2 | 1 / 2 |
| Volume (mm³) | 817759.770060 | 817759.420845 |

Table 52. Moller-cone extension lead case tracking; five repetitions of 200 events per particle.

| Particle | Before (s) | After (s) | Ratio | Paired range |
| --- | --- | --- | --- | --- |
| Electron | 4.14328 | 3.93523 | 1.0529 | 1.0292--1.1052 |
| Proton | 0.99817 | 0.96193 | 1.0377 | 1.0001--1.0377 |
| Positive pion | 0.88047 | 0.87188 | 1.0098 | 1.0032--1.0308 |
| Neutron | 0.81340 | 0.79759 | 1.0198 | 0.9544--1.0198 |

![Moller-cone extension lead case](figures/extension_case_stl_comparison.png)

Figure 23. Moller-cone extension lead case before and after optimization, with identical bounds and camera.
The bore and radial opening remain.

## 23. Moller-cone extension tungsten add-on

The sixteenth beamline mesh study renames `outer-cone` to `moller-cone-extension-tungsten-addon` in runs 5874,
11620, 18304, and 20000. Both repositories, their CAD placements, and the GEMC2 CAD database use the new name.
The `beamline_W` material, passive 180-degree y rotation, and 1273.27 mm z translation remain unchanged. GEMC3
banks remain under `default`, indexed by run number. The original is archived, and all three optimized meshes
have identical bytes.

The original has 27,778 triangles and 68 boundary edges in two loops. These 33- and 35-vertex rims surround an
inclined radial port whose connecting wall is missing. Fitting the rim coordinates indicates a 6.350052 mm
radius and a 4.499946-degree inclination toward positive local z along positive local y. The builder orders the
existing rim vertices around the nominal 4.5-degree axis; it imposes no new rim coordinates. Bridging them adds
68 wall triangles without moving any original vertex or removing any original face geometry. No beam passage or
radial opening is capped; there is no surface reconstruction. The independent repair audit retains the original
vertices and triangle coordinates exactly, allowing coherent face orientation.

The repaired reference is a closed manifold component with genus five and 27,846 triangles. The open source has
no valid solid volume; its reported genus four describes a surface with boundary, not the repaired solid.
Protected quadric decimation retains 9,154 faces, including sharp features, port-adjacent faces, faces with a
vertex within 0.25 mm of the main Moller cone, and faces adjoining the extension joint below local z = -169.5
mm. The main-cone dependency is guarded by its mesh hash. The final mesh has 12,000 triangles, 56.80% fewer than
the raw source and 56.91% fewer than the repaired reference. Its 600,084 bytes compare with 1,388,984 raw and
1,392,384 repaired bytes. Bounds and all protected face coordinates are exact. The mesh is closed, manifold, and
free of detected intersections and zero-area triangles. Table 53 inventories the meshes; Figure 24 compares
their tessellation.

Repaired tungsten volume is 3224441.660431 mm³ and optimized volume is 3224441.511484 mm³, a -0.0000046193%
decimation change. Maximum bidirectional vertex/edge/surface sampled deviation from the repaired reference is
0.012837 mm, below the 0.05 mm guard. This is a sampled measurement, not a proven global bound. Minimum triangle
altitude is 0.000473 mm. More aggressive protected trials distort the shape and are rejected. Independent probes
check 25 points along the beam passage, three along the inclined port, and four in adjacent tungsten. The
passages remain empty and the surrounding material remains filled. Both the repaired and optimized STLs
reproduce byte for byte.

Two separate isolated benchmarks select run 5874 with `default`. Matched 5 GeV electron, proton, positive-pion,
and neutron primaries originate at the target, uniform in solid angle over 2.7--5.0 degrees and full azimuth.
Physics is FTFP_BERT with no field or optical processes, one thread, default production cuts, and no GUI or
event output. Each comparison uses five alternating-order repetitions of 200 events per particle, seeds
12345--12349, the same fixed executable as the recent beamline studies, and identical primary hashes within seed
pairs.

Table 54 compares raw input with the upgraded mesh. Table 55 compares the closed, unreduced reference with the
optimized mesh. Median Geant4 beamOn wall times exclude initialization; ratios are baseline/optimized, so values
above one indicate faster tracking. Raw timings include the incomplete port wall and navigation defects and do
not establish faster correct transport. The repaired-reference control measures decimation with the repaired
shape and material volume preserved to the reported precision.

Raw-upgrade tracking ratios are 1.754, 1.488, 1.634, 1.472 for electrons, protons, positive pions, and neutrons,
respectively. Faster-pair counts are 5/5, 5/5, 5/5, 5/5 in the same order. Loading process wall time changes
from 0.997174 to 0.890545 s; loading CPU time is 0.93 versus 0.81 s. Startup peak RSS is 156.969 versus 131.500
MiB. Complete process CPU, memory, wall time, and seed-paired results are retained independently.

Repaired-reference tracking ratios are 1.647, 1.548, 1.642, 1.535 for electrons, protons, positive pions, and
neutrons, respectively. Faster-pair counts are 5/5, 5/5, 5/5, 5/5 in the same order. Loading process wall time
changes from 0.951752 to 0.840506 s; loading CPU time is 0.90 versus 0.79 s. Startup peak RSS is 155.031 versus
131.188 MiB. Complete process CPU, memory, wall time, and seed-paired results are retained independently.

Across the valid raw-input benchmark processes, exception totals are 66 GeomNav1002, 26 GeomSolids1001. All
optimized runs and both sides of the repaired-reference control have no Geant4 exceptions. These are
process-level diagnostic counts, not unique physical overlaps or counts of affected events.

A separate five-part 10,000-point assembly check includes the add-on, main cone, inner extension, lead fill, and
lead case. Exception blocks are original: 1 GeomSolids1001, 12 GeomVol1002; reference: 12 GeomVol1002;
optimized: 12 GeomVol1002. The restored wall removes the extension surface-hole warning; engineering overlaps
remain. Independent surface collisions use the actual CAD transforms, with identical passive placements.
Main-cone contact counts remain 3041 and lead-case counts remain 233 in all three fixtures; the inner extension
and lead fill have zero surface contacts with the add-on. Collision counts depend on tessellation and are not
overlap volumes or clearance proofs.

All four complete affected configurations construct 39 Geant4 volumes including the world. Per-configuration
exception blocks are original: 1 GeomSolids1001, 21 GeomVol1002; optimized: 21 GeomVol1002. All 17 beamline
configurations pass volume-count construction checks. All 15 native geometry, 15 material, and 14 CAD semantic
comparisons pass. Direct database checks allow only the four names and STL paths to change; every other mesh
retains its prior hash. These checks do not establish complete overlap freedom, full CLAS12 speed gains, or
detector-response equivalence.

Table 53. Tungsten add-on raw input, repaired reference, and optimized mesh.

| Quantity | Raw | Repaired | Optimized |
| --- | --- | --- | --- |
| Triangles | 27,778 | 27,846 | 12,000 |
| Bytes | 1,388,984 | 1,392,384 | 600,084 |
| Boundary edges | 68 | 0 | 0 |
| Closed components / genus | undefined | 1 / 5 | 1 / 5 |
| Volume (mm³) | undefined | 3224441.660431 | 3224441.511484 |

Table 54. Raw versus optimized tungsten add-on; five repetitions of 200 events per particle.

| Particle | Raw (s) | After (s) | Ratio | Paired range |
| --- | --- | --- | --- | --- |
| Electron | 26.35900 | 15.02950 | 1.754 | 1.735--1.781 |
| Proton | 4.75147 | 3.19228 | 1.488 | 1.409--1.491 |
| Positive pion | 7.16772 | 4.38598 | 1.634 | 1.523--1.634 |
| Neutron | 4.33537 | 2.94566 | 1.472 | 1.472--1.508 |

Table 55. Repaired versus optimized tungsten add-on; five repetitions of 200 events per particle.

| Particle | Repaired (s) | After (s) | Ratio | Paired range |
| --- | --- | --- | --- | --- |
| Electron | 27.83340 | 16.90260 | 1.647 | 1.554--1.874 |
| Proton | 5.06416 | 3.27214 | 1.548 | 1.496--1.564 |
| Positive pion | 7.66426 | 4.66753 | 1.642 | 1.568--1.642 |
| Neutron | 4.69515 | 3.05862 | 1.535 | 1.499--1.556 |

![Tungsten add-on comparison](figures/extension_tungsten_stl_comparison.png)

Figure 24. Original and optimized Moller-cone extension tungsten add-on meshes with matched bounds and camera.
The beam passage and radial ports remain open; the missing inclined port wall is restored.

## 24. FT and Moller-cone interface clearances

This October 16 revision corrects the remaining FT/Moller-cone interfaces after the individual mesh studies.
Five meshes receive local material-removing operations: the inner extension, lead fill, lead case, main cone,
and tungsten add-on. FTInnerShield, FTFlange, and the cone tip remain byte-identical. Placements, passive
rotations, materials, names, and run keys are unchanged. All SQLite banks remain in `default`, indexed by run
number.

Several original engineering bores are coarse inscribed polygons. Their facets intrude into neighboring
surfaces even when nominal vertex radii agree. The inner extension also has a small shoulder at the main-cone
joint. The corrections use closed, polygonal cutters whose faces enclose the desired circular clearance
profiles, together with a conservative convex envelope of the actual lead fill. Cutters are intermediate
construction objects and are not additional detector volumes.

The inner-extension bore clears the placed FT shield, which is offset -369.73 mm in the common cone frame. Its
end is relieved around the unchanged flange bore. The lead-fill bore clears the inner extension. A scaled
convex envelope of the pre-clearance lead fill supplies at least 0.02002 mm plane clearance before final
casing simplification; a separate local cutter clears the unchanged flange. This envelope reduces casing
material loss from 4.4702% in a rejected circular-envelope trial to 1.2093%. The main cone receives a short
stepped relief around the inner-extension shoulder and a profiled opening around the cone tip. Its upper face
moves from z=712.002991 to 711.950012 mm. The add-on bore clears the main cone by a nominal 0.10 mm radial
profile margin. The health report retains every cutter profile and input hash.

All five corrected meshes retain one closed manifold component and their previous genera, with no detected
self-intersections or zero-area facets. The existing beam passages and radial ports remain open. A 0.0001 mm
weld of the saved float32 meshes removes numerical fragments. The casing is simplified from its boolean
reference to 16000 triangles with endpoint collapses and a maximum sampled deviation of 0.007648 mm; its
volume changes by +0.00002023% during this simplification. It contains more triangles than the earlier
10000-triangle casing but remains below the engineering source. The eight-part total changes from 59540 to
60100 triangles (+0.9405%). The material changes in Table 56 are intentional clearance removals, separate from
the earlier decimation volume guards.

An initial cut end face passed overlap checks but produced nine GeomNav1002 boundary-navigation warnings
during tracking. Retriangulating that annular face as an angular strip retains its exact surface, boundary
coordinates, triangle count, and material volume. The previously failing electron seed passes after this
change. The initial benchmark is retained as an excluded trial and is not used in the final timing table.
Canonical STL output changes facet order and cyclic starting vertices without changing geometry or winding;
all eight outputs and the casing reference reproduce byte for byte.

Independent placed-surface checks find zero triangle contacts and zero contained vertices in both directions
at all eight corrected interfaces. Table 57 gives minimum vertex-to-surface samples, not proven global
distance bounds. Three seeds (12345--12347) with 20000-point Geant4 overlap checks produce no exceptions. The
previous eight-part fixture produced 21 GeomVol1002 blocks. Matched meridian sections show the local changes
in Figures 25 and 26; the FT shield uses its actual placement offset.

The isolated tracking comparison includes the corrected eight-part assembly in run 5874 with `default`.
Matched 5 GeV electrons, protons, positive pions, and neutrons originate at the target, uniform in solid angle
over 0.8--4.8 degrees and full azimuth. FTFP_BERT uses one thread, default production cuts, no field or
optical processes, and no GUI or event output. Five alternating-order repetitions use 200 events per particle
and seeds 12345--12349. Executable and primary hashes are retained. Table 58 reports median Geant4 beamOn wall
times excluding initialization, before/corrected ratios, and paired ratio ranges. These timings include
changed clearances and material, so they are not a measurement of decimation alone.

Median tracking ratios are 0.8568, 0.8541, 0.8465, 0.8920 for electrons, protons, positive pions, and
neutrons, respectively. The corrected median tracking times are 12.1--18.1% longer than the pre-clearance
baseline. Faster-pair counts are 0/5, 0/5, 0/5, 0/5 in the same order. All 52 final benchmark processes
complete. The 26 corrected processes report no Geant4 exceptions. The baseline overlap diagnostic reports 21
GeomVol1002 blocks. The raw per-seed results retain process CPU, wall time, initialization, and memory
separately from transport.

Loading process wall time changes from 1.279579 to 1.272204 s; CPU changes from 1.190 to 1.230 s. Startup peak
RSS is 180.453 versus 180.188 MiB. The earlier individual-piece benchmarks remain historical measurements of
their stated geometries.

All 9 affected complete run configurations pass construction without Geant4 exceptions. All 17 beamline
configurations pass volume-count construction checks, and the comparator passes 15 native geometry, 15
material, and 14 CAD comparisons. Direct database checks preserve all GEMC2 tables and all GEMC3 physical
rows; every other STL retains its previous hash in all three runtime trees. The historical add-on optimization
remains reproducible using the archived main-cone dependency. These geometry and isolated timing checks do not
establish detector-response equivalence or full CLAS12 performance.

Table 56. Local clearance revisions relative to the previous optimized meshes.

| Mesh | Before | Corrected | Volume change (%) |
| --- | --- | --- | --- |
| Inner extension | 12500 | 11200 | -0.689274 |
| Lead case | 10000 | 16000 | -1.209323 |
| Lead fill | 8000 | 3958 | -0.192478 |
| Tungsten add-on | 12000 | 8356 | -0.374681 |
| Main cone | 5000 | 8546 | -0.118539 |

Table 57. Placed interface checks; distances sample vertices against the other surface.

| Interface | Sampled gap (mm) | Contacts |
| --- | --- | --- |
| Shield / inner extension | 0.062045 | 0 |
| Flange / inner extension | 0.053650 | 0 |
| Flange / case | 0.020020 | 0 |
| Case / lead fill | 0.019957 | 0 |
| Lead fill / inner extension | 0.053503 | 0 |
| Main cone / inner extension | 0.054603 | 0 |
| Cone tip / main cone | 0.052979 | 0 |
| Add-on / main cone | 0.094198 | 0 |

Table 58. Eight-part tracking; five repetitions of 200 events per particle.

| Particle | Before (s) | After (s) | Ratio | Paired range |
| --- | --- | --- | --- | --- |
| Electron | 19.36220 | 22.59820 | 0.8568 | 0.8543--0.8773 |
| Proton | 5.29483 | 6.19904 | 0.8541 | 0.8507--0.8899 |
| Positive pion | 6.94979 | 8.21029 | 0.8465 | 0.8001--0.8923 |
| Neutron | 5.55687 | 6.22962 | 0.8920 | 0.8433--0.9094 |

![FT/cone interface sections 1](figures/ft_joint_sections_1.png)

Figure 25. Matched meridian sections before and after the local clearance corrections. Blue and orange
identify the two named parts. Coordinates use the common passive cone frame; the shield is translated by its
actual offset. Solid outlines are sections of the stored STLs, with matched axes within each pair.

![FT/cone interface sections 2](figures/ft_joint_sections_2.png)

Figure 26. Matched meridian sections before and after the local clearance corrections. Blue and orange
identify the two named parts. Coordinates use the common passive cone frame; the shield is translated by its
actual offset. Solid outlines are sections of the stored STLs, with matched axes within each pair.


## 25. HTCC CAD cone transfer and validation

The October 19 HTCC update transfers three cured GEMC3 meshes into the GEMC2 clas12Tags repository. These are
the HTCC entry cone, Moller cone, and Moller-cone extension; they are separate from the beamline Moller-cone
studies above. The active source and runtime copies match the GEMC3 assets byte for byte, and the unmodified
GEMC2 engineering inputs are archived separately. Names, Rohacell material, passive 180-degree y rotations,
and all run-dependent placements remain unchanged. The variations default, rga_spring2018, and rga_fall2018
use runs 11, 3029, and 4763, respectively; the extension retains its additional 1 mm z shift.

Curing merges vertices, closes mesh boundaries, and repairs orientation. The entry cone is simplified to 6,000
triangles; the Moller cone additionally uses self-intersection removal and finishes at 5,866 triangles. The
already-light extension retains 1,748 triangles. No additional engineering-hole filling or Poisson
reconstruction is applied. Total stored triangles fall from 26,798 to 13,614, a 49.20% reduction. The table
below lists the topology counts from the same PyMeshLab inspection.

| Mesh | Input | Triangles | Boundary edges | Non-manifold edges |
|------|-------|----------:|---------------:|-------------------:|
| `htccCone` | Raw | 18,818 | 144 | 0 |
| `htccCone` | Cured | 6,000 | 0 | 0 |
| `htccMollerCone` | Raw | 6,232 | 0 | 45 |
| `htccMollerCone` | Cured | 5,866 | 0 | 24 |
| `htccMollerConeExt` | Raw | 1,748 | 0 | 0 |
| `htccMollerConeExt` | Cured | 1,748 | 0 | 0 |

All three cured meshes have zero boundary edges. The entry cone and extension have no non-manifold edges,
while the Moller cone retains 24, reduced from 45 in the raw input. These edge counts depend on the mesh
import and vertex-merging convention and should not be equated to affected-face counts. The largest change
among the six axis-aligned entry-cone bounds is 0.737915 mm. The Moller cone and extension retain their
original bounds exactly. Bounds agreement and zero boundary edges do not establish material-volume or surface
equivalence, and the remaining non-manifold Moller-cone edges are an unresolved topology limitation.

Validation uses GEMC 6.2 with Geant4 10.7.4, a local CCDB SQLite database, no magnetic field, no GUI, no event
output, and zero transported events. Native-plus-CAD initialization uses STD + FTFP_BERT + Optical. All three
variations complete through both TEXT/CAD and SQLite/CAD, giving six successful initializations. For each
variation, the 537 native TEXT rows match the effective SQLite geometry rows field by field; the three GXML
CAD placements match their effective SQLite CAD rows. Native geometry and materials, CAD placements, and the
SQLite database were retained by the transfer.

The full default SQLite overlap check reports entry-cone contact with htccEntryWindow. An isolated cone/window
fixture uses STD + FTFP_BERT, CHECK_OVERLAPS=1000, RANDOM=12345, and the unchanged window geometry and cone
placement. The cured cone produces one GeomVol1002 exception block, with reported penetration of at least
52.4771 micrometres; the matched raw-cone check produces none. The full default check reports at least 52.6119
micrometres for the same pair, approximately 0.053 mm. The two Moller cones report no overlap in that default
assembly check. The entry-window overlap remains unresolved in the transferred mesh; successful construction
does not certify an overlap-free assembly. Sampled penetration reports are not exact overlap depths or
volumes.

The retained zero-event logs verify construction and provide geometry diagnostics. They are not repeated
loading or tracking benchmarks, so no CPU, wall-time, memory, or transport-speed gain is assigned to the
49.20% triangle reduction. Photon yield, material budget, detector response, and particle navigation
equivalence require separate studies. The HTCC archive retains raw and cured STLs, input fixtures, scripts,
topology hashes, validation logs, and database-row snapshots.

### October 23: engineering Moller cone and collar union

The October 23 repair supersedes the Moller-cone topology limitation of the October 19 transfer. The
GeomSolids1001 warning is reproduced with the former active STL in GEMC3. It is caused by non-manifold and
intersecting facets near the collar, rather than by stored STL normal vectors alone. The engineering mesh
separates at its 45 four-face edges into two individually closed genus-one pieces: a 5,688-facet cone and a
544-facet collar. The earlier generic curing removed part of a 72.5 mm conical section and generated
inappropriate planar closures; retaining that defective mesh merely because it has zero boundary edges is
insufficient.

The replacement starts from the unchanged archived engineering export. Only the collar's 45 shared ring
vertices move radially inward by 0.0001 mm, resolving the zero-width seam for an exact Boolean union.
Intersection vertices that coincide after binary-STL rounding are welded at 0.0002 mm; null and duplicate
faces are removed, winding is made coherent, and faces are ordered deterministically. No Poisson
reconstruction, engineering-hole filling, or bore cap is applied. Repeated processes reproduce the final STL
and audit report byte for byte with the recorded software versions.

The final mesh has 3,451 vertices and 6,902 facets in one closed manifold component of genus one. It has zero
boundary edges, non-manifold edges or vertices, degenerate triangles, or detected intersecting faces. All six
engineering bounds remain identical. A final-to-engineering surface comparison samples 153,451 points and
finds a maximum distance of 0.000096786 mm. The reference includes both engineering surfaces, including
internal contact faces; this is a one-direction sampled comparison, not a global distance proof. The main bore
remains outside the solid at all 200 tested axial points in direct Geant4 classification.

The union volume before STL rounding is 783,909.77844 cubic millimetres; the stored mesh has 783,909.77434
cubic millimetres, a rounding/welding change of about -0.000000523%. The two original engineering pieces have
individually well-defined volumes, but their sum double-counts their contact/intersection region. No physical
material volume is assigned to the former defective active mesh. The restored section is visible in the exact
mesh-plane sections below.

The repaired mesh replaces the former 5,866-facet active Moller cone, adding 1,036 facets. The entry cone and
extension remain byte-identical at 6,000 and 1,748 facets. Total active HTCC CAD facets therefore rise from
13,614 to 14,650; this is still 45.33% fewer than the 26,798 engineering facets. This update repairs the
material geometry and winding; no new repeated loading or tracking benchmark was run, and no simulation
speedup is assigned to it.

All nine repaired native-plus-CAD initializations succeed for runs 11, 3029, and 4763: GEMC3 with Geant4
11.3.2, and GEMC2 SQLite/CAD and TEXT/CAD with Geant4 10.7.4. Every repaired process has zero GeomSolids
warnings. The GEMC3 fixtures explicitly select their named survey variations and require all 541 constructed
rows including the world. Direct Geant4 11.4.3 solid checks accept all 6,902 facets without rejection or solid
warnings; the unchanged other two meshes also pass. Native comparison matches 537 geometry and eight material
rows per configuration, and nine CAD placements match in name, material, passive rotation, and survey shift.
All four active source/runtime mesh trees are synchronized, and engineering originals are unchanged.

The existing contact between htccCone and htccEntryWindow is separate from the Moller repair and remains
visible in some GEMC2 overlap checks. No sampled overlap warning involving the repaired Moller cone is present
in these nine logs. Successful construction and sampled checks do not establish full particle-navigation or
detector-response equivalence.

![HTCC Moller repair](figures/htcc_moller_repair.png)

Exact sections at local y = 0.004092 mm through the archived engineering pieces, previous cured mesh, and
repaired union. The right panel shows the conical wall lost during curing and restored by the repair. Grey
internal engineering interfaces disappear in the union; the retained seam adjustment is below this figure's
resolution. No coordinate rescaling is applied.

data/htcc_moller_repair and htcc_moller_repair_archive.zip retain the repair metrics, source and output
hashes, software versions, baseline warning, all nine repaired construction logs and cards, surface samples,
CAD and native comparisons, direct Geant4 checks, original and previous/final meshes, builder, and figure
renderer. Executables are identified by hash and are not redistributed. The October 19 HTCC archive and all
earlier study archives remain unchanged.

## 26. Magnets duplicate shielding removal

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, the October 21 magnets cleanup removes nine DSShield meshes
and apex from the magnets CAD collection because this shielding is owned by the beamline. All three
configurations are updated in the GEMC2 and GEMC3 sources, runtime collections, and SQLite banks. The retained
51 magnet meshes, their materials and passive placements, the native solenoid, and all beamline geometry are
unchanged. Load the beamline alongside magnets to include the shielding.

This is removal of redundant geometry, without retriangulation or surface repair. The magnets collection falls
from 61 to 51 source meshes, from 148,940 to 132,230 stored triangles (16,710 removed; 11.22%), and from
7,452,124 to 6,615,784 bytes (836,340 removed; 11.22%). The nine downstream meshes account for 14,272
triangles and apex for 2,438. Each retained mesh matches its pre-removal bytes in all four source/runtime
collections.

The benchmark retains the native beamline and solenoid, the complete run-11 beamline CAD bank, and all
remaining magnets CAD. The original fixture includes the ten obsolete placements; the optimized fixture
removes them. Both use the same fixed GEMC3 dev executable, released October 19, 2026, Geant4 11.4.3, macOS
arm64, FTFP_BERT, one thread, and default production cuts. There is no magnetic field, optical physics, GUI,
event output, target, luminosity normalization, or pileup. The 5 GeV/c electron, proton, positive-pion, and
neutron primaries start at the origin, uniformly distributed in solid angle from 0.25 to 3.5 degrees over full
azimuth. Five alternating-order repetitions use 200 events per particle and seeds 12345--12349, with identical
LUND inputs within each seed pair. All 52 processes complete; every tracking process reports 200 events.

| Removed mesh | Triangles |
|---|---:|
| `DSShieldBackAss` | 988 |
| `DSShieldBackCover` | 1,012 |
| `DSShieldBackLead` | 1,244 |
| `DSShieldFlange` | 5,172 |
| `DSShieldFlangeAttachment` | 1,888 |
| `DSShieldFrontAss` | 1,056 |
| `DSShieldFrontCover` | 1,252 |
| `DSShieldFrontLead` | 988 |
| `DSShieldInnerAss` | 672 |
| `apex` | 2,438 |

Median zero-event process wall time changes from 1.98732 to 1.89090 s (1.051 times faster), CPU time from
1.920 to 1.840 s, and peak RSS from 321.53 to 306.98 MiB (4.52% lower). Tracking times below are median Geant4
beamOn wall times excluding initialization; speedup is before/after. These short, isolated workloads do not
establish a full-CLAS12 gain. Removing intersecting material changes transport histories, so timing changes
cannot be attributed solely to fewer facets or taken as proof of response equivalence.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 35.49510 | 34.50800 | 1.029 | 1.002--1.029 |
| Proton | 10.53440 | 10.34530 | 1.018 | 1.007--1.098 |
| Positive pion | 14.12550 | 14.32390 | 0.986 | 0.981--1.049 |
| Neutron | 10.53630 | 10.27570 | 1.025 | 0.957--1.078 |

The matched zero-event construction diagnostics use check_overlaps=2 and seed 12345. Built volume counts,
including the world, fall from 95 to 85; GeomVol1002 exception blocks fall from 58 to 26. Each fixture still
reports 26 GeomSolids1001 and 11 GeomSolids1002 blocks per import. Warning counts are sampled diagnostics, not
counts of all intersecting pairs, and the retained invalid/rejected-facet warnings and assembly contacts
remain unresolved. All three updated runs pass standalone GEMC3 magnets construction (53 volumes including the
world) and combined magnets/beamline GEMC2 TEXT/CAD and SQLite/CAD initialization. The GEMC3 semantic
comparator matches one native solenoid row and 51 CAD rows per configuration; independent checks match the
effective GEMC2 SQLite CAD rows to the GXML placements and the native TEXT rows to SQLite. All unrelated GEMC2
CAD rows and beamline meshes are unchanged. A supplemental combined GEMC3 card constructs 85 volumes at runs
11 and 3029, but only 53 at run 4763: the current GEMC3 lookup omits the beamline banks without that exact run
key, where GEMC2 selects the earlier run-3029 banks. This existing run-selection limitation is outside the
mesh-removal change and remains unresolved. The timed run-11 comparison loads both systems and is unaffected.
Across the forty timed tracking processes, navigation exception blocks total GeomNav1002: 4 before and 2
after.

The dedicated data/magnets_dedup directory records all measurements, mesh hashes, removed-facet inventory,
database checks, and validation. magnets_dedup_archive.zip retains the complete before/after fixtures,
original collected inputs, all raw logs and process reports, matched primary files, source snapshots, and
reproduction scripts. The executable is identified by hash and is not redistributed. Earlier study archives
remain unchanged.

## 27. Downstream shielding plate and vacuum jacket

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, DownstreamShieldingPlate and DownstreamVacuumJacket are
optimized as two separate volumes under their original names. Both retain their stainless steel, passive
180-degree y rotation, and 1273.27 mm z translation in the default, rga_spring2018, and rga_fall2018
configurations (runs 11, 3029, and 4763). All source and runtime copies match in GEMC2 and GEMC3; original
engineering inputs are archived in the owning GEMC2 repository.

The plate fills eight through-holes: six bolt holes of approximately 9.525 mm radius and two smaller holes of
approximately 2.38125 mm radius. The jacket fills six blind drilled recesses of approximately 6.35 mm entry
radius. Main circular rims and the hexagonal jacket step are extracted from the original vertices; only the
flat-face triangulation and fastener features change. No Poisson reconstruction, vertex displacement, or
joining of the separated parts is applied. The main aperture radii remain 76.35 mm for the plate and 63.5 mm
for the jacket, with the exact engineering polygon coordinates. The 32.83203125 mm axial gap and both original
bounds are retained.

The plate falls from 1,380 to 508 triangles (63.19% fewer); the jacket falls from 2,392 to 556 (76.76% fewer).
Together they fall from 3,772 to 1,064 triangles (71.79% fewer) and from 188,768 to 53,368 bytes. Each result
is a single closed, consistently oriented manifold component of genus one, with no boundary edges, detected
self-intersections, or zero-area triangles. Independent polygon-area and thickness calculations match the
filled STL volumes within the stated builder tolerance of one part per billion. These checks describe the
stored surfaces, not a certified engineering mass.

Signed plate volume changes from 243534.863634 to 249067.081984 cubic millimetres (+2.271633%); jacket volume
changes from 4082168.940709 to 4101145.339931 cubic millimetres (+0.464861%). The pair gains 0.566581% signed
steel volume from the authorized hole filling. This is a deliberate material-model change. The magnets
collection retains 51 meshes and now contains 129,522 triangles, after the separately documented
redundant-shielding removal.

Independent VTK containment checks identify all fourteen drilled features from the raw meshes. Forty-eight
probes that were inside the original holes are inside steel after filling; 1,296 bore probes remain outside
steel. Another 10,080 envelope probes away from the fastener features match the original geometry, and all 120
gap probes remain outside both separate volumes. These are sampled checks; exact rim-coordinate preservation
and analytic volume checks provide additional constraints.

The isolated benchmark loads only these two CAD rows at run 11, before and after optimization, with the same
fixed GEMC3 dev executable and Geant4 11.4.3 on macOS arm64. Both fixtures use FTFP_BERT, one thread, default
production cuts, and no field, optical physics, GUI, or event output. Each 5 GeV/c primary starts at the
origin with polar angle uniform in solid angle from 0.5 to 3.2 degrees and full azimuth. There is no target,
luminosity normalization, or pileup. Five alternating-order repetitions use 2,000 events per particle and
seeds 12345--12349; LUND primary hashes match within every seed pair. All fifty timed processes and both
separate construction diagnostics complete, with all forty tracking processes reporting 2,000 events.

| Volume | Raw triangles | Optimized | Signed volume change |
|---|---:|---:|---:|
| `DownstreamShieldingPlate` | 1,380 | 508 | +2.271633% |
| `DownstreamVacuumJacket` | 2,392 | 556 | +0.464861% |

Median zero-event process wall time is 0.73826 s before and 0.73375 s after; CPU time is 0.710 and 0.700 s,
and peak RSS is 124.05 and 120.06 MiB. Tracking values are median Geant4 beamOn wall times excluding startup.
Ratios are before/after: values below one indicate slower tracking. These observations describe the final
two-volume model; material changes and elimination of rejected source facets prevent interpreting the
comparison as a pure tessellation-speed measurement. It establishes neither full-CLAS12 performance nor
response equivalence.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 14.25750 | 11.78500 | 1.210 | 1.199--1.223 |
| Proton | 5.53148 | 5.14433 | 1.075 | 1.061--1.107 |
| Positive pion | 5.51953 | 5.00997 | 1.102 | 1.089--1.103 |
| Neutron | 3.94107 | 3.68135 | 1.071 | 1.068--1.117 |

Each isolated raw import reports ten GeomSolids1001 and four GeomSolids1002 warning blocks; each optimized
import is clean. The optimized timed tracking processes and isolated check_overlaps=2 construction report no
Geant4 exceptions. All three runs pass standalone GEMC3 magnets construction (53 volumes including the world),
combined GEMC2 TEXT/CAD and SQLite/CAD initialization, and native/CAD semantic checks with one solenoid row
and 51 CAD rows. Existing full-magnets assembly and unrelated mesh warnings remain in the retained validation
logs. The run-4763 GEMC3 beamline-bank limitation documented in the preceding section also remains. Isolated
construction success does not certify the complete assembly or detector response.

![Downstream plate and jacket](figures/downstream_plate_comparison.png)

Original (left) and optimized (right) stored STL surfaces in millimetres, with common bounds, orthographic
projection and physical scale within each row. The first row shows the plate entry face, the second the
drilled jacket face, and the third both separately placed parts at their original spacing. The face panels
show stored planar facets; assembly panels use complete stored meshes, including triangles rejected by Geant4.

The dedicated data/magnets_plate directory retains the mesh inventory, independent feature checks, all timing
samples, paired-input provenance, and three-run validation. magnets_plate_archive.zip contains both raw and
optimized two-volume fixtures, raw logs and process reports, source snapshots, matched primary files, original
engineering meshes, and reproduction scripts. The fixed executable is identified by hash and is not
redistributed. Earlier study archives remain unchanged.

## 28. Upstream shielding plate and vacuum jacket

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, UpstreamShieldingPlate and UpstreamVacuumJacket remain
separate under their original names in all three configurations: default, rga_spring2018, and rga_fall2018
(runs 11, 3029, and 4763). Stainless steel, passive 180-degree y rotation, and 1273.27 mm z translation are
unchanged. All four source/runtime collections match byte for byte; original engineering meshes are archived
in the owning GEMC2 repository.

Eight plate through-holes and six blind jacket bolt recesses are filled. The plate retains its original 76.35
mm aperture and 175 mm outer polygon rims. The jacket retains its stepped bore (76.2 mm and 73.025 mm radii),
reentrant outer contour, and rounded outer features. Its 894 non-cap/non-pocket triangles are preserved
exactly. The drilled entry face is retriangulated against its original 60-vertex outer boundary and 50-vertex
bore boundary, following actual edge connectivity. No rim displacement, joining, or Poisson reconstruction is
applied. Both original bounds and the 42.8780517578125 mm axial gap are retained.

The plate falls from 1,380 to 508 triangles; the jacket falls from 2,876 to 1,004. Together they fall from
4,256 to 1,512 triangles (64.47% fewer). Each optimized mesh is a single closed manifold component of genus
one, without boundary edges, detected self-intersections, or zero-area triangles. All four upstream/downstream
optimized meshes reproduce byte for byte with the extended builder. The final magnets collection has 51 meshes
and 126,778 triangles.

Signed plate volume changes from 243544.153894 to 249076.583284 cubic millimetres (+2.271633%). Jacket volume
changes from 3649980.788315 to 3669204.137370 cubic millimetres (+0.526670%). The pair gains 0.635819% signed
steel volume. The plate also passes an independent polygon-area/thickness volume calculation; the jacket
validation instead checks unchanged outer/bore surfaces and the preserved triangles. Hole filling deliberately
changes the material model and does not establish detector-response equivalence.

Independent VTK tests identify all fourteen source holes: 48 interior probes switch from empty to steel, 1,296
bore probes remain empty, and 10,080 envelope probes away from drilled features match the raw surfaces. All
120 inter-part gap probes remain outside both meshes. These sampled checks supplement exact preservation of
the retained contour vertices and faces.

The isolated run-11 benchmark loads the same two named CAD rows before and after optimization. It uses the
same fixed GEMC3 dev executable, Geant4 11.4.3, macOS arm64, FTFP_BERT, one thread, and default production
cuts. There is no field, optical physics, GUI, event output, target, luminosity normalization, or pileup. Each
5 GeV/c primary starts at the origin, uniformly in solid angle over 1.0--5.2 degrees and full azimuth. Five
alternating-order repetitions use 2,000 events per particle and seeds 12345--12349, with identical LUND inputs
within each pair. All fifty timed processes and both separate construction checks complete without Geant4
exceptions; each of the forty tracking processes reports 2,000 events.

Median zero-event process wall time is 0.78839 s before and 0.78842 s after; CPU time is 0.720 and 0.710 s,
and peak RSS is 124.72 and 120.61 MiB. Tracking measurements below are median Geant4 beamOn wall times
excluding startup; ratios are before/after and values above one indicate faster tracking. These results apply
to this isolated two-part workload. The authorized hole filling changes physical transport, so the comparison
does not isolate tessellation cost or establish a full-CLAS12 gain. The benchmark runner verifies its
executable hash at both start and completion. The installed executable was updated after the benchmark;
provenance records the later documentation-time hash separately, without assigning it to the timed processes
or the earlier validation checks.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 17.66120 | 14.09530 | 1.253 | 1.230--1.257 |
| Proton | 6.02561 | 5.51877 | 1.092 | 1.077--1.116 |
| Positive pion | 5.68061 | 5.07695 | 1.119 | 1.087--1.145 |
| Neutron | 4.06531 | 3.57569 | 1.137 | 1.108--1.153 |

All three runs pass standalone GEMC3 magnets construction with 53 volumes including the world, combined GEMC2
TEXT/CAD and SQLite/CAD initialization, and semantic comparisons of one native solenoid row and 51 CAD rows.
The sampled full-magnets GEMC3 diagnostics retain 16 GeomSolids1001, seven GeomSolids1002, and 23 GeomVol1002
warning blocks per run, originating outside the clean isolated upstream pair. Assembly validation remains
incomplete; the previously documented run-4763 beamline-bank selection limitation also remains.

![Upstream meshes](figures/upstream_plate_comparison.png)

Original (left) and optimized (right) upstream STL surfaces, with common bounds and orthographic physical
scale within each row. Entry-face panels show stored planar facets; the assembly row shows both separate
complete meshes at their original spacing. Outer jacket recesses and rounded features remain; only drilled
features and the entry-cap triangulation change.

data/magnets_upstream retains the inventory, shape probes, raw timing results, hashes, and three-run
validation. magnets_upstream_archive.zip retains both two-volume fixtures, matched primaries, all raw
logs/time reports, original meshes, final outputs, and builder/validation scripts. The executable is
identified by hash and is not redistributed. Earlier archives are unchanged.

## 29. DC region-1 back membranes

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, the six dcs1r1back through dcs6r1back Kapton membranes move
from magnets to the DC system. A new DC cad directory owns one unchanged dcs5r1back STL. The other five named
placements share its solid. GEMC3 publishes all six passive placements in dc_cad; GEMC2 uses one CAD source in
dc_cad and five native CopyOf rows in dc_copies. The supplied DC cards and the GEMC3 experiment card load the
required companions. Native DC geometry and materials remain unchanged.

The six engineering files are not byte-identical: sector coordinates and small tilts are baked into the
vertices. Proper rigid fits of their twelve corresponding vertices give a maximum error of 0.00007613 mm
against the shared reference. This is comparable to single-precision STL export rounding. Sector-specific
translations are retained rather than assuming exact rotations of a single unshifted sector. Original meshes
are archived separately in the owning GEMC2 source repository.

Each source has twenty triangles, twelve vertices, thirty edges, one closed manifold component, genus zero,
and no boundary edges. These hexagonal prisms already have the minimum closed triangular surface for their
twelve retained corners. No geometric decimation or hole filling is applied. Unique stored and built triangles
fall from 120 to 20 (83.33% fewer), and active STL storage falls from 6,504 to 1,084 bytes. The six physical
membranes still have 120 placed triangles. Magnets now has 45 STL files with 126,658 triangles; DC owns the
additional twenty unique triangles.

Sharing the rounded approximately 2.5-micrometre reference film changes total signed Kapton volume from
23637.244828 to 23756.565606 cubic millimetres (+0.504800%). Float coordinate rounding is significant relative
to this thickness. This numerical material difference is reported separately from the storage reduction; it
does not establish detector-response equivalence.

At the user's request, angles are rounded to integers after comparing them with the fitted angles. The largest
resulting vertex displacement is 0.759079 mm in sector 1; sectors 2 and 3 move by at most 0.634661 mm. The
comparison loads native DC, both DC and magnets CAD, the solenoid, native beamline, and beamline CAD at run
11: 139 volumes including the world. Both variants use the same seed and 100,000 Geant4 surface samples per
tested volume. No overlap involves any of the six membranes in either variant, and both variants report 48
overlap messages covering the same 23 distinct ordered volume pairs. Existing overlaps elsewhere are retained.
Surface sampling is not a mathematical proof of clearance.

All three inherited CAD runs (11, 3029, 4763) pass GEMC2 TEXT/CAD, GEMC2 SQLite/CAD, and GEMC3 initialization.
GEMC3 also constructs its custom DDVCS run, for ten successful checks in total. The semantic comparison
matches both native DC variations and all four DC CAD banks, along with all three reduced magnets CAD banks.
Independent database checks verify the GEMC2 five-copy and one-mesh rows, unchanged unrelated native/material
banks, byte-identical source/runtime meshes in both repositories, and the six unchanged archived originals.

The timing fixture isolates the six membranes at run 11. Before optimization it builds six separate
tessellated solids; afterward it builds one shared solid with five copies, using the final integer angles. One
fixed GEMC3 dev executable and Geant4 11.4.3 run FTFP_BERT with default production cuts, one thread, no field,
no optical physics, no GUI, no event output, and no target or pileup. Each 5 GeV/c electron, proton, positive
pion, or neutron starts at the origin, uniformly in solid angle from 5 to 45 degrees with full azimuth. Five
alternating-order repetitions use 2,000 matched LUND primaries per particle and seeds 12345--12349. Startup
and beamOn tracking are reported separately; forty tracking processes each report 2,000 events. All fifty
timed processes and two separate construction checks complete without Geant4 exceptions.

Median zero-event process wall time falls from 0.72316 to 0.40457 s (1.787 times faster). Median process CPU
time changes from 0.660 to 0.360 s and peak RSS from 118.45 to 73.34 MiB. Tracking ratios below are
before/after; values above one indicate faster tracking. They describe this thin-membrane workload and do not
establish a full-CLAS12 speedup. The physical surface change from angle rounding and the small material-volume
difference are included in these timings.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 2.18817 | 2.22178 | 0.985 | 0.963--1.002 |
| Proton | 3.31635 | 3.36257 | 0.986 | 0.972--1.012 |
| Positive pion | 3.04980 | 3.08063 | 0.990 | 0.970--1.007 |
| Neutron | 0.91443 | 0.91720 | 0.997 | 0.965--0.999 |

![DC back membranes](figures/dc_back_comparison.png)

World x-y projections of the six original membranes and their shared-mesh copies, with sector numbers
retained. The right panel shows the maximum vertex displacement caused by the accepted integer-angle
placement, including the small rigid-fit residual. Lines overlap at the displayed millimetre scale; the bar
chart exposes the submillimetre changes.

data/dc_back and dc_back_archive.zip retain shape fits, rounded-angle displacements, database checks, both
dense assembly checks, repeated timing inputs/results, and raw logs. The archive includes the original and
final fixtures, archived engineering meshes, builder and validation scripts, and executable hash. The
executable itself is not redistributed. Earlier study archives are unchanged. Rebuild the shared mesh with the
builder's --round-angles option.

## 30. DC region-1 supports

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, the six dcs1r1support through dcs6r1support aluminum
support assemblies move from magnets into the DC cad directory. One unchanged dcs1r1support STL supplies all
six named placements through five copies. Together with the previously relocated back membranes, DC now owns
two STL files and twelve passive placements. GEMC3 stores them in dc_cad; GEMC2 uses two CAD rows in dc_cad
and ten native CopyOf rows in dc_copies at each inherited run. Native DC geometry and materials, the membrane
placements, and all unrelated banks remain unchanged.

All six supports contain 499 vertices and 1,006 triangles. A nearest-vertex rigid registration initialized
with nominal sector rotations converges to a one-to-one vertex correspondence. Proper rotations, without
reflection, match the shared reference within 0.00011619 mm; six-decimal fitted angles match the world
vertices within 0.00011771 mm. These residuals are comparable to the STL coordinate precision. Sector-specific
translations are retained. Original six files are archived separately in the owning GEMC2 repository.

Each engineering mesh has two closed manifold components, 1,509 edges, no boundary edges, and aggregate genus
four. Both connected pieces, curved openings, and all engineering facets are retained in the canonical STL.
Trial decimation distorted opening surfaces by tenths of a millimetre for little additional reduction, so this
optimization shares the solid rather than modifying its surfaces. MeshLab flags 30 faces in the canonical
contact region, with numerically varying counts in the other rotated exports; these original contacts are
retained. Geant4 construction and the isolated tracking runs report no exceptions.

Unique stored and built facets fall from 6,036 to 1,006 (83.33% fewer), and active STL storage falls from
302,304 to 50,384 bytes. Six physical supports remain, with 6,036 placed triangles. Magnets now has 39 STL
files and 120,622 triangles. Including both DC groups, the final shared inventory has 121,648 unique
triangles, compared with 126,778 before the membrane and support deduplication.

Sharing the reference changes total signed aluminum volume by only -0.000001606%. Original names, G4_Al
material, colors, passive placement, and sector offsets are retained. This is separate from the deliberate
placement change introduced by angle rounding; detector-response equivalence has not been established.

Following the same overlap gate as the membranes, support angles are rounded to integers. Sectors 3, 4, and 5
move by at most 2.755827 mm relative to their engineering placements; sector 6 moves by at most 2.189899 mm.
The fitted and rounded variants load native DC, both DC groups, magnets, solenoid, and native/CAD beamline at
run 11, with 139 volumes including the world. Both use the same seed and 100,000 Geant4 surface samples per
tested volume. Neither variant reports a support overlap. Each reports 49 overlap messages covering the same
22 distinct ordered volume pairs elsewhere, so rounding introduces no sampled overlap pair. Existing assembly
overlaps remain; sampling is not a proof of clearance.

All three inherited CAD runs (11, 3029, 4763) pass GEMC2 TEXT/CAD, GEMC2 SQLite/CAD, and GEMC3 construction.
GEMC3 also constructs the custom DC DDVCS run, for ten checks total. Each GEMC3 CAD-only fixture contains
thirteen volumes including the world. Semantic comparison matches both native DC variations, all four
twelve-row DC CAD banks, and all three thirty-nine-row magnets CAD banks. Both source/runtime collections and
the twelve archived engineering originals match by hash. The extended builder reproduces both active STLs, the
complete placement catalog, and both health reports byte for byte.

The timing fixture isolates six support placements at run 11. The original builds six independent solids; the
final fixture shares one solid with five copies and the validated integer angles. One fixed GEMC3 dev
executable and Geant4 11.4.3 run FTFP_BERT with default production cuts, one thread, no field, no optical
physics, no GUI, no event output, and no target, luminosity normalization, or pileup. Five-GeV/c electrons,
protons, positive pions, and neutrons start at the origin, uniformly in solid angle from 2 to 15 degrees with
full azimuth. Five alternating-order repetitions use 2,000 matched LUND primaries per particle and seeds
12345--12349. All fifty timed processes and both construction checks finish without Geant4 exceptions; each
tracking process reports 2,000 events.

Median zero-event process wall time falls from 0.73577 to 0.45538 s (1.616 times faster). Median process CPU
time changes from 0.680 to 0.390 s and peak RSS from 123.64 to 74.98 MiB. Tracking ratios below are
before/after; values above one indicate faster tracking. They describe this support workload and do not
establish a full-CLAS12 speedup. The physical placement change from angle rounding and the small
material-volume difference are included in these timings.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 3.29761 | 3.35005 | 0.984 | 0.964--1.058 |
| Proton | 3.35892 | 3.22980 | 1.040 | 0.988--1.041 |
| Positive pion | 3.00896 | 3.08031 | 0.977 | 0.956--1.107 |
| Neutron | 1.07484 | 1.03238 | 1.041 | 0.967--1.139 |

![DC supports](figures/dc_support_comparison.png)

World x-y projections of all six support assemblies before and after sharing one STL. All original facets and
openings remain; the red overlay uses the final integer angles. The right panel shows maximum vertex
displacements relative to the engineering placements, including rigid-fit residuals. Both angle variants pass
the dense sampled overlap gate.

data/dc_support and dc_support_archive.zip retain shape fits, rounded-angle displacements, database checks,
both dense assembly checks, repeated timing inputs/results, and raw logs. The archive includes the original
and final fixtures, archived engineering meshes, builder and validation scripts, and executable hash. The
executable itself is not redistributed. Earlier study archives are unchanged. Rebuild the shared mesh with the
builder's --round-angles option.

### DC position precision update

All twelve DC CAD positions are now written with three decimal places in millimetres. This adds at most
0.000674 mm of translation relative to the study fixtures. The regenerated GEMC2 and GEMC3 banks pass semantic
comparisons and all ten construction checks. A further assembled check with 100,000 surface samples per volume
finds no new overlap pairs. Facet counts, materials, and rotations are unchanged. Existing timing archives
retain their measured inputs; the precision follow-up and validation are recorded in
data/dc_position_precision.

## 31. Vacuum jacket sharing with all holes retained

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, shell1a is renamed vacuumJacket. The twelve archived
shell[1--6][ab] jackets are not all identical: the a and b families have different outlines and hole patterns.
The accepted implementation uses six STL sources and six copies for twelve placements. vacuumJacket2a,
vacuumJacket4a, and vacuumJacket5a copy vacuumJacket; vacuumJacket3b, vacuumJacket4b, and vacuumJacket6b copy
vacuumJacket1b. All jacket names now use the vacuumJacket prefix. Materials, colors, and passive placements
are retained. Source and runtime collections are synchronized in both owning repositories.

Copies use exact 60-degree sector rotations and positions written with three decimal places in millimetres.
These are nominally repeated engineering parts, with different exported tessellations. On every axial plane,
fitted circular-hole centres, radii, and depths in the copied exports agree with the reference within 0.0001
mm. Parameters use unsnapped coordinates after nominal-plane grouping; individual exported vertices depart
from those planes by up to 0.000156 mm. Both directions of sampled polygonal-surface comparison are retained;
coarse sector-4 tessellations produce differences up to 0.27 mm. Thus the copies preserve the nominal hole
parameters, while their polygonal approximations follow the canonical STL.

Every hole is kept, including countersinks, buried steps, and the narrow slot. The builder finds boundary
contours on all distinct axial planes, protects their complete surface triangles, and decimates only the
remaining border region. The a and b references have 78 and 73 protected axial contours, respectively;
repeated depth contours are not distinct drilled holes. All 8,143 and 7,353 hole-region triangles remain
coordinate-exact after binary STL serialization. Bounds are unchanged. The two canonical meshes remain closed,
manifold, single-component solids with genus 38 and 35 and no detected self-intersecting faces. Each loses
only four border triangles: 8,388 to 8,384 and 7,560 to 7,556. The large saving comes from sharing, rather
than aggressive surface decimation.

Four engineering exports remain byte-identical originals. vacuumJacket6a includes an additional disconnected
100-triangle component, which is retained. Trial copies of vacuumJacket2b, vacuumJacket3a, and vacuumJacket5b
created new approximately 1.8--2.7 nm contacts with Plate6, Plate6, and Plate3. Focused original/copy pair
checks confirmed these contacts, so those three copies were rejected and their original STLs restored. No
compensating translation or contact relief is applied.

Unique jacket facets fall from 93,726 to 47,934, a reduction of 45,792 (48.86%). Twelve physical placements
remain. Their total placed facets increase from 93,726 to 95,754 because the shared reference is finer than
the sector-4 exports. Signed steel volume changes from 1,114,226,112.24 to 1,114,222,358.59 cubic millimetres,
or -0.000336885%. Across the complete magnets collection, 33 STLs containing 74,830 unique facets now supply
39 CAD placements. Detector-response equivalence has not been established by this isolated geometry and timing
study.

GEMC3 keeps the copies in magnets_cad. GEMC2 uses 33 SQLITECAD sources and six native CopyOf rows in
magnets_copies at each inherited run; the supplied SQLite and TEXT cards load that companion bank. All nine
construction checks pass across runs 11, 3029, and 4763 and both engines, including GEMC2 TEXT/CAD. Native
solenoid and all three 39-row CAD banks pass semantic comparison. Unrelated native geometry, materials, and DC
banks remain unchanged. The builder reproduces all six active jacket STLs and all three placement catalogs
byte for byte.

A dense run-11 assembly check loads native DC, both DC CAD groups, solenoid, magnets, and native/CAD beamline:
139 volumes including the world. At 100,000 surface samples per tested volume and the same seed, it reports
the same 22 ordered overlap pairs as before jacket sharing, normalizing shell1a to its new name. There are no
added or removed sampled pairs. Existing assembly orientation and overlap warnings remain; this is not a claim
of a warning-free assembly or a mathematical clearance proof.

Timing isolates the twelve jackets at run 11, comparing twelve independent solids with six sources and six
copies. One fixed GEMC3 dev executable with Geant4 11.4.3 runs FTFP_BERT, default production cuts, one thread,
no field, no optical physics, no GUI, and no event output. There is no target, luminosity normalization, or
pileup. Five-GeV/c electrons, protons, positive pions, and neutrons start at the origin, uniformly in solid
angle from 5 to 70 degrees, with full azimuth. Five alternating-order repetitions use 1,000 matched LUND
primaries per particle and seeds 12345--12349. All fifty timed processes and two isolated overlap checks
complete without Geant4 exceptions; each tracking process reports 1,000 events. Sleep prevention is enabled
for the reported repeat. An earlier complete repeat has inconsistent long internal wall-clock readings and is
archived separately rather than pooled with these results.

Median zero-event process wall time falls from 1.11389 to 0.94827 s (1.175 times faster). Median process CPU
time changes from 1.050 to 0.900 s, and peak RSS from 204.47 to 168.58 MiB. The table reports median internal
transport wall times, their before/after ratio, and the range of paired seed ratios. Ratios above one indicate
faster tracking. Geometry and stochastic trajectory changes are included; the ratios are not pure facet-count
scaling and do not establish a full-CLAS12 speedup.

| Particle | Before (s) | After (s) | Speedup | Paired ratio range |
|---|---:|---:|---:|---:|
| Electron | 8.57518 | 8.07752 | 1.062 | 1.012--1.062 |
| Proton | 4.45965 | 3.48069 | 1.281 | 1.196--1.291 |
| Positive pion | 4.46794 | 3.78943 | 1.179 | 1.155--1.306 |
| Neutron | 1.94376 | 1.63337 | 1.190 | 1.153--1.355 |

![Vacuum jackets](figures/vacuum_jacket_comparison.png)

The two distinct canonical jackets before and after conservative border simplification. All holes,
countersinks, and slots remain. The right column overlays a section through one stepped hole; the unchanged
protected surfaces coincide. The four retained original exports are not shown.

data/magnets_vacuum and magnets_vacuum_archive.zip retain mesh health, hole parameters, surface comparisons,
original and final inventories, all repeated timings, matched primaries, raw logs, rejected-copy contacts,
semantic checks, and both dense assembly fixtures. The archive also includes the twelve original engineering
exports, six final meshes, three catalogs, builder, benchmark, validation code, and executable hash. The
executable is not redistributed. Earlier study archives remain unchanged. REPRODUCE.md documents the commands
and fixture paths.

All active jacket placements now use vacuumJacket names: the original shell1a keeps vacuumJacket, and every
other shellN[a/b] becomes vacuumJacketN[a/b]. For example, shell1b becomes vacuumJacket1b and shell6b becomes
vacuumJacket6b. The five remaining shell-named STL sources and all copy references are renamed consistently in
both engines. Archived engineering inputs and previous timing datasets retain their recorded names. The naming
follow-up verifies identical mesh hashes and database rows after identifier mapping, and all nine construction
checks and all three native/CAD comparisons pass again. The builder reproduces six meshes, three catalogs, and
the health report byte for byte. Holes, facets, materials, transforms, and copy relationships are unchanged;
the measured 48.86% unique-facet reduction, 1.175 startup ratio, and particle-specific tracking results remain
those above. No additional simulation speedup is attributed to renaming. Mapping and validation are retained
in data/magnets_vacuum_naming and magnets_vacuum_naming_archive.zip.

## 32. Torus coil sharing with openings retained

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, the six copper torus coils share one unchanged engineering
mesh. coil1 is renamed coil, while coil2 through coil6 keep their sector suffixes and become five passive
copies. All openings, rounded corners, thickness, G4_Cu material, and colors are retained. Both source and
runtime collections are synchronized in the two owning repositories; the six engineering originals are
archived separately.

Every original has 508 vertices and 1,016 triangles in one closed manifold component, with genus one, no
boundary edges, and no detected self-intersections. Exact 60-degree sector rotations give a one-to-one vertex
correspondence with maximum residual 0.000224728 mm, consistent with binary STL coordinate precision. Four
exports have identical mapped facet connectivity. coil2 and coil3 each use the opposite diagonal on one planar
side quadrilateral; the builder verifies the same four corners, perimeter, and plane. This changes the
triangulation rather than the represented surface.

The canonical coil STL is byte-identical to coil1. All 1,016 facets, including every surface around the large
central opening, remain. The source is already a clean tessellated ring; sharing achieves the reduction
without further contour simplification or hole filling. The copy placements use integer sector angles and
millimetre positions with three decimal places. No empirical translation or contact relief is introduced.

Unique stored and built coil facets fall from 6,096 to 1,016, a reduction of 5,080 (83.33%). Active STL
storage falls from 305,304 to 50,884 bytes. All six physical coils remain, with 6,096 placed facets. Total
signed copper volume changes from 691,360,208.654 to 691,360,128.713 cubic millimetres (-0.000011563%) because
the canonical coordinates replace separately rounded exports. The complete magnets collection now has 28 STL
sources and 69,750 unique facets for 39 CAD placements.

GEMC3 keeps the sources and copies together in magnets_cad. GEMC2 uses 28 CAD sources and 11 native
magnets_copies rows per inherited run, including the six existing jacket copies. The supplied cards already
load this companion bank. All nine GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD construction checks pass across
runs 11, 3029, and 4763. Semantic comparison matches all three native solenoid configurations and the three
39-row CAD banks. Unrelated native geometry, materials, and DC banks are unchanged. The builder reproduces the
canonical mesh, health report, and all three placement catalogs byte for byte.

The full run-11 assembly contains native DC, both DC CAD groups, solenoid, magnets, and native/CAD beamline:
139 volumes including the world. Matched baseline and final fixtures use seed 12345 and 100,000 Geant4 surface
samples per tested volume. Readout is disabled in these geometry-only fixtures. Existing orientation and
overlap warnings remain; the baseline reports 22 ordered overlap pairs and the final fixture reports 22. No
new sampled overlap pair is introduced by sharing the coil. Sampling is not a mathematical clearance proof.

The timing fixture isolates the six coil placements at run 11. The baseline builds six independent solids; the
optimized fixture builds one solid and reuses it through five copies. One fixed GEMC3 dev executable reports
geant4-11-03-patch-02 [MT]   (25-April-2025). It uses the serial run manager, FTFP_BERT, default production
cuts, one execution thread, no field, no optical physics, no GUI, no digitization, and no event output.
Five-GeV/c electrons, protons, positive pions, and neutrons start at the origin, uniformly in solid angle from
5 to 70 degrees with full azimuth. There is no target, luminosity normalization, or pileup. Five
alternating-order repetitions use 2,000 matched LUND primaries per particle and seeds 12345--12349. Fifty
timed processes and two isolated overlap checks are scheduled. Every successful tracking process reports 2,000
events; 7 serial processes fail as recorded below. Statistics use only seeds for which both fixtures complete;
a failed pair is excluded from both timing samples. Sleep prevention remains enabled throughout.

An initial tasking-mode attempt stopped after twenty processes when the optimized 2,000-event electron run at
seed 12349 raised fatal PART122: Cu62 was already registered in the Geant4 particle table during a
photonuclear interaction. This is a particle-table error, rather than a reported geometry overlap. Both
fixtures complete those electron primaries in a serial-mode probe, but the full serial repeat also fails on
the original proton geometry at seed 12349 with duplicate Co60[58.590] registration. Thus serial execution
does not resolve the issue, and it affects the reference geometry as well. The scheduled serial processes are
continued after failures, with the same executable hash. All failures, raw logs, and probe inputs are
archived. Tasking and serial results are not pooled. These failures prevent an unconditional
tracking-performance conclusion.

Median zero-event process wall time falls from 0.18605 to 0.13280 s (1.401 times faster). Median process CPU
time changes from 0.100 to 0.090 s, and peak RSS from 63.17 to 59.25 MiB. Tracking entries below are median
internal transport wall times; before/after ratios above one indicate faster tracking. The paired range
retains seed dependence. These isolated coil measurements do not establish a full-CLAS12 speedup or
detector-response equivalence, and the tiny geometric differences can alter stochastic trajectories. Paired
startup ratios range from 1.004 to 1.451. Ranges that span one do not establish a consistent gain in this
sample. The interrupted tasking attempt completed its ten zero-event measurements: median loading wall times
were 0.68288 and 0.67769 s, essentially unchanged, with peak RSS 121.70 and 117.52 MiB. Performance depends on
execution mode; the table below uses serial mode throughout.

| Particle | Pairs | Before (s) | After (s) | Ratio | Paired ratio range |
|---|---:|---:|---:|---:|---:|
| Electron | 5 | 6.41057 | 5.80693 | 1.104 | 1.043--1.168 |
| Proton | 4 | 4.97728 | 3.90553 | 1.274 | 1.207--1.451 |
| Positive pion | 2 | 4.99705 | 3.99851 | 1.250 | 1.211--1.289 |
| Neutron | 3 | 3.03117 | 2.02905 | 1.494 | 1.303--1.562 |

![Torus coils](figures/coil_comparison.png)

All six engineering coil exports aligned to sector 1, with their full ring profiles and central opening
retained. The right panel shows maximum matched-vertex residuals under exact nominal sector rotations; the
largest is 0.225 micrometres. The canonical mesh is unchanged, so an additional before/after surface overlay
would coincide.

data/magnets_coils and magnets_coils_archive.zip retain engineering mesh analysis, the shared-mesh proof,
material-volume changes, database comparisons, all nine construction logs, both dense assembly fixtures,
repeated timing inputs, matched primaries, raw logs, and executable hash. The archive includes the six
originals, final collected geometry and meshes, catalogs, builder, benchmark, and validation code. The
executable is not redistributed. Earlier study archives remain unchanged.

## 33. Hub cover sharing with holes retained

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, Plate1 through Plate6 are renamed hubCover1 through
hubCover6. The plain hubCover1 mesh supplies copies 2, 4, and 5; the holed hubCover3 mesh supplies copy 6.
Both canonical STLs are byte-identical to their engineering originals. All holes, thicknesses, contours, G4_Al
material, colors, and six physical placements are retained in both owning repositories and their runtime
collections.

The four plain exports each contain eight vertices and 12 triangles in one closed manifold component of genus
zero. The two holed exports each have 75 vertices and 150 triangles, with genus one. All have zero boundary
edges and no detected self-intersections. Nominal sector rotations match every vertex one to one: the largest
plain-cover residual is 0.000005540 mm, and the holed pair agrees to numerical roundoff. Three plain exports
use the alternate diagonal on one planar quadrilateral. The builder verifies identical perimeters, four
corners, and coplanarity, establishing surface equivalence despite different triangle connectivity.

The two sources already have simple tessellations. Optimization therefore shares solids without further
decimation or hole filling. Every canonical triangle remains, including the complete hole wall and rim in
hubCover3. Passive copies use exact integer sector angles and positions with three decimal places in
millimetres. No contact relief or empirical translation is introduced.

Unique cover facets fall from 348 to 162, saving 186 (53.45%). Active cover STL storage falls from 17,904 to
8,268 bytes. The six placements still contain 348 placed facets. Total signed aluminum volume is
7,346,686.175700 cubic millimetres before and after, with a relative change below one part in a trillion from
numerical roundoff. The complete magnets collection now contains 24 STL sources, 69,564 unique facets, and 39
CAD placements. GEMC3 keeps sources and copies in magnets_cad; GEMC2 uses 24 CAD sources and 15 native
magnets_copies rows per inherited run, including the existing jacket and coil copies.

All nine GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD construction checks pass across runs 11, 3029, and 4763.
Semantic comparison matches all three native solenoid configurations and the three 39-row CAD banks. Unrelated
native geometry, materials, and DC banks are unchanged at synchronization. The builder reproduces both
canonical STLs, the health report, and all three catalogs byte for byte. Original engineering exports remain
archived.

The dense run-11 fixture contains native DC, both DC CAD groups, solenoid, magnets, and native/CAD beamline:
139 volumes including the world. Readout is disabled. Renaming volumes changes Geant4 construction/check
ordering and thus assigns surface samples differently among unchanged volumes. The initial comparison records
four added and four removed ordered contact pairs, all among unchanged non-cover volumes. A controlled
baseline keeps the six independent original meshes and original poses but uses the final hubCover names. With
seed 12345 and 100,000 surface samples per tested volume, this baseline and the final shared geometry report
exactly the same 22 ordered overlap pairs. No new sampled overlap pair is introduced. Existing contacts,
including covers against the upstream jacket, and orientation warnings remain. Sampling does not establish
mathematical clearance.

The timing fixture isolates the six cover placements at run 11. The baseline builds six independent solids,
and the final fixture builds two solids with four copies. A fixed executable reports geant4-11-03-patch-02
[MT]   (25-April-2025). It uses the serial run manager, FTFP_BERT, default production cuts, and one execution
thread. Field, optical physics, GUI, readout, and event output are disabled. Five-GeV/c electrons, protons,
positive pions, and neutrons start at the origin, uniform in solid angle from 1.5 to 5.5 degrees with full
azimuth, covering these small-radius parts. There is no target, luminosity normalization, or pileup. Five
repetitions alternate fixture order and use 2,000 identical LUND primaries per particle at seeds 12345--12349.
Ten zero-event processes, forty tracking processes, and two isolated overlap checks are scheduled. Idle-sleep
prevention remains enabled throughout. The executable hash is checked at both ends. Inputs are frozen
independently of concurrent framework builds and experiment database regeneration.

One of the 52 scheduled processes fails. Raw logs, exception codes, and inputs are retained. The original
proton
fixture at seed 12345 raises PART122 because Na24 is already registered in the Geant4 particle table. Tracking
statistics include only pairs where both versions complete all 2,000 events; failures exclude both members of
that seed pair. These conditional measurements do not establish an unconditional tracking-performance gain.

Median zero-event process wall time changes from 0.13304 to 0.13308 s, a before/after ratio of 1.000. Median
CPU time changes from 0.090 to 0.090 s, and peak RSS from 58.05 to 57.69 MiB. Paired startup ratios range from
0.997 to 1.392. Tracking entries below are median internal transport wall times. Ratios above one indicate
faster execution; paired ranges show seed dependence, and ranges spanning one do not establish a consistent
gain in this sample. The principal demonstrated benefit is fewer unique solids and facets. These isolated
measurements do not establish a full-CLAS12 speedup or detector-response equivalence.

| Particle | Pairs | Before (s) | After (s) | Ratio | Paired ratio range |
|---|---:|---:|---:|---:|---:|
| Electron | 5 | 4.45213 | 4.47410 | 0.995 | 0.967--1.108 |
| Proton | 4 | 4.46378 | 4.67747 | 0.954 | 0.904--1.018 |
| Positive pion | 5 | 4.01745 | 3.93746 | 1.020 | 0.881--1.119 |
| Neutron | 5 | 2.44995 | 2.73761 | 0.895 | 0.759--1.203 |

![Hub covers](figures/hub_cover_comparison.png)

Original and shared hub-cover footprints coincide in all six sectors (left). The hole rim retained by
hubCover3 and its hubCover6 copy is unchanged (right); all 150 canonical facets remain. Plain covers 1, 2, 4,
and 5 retain their original 12-triangle shape.

data/magnets_hub_covers and magnets_hub_covers_archive.zip retain mesh equivalence and topology checks, facet
and volume metrics, all nine construction logs, semantic comparisons, the controlled and initial dense overlap
fixtures, repeated timings, matched primaries, raw logs, and the fixed executable hash. The archive includes
original exports, final collected geometry and meshes, catalogs, builders, benchmark, validation code, and
figure-generation inputs. The executable is not redistributed; previous study archives remain unchanged.

## 34. Hub shield sharing with holes retained

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, all seven Shield volumes use the hub_shield prefix. Shield2
becomes hub_shield and supplies hub_shield3 through hub_shield6 through four passive copies. Shield1 and
Shield7 are distinct end pieces, retained as hub_shield1 and hub_shield7 with byte-identical STLs. The seven
original exports remain archived. All holes, radial contours, stepped joints, beamline_W material, colors, and
physical placements remain.

The seven exports are not one identical family. Shield2 through Shield6 each contain 319 vertices and 638
triangles. Translation by the nominal 304.8 mm pitch gives a one-to-one vertex correspondence with identical
mapped facet connectivity and maximum residual 0.000195313 mm from STL coordinate rounding. Shield1 and
Shield7 each contain 239 vertices and 478 triangles, with different end profiles. Their signed volumes are
1,836,423.892 and 1,828,397.730 cubic millimetres, compared with 1,785,903.279 for Shield2. All seven meshes
have one closed manifold component, genus one, no boundary edges, and no detected self-intersections. Both
distinct end profiles must remain.

Directly copying the original Shield2 at three-decimal millimetre positions introduces 48.8281-nanometre
contacts at the stepped joints: the large absolute STL coordinates round the nominal body length upward. The
first dense candidate adds six ordered overlap pairs. Recentring the shared source by 1,794.392 mm reduces the
float32 quantization. The source is placed at world z = 3,067.662 mm; copies advance by exactly 304.8 mm. Far
axial faces are rounded inward, shortening them by 0.0000593262 mm relative to the original source. Nearest
rounding of a leading face initially leaves a 0.198-nanometre contact, recorded as two ordered overlap pairs.
Directed rounding retains that face on the clearance side and removes these contacts. No clearance is
manufactured by moving complete volumes.

Every radial coordinate and all 638 shared-source triangle connections remain exactly unchanged, including the
complete bore and both radial steps. No hole is filled and no circular contour is decimated. Both end meshes
are unchanged. Including axial normalization and independently rounded exports, final world vertices differ
from the originals by at most 0.000146485 mm. All positions have three decimal places in millimetres, and
rotations remain the original exact 180-degree passive rotation.

Unique shield facets fall from 4,146 to 1,594, saving 2,552 (61.55%). Active shield STL storage falls from
207,888 to 79,952 bytes. Seven physical placements still contain 4,146 placed facets. Total signed
tungsten-alloy volume changes from 12,594,336.584631 to 12,594,336.280296 cubic millimetres (-0.000002416%).
Magnets now uses 20 STL sources and 67,012 unique facets for 39 CAD placements. GEMC3 keeps every placement in
magnets_cad; GEMC2 has 20 CAD sources and 19 native magnets_copies rows per inherited run.

All nine GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD construction checks pass for runs 11, 3029, and 4763,
including explicit resolution of every copy source. Semantic comparison matches the three native solenoid
configurations and the three 39-row CAD banks. Unrelated native geometry, materials, and DC banks are
unchanged. The builder reproduces three STLs, the health report, and three placement catalogs byte for byte.

The dense run-11 fixture contains native DC, both DC CAD groups, solenoid, magnets, and native/CAD beamline:
139 volumes including the world. Readout is disabled. The controlled baseline retains seven independent
original meshes and original poses but uses the final volume names, keeping the Geant4 check order consistent.
At seed 12345 and 100,000 surface samples per tested volume, both the baseline and the final geometry report
exactly the same 22 ordered contact pairs, with no added or removed pair. The isolated seven-shield fixture
also passes 100,000-sample checks without any contact warning. Existing contacts and orientation warnings
elsewhere in the assembly remain. Sampling does not constitute a mathematical clearance proof.

The timing fixture isolates seven shield placements at run 11, building seven independent solids before
optimization and three sources plus four copies afterward. One fixed GEMC3 executable reports
geant4-11-03-patch-02 [MT]   (25-April-2025). The serial run manager uses one execution thread, FTFP_BERT, and
default production cuts. Field, optical physics, GUI, readout, and event output are disabled. Five-GeV/c
electrons, protons, positive pions, and neutrons start at the origin, uniform in solid angle from 0.3 to 1.4
degrees with full azimuth, covering the small-radius shield chain. There is no target, luminosity
normalization, or pileup. Five repetitions alternate fixture order and use 2,000 identical LUND primaries per
particle and seeds 12345--12349. Ten zero-event processes, forty tracking processes, and two isolated overlap
checks are scheduled. Idle-sleep prevention remains active, and the executable hash is checked at the start
and end.

38 of the 52 scheduled processes fail; exception counts are PART122=38. Raw logs, failed inputs, and exception
codes are retained. Tracking statistics include only seed pairs for which both fixtures complete all 2,000
events. Failures exclude both members of that seed pair, so these measurements are conditional on completion
and do not establish an unconditional performance gain.

All 38 fatal errors are duplicate-isotope registration failures in the Geant4 particle table: 19 in the
original geometry and 19 in the optimized geometry. Examples include W183, W187, Fe57, and tantalum isotopes.
The two successful tracking processes are unmatched; this study therefore supplies no valid tracking-speed
comparison.

No completed matched tracking pair is available for electrons, protons, positive pions, neutrons; no
tracking-time ratio can be estimated for those particles. Unmatched successful processes are archived but
excluded from comparisons.

Median zero-event process wall time changes from 0.18750 to 0.13374 s, a before/after ratio of 1.402. Median
CPU time changes from 0.100 to 0.090 s, and peak RSS from 61.47 to 59.52 MiB. Paired startup ratios range from
0.988 to 1.882. Tracking entries below are median internal transport wall times. Ratios above one indicate
faster execution; paired ranges show seed dependence, and ranges spanning one do not establish a consistent
gain in this sample. The principal demonstrated benefit is fewer unique solids and facets. These isolated
measurements do not establish a full-CLAS12 speedup or detector-response equivalence.

| Particle | Pairs | Before (s) | After (s) | Ratio | Paired ratio range |
|---|---:|---:|---:|---:|---:|
| Electron | 0 | -- | -- | -- | -- |
| Proton | 0 | -- | -- | -- | -- |
| Positive pion | 0 | -- | -- | -- | -- |
| Neutron | 0 | -- | -- | -- | -- |

![Hub shields](figures/hub_shield_comparison.png)

Longitudinal sections at world y = 0.1 mm compare original exports and shared geometry. All seven placements
remain, including both distinct end profiles (top). The middle-source bore and stepped radial contours are
retained exactly (bottom). Nanometre axial changes are below the figure resolution; their measured bounds are
reported in the text.

data/magnets_hub_shields and magnets_hub_shields_archive.zip retain original mesh analysis, equivalence and
topology checks, axial normalization, facet and volume metrics, all nine construction logs, semantic
comparisons, dense overlap fixtures, repeated timings, matched primaries, raw logs, and the fixed executable
hash. The rejected candidates and their contact warnings are retained too. The archive includes original
exports, final collected geometry and meshes, catalogs, builder, benchmark, validation code, and figure
inputs. The executable is not redistributed. Earlier study archives remain unchanged.

## 35. Cold hub optimization with holes retained

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, Hub001 is renamed ColdHub in all three configurations and
both owning repositories. Every drilled opening, main bore, G4_Al material, color, and passive placement
remains. The position is written with three decimal places in millimetres; the exact 180-degree rotation is
unchanged. The original engineering STL is archived separately.

The input has 6,235 vertices and 12,600 facets, with six boundary edges, one non-manifold vertex, seven
degenerate triangles, and eight detected intersecting faces. Its genus and physical material volume are
undefined until the open seam is repaired. Two triangular export slivers, with areas 0.000211868 and
0.000388564 square millimetres, are closed using existing vertices. These slivers are separate from the
physical drilled openings. Thirteen faces are oriented coherently. Seven collinear T-junctions are
retriangulated by splitting their opposite edge faces, without moving vertices. The repaired reference has
12,602 facets in one closed manifold component of genus 34, with no degenerate or intersecting faces.

Conservative edge collapses then remove 27 redundant vertices and 54 facets. Each collapse satisfies the
manifold link condition, preserves winding, and limits local plane error to 0.0001 mm. The largest actual
error is 0.000053917 mm. All surviving vertices retain their exact engineering coordinates. The isolated
original emits 16 GeomSolids1001 and seven GeomSolids1002 construction warnings per process; the optimized
source emits neither. Completed baseline runs with these nonfatal warnings remain eligible for timing pairs.
Every opening remains: the final mesh is closed, manifold, and genus 34, with no self-intersections or
degenerate triangles. Relative to the raw export, facets fall from 12,600 to 12,548, saving 52 (0.41%). STL
storage falls from 630,084 to 627,484 bytes. This is primarily a geometry repair; the facet reduction is
modest because the hole and curved profiles are retained. The performance comparison includes both repair and
simplification; it does not isolate the effect of the facet reduction.

All bounding coordinates are unchanged. Bidirectional surface-distance checks include all vertices plus
sampled edges and faces: 206,235 points from the original to the final mesh and 206,208 in the reverse
direction. Maximum sampled deviations are 0.000035946 and 0.000026133 mm, respectively. Sampling does not
prove a global distance bound. The closed repaired reference has signed volume 34,158,810.76890473 cubic
millimetres, compared with 34,158,810.76892262 after simplification: a change below 0.000000001%. No physical
volume is assigned to the original non-watertight export.

All nine GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD construction checks pass for runs 11, 3029, and 4763.
Semantic comparison matches the three native solenoid configurations and the three 39-row CAD banks. Unrelated
native geometry, materials, DC banks, and existing copy placements are unchanged. The builder reproduces the
STL, health report, and three catalogs byte for byte. Magnets still has 20 STL sources and 39 CAD placements,
now with 66,960 unique facets. GEMC2 uses 20 CAD sources and 19 native copy rows per run.

The dense run-11 fixture contains native DC, both DC CAD groups, solenoid, magnets, and native/CAD beamline:
139 volumes including the world, with readout disabled. The baseline retains the original mesh and pose but
uses the final ColdHub name to keep construction and surface-sampling order consistent. At seed 12345 and
100,000 surface samples per tested volume, both versions report the same 22 ordered contact pairs, with no
added or removed pair. Existing contacts elsewhere remain; this sampled comparison does not constitute a
mathematical clearance proof.

The timing fixture isolates one hub at run 11. One fixed GEMC3 executable reports geant4-11-03-patch-02 [MT]
(25-April-2025). The serial run manager uses one execution thread, FTFP_BERT, and default production cuts.
Field, optical physics, GUI, readout, and event output are disabled. Five-GeV/c electrons, protons, positive
pions, and neutrons start at the origin, uniform in solid angle from 0.5 to 3.0 degrees with full azimuth.
There is no target, luminosity normalization, or pileup. Five repetitions alternate fixture order and use
2,000 identical LUND primaries per particle and seeds 12345--12349. Ten zero-event processes, forty tracking
processes, and two isolated overlap checks are scheduled. Idle-sleep prevention remains active, and the
executable hash is checked at the start and end.

PART122 denotes duplicate-isotope registration in the Geant4 particle table; these failures are retained
separately from geometry warnings and excluded from timing pairs.

14 of the 52 scheduled processes fail; exception counts are GeomSolids1001=112, GeomSolids1002=49, PART122=14.
Raw logs, failed inputs, and exception codes, including nonfatal solid warnings, are retained. Tracking
statistics include only seed pairs for which both fixtures complete all 2,000 events. Failures exclude both
members of that seed pair, so these measurements are conditional on completion and do not establish an
unconditional performance gain.

Median zero-event process wall time changes from 0.35595 to 0.30656 s, a before/after ratio of 1.161. Median
CPU time changes from 0.180 to 0.180 s, and peak RSS from 80.91 to 81.66 MiB. Paired startup ratios range from
0.785 to 1.242. Tracking entries below are median internal transport wall times. Ratios above one indicate
faster execution; paired ranges show seed dependence, and ranges spanning one do not establish a consistent
gain in this sample. The principal demonstrated benefit is a valid closed mesh with every opening retained.
Repair and facet ordering can alter navigation and stochastic trajectories. These isolated measurements do not
establish a full-CLAS12 speedup or detector-response equivalence.

| Particle | Pairs | Before (s) | After (s) | Ratio | Paired ratio range |
|---|---:|---:|---:|---:|---:|
| Electron | 2 | 109.44350 | 97.52760 | 1.122 | 1.111--1.133 |
| Proton | 3 | 14.05220 | 13.31090 | 1.056 | 1.056--1.063 |
| Positive pion | 4 | 17.63475 | 16.40535 | 1.075 | 1.048--1.097 |
| Neutron | 4 | 11.85130 | 11.43430 | 1.036 | 1.028--1.039 |

![Cold hub](figures/cold_hub_comparison.png)

Engineering Hub001 (left) and optimized ColdHub (right), shown with the same projections. The full aluminum
hub retains its long bore and side openings (top). The upstream head detail is clipped at world z = 2,945 mm
to expose the drilled features (bottom). Nanometre surface differences are below the figure resolution.

data/magnets_cold_hub and magnets_cold_hub_archive.zip retain the original mesh analysis, seam repair,
triangle and topology metrics, collapse history, bidirectional surface samples, all nine construction logs,
semantic comparisons, dense overlap fixtures, repeated timings, matched primaries, raw logs, and the fixed
executable hash. The archive includes original exports, final geometry and meshes, catalogs, builder,
benchmark, validation code, and figure renderer. The executable is not redistributed. Earlier study archives
remain unchanged.

## 36. Bore-tube profile preservation audit

Upcoming in GEMC2 6.2 and CLAS12 GEMC Systems 0.4, CenterTube becomes BoreCenterTube in all three
configurations and both owning repositories. BoreShield and WarmBoreTube retain their names. Every original
profile and hole is retained, as requested after reviewing the simplification options. All three active STLs
remain byte-identical to their engineering exports. Materials, bounds, volumes, passive placements, and the
exact 180-degree rotation are unchanged.

These tubes are already one closed, consistently oriented manifold component of genus one each, with zero
boundary edges, degenerate triangles, or detected intersecting faces. Their vertices all lie on the inner and
outer end rims. Each ring has strictly positive turns at every corner, so removing a corner changes its
polygonal profile. For a closed triangulated genus-one surface, Euler's relation and twice-edge triangle
incidence give F = 2V. The existing meshes already attain this minimum for their required rim vertices.
Conservative simplification at the previous 0.0001 mm local-plane bound accepts no vertex collapse. Coarser
outer walls or native circular tubes would change the engineering surfaces and were not selected.

BoreShield retains 178 vertices and 356 facets; BoreCenterTube retains 203 vertices and 406 facets;
WarmBoreTube retains 184 vertices and 368 facets. The total remains 565 vertices and 1,130 facets: zero facets
removed and 0% reduction. The full magnets inventory remains 20 STL sources, 66,960 unique facets, and 39 CAD
placements. GEMC2 uses 20 CAD sources and 19 native copy rows per run.

All nine zero-event construction checks pass: GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD for runs 11, 3029,
and 4763. The semantic comparison matches all three native solenoid configurations and all three 39-row CAD
banks. The before/after database checks match all 117 GEMC3 CAD rows and all 60 GEMC2 CAD rows after
normalizing the renamed volume and mesh path; the 57 GEMC2 copy rows are unchanged. All four active mesh trees
and all three catalog trees agree. Identical mesh bytes and physical placement rows establish unchanged
surfaces and clearances; existing assembly overlap warnings remain. No new dense sampling campaign is needed
to infer geometric identity.

No new loading or particle-transport benchmark was run for this unchanged geometry. This step establishes no
simulation speedup; a name-only change and zero facet reduction provide no geometric basis for claiming a
gain. There is no new measured before/after timing ratio, and results from earlier optimization studies are
not attributed to these tubes.

data/magnets_bore_tubes and magnets_bore_tubes_archive.zip retain mesh hashes, rim-corner and topology
metrics, database identity checks, the nine construction fixtures and logs, semantic comparisons, original and
final STLs, catalogs, and the audit program. The archive also retains the conservative simplification probe
and its empty collapse histories. The validation executable hash is recorded; executables are not
redistributed. Earlier study archives remain unchanged.

## 37. Consolidating DC and magnets geometry banks

The October 23 consolidation retires the separate dc_copies and magnets_copies geometry banks in GEMC2. The
ten DC copies are published with native dc; the 19 magnet copies join the renamed native magnets bank. Only
the former solenoid system/bank is renamed: the physical copper polycone remains named solenoid. All volume
names, mesh paths, positions, rotations, materials, and copy sources remain. GEMC2 keeps two source STLs in
dc_cad and 20 in magnets_cad because its native and CAD loaders are distinct factories. Updated standalone and
combined cards no longer load the retired copy banks.

GEMC3 now loads dc and magnets as single SQLite systems. Each contains its native solids, CAD sources, and
copy rows. Keeping sources with their copies is required by the current within-system copy dependency lookup;
the SQLite factory already supports CAD solids. Native DC and its 12 CAD placements total 66 rows, or 72 for
DDVCS. Magnets has 40 rows: one solenoid, 20 CAD sources, and 19 copies. The old dc_cad and magnets_cad
companion rows are removed when regenerating GEMC3 databases.

DC survey run keys 3029 and 4763 reuse the unchanged default chambers at run 11, now published alongside their
CAD sources and copies. This retains the complete DC detector under GEMC3's exact-run selection. The custom
DDVCS bank retains its six extra shields at run 10000001. GEMC2 continues to inherit its unchanged native DC
bank from run 11 and publishes the ten copies in both default and DDVCS TEXT geometry. Magnet survey shifts
retain runs 11, 3029, and 4763, with default SQLite variation keys and named ASCII configurations.

The previous GEMC2 DC copy bank contained two rows for each of its ten named placements. The new generators
publish each copy once, adjacent to the native rows for the same configuration. This ordering also avoids the
Perl authoring API's whole-bank deletion when switching back to a previously written detector/variation.
Repeated generation reproduces the GEMC2 TEXT bytes and database rows; regenerating GEMC3 over old databases
matches fresh databases and removes obsolete system keys.

The semantic comparator now checks the merged native/copy rows against GEMC2 native tables and independently
compares all mesh-source and copy placements with the GXML catalogs. All four DC configurations match 64
native/copy rows, or 70 for DDVCS, two material rows, and 12 CAD placements. Each of the three magnets
configurations matches 20 native/copy rows, one material row, and 39 CAD placements. The added local magnets
tungsten-alloy definition matches the existing beamline material and makes the native/copy bank
self-contained.

Twenty zero-event construction checks pass without Geant4 exceptions, using GEMC3 with Geant4 11.4.3 and GEMC2
with Geant4 10.7.4. These include GEMC3, GEMC2 SQLite/CAD, and GEMC2 TEXT/CAD for both detectors at runs 11,
3029, and 4763, plus GEMC3 DC DDVCS and GEMC2 DC DDVCS TEXT/CAD. GEMC3 fixtures disable readout and require 67
constructed volumes including the world for DC, 73 for DDVCS, and 41 for magnets. GEMC2 copy dependencies
resolve against the unchanged CAD sources. These checks validate construction and ownership; no new dense
overlap, particle-transport, or detector-response study is performed.

All stored STL hashes remain identical. DC retains two source meshes with 1,026 unique facets; magnets retains
20 with 66,960 unique facets. No facets are removed by this consolidation, and no new simulation speedup is
established. Effective GEMC2 native geometry records match the earlier solenoid/copy/DC banks after
normalizing system ownership and duplicate rows. Every GEMC2 CAD source row and all unrelated native geometry
rows remain unchanged. Existing assembly contacts and mesh limitations documented in the earlier studies still
apply.

data/detector_banks and detector_banks_archive.zip retain the before/after bank checks, mesh inventory and
hashes, native/material/CAD comparisons, repeated-generation evidence, twenty construction fixtures and logs,
original database and TEXT references, and updated authoring and validation scripts. The earlier study
archives retain their historical bank names and remain unchanged. Executables are identified by hash and are
not redistributed.

## 38. Conclusions

1. For LTCC, against the complete original hardware, the optimized CAD bundle contains 93.9% fewer triangles
and 93.9% fewer bytes. CAD-only loading CPU time decreases by 92.6%. This is direct evidence that the
simplified files reduce loading work.

2. Complete LTCC initialization CPU time falls by 63.5% and startup peak memory falls by 56.8%. These gains
include both optimized files and the simplified native hierarchy.

3. Nonoptical electron transport is 1.29 times faster; hadron workloads take 1.35–1.53 times as much CPU time.
The separate cone-only measurements quantify the isolated Winston-cone substitution.

4. Full-port optical electron transport requires 1.73 times as much median CPU time in this benchmark. The
increased CPU use may reflect more complete transport after geometry defects are removed: the original model
repeatedly requires corrective navigation pushes, while optimized diagnostic samples contain more tracks and
steps. Lower original CPU time is therefore not sufficient evidence of faster correct transport. Revised
materials and containment also contribute, so the separate causes remain unresolved.

5. The optimized meshes remove 857 exact zero-area triangles and eliminate the 1,714 invalid/rejected-facet
warnings per original import. Navigation reports across the tested workloads fall from 9,546 to 1. Overlap and
containment reports remain, so these gains do not establish overlap-free geometry.

6. Ported TEXT and SQLite geometries agree for all six run-dependent configurations. Warning counts are reported
for the tested construction sample and transport workloads; they do not establish that the complete CLAS12
geometry is free of overlaps. Detector-response, material-budget, magnetic-field, and full-experiment
comparisons remain outside this study.

7. The separate beamline apex pair contains 45.4% fewer triangles while preserving topology, sharp hub
features, materials, and placements, with sampled shape differences below 0.05 mm. Its median loading wall
time falls by 15.7% and startup peak memory by 17.4%. Transport wall time improves by 1.77--2.01 times in
the first, smaller matched-primary sample. These gains describe the isolated GEMC3 pair and do not establish
full-experiment performance or detector-response equivalence.

8. The downstream tube pair is reduced by 3.75% in triangles, and Segment 1 is closed by registering and
bridging its missing annular joins while retaining the bore. Import surface-hole warnings are removed, but
overlaps and navigation warnings remain. The measured transport ratios describe this limited workload and do
not establish response equivalence or faster correct transport.

9. The already-coarse adapter and torus exit-shield group permits only a 0.434% triangle reduction with
protected casing mating faces. The adapter is renamed consistently, and the lead fill is retained exactly.
Its repeated benchmark does not establish substantial performance gains; shape preservation takes priority
over a larger triangle reduction.

10. The FT adjuster trio is replaced by one 48-triangle closed prism, reducing triangles by 98.74% while
matching the estimated sealed reference union volume within 0.00003%. The material and common placement are
retained, and internal overlaps disappear in the isolated check. The reference mass remains approximate
because two original shells are open; deliberate material redistribution prevents a claim of
detector-response equivalence.

11. The renamed FT inner shield and flange contains 36.14% fewer triangles with retained bounds, alloy material,
placement, two closed components, and mounting/bore topology. Its small enclosed pocket is unchanged,
sampled surface differences remain below 0.05 mm, and total signed volume changes by about -0.000044%. The
isolated benchmark quantifies loading, transport, and diagnostics without establishing full-experiment
response equivalence.

12. Nine renamed FT inner-shield bolts use smooth solid shafts and round heads, reducing triangles by 89.38%
while retaining each copper volume within 0.0001%. Shortened tips leave 0.15 mm gaps at the blind-hole ends;
independent collision, containment, and 10,000-point Geant4 checks find no shield interference. Electron,
pion, and neutron transport timings improve in this isolated sample, while proton tracking is essentially
unchanged. These results do not establish full-experiment speedup or response equivalence.

13. The renamed FT outer flange closes twelve bolt tunnels and reduces triangles by 60.79% while retaining the
central opening, engineering rim coordinates, bounds, and placement. The authorized hole closure adds
8.296635% stainless-steel volume. Repeated tracking timings and residual assembly overlaps are recorded
separately; added material prevents attributing timing differences solely to fewer triangles or inferring
response equivalence.

The separate control at fixed material volume gives median tracking speedups of 1.073, 1.016, 1.034, and
1.013 for electrons, protons, positive pions, and neutrons, with the simplified mesh faster in every seed
pair of this larger sample.

14. The renamed FT outer mount repairs four triangular surface gaps and reduces triangles by 11.44%, retaining
its existing openings and placement. Protected radial relief removes about 0.24924% material against the
sealed reference and provides at least 0.03597 mm radial separation from the flange in their common axial
interval. Surface checks and the 10,000-point assembly test find no joint overlap, resolving the earlier
flange/mount interference. Repeated tracking results show modest electron, proton, and pion gains with
slower neutron tracking; unrelated full-beamline diagnostics remain.

15. The final downstream FT inner shield has smooth flange faces with every bolt recess filled, while retaining
both longitudinal grooves and the central passage. It contains 6,500 triangles, 85.27% fewer than the raw
input and 51.85% fewer than the first revision. Recess closure adds 0.436019% tungsten volume relative to
the prior closed mesh. Upgrade and smooth-reference tracking comparisons are reported separately with clean
isolated transport; the subsequent Moller-cone revision resolves the shield/cone interference.

16. The renamed Moller cone fills its surface openings, retains its beam passage and outer bounds, and reduces
triangles by 68.32%. A widened protected counterbore removes about 0.168806% tungsten relative to the
hole-filled reference and provides at least 0.187891 mm radial shield clearance. The cone/shield assembly
passes the 10,000-point overlap check. Raw-input timing includes solid and navigation warnings; the clean
clearance-reference control separately measures tessellation gains at effectively unchanged material volume.

17. Local relief of both Segment 1 sockets resolves the remaining downstream adapter and tube contacts without
changing placements or neighboring meshes. Segment 1 has 5,096 triangles, 0.604764% less steel than its
previous closed mesh, and at least 0.1 mm socket-face clearance. The three-part high-resolution overlap test
and full default beamline construction pass without exceptions. Separate repeated tracking results include
the repair and material change.

18. The beamline runtime database now selects every configuration by run number under `default`.
Run 16000 loads all 32 geometry volumes, and all 17 configured runs pass construction with unchanged
physical geometry. This selection fix has no independently measured tracking-speed gain.

19. The renamed Moller cone tip has 63.58% fewer triangles with retained topology, sharp faces,
bounds, and a -0.000486% material-volume change. Isolated tracking is 1.659, 1.133, 1.177, and 1.159
times faster for electrons, protons, positive pions, and neutrons in this sample. Its pre-existing main-cone
overlap remains in the four affected complete configurations and is reported separately.

20. The renamed FT flange retains its opening, flat faces, bounds, and topology with 540 triangles,
2.17% fewer than the already-coarse original. Steel volume changes by -0.000109%, and sampled surface
differences remain below 0.05 mm. Median tracking ratios remain within 0.18% of one, providing no
meaningful speed-gain evidence. Existing neighboring assembly defects remain and are reported separately.

21. The renamed inner Moller-cone extension restores its missing radial-port wall and reduces triangles by
30.77% while retaining its passages, bounds, and protected faces. Decimation changes the repaired reference
volume by +0.000009303%, with sampled deviations below 0.016 mm. Repaired-reference tracking ratios are 1.261,
1.086, 1.144, 1.095 for electrons, protons, positive pions, and neutrons. The original is open and produces
navigation warnings; those raw timings are reported separately. Existing assembly overlaps remain.

22. The moller-cone extension lead fill retains its mating surface and openings with 24.49% fewer triangles.
Median isolated tracking ratios are 1.0826, 1.0795, 1.1226, 1.0882 for electrons, protons, positive pions, and
neutrons. Every paired measurement improves in this sample. Existing assembly overlaps remain.
23. The moller-cone extension lead case retains its mating surface and openings with 42.40% fewer triangles.
Median isolated tracking ratios are 1.0529, 1.0377, 1.0098, 1.0198 for electrons, protons, positive pions, and
neutrons. Some paired ranges include one; those particle samples do not establish a consistent gain. Existing
assembly overlaps remain.

24. The renamed Moller-cone extension tungsten add-on restores its missing radial-port wall and reduces
triangles by 56.80% while retaining its passages, bounds, and protected faces. Decimation changes the repaired
reference volume by -0.0000046193%, with sampled deviations below 0.013 mm. Repaired-reference tracking ratios
are 1.647, 1.548, 1.642, 1.535 for electrons, protons, positive pions, and neutrons. The original is open and
produces navigation warnings; those raw timings are reported separately. Existing assembly overlaps remain.

25. Local FT/cone joint reliefs clear all eight checked interfaces while retaining the shield, flange, and
cone tip. Five meshes lose 0.119--1.209% material by volume. All affected complete configurations construct
without exceptions, and final corrected tracking runs are clean. Isolated tracking ratios 0.8568, 0.8541,
0.8465, 0.8920 describe the eight-part clearance revision; they are not pure decimation gains.

26. The three HTCC cones have 49.20% fewer triangles, and the entry cone's 144 boundary edges are closed. All
six TEXT/CAD and SQLite/CAD initialization checks and the three native/CAD database comparisons pass. The
Moller cone retains 24 non-manifold edges, and the cured entry cone introduces an observed contact of
approximately 0.053 mm with the entry window. These unresolved defects preclude a claim of complete geometry
validation; no performance or detector-response gain has been measured for this transfer.

27. The magnets cleanup removes ten redundant shielding placements from each configuration, reducing
its inventory by 16,710 triangles (11.22%) while retaining the beamline shielding. Repeated timing
results and residual geometry warnings are reported separately; all three runs pass both-engine checks.

28. The downstream shielding plate and vacuum jacket retain their original names and separate placements,
with fourteen fastener features filled and 71.79% fewer triangles. The signed steel volume increases
by 0.566581%; repeated tracking, clean isolated construction, and remaining assembly limits are reported
separately. All three runs pass both-engine geometry checks.

29. The separate upstream plate and jacket retain their original names, main openings, rounded outer
features, and gap with 64.47% fewer triangles. Both-engine checks pass all three runs; measured tracking
and signed material-volume changes are reported separately from remaining assembly limits.

30. Six DC region-1 back membranes move out of magnets and share one twenty-triangle solid with five copies:
83.33% fewer unique facets. Integer angles pass the dense overlap comparison; startup, tracking,
material-volume changes, and the accepted submillimetre displacement are recorded separately.

31. Six aluminum region-1 support assemblies move from magnets into DC and share one unchanged 1,006-triangle STL.
Unique facets fall by 83.33%, while both pieces and all openings remain. Integer angles pass the dense overlap
comparison; repeated loading, memory, tracking, and the accepted millimetre-scale placement changes are
reported separately.

32. Vacuum jacket sharing retains all holes and twelve placements, using six sources and six copies. Unique facets
fall by 48.86%; two distinct families and four original exports are retained. The dense assembly check finds
no new overlap pairs; isolated startup is 1.175 times faster. Particle-specific tracking and the small
steel-volume change are reported separately.

33. Six torus coils share one unchanged STL with every opening retained, reducing unique facets by 83.33%. The
dense comparison adds no sampled overlap pairs; the isolated startup before/after ratio in serial mode is
1.401. Particle-specific tracking and the small copper-volume change are reported separately.
Duplicate-isotope failures in both execution modes and both geometry versions remain unresolved; tracking
statistics are conditional on completed pairs.

34. Six hub covers retain every hole and share two unchanged source meshes, reducing unique facets from 348 to 162
(53.45%). A naming-controlled dense comparison adds no sampled overlap pairs. The isolated serial startup
before/after ratio is 1.000; particle-specific timing and paired ranges are reported separately without a
full-detector claim.

35. The seven hub shields comprise five matching middle pieces and two different ends. Three source meshes
preserve every hole and reduce unique facets by 61.55%. Nanometre axial normalization avoids new sampled
overlap pairs; maximum vertex change is 0.000146485 mm. The isolated serial startup before/after ratio is
1.402; tracking ranges and completion limitations are reported separately.

36. ColdHub retains every opening while repairing the export seam, winding, and degenerate junctions. The closed
genus-34 mesh has no intersecting faces; unique facets fall from 12,600 to 12,548 (0.41%). Surface samples
differ by less than 0.000036 mm, and the dense assembly adds no sampled contact pairs. The serial startup
ratio is 1.161; transport results and completion limitations are reported separately.

37. The three bore tubes already require all 1,130 facets for their retained rim profiles. CenterTube becomes
BoreCenterTube; all meshes, holes, physical placements, and clearances remain unchanged. The facet reduction
is 0%, and no simulation speedup is established.

38. The HTCC Moller repair restores its engineering conical section and resolves the tessellated-solid orientation
warning in both engines. Its 6,902 facets form one closed genus-one manifold with unchanged bounds and an open
bore. The nine construction checks report no solid warnings; the separate entry-cone/window contact remains.
No speedup is claimed.

39. DC and magnets copies now belong to their main detector banks. The physical solenoid name, every STL hash, and
all existing placements remain. Twenty geometry-only construction checks and native/CAD comparisons pass;
repeated generation does not duplicate copies. This consolidation removes no facets and establishes no
speedup.

## 39. Reproducibility and references

The companion data archive retains metadata and per-run JSON results for each workload, all raw logs and time
reports, the geometry validation summary, and matched primary-input hashes. The repository benchmark script runs
offline with the local CCDB database. The retained metadata provides the exact executable hash; use that binary
and the original revision for exact reproduction. Timing results are specific to this machine and workload.

The separate downstream and adapter/exit-shield archives retain the corresponding fixtures, matched
primaries, raw logs, time reports, mesh checks, executable hashes, and reproduction scripts. Each beamline
workload has its own archive and data directory; the unchanged lead-fill geometry is included in both exit-
group fixtures. These archives do not redistribute the executables.

[1] GEMC clas12Tags, main revision ea3625f: original LTCC geometry and CAD data; cadTempRemoved hardware
restored for this comparison using the legacy ltcc_frame.pl placements.

[2] GEMC clas12Tags, meson revision 4c7c6af, “new optimized STL for ltcc and new mother volume for each ltcc
sector”: optimized meshes, CAD placements, mother geometry, and effective nose material.

[3] M. Ungaro et al., “The CLAS12 Geant4 simulation”, Nuclear Instruments and Methods A 959 (2020) 163422.
Background on the CLAS12 GEMC simulation.

[4] R. De Vita and M. Ungaro, “CLAS12-note 2017-017: Importing CLAS12 CAD Models of Target and Beamline”.
Background on CAD geometry import.

[5] Companion datasets, LTCC and beamline CAD optimization studies, October 1, October 12--16, and October 19, 2026:
measured configurations, warnings, timing, memory, hashes, and validation results; the LTCC and sixteen
beamline study archives and supplemental smooth-flange, downstream-joint, and FT/cone clearance revision archives accompany this note.

The separate HTCC archive retains the October 19 raw and cured cones, the six zero-event initialization
fixtures, three run-dependent native/CAD row snapshots, the full default overlap log, and the matched
raw/cured entry-window fixtures. Topology and STL hashes identify the exact transferred meshes. These checks
include no timing benchmark or response-equivalence study. The entry-window overlap and non-manifold
Moller-cone edges remain unresolved. Earlier archives are unchanged.
