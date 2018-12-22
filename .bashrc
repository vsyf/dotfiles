

###################### grep ##########################
# for grep
GREP_OPTIONS+="--exclude-dir=\.svn --exclude-dir=\.git --exclude=tags --exclude=cscope\.out"
GREP_OPTIONS+=" --color=auto"
alias grep="grep $GREP_OPTIONS"
#export GREP_COLOR='1;32'

######################################################


#PS1='\$ '

export PATH=$PWD/bin:$PATH
