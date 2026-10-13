#!/bin/bash
# Rebuilds the public site (../public-draft) and the back office (../public-admin) from the source files in this folder.
cd "$(dirname "$0")"
export OUT_DIR="$(pwd)/../public-draft"
export ADMIN_OUT_DIR="$(pwd)/../public-admin"
export HERO_VIDEO="https://d8j0ntlcm91z4.cloudfront.net/user_37HsBZKzp3azVbNUBQIhUBwn3eG/hf_20261005_210706_f5193365-ad84-4027-ac2f-8b78d749a66d.mp4"
export HERO_POSTER="https://d8j0ntlcm91z4.cloudfront.net/user_37HsBZKzp3azVbNUBQIhUBwn3eG/hf_20261001_165123_05449b50-841d-49e8-a6aa-547c82591af0.png"
python3 build.py | head -c 60; echo
