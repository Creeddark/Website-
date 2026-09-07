#!/bin/sh
# Einzelbilder -> mp4. libx264 und yuv420p, weil das die Kombination ist, die
# Etsy, Instagram, Pinterest und jeder Browser ohne Rueckfrage abspielen.
set -e
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
DIR="$1"; OUT="$2"; FPS="${3:-30}"
"$FF" -y -loglevel error -framerate "$FPS" -i "$DIR/f%05d.png" \
  -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -movflags +faststart "$OUT"
ls -l "$OUT" | awk '{printf "%s  %.1f MB\n", $9, $5/1048576}'
