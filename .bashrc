

###################### grep ##########################
# for grep
GREP_OPTIONS="--exclude-dir=\.svn --exclude-dir=\.git --exclude=tags --exclude=cscope\.out"
GREP_OPTIONS+=" --color=auto"
alias grep="grep $GREP_OPTIONS"
#export GREP_COLOR='1;32'

######################################################


#PS1='\$ '

export PATH=~/dotfiles/bin:$PATH
export EDITOR=vim

export YF_AOSP_TAGS_APPEND_LIST=~/dotfiles/etc/aosp_tags_append_list
