#!/bin/bash -eu

outdir=/tmp/doom
framedir="${outdir}/frames"

# clear the output dirs
[ ! -d "${outdir}" ] && mkdir "${outdir}"
[ ! -d "${framedir}" ] && mkdir "${framedir}"
rm -rf "${framedir}"/*

# split play.txt into tweet-*.txt and input.txt
# also removes comments, and optimises commands
/opt/parse-cmds.py

read frame_count < <( cat ./input.txt | tr ',' $'\n' | wc -l)
/opt/doomreplay \
	-iwad /opt/doom1.wad \
	-input ./input.txt \
	-output "${outdir}/record.mp4" \
	-nrecord "${frame_count}" \
	-nfreeze 18 \
	-render_frame \
	-render_input \
	-render_username

ffmpeg -i "${outdir}/record.mp4" "${framedir}/f%05d.png"
