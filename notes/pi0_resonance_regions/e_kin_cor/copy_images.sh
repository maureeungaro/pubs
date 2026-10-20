#!/bin/zsh

local_dir=e_kin_cor

orig_dir=/opt/projects/mauriplots/$local_dir

# if we are on the docker container set orig_dir to /root
if [ -d /root ]; then
  orig_dir=/root/plots/$local_dir
  git clone https://github.com/MauriPlots/$local_dir $orig_dir
fi

imgs=(
dist-W_sector-1
dist-W_sector-4
dist-WvsPhi_sector-1
dist-WvsTheta_sector-1
dist-pi0_sector-1
dist-pi0_sector-4
dist-pi0vsPhi_sector-1
dist-eta_sector-1
dist-eta_sector-4
dist-etavsPhi_sector-1
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

