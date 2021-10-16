#!/usr/bin/env python3

import re
from itertools import chain

def load_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [ _.strip() for _ in lines ]
    lines = filter(lambda _: _ != '' and _[0] != '#', lines)
    cmds = chain.from_iterable( _.split(',') for _ in lines )
    return expand_cmds(cmds)

def expand_cmds(cmds):
    for cmd in cmds:
        m = re.fullmatch(r'^((?P<repeat>[0-9]+)-)?(?P<cmd>.*)$', cmd)

        if m is None:
            m = { 'repeat': 1, 'cmd': '' }
        else:
            m = m.groupdict()

        if m['repeat'] is None:
            m['repeat'] = 1

        for i in range(int(m['repeat'])):
            yield m['cmd']

def gen_cmds(cmds):
    last_cmd = next(cmds)
    last_count = 1

    for cmd in cmds:
        if cmd == last_cmd:
            last_count += 1
            continue

        yield last_count, last_cmd

        last_cmd = cmd
        last_count = 1

    yield last_count, last_cmd

def gen_tweets(cmds, max_cmds=350):
    tweet_cmds = []
    tweet_count = 0

    for count, cmd in gen_cmds(cmds):
        tweet_count += count
        tweet_over = 0 if tweet_count < max_cmds else tweet_count - max_cmds

        if tweet_over > 0:
            tweet_cmds.append((count-tweet_over, cmd))
            yield tweet_cmds

            tweet_cmds = []
            tweet_count = tweet_over
            count = tweet_over

        tweet_cmds.append((count, cmd))

    if len(tweet_cmds) > 0:
        yield tweet_cmds

def format_cmd(count, cmd):
    if count > 1:
        return f'{count}-{cmd}'
    return cmd

cmds = load_file('./play.txt')
for i, tweet in enumerate(gen_tweets(cmds), start=1):
    with open(f'./tweet-{i:03d}.txt', 'w') as f:
        f.write(','.join( format_cmd(*_) for _ in tweet ))
        f.write('\n')

cmds = load_file('./play.txt')
with open(f'./input.txt', 'w') as f:
    for cmd in expand_cmds(cmds):
        f.write(f'{cmd},')
    f.write('#doomreplay-docker#')
