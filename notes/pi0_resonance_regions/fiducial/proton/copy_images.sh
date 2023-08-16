#!/bin/zsh

local_dir=pfid

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
plane-SC_intsector-1
plane-DC1_intsector-5
plane-DC2_intsector-5
)

imgs_slices=(
slice-05_sector-1_plane-DC1
slice-06_sector-1_plane-DC1
slice-07_sector-1_plane-DC1
slice-08_sector-1_plane-DC1
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
