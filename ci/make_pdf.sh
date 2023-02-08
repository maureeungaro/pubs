#!/usr/bin/env zsh

# Purpose:
# Make the requested pdf

# Container run:
# docker run -it --rm maureeungaro/base:fedora36-latex sh
# git clone https://github.com/maureeungaro/pubs       /root/pubs && cd /root/pubs
# ./ci/make_pdf.sh -d pi0_resonance_regions/pid/electron
# ./ci/make_pdf.sh -d pi0_resonance_regions


Help()
{
	# Display Help
	echo
	echo "Syntax: tests.sh [-h|d]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-d <Doc>: make pdf for <Doc>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

while getopts ":hd:" option; do
   case $option in
      h)
         Help
         exit
         ;;
      d)
         doc_to_make=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit 1
         ;;
   esac
done


DocDirNotExisting() {
	echo Test Type dir: $example/$doc_to_make not existing
	Help
	exit 3
}

cdir=$(pwd)

[[ -v doc_to_make ]] && echo Making $doc_to_make || DocDirNotExisting
cd $doc_to_make


# if doc_to_make is pi0_resonance_regions, run pi0_resonance_regions/makeNote
case $doc_to_make in
    pi0_resonance_regions)
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
fi

pwd
ls -lrt

mv *.pdf $cdir/pdfs

if [ $? -ne 0 ]; then
	echo Moving pdf failed
	exit 1
fi

scons -c

git config --global --add safe.directory /__w/pubs/pubs