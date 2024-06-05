#! /bin/sh
#
# install_oh-my-zsh.sh
# Copyright (C) 2024 youfa <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#

DOTFILES_DIR=$HOME/.dotfiles
OH_MY_ZSH_DIR=$DOTFILES_DIR/.oh-my-zsh
OH_MY_ZSH_CUSTOM_DIR=$DOTFILES_DIR/configs/oh-my-zsh/custom

# install oh-my-zsh
export ZSH="$OH_MY_ZSH_DIR"

# ZSH and ~/.oh-my-zsh neither exist, install
if [ ! -d "$ZSH" ]; then
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended --keep-zshrc
else
  echo "oh-my-zsh already installed"
fi

# install oh-my-zsh plugins
[ -d $OH_MY_ZSH_CUSTOM_DIR ] || mkdir -p $OH_MY_ZSH_CUSTOM_DIR

ZSH_SYNTAX_HIGHLIGHTING_DIR=$OH_MY_ZSH_CUSTOM_DIR/plugins/zsh-syntax-highlighting
[ -d $ZSH_SYNTAX_HIGHLIGHTING_DIR ] ||
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_SYNTAX_HIGHLIGHTING_DIR

ZSH_AUTOSUGGESTIONS_DIR=$OH_MY_ZSH_CUSTOM_DIR/plugins/zsh-autosuggestions
[ -d $ZSH_AUTOSUGGESTIONS_DIR ] ||
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_AUTOSUGGESTIONS_DIR







#. "$HOME/.zshrc"


