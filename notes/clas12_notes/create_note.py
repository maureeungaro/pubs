#!/usr/bin/env python3

import argparse
import re
import shutil
from datetime import date
from pathlib import Path


TEMPLATE_FILES = {
    'template.tex': '{name}.tex',
    'template_preamble.tex': '{name}_preamble.tex',
    'template_doc.tex': '{name}_doc.tex',
    'template_bib.tex': '{name}_bib.tex',
    'meson.build': 'meson.build',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Create a CLAS12 technical note from the TeX template.',
    )
    parser.add_argument(
        'name',
        help='snake-case filename stem, for example simgrid_osg_portal',
    )
    args = parser.parse_args()

    if re.fullmatch(r'[a-z0-9]+(?:_[a-z0-9]+)*', args.name) is None:
        parser.error('name must contain lowercase letters, numbers, and single underscores')

    return args


def render_template(source_name: str, text: str, note_name: str) -> str:
    if source_name == 'template.tex':
        return (
            text.replace('template_preamble', f'{note_name}_preamble')
            .replace('template_doc', f'{note_name}_doc')
            .replace('template_bib', f'{note_name}_bib')
        )
    if source_name == 'meson.build':
        return text.replace("note_name = 'template'", f"note_name = '{note_name}'")
    return text


def main() -> int:
    args = parse_args()
    repository_dir = Path(__file__).resolve().parent
    template_dir = repository_dir / 'tex_template'
    year_dir = repository_dir / str(date.today().year)
    note_dir = year_dir / args.name

    missing = [name for name in TEMPLATE_FILES if not (template_dir / name).is_file()]
    if missing:
        names = ', '.join(missing)
        raise SystemExit(f'missing template files: {names}')
    if note_dir.exists():
        raise SystemExit(f'refusing to overwrite existing path: {note_dir}')

    year_dir.mkdir(exist_ok=True)
    note_dir.mkdir()

    try:
        for source_name, destination_pattern in TEMPLATE_FILES.items():
            source = template_dir / source_name
            destination = note_dir / destination_pattern.format(name=args.name)
            text = render_template(source_name, source.read_text(), args.name)
            destination.write_text(text)

        # Copy the per-chapter body files verbatim (they carry no note name).
        chapters_src = template_dir / 'chapters'
        if chapters_src.is_dir():
            shutil.copytree(chapters_src, note_dir / 'chapters')
    except BaseException:
        shutil.rmtree(note_dir)
        raise

    print(f'Created {note_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
