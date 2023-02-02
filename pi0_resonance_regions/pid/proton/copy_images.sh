#!/bin/zsh

orig_dir=/opt/projects/mauriplots/ppid

hostname=`hostname -s`
case "$hostname" in
	jlabl4)
    orig_dir=/userweb/ungaro/public_html/plots/ppid
		;;
esac

ppid_imgs=(
  dist-dtfit_sector-1
  dist-dtfit_sector-all
  dist-massandbeta_sector-1
)

ppid_imgs_slices=(
  slice-2_sector-1
  slice-4_sector-1
)

for cc in $ppid_imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $ppid_imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
