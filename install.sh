#! /bin/sh
#
# install.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


#export DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DOTFILES_DIR="$PWD"

ln -sfv "$DOTFILES_DIR/git/.gitconfig" ~
ln -sfv "$DOTFILES_DIR/git/.gitignore_global" ~
ln -sfv "$DOTFILES_DIR/.vim" ~

# install chromium tools
wget -O - https://raw.githubusercontent.com/vsyf/chromium_tools/master/install_chromium_tool.sh | bash

# get oh-my-bash
git clone https://github.com/ohmybash/oh-my-bash.git $DOTFILES_DIR/.oh-my-bash


# At last, append bashrc
echo ". $DOTFILES_DIR/.bashrc" >> ~/.bashrc
