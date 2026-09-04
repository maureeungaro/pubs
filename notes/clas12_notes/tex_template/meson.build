project('clas12-technical-note-template')

note_name = 'template'
latexmk = find_program('latexmk')
latex_output_dir = meson.current_build_dir()
tex_sources = files(
  note_name + '.tex',
  note_name + '_preamble.tex',
  note_name + '_doc.tex',
  note_name + '_bib.tex',
)

custom_target(
  note_name + '.pdf',
  input: tex_sources,
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
