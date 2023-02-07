#!/bin/zsh

local_dir=vertex

orig_dir=/opt/projects/mauriplots/$local_dir

# if on github ci, clone mauriplots and use that
if [ -n "$GITHUB_WORKSPACE" ]; then
  git clone https://github.com/MauriPlots/$local_dir
  orig_dir=`pwd`/$local_dir
fi

imgs=(
    vtx_2D_all_sector
    vtx_all_sector
)

for cc in $imgs; do
    echo $cc
    cp $orig_dir/$cc.png img
done

