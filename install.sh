#! /bin/sh
#
# install.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


#export DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DOTFILES_DIR="$PWD"

#clone vim
git clone git@github.com:vsyf/vim.git $DOTFILES_DIR/.vim

ln -sfv "$DOTFILES_DIR/git/.gitconfig" ~
ln -sfv "$DOTFILES_DIR/git/.gitignore_global" ~
ln -sfv "$DOTFILES_DIR/.vim" ~

echo ". $DOTFILES_DIR/.bashrc" >> ~/.bashrc
