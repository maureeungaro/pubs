#!/bin/zsh

mkdir -p img

orig_dir=/opt/projects/mauriplots/epid/
orig_dir=/opt/projects/analysis/pid/electron # remove after copying to mauriplots



cc_match_files=(cut-01-cc-theta-match-pars_sector-1
                cut-01-cc-theta-match-cuts_sector-1
                cut-02-cc-phi-match_sector-1)

cc_match_files_slices=(slice-06_cut-01-cc-theta-slice_sector-1
                       slice-14_cut-01-cc-theta-slice_sector-1
                       slice-03_cut-03-cc-time-match_sector-1
                       slice-08_cut-03-cc-time-match_sector-1
                       slice-12_cut-03-cc-time-match_sector-1
                       slice-15_cut-03-cc-time-match_sector-1)

for cc in $cc_match_files; do
    echo $cc
    cp $orig_dir/img/$cc.png img
done

for cc in $cc_match_files_slices; do
    echo $cc
    cp $orig_dir/img_slices/$cc.png img
done
