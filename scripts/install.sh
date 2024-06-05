#! /bin/sh
#
# install.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#

#export DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DOTFILES_DIR=$(cd $(dirname $0)/.. && pwd)
. "$DOTFILES_DIR/scripts/install_helper.sh"

# install chromium tools
#TODO use another script to install chromium tools
wget -O - https://raw.githubusercontent.com/yoofa/chromium_tools/master/install_chromium_tool.sh | bash

# get oh-my-bash
# TODO change to oh-my-zsh
git clone https://github.com/ohmybash/oh-my-bash.git $DOTFILES_DIR/.oh-my-bash

# neovim config
git clone https://github.com/yoofa/nvim.git $DOTFILES_DIR/nvim

# link
## git
ln -sfv "$DOTFILES_DIR/configs/.gitconfig" ~
ln -sfv "$DOTFILES_DIR/configs/.gitignore_global" ~
## kitty
ln -sfv "$DOTFILES_DIR/configs/kitty/kity.conf" ~/.config/kitty/
## nvim
ln -sfv "$DOTFILES_DIR/nvim" ~/.config/

# At last, append dotrc
prefix=$DOTFILES_DIR/.dotrc
shells="bash zsh fish"
update_config=1
for shell in $shells; do
  [ "$shell" = fish ] && continue
  [ "$shell" = zsh ] && dest=~/.zshrc || dest=~/.bashrc
  append_line $update_config "[ -f ${prefix} ] && source ${prefix}" "$dest" "${prefix}"
done
