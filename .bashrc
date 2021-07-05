

###################### grep ##########################
# for grep
#GREP_OPTIONS="--exclude-dir=\.svn --exclude-dir=\.git --exclude=tags --exclude=cscope\.out"
#GREP_OPTIONS+=" --color=auto"
#alias grep="grep $GREP_OPTIONS"
#export GREP_COLOR='1;32'

######################################################


#PS1='\$ '

export DOTFILES_BIN=~/.dotfiles/bin
export CHROMIUM_DEPOTTOOLS_PATH=~/.dotfiles/depot_tools
export CHROMIUM_BUILDTOOLS_PATH=~/work/code/webrtc_android/src/buildtools
export PATH=$DOTFILES_BIN:$CHROMIUM_DEPOTTOOLS_PATH:$CHROMIUM_BUILDTOOLS_PATH:$PATH

export EDITOR=vim

export YF_AOSP_TAGS_APPEND_LIST=~/dotfiles/etc/aosp_tags_append_list

alias clear="printf '\33[H\33[2J'"
alias div='echo;echo "------------------------------------------------------------------------------";echo;echo;echo;echo;echo;echo;echo;echo;echo;echo;echo;echo "------------------------------------------------------------------------------";clean'

source ~/.dotfiles/.bashrc_oh-my-bash

settitle() { printf '\e]2;%s\a' "$*"; }
