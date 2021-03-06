#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from pathlib import Path

clp = argparse.ArgumentParser(prog='git-pull-repos',
                              description='For each sub-dir, pull git repos',
                              epilog='Default root dir is ~/src/github.com/enigmata')

clp.add_argument('--dir', dest='root_dir',
                          help='pull repos from sub-dirs of this root dir')

args = clp.parse_args()

root_dir = '~/src/github.com/enigmata'

if args.root_dir is not None:
   root_dir = args.root_dir

repos_root_dir = Path(root_dir).expanduser().resolve()

if not repos_root_dir.is_dir():
    print(f'ERROR: "{repos_root_dir}" is not a directory!')
    sys.exit(1)

print(f'INFO Invoking "git pull" for each sub-directory of "{repos_root_dir}" ...')

for repo_root_dir in (d for d in repos_root_dir.iterdir() if d.is_dir()):
    os.chdir(repo_root_dir)
    banner_len = len(repo_root_dir.as_posix()) + 13
    if (repo_root_dir / ".git").is_dir():
        print("=" * banner_len)
        print(f'PULLING: {repo_root_dir} ...')
        print("=" * banner_len)
        subprocess.run(["git", "pull"])
    os.chdir(repos_root_dir)

sys.exit(0)
