project('clas12-technical-note-template')

note_name = 'simgrid_osg_portal'
latexmk = find_program('latexmk')
latex_output_dir = meson.current_build_dir()
tex_sources = files(
  note_name + '.tex',
  note_name + '_preamble.tex',
  note_name + '_doc.tex',
  note_name + '_bib.tex',
)

# One file per chapter, inputted through <note>_doc.tex.
chapter_sources = files(
  'chapters/01.tex', 'chapters/02.tex', 'chapters/03.tex', 'chapters/04.tex',
  'chapters/05.tex', 'chapters/06.tex', 'chapters/07.tex', 'chapters/08.tex',
  'chapters/09.tex', 'chapters/10.tex', 'chapters/11.tex', 'chapters/12.tex',
  'chapters/13.tex', 'chapters/14.tex', 'chapters/15.tex', 'chapters/16.tex',
  'chapters/17.tex', 'chapters/18.tex', 'chapters/19_appendices.tex',
)

# Workflow figures (built from the SVGs under figures/).
figure_sources = files(
  'figures/fig1_architecture.pdf', 'figures/fig2_state_machine.pdf',
  'figures/fig3_file_chain.pdf', 'figures/fig4_two_priorities.pdf',
)

custom_target(
  note_name + '.pdf',
  input: [tex_sources, chapter_sources, figure_sources],
  output: [
    note_name + '.pdf',
    note_name + '.aux',
    note_name + '.fdb_latexmk',
    note_name + '.fls',
    note_name + '.log',
    note_name + '.out',
    note_name + '.toc',
  ],
  command: [
    latexmk,
    '-cd',
    '-pdf',
    '-interaction=nonstopmode',
    '-halt-on-error',
    '-outdir=' + latex_output_dir,
    '@INPUT0@',
  ],
  build_by_default: true,
  install: true,
  install_dir: [
    meson.current_source_dir(),
    false,
    false,
    false,
    false,
    false,
    false,
  ],
)
