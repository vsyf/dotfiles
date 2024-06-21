#! /bin/sh
#
# install_snippets.sh
# Copyright (C) 2024 youfa <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


DOTFILES_DIR=$(cd "$(dirname "$0")"/.. && pwd)
TEMPLATES_DIR="$DOTFILES_DIR/tools/templates-to-snippets"

# clone competitive_programming tempaltes
git clone git@github.com:yoofa/templates-to-snippets.git "$TEMPLATES_DIR"

cd "$TEMPLATES_DIR" || exit

python scripts/generate_snippets.py

ln -sfv "$TEMPLATES_DIR/snippets" "$DOTFILES_DIR/configs/nvim/snippets/competitive_programming"
