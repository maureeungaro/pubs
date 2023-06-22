#!/bin/zsh

# */30  *  *  *  * flock -n $HOME/.plots.lock $HOME/update_mauriplots_jlabl4.zsh >& $HOME/logs/plots.log   >/dev/null 2>&1
# scp update_mauriplots_jlabl4.zsh ftp:

# This script is meant to be run by a cronjob on jlabl4 to update on /userweb/ungaro/public_html:
# - mauriPlots
# - slides
# - pubs

plots=/userweb/ungaro/public_html/plots
plotsr=https://github.com/mauriPlots

# the repos are reset every time
# so git pull is enough
plots_r=(epid ppid vertex efid)
cd $plots
for r in $plots_r; do
  rm -rf $r
  git clone $plotsr/$r
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

pubs=/userweb/ungaro/public_html/pubs
pubsr=https://github.com/maureeungaro/pubs
if [[ -d $pubs ]]; then
  cd $pubs
  git pull
  echo pubs pulled
else
  cd /userweb/ungaro/public_html/
  git clone $pubsr
  echo pubs cloned
fi


