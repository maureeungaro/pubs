#!/bin/zsh

local_dir=ppid

orig_dir=/opt/projects/mauriplots/$local_dir

# if on github ci, clone mauriplots and use that
if [ -n "$GITHUB_WORKSPACE" ]; then
  git clone https://github.com/MauriPlots/$local_dir
  orig_dir=`pwd`/$local_dir
fi

imgs=(
  dist-dtfit_sector-1
  dist-dtfit_sector-all
  dist-massandbeta_sector-1
)

imgs_slices=(
  slice-2_sector-1
  slice-4_sector-1
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
