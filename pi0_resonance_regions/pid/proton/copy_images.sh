#!/bin/zsh

mkdir -p img

orig_dir=/opt/projects/mauriplots/ppid/
orig_dir=/opt/projects/analysis/pid/proton # remove after copying to mauriplots

exit 0

ppid_imgs=()

ppid_imgs_slices=()

for cc in $ppid_imgs; do
    echo $cc
    cp $orig_dir/img/$cc.png img
done

for cc in $ppid_imgs_slices; do
    echo $cc
    cp $orig_dir/img_slices/$cc.png img
done
