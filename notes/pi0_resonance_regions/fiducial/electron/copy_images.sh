#!/bin/zsh

local_dir=efid

orig_dir=/opt/projects/mauriplots/$local_dir

# if we are on the docker container set orig_dir to /root
if [ -d /root ]; then
  orig_dir=/root/plots/$local_dir
  git clone https://github.com/MauriPlots/$local_dir $orig_dir
fi

imgs=(
plane-DC1_intsector-1
plane-DC2_intsector-1
plane-DC3_intsector-1
plane-DC1_intsector-5
plane-DC2_intsector-5
plane-SC_intsector-1
phiTheta-after_sector-5
phiTheta-before_sector-5
PnPvsTmom-3.8_sector-5_plot-phiVsTheta
)

imgs_slices=(
slice-05_sector-1_plane-DC3
slice-06_sector-1_plane-DC3
slice-07_sector-1_plane-DC3
slice-08_sector-1_plane-DC3
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
