#!/bin/zsh

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

plots_r=(epid ppid)

for r in $plots_r; do
  echo " > updating $r"
  cd $plots/$r
  git pull
  cd -
done

echo " > updating pubs"
cd $pubs
git pull

#echo " > making pi0_resonance_regions"
#cd pi0_resonance_regions
#./makeNote
#mv pi0.pdf $docs
#cd -

