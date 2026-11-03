project('candidacy-thesis')

thesis_name = 'candidacy'
latexmk = find_program('latexmk')
find_program('latex')
find_program('dvips')
find_program('ps2pdf')
latex_output_dir = meson.current_build_dir()

tex_sources = files(
  thesis_name + '.tex',
  'fonts.tex',
  'macros.tex',
  'cover.tex',
  'intro.tex',
  'overview.tex',
  'setup.tex',
  'status.tex',
  'future.tex',
  'biblio.tex',
)
figure_sources = files(
  'img/cross.eps',
  'img/kine.eps',
  'img/ratios.ps',
  'img/clas.eps',
  'img/Ec1.ps',
  'img/closer.ps',
  'img/result_pass1.ps',
  'img/fidu.ps',
  'img/bethe.eps',
  'img/bethecut.eps',
  'img/Allmm.eps',
  'img/radiative.eps',
  'img/electron_pseudo.eps',
  'img/proton_pseudo.eps',
  'img/acce.eps',
  'img/cross_fit.eps',
)

custom_target(
  thesis_name + '.pdf',
  input: [tex_sources, figure_sources],
  output: [
    thesis_name + '.pdf',
    thesis_name + '.aux',
    thesis_name + '.dvi',
    thesis_name + '.fdb_latexmk',
    thesis_name + '.fls',
    thesis_name + '.log',
    thesis_name + '.ps',
  ],
  command: [
    latexmk,
    '-cd',
    # Preserve the legacy EPS/PostScript figures and their bounding boxes.
    '-pdfps',
    '-interaction=nonstopmode',
    '-halt-on-error',
    '-outdir=' + latex_output_dir,
    '@INPUT0@',
  ],
  build_by_default: true,
  install: true,
  install_dir: [meson.current_source_dir(), false, false, false, false, false, false],
)
