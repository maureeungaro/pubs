#!/bin/zsh

local_dir=epid

orig_dir=/opt/projects/mauriplots/$local_dir

# if on github ci, clone mauriplots and use that
if [ -n "$GITHUB_WORKSPACE" ]; then
  git clone https://github.com/MauriPlots/$local_dir
  orig_dir=`pwd`/$local_dir
fi

imgs=(
  cut-01-tmp_sector-1
  cut-01-tmc_sector-1
  cut-02-pm_sector-1
  cut-03-timc_sector-1
  cut-04-thr_sector-1
  cut-05-sf_sector-1
  cut-05-sfc_sector-1
  cut-05-sf_sector-all
  cut-06-ECU_sector-all
  cut-07-ECV_sector-all
  cut-08-ECW_sector-all
  cut-09-UVW_sector-all
  cut-10-mip_sector-1
  cut-10-mip_sector-all
  cut-11-shsh_sector-1
  cut-12-nphe_sector-all
  epidsummary
)

imgs_slices=(
  slice-06_cut-01-ts_sector-1
  slice-14_cut-01-ts_sector-1
  slice-03_cut-03-tim_sector-1
  slice-08_cut-03-tim_sector-1
  slice-12_cut-03-tim_sector-1
  slice-15_cut-03-tim_sector-1
  slice-04_cut-05-sf_sector-1
  slice-08_cut-05-sf_sector-1
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
