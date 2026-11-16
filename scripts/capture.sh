#!/usr/bin/env bash
# Capture a screenshot and a GIF of a theme on a mock T3 Code page.
# Usage: scripts/capture.sh <theme.json> <idle|working> <speed> <out-prefix>
# Needs Google Chrome and ffmpeg. Do not pass --disable-gpu: CSS masks then do not render.
set -euo pipefail
theme=$1 status=$2 speed=$3 out=$4
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
python3 "$(dirname "$0")/mock_page.py" "$theme" "$status" 1 "$work/still.html"
python3 "$(dirname "$0")/mock_page.py" "$theme" "$status" "$speed" "$work/anim.html"
shot() { "$chrome" --headless=new --hide-scrollbars --user-data-dir="$work/profile" \
  --window-size=1200,720 --virtual-time-budget="$2" --screenshot="$3" "file://$work/$1" >/dev/null 2>&1; }
shot still.html 25000 "$out.png"
mkdir "$work/frames"
for i in $(seq 0 59); do shot anim.html $((3000 + i * 83)) "$work/frames/$(printf %03d "$i").png"; done
ffmpeg -loglevel error -y -framerate 12 -i "$work/frames/%03d.png" \
  -vf "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a" "$out.gif"
echo "Wrote $out.png and $out.gif"
