#!/usr/bin/env zsh

# reads the yaml file to extract the PDF to make
yaml_file=.github/workflows/build.yaml
dirs_to_test=$(grep -A300 "doc:" $yaml_file | grep "          - " | awk '{print $2}')
cdir=$(pwd)

DocDirNotExisting() {
	echo Test Type dir: $example/$doc_to_make not existing
	Help
	exit 3
}

for doc_to_make in $=dirs_to_test
do
  [[ -v doc_to_make ]] && echo Making $doc_to_make || DocDirNotExisting
  cd $cdir/$doc_to_make
  # if doc_to_make is pi0_resonance_regions_note, makeNote
  case $doc_to_make in
    notes/pi0_resonance_regions)
      ./makeNote
      ;;
    *)
      scons -c
      scons
      ;;
  esac
  if [ $? -ne 0 ]; then
	  echo Making $doc_to_make pdf failed
	  exit 1
	else
	  mv *.pdf $cdir/pdfs/
	  scons -c
  fi
done