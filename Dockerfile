FROM ubuntu:20.04 AS build-doomreplay

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
	&& apt install -y build-essential clang git libx11-dev

RUN git clone https://github.com/ggerganov/doomreplay.git /opt/doomreplay \
	&& cd /opt/doomreplay/doomgeneric \
	&& make -f Makefile.dr clean all \
	&& mv doomgeneric doomreplay \
	&& make -f Makefile clean all

# --- #

FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
	&& apt install -y ffmpeg python3

COPY --from=build-doomreplay /opt/doomreplay/doomgeneric/doomgeneric /opt/doomgeneric
COPY --from=build-doomreplay /opt/doomreplay/doomgeneric/doomreplay  /opt/doomreplay
COPY run.sh parse-cmds.py /opt/
