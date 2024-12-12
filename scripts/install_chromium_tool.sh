#!/bin/bash -
#! /bin/sh
#
# install_chromium_tool.sh
# Copyright (C) 2020 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#

set -o nounset # Treat unset variables as an error

INSTALL_DIR_DEFAULT=$HOME/.dotfiles
INSTALL_RC_DEFAULT=$INSTALL_DIR_DEFAULT/.bashrc

INSTALL_DIR=$INSTALL_DIR_DEFAULT
INSTALL_RC=$INSTALL_RC_DEFAULT

function usage() {
  cat <<USAGE
Description:
  install chromium tools

Options:
  [-h, --help]
    Display this help message
  [-d, --install_dir]
    The dir you want to save the chromium tools, default is $INSTALL_DIR_DEFAULT
  [-a, --append_rc]
    The rc files you want to append the env values, default is $INSTALL_RC_DEFAULT

Usage:
  $@ -d <instal dir> -a <rc files>
USAGE
}

function get_opts() {
  local opts="h"
  opts+="a:d:"
  local long_opts="help,"
  long_opts+="install_dir:,append_rc:,"

  getopt_cmd=$(getopt -o "$opts" --long "$long_opts" -n $(basename $0) -- "$@") ||
    {
      echo -e "\nError: getopt failed. Extra args\n"
      usage
      exit 1
    }
  eval set -- "$getopt_cmd"

  while true; do
    echo "\$1:$1"
    case "$1" in
    -h | --help)
      usage
      exit 0
      ;;
    -a | --append_rc)
      INSTALL_RC=$2
      shift
      ;;
    -d | --install_dir)
      INSTALL_DIR=$2
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "error args"
      usage
      exit 1
      ;;
    esac
    shift
  done
}

function install() {
  if [ ! -d $INSTALL_DIR ]; then
    mkdir $INSTALL_DIR
  fi

  # download depot_tools
  echo -e "\033[32m download depot_tools ... \033[0m"
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools $INSTALL_DIR/tools/depot_tools

  # chromium tools fetch config into depot_tools
  wget https://raw.githubusercontent.com/yoofa/chromium_tools/main/chromium_tools.py -O $INSTALL_DIR/tools/depot_tools/fetch_configs/chromium_tools.py

  echo "export CHROMIUM_DEPOT_TOOL=$INSTALL_DIR/tools/depot_tools" >>$INSTALL_RC
  echo "export PATH=\$CHROMIUM_DEPOT_TOOL:\$PATH" >>$INSTALL_RC

  export CHROMIUM_DEPOT_TOOL=$INSTALL_DIR/tools/depot_tools
  export PATH=$PATH:$CHROMIUM_DEPOT_TOOL

  source $INSTALL_RC

  cd $INSTALL_DIR/tools
  echo "enter $INSTALL_DIR/tools"
  echo -e "\033[32m download build tools ... \033[0m"

  fetch --nohooks chromium_tools
  gclient sync

  echo "export CHROMIUM_BUILDTOOLS_PATH=$INSTALL_DIR/tools/chromium_tools/buildtools" >>$INSTALL_RC
  source $INSTALL_RC

  echo -e "\033[32m install done \033[0m"
}

function main() {
  get_opts $@
  install
}

main $@
