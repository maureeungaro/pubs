#!/bin/zsh

local_dir=vertex

orig_dir=/opt/projects/mauriplots/$local_dir

# if we are on the docker container set orig_dir to /root
if [ -d /root ]; then
  orig_dir=/root/plots/$local_dir
fi

imgs=(
    vtx_2D_all_sector
    vtx_all_sector
)

for cc in $imgs; do
    echo $cc
    cp $orig_dir/$cc.png img
done

