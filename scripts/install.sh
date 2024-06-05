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

# clone neovim config
git clone https://github.com/yoofa/nvim.git $DOTFILES_DIR/configs/nvim

# copy
## git config files
[ -f $HOME/.gitconfig ] || cp $HOME/.gitconfig $HOMD/.gitconfig.bak
cp "$DOTFILES_DIR/configs/.gitconfig" ~

[ -f $HOME/.gitignore ] || cp $HOME/.gitconfig $HOMD/.gitignore_global
cp "$DOTFILES_DIR/configs/.gitignore_global" ~

# link
## kitty
ln -sfv "$DOTFILES_DIR/configs/kitty" ~/.config/
## nvim
ln -sfv "$DOTFILES_DIR/configs/nvim" ~/.config/

# At last, append dotrc
prefix=$DOTFILES_DIR/.dotrc
shells="bash zsh fish"
update_config=1
for shell in $shells; do
  [ "$shell" = fish ] && continue
  [ "$shell" = zsh ] && dest=~/.zshrc || dest=~/.bashrc
  append_line $update_config "[ -f ${prefix} ] && source ${prefix}" "$dest" "${prefix}"
done
