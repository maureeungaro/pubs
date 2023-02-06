#!/bin/zsh

mkdir -p img

orig_dir=/opt/projects/mauriplots/vertex/

imgs=(
    vtx_2D_all_sector
    vtx_all_sector
)


for cc in $imgs; do
    echo $cc
    cp $orig_dir/$cc.png img
done

