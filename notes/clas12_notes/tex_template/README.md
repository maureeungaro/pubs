# CLAS12 technical note TeX template

This directory contains the TeX sources for the CLAS12 technical note template. Meson builds the PDF with
`latexmk`, which runs `pdflatex` as many times as needed to resolve the table of contents and references.

## House style

The template reproduces the style of the Pages template
`templates/CLAS12_technical_note_template.pages`:

| Element            | Font                     | Size    | Alignment | LaTeX                                  |
|--------------------|--------------------------|---------|-----------|----------------------------------------|
| Title              | Helvetica bold           | 19 pt   | centred   | `\notetitle{...}`                      |
| Author             | Helvetica bold           | 14 pt   | centred   | `\noteauthor{...}`                     |
| Affiliation        | Times New Roman italic   | 12 pt   | centred   | `\noteaffiliation{...}`                |
| Note number / date | Times New Roman          | 11 pt   | centred   | `\notenumberdate{...}`                 |
| "Abstract" + body  | Helvetica bold / Times   | 14 / 12 | centred   | `noteabstract` environment             |
| Section heading    | Helvetica bold           | 14 pt   | left      | `\section{...}`                        |
| Sub-heading        | Helvetica bold           | 12.5 pt | left      | `\subsection{...}`                     |
| Body               | Times New Roman          | 12 pt   | ragged r. | (default)                              |
| Figure/table caption | Times New Roman italic | 10.5 pt | left, grey| `\caption{...}` (grey `0.40`)          |

Implementation (see `template.tex`): `mathptmx` (Times body + maths),
`helvet` (Helvetica headings), `courier` (monospace); `titlesec` sets the heading fonts and sizes;
`caption` styles captions as `Figure N. ...`; `ragged2e` + `parskip` give ragged-right body text with
blank-line paragraph separation; `geometry` sets US-Letter with 1-inch margins. The front-matter helper
macros (`\notetitle`, `\noteauthor`, `\noteaffiliation`, `\notenumberdate`, `noteabstract`) live in the
`template.tex` preamble.

## Structure

- `template.tex` — main file: front matter, then it inputs the preamble, the body, and the references.
- `template_preamble.tex` — everything before `\begin{document}`: document class, packages, and the
  house-style definitions (fonts, heading and caption styles, header/footer, front-matter macros). Edit the
  style here.
- `template_doc.tex` — the note body: section skeleton and standard simulation constants (authoring guide
  sections 2 and 3). Replace the bracketed `[ ... ]` guidance with content.
- `template_bib.tex` — the recurring foundational CLAS12-note references (authoring guide section 7).

## Requirements

- Meson
- Ninja
- `latexmk` and `pdflatex`

## Build

Configure a build directory once:

```shell
meson setup build
```

Build `build/template.pdf`:

```shell
meson compile -C build
```

After editing any of the TeX sources, run the compile command again.

## Install the final PDF

Build the PDF if needed and copy it to `template.pdf` in this directory:

```shell
meson install -C build
```

## Clean

Remove the build-directory PDF and LaTeX intermediate files while keeping the configured build directory. The
installed PDF beside the TeX sources is retained.

```shell
meson compile -C build --clean
```

To configure the build again after changing Meson options or build definitions, run:

```shell
meson setup --reconfigure build
```

## Create a note

From the repository's `clas12_notes` directory, pass a snake-case filename stem to the note generator:

```shell
python3 create_note.py simgrid_osg_portal
```

The generator creates `<current-year>/simgrid_osg_portal/`, copies the template into it, and renames the TeX
sources and PDF target to use `simgrid_osg_portal`.
