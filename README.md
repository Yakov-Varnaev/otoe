![lint and test](https://github.com/Yakov-Varnaev/otoe/actions/workflows/lint_and_test.yml/badge.svg)
![coverage](https://github.com/Yakov-Varnaev/otoe/blob/main/coverage.svg?raw=true)
[![Generic badge](https://img.shields.io/badge/python-3.11-blue.svg)](https://shields.io/)


# otoe
This is simple tool for espanso users. It allows to use obsidian as note editor and then with just one command process them to match config.


# Obsidian root structure
Structure for obsidian files:

```
obsidian_root/
  project_name/
    file1.md
    file2.md
    file3.md
  other_project/
    file1.md
    file2.md
    file3.md
  file4.md       # files in root dir will be associeted with 'common' project
```

# File example

You can see example markdown (here)[https://github.com/Yakov-Varnaev/otoe/blob/main/example.md].

# Install

Maybe I'll publish this pip oneday... But now just clone repo:

```
git clone git@github.com:Yakov-Varnaev/otoe.git
```

# Usage

```
export OBSIDIAN_ROOT=...  # set env var to directory, where your md files are stored

cd .../otoe  # go to otoe dir
python -m venv venv  # NOTE: python 3.11 required
pip install --upgrade pip && pip install -r requirements.txt
bash otoe.sh
```
