#!/bin/zsh

*/30  *  *  *  * flock -n $HOME/.plots.lock $HOME/update_mauriplots_jlabl4.zsh >& $HOME/logs/plots.log   >/dev/null 2>&1

# This script is meant to be run by a cronjob on jlabl4 to update
# the mauriPlots repo on /userweb/ungaro/public_html

plots=/userweb/ungaro/public_html/plots
plotsr=https://github.com/mauriPlots

plots_r=(epid ppid vertex efid)
cd $plots
for r in $plots_r; do
  echo " > updating $r"
  rm -rf $r
  git clone $plotsr/$r
done

