#!/bin/zsh

local_dir=epid

orig_dir=/opt/projects/mauriplots/$local_dir

exit 0
# if we are on the docker container set orig_dir to /root
if [ -d /root ]; then
  orig_dir=/root/plots/$local_dir
  git clone https://github.com/MauriPlots/$local_dir $orig_dir
fi

imgs=(

)

imgs_slices=(

)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
