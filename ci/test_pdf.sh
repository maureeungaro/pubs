#!/usr/bin/env zsh

# Purpose:
# Make the requested pdf

# Container run:
# docker_run_image maureeungaro/base:fedora36-latex sh
# git clone https://github.com/maureeungaro/pubs       /root/pubs && cd /root/pubs
# ./ci/test_pdf.sh -d notes/pi0_resonance_regions/pid/electron
# ./ci/test_pdf.sh -d notes/pi0_resonance_regions
# ./ci/test_pdf.sh -d papers/pi0_delta
# ./ci/test_pdf.sh -d proceedings/chep2023

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
	echo Test Type dir: "$doc_to_make" not existing
	Help
	exit 3
}

cdir=$(pwd)

echo "Current dir $cdir content:"
ls -lrt

[[ -v doc_to_make ]] && echo PDFLatex compiling "$doc_to_make" || DocDirNotExisting
cd "$doc_to_make" || exit


# if doc_to_make is pi0_resonance_regions_note, makeNote
exit_code=0
case $doc_to_make in
    notes/pi0_resonance_regions)
        ./makeNote
        exit_code=$?
        ;;
    *)
        scons -c
        scons
        exit_code=$?
        ;;
esac

if [ $exit_code -ne 0 ]; then
	echo Making "$doc_to_make" pdf failed
	cat *.log
	exit 1
fi

echo
echo "Current dir $cdir content:"
ls -lrt
echo
echo "Copying pdf(s) to $cdir/pdfs"
cp *.pdf "$cdir"/pdfs/
if [ $? -ne 0 ]; then
	echo "Copying pdf(s) failed"
	exit 1
fi
scons -c

# this was done in the ci, but it would produce a new pdf version for each commit
#
#git config --global --add safe.directory /__w/pubs/pubs
#
## refresh the pdfs that may have been changed by other actions
#git pull
