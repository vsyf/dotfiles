#! /bin/sh
#
# install.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


#export DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DOTFILES_DIR="$PWD"

ln -sfv "$DOTFILES_DIR/configs/.gitconfig" ~
ln -sfv "$DOTFILES_DIR/configs/.gitignore_global" ~

# install chromium tools
TODO use another script to install chromium tools
wget -O - https://raw.githubusercontent.com/vsyf/chromium_tools/master/install_chromium_tool.sh | bash

# get oh-my-bash
# TODO change to oh-my-zsh
git clone https://github.com/ohmybash/oh-my-bash.git $DOTFILES_DIR/.oh-my-bash


# install SpaceVim
# https://spacevim.org/cn/quick-start-guide/
curl -sLf https://spacevim.org/cn/install.sh | bash
rm -rf ~/.SpaceVim.d
ln -sfv "$DOTFILES_DIR/.SpaceVim.d" ~

# At last, append bashrc
echo ". $DOTFILES_DIR/.bashrc" >> ~/.bashrc
