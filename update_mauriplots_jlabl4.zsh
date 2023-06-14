#!/bin/zsh

# */30  *  *  *  * flock -n $HOME/.plots.lock $HOME/update_mauriplots_jlabl4.zsh >& $HOME/logs/plots.log   >/dev/null 2>&1

# This script is meant to be run by a cronjob on jlabl4 to update
# the mauriPlots and the slides repos on /userweb/ungaro/public_html

plots=/userweb/ungaro/public_html/plots
plotsr=https://github.com/mauriPlots

plots_r=(epid ppid vertex efid)
cd $plots
for r in $plots_r; do
  if [[ -d $r ]]; then
    cd $r
    git pull
    echo "$r pulled"
    cd ..
  else
    echo " > updating $r"
    rm -rf $r
    git clone $plotsr/$r
    echo "$r cloned"
  fi
  echo
done

slides=/userweb/ungaro/public_html/slides
slidesr=https://github.com/maureeungaro/slides
if [[ -d $slides ]]; then
  cd $slides
  git pull
  echo slides pulled
else
  cd /userweb/ungaro/public_html/
  git clone $slidesr
  echo slides cloned
fi




