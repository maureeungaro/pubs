#!/bin/zsh

orig_dir=/opt/projects/mauriplots/epid/

hostname=`hostname -s`
case "$hostname" in
	jlabl4)
    orig_dir=/userweb/ungaro/public_html/plots/epid
		;;
esac

imgs=(
  cut-01-cc-theta-match-pars_sector-1
  cut-01-cc-theta-match-compare_sector-1
  cut-02-cc-phi-match_sector-1
  cut-03-cc-time-match-compare_sector-1
  cut-04-ec-threshold_sector-1
  cut-05-sampling-f_sector-1
  cut-05-sampling-f-compare_sector-1
  cut-05-sampling-f_sector-all
  cut-06-ECU_sector-all
  cut-07-ECV_sector-all
  cut-08-ECW_sector-all
  cut-09-UVW_sector-all
  cut-10-mip_sector-1
  cut-10-mip_sector-all
  cut-11-shower-shape_sector-1
  cut-12-nphe_sector-all
  epidsummary
)

imgs_slices=(
  slice-06_cut-01-cc-theta-slice_sector-1
  slice-14_cut-01-cc-theta-slice_sector-1
  slice-03_cut-03-cc-time-match_sector-1
  slice-08_cut-03-cc-time-match_sector-1
  slice-12_cut-03-cc-time-match_sector-1
  slice-15_cut-03-cc-time-match_sector-1
  slice-04_cut-05-sampling-f_sector-1
  slice-08_cut-05-sampling-f_sector-1
)

for cc in $imgs; do
  echo $cc
  cp $orig_dir/img/$cc.png img
done

for cc in $imgs_slices; do
  echo $cc
  cp $orig_dir/img_slices/$cc.png img
done
