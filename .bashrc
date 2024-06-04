###################### grep ##########################
# for grep
#GREP_OPTIONS="--exclude-dir=\.svn --exclude-dir=\.git --exclude=tags --exclude=cscope\.out"
#GREP_OPTIONS+=" --color=auto"
#alias grep="grep $GREP_OPTIONS"
#export GREP_COLOR='1;32'

######################################################

export DOTFILES_BIN=~/.dotfiles/bin
export DOTFILES_DEMUX_BIN=~/.dotfiles/bin/demux
export CHROMIUM_DEPOTTOOLS_PATH=~/.dotfiles/depot_tools
export CHROMIUM_BUILDTOOLS_PATH=~/work/code/webrtc_android/src/buildtools
export PATH=$DOTFILES_BIN:$DOTFILES_DEMUX_BIN:$CHROMIUM_DEPOTTOOLS_PATH:$CHROMIUM_BUILDTOOLS_PATH:$PATH
# chromium_tools
export CHROMIUM_DEPOT_TOOL=$HOME/.dotfiles/tools/depot_tools
export PATH=$CHROMIUM_DEPOT_TOOL:$PATH
export CHROMIUM_BUILDTOOLS_PATH=$HOME/.dotfiles/tools/chromium_tools/chromium_tools/buildtools

export EDITOR=vim

export YF_AOSP_TAGS_APPEND_LIST=$HOME/.dotfiles/etc/aosp_tags_append_list

#alias clear="printf '\33[H\33[2J'"
alias div='echo;echo "------------------------------------------------------------------------------";echo;echo;echo;echo;echo;echo;echo;echo;echo;echo;echo;echo "------------------------------------------------------------------------------";clean'

# shellcheck source=.oh-my-bash.bashrc
if [ -r "$HOME/.dotfiles/.oh-my-bash.bashrc" ]; then
  source "$HOME/.dotfiles/.oh-my-bash.bashrc"
fi

# confirm reboot
alias reboot="confirm_reboot"
confirm_reboot() {
  read -r -p 'Are you sure you want to reboot? (yes/no): ' answer
  if [ "$answer" == "yes" ]; then
    sh -c "sudo reboot"
  else
    echo "Reboot canceled."
  fi
}

# kitty
IS_KITTY=0
if [ -n "$KITTY_WINDOW_ID" ]; then
  IS_KITTY=1
  # kitty specific settings
  alias ssh="kitty +kitten ssh"
  alias kdiff="kitty +kitten diff"

fi


# settitle
settitle() {
  if [ $IS_KITTY -eq 1 ]; then
    kitty @ set-tab-title "$@"
  else
    printf '\e]2;%s\a' "$*"
  fi
}
