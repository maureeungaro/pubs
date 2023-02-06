#!/bin/zsh

# TODO: RUN THE PDF MAKER ON GITHUB CI Instead

# This script is meant to be run by a cronjob on jlabl4
#
# 1. Update the repos:
#
# - mauriplots
# - pubs
#
# 2. Make the PDF and copy them to docs for:
#
# - pubs/pi0_resonance_regions

plots=/userweb/ungaro/public_html/plots
pubs=/userweb/ungaro/public_html/pubs
docs=/userweb/ungaro/public_html/docs


echo " > updating pubs"
cd $pubs
git pull

# mauriPlots repos
plots_r=(epid ppid vertex)
for r in $plots_r; do
  echo " > updating $r"
  cd $plots/$r
  git pull
  cd -
done

echo " > making pi0_resonance_regions"
cd pi0_resonance_regions
./makeNote
mv pi0.pdf $docs


# compiling individual chapters and copy them to docs
# for s in (pid/electron pid/proton vertex); do
#   echo " > making $s"
#   cd $s
#   scons
#   mv *.pdf $docs
#   cd -
# done