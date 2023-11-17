#!/bin/zsh

# */30  *  *  *  * flock -n $HOME/.plots.lock $HOME/update_mauriplots_jlabl4.zsh >& $HOME/logs/plots.log   >/dev/null 2>&1
# scp update_mauriplots_jlabl4.zsh ftp:

# This script is meant to be run by a cronjob on jlabl4 to update on /userweb/ungaro/public_html:
# - mauriPlots
# - slides
# - pubs

basedir=/userweb/ungaro/public_html

function pull_or_clone() {
  project_name=$1
  project_repo=$2
  cd $basedir
  # optional reset argument will remove and re-clone the repo
  if [[ $# -eq 3 && $3 == "reset" ]]; then
    rm -rf $project_name ; mkdir -p 3$project_name ; cd $project_name/..
    git clone -s $project_repo
    echo "$project_name reset and cloned"
  else
    if [[ -d $project_name ]]; then
      cd $project_name
      git pull
      echo "$project_name pulled"
    else
      cd $basedir
      git clone $project_repo
      echo "$project_name cloned"
    fi
  fi
}

# the plots repos are reset every time
# git pull is enough, removing and re-cloning repos
repo=https://github.com/mauriPlots
plots_r=(pi0_delta_distributions epid ppid vertex efid pfid e_kin_cor)
for r in $plots_r; do
  pull_or_clone plots/$r $repo/$r reset
done

repo=https://github.com/maureeungaro/slides
pull_or_clone slides $repo

repo=https://github.com/maureeungaro/pubs
pull_or_clone pubs $repo
