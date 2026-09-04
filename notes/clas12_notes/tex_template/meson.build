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

# One file per chapter, inputted through <note>_doc.tex.
chapter_sources = files(
  'chapters/01.tex',
  'chapters/02.tex',
)

custom_target(
  note_name + '.pdf',
  input: [tex_sources, chapter_sources],
  output: [
    note_name + '.pdf',
    note_name + '.aux',
    note_name + '.fdb_latexmk',
    note_name + '.fls',
    note_name + '.log',
    note_name + '.out',
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
  ],
)
