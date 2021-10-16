# How to Use

Place `doom1.wad` at `/opt/doom1.wad`.

Put your input play in `./play.txt`, and run `/opt/run.sh`...

If everything is successful, you should see the following output:

- `input.txt` - the full input passed to Doom
- `tweet-*.txt` - a series of tweets for your play, compatible with `@tweet2doom`
- `/tmp/doom/record.mp4` - the video recording if your play
- `/tmp/doom/frames/f*.png` - the raw video frames of your play

## Example (Script)

```bash
docker build --tag doomreplay .
docker run --rm -it -d \
  --name doomreplay \
  -v "${PWD}/doom1.wad:/opt/doom1.wad:ro" \
  -v "${PWD}/e1m1-in-450-frames.txt:/play.txt:ro" \
  -v "${PWD}/doom_output:/tmp/doom" \
  doomreplay
docker exec -it doomreplay /opt/run.sh
docker rm -f doomreplay
```

## Example (Play)

```bash
docker build --tag doomreplay .
docker run --rm -d \
  --name doomgeneric \
  -v "${PWD}/doom1.wad:/opt/doom1.wad:ro" \
  -e DISPLAY='10.42.0.18:0' \
  doomreplay \
  /opt/doomgeneric -iwad /opt/doom1.wad
```
