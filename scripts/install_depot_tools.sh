#! /bin/sh
#
# install_depot_tools.sh
# Copyright (C) 2024 youfa <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#

INSTALL_TOOL_DIR=$HOME/.dotfiles/tools
DEPOT_TOOLS_DIR=$INSTALL_TOOL_DIR/depot_tools
CHROMIUM_BUILD_TOOL_DIR=$INSTALL_TOOL_DIR/chromium_build_tools

if [ ! -d $DEPOT_TOOLS_DIR ]; then
  mkdir -p $DEPOT_TOOLS_DIR
  # download depot_tools
  echo -e "\033[32m download depot_tools ... \033[0m"
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools $DEPOT_TOOLS_DIR

  # chromium tools fetch config into depot_tools
  wget https://raw.githubusercontent.com/vsyf/chromium_tools/main/chromium_tools.py -O $DEPOT_TOOLS_DIR/fetch_configs/chromium_tools.py

else
  echo -e "\033[32m $DEPOT_TOOLS_DIR already exists, no need install again \033[0m"
fi

export CHROMIUM_DEPOT_TOOL=$INSTALL_DIR/tools/depot_tools
export PATH=$PATH:$CHROMIUM_DEPOT_TOOL

if [ ! -d $CHROMIUM_BUILD_TOOL_DIR ]; then
  mkdir -p $CHROMIUM_BUILD_TOOL_DIR
  cd $INSTALL_TOOL_DIR || exit
  echo "enter $INSTALL_TOOL_DIR"
  echo -e "\033[32m download build tools ... \033[0m"
  fetch --nohooks chromium_tools
  gclient sync
else
  echo -e "\033[32m $CHROMIUM_BUILD_TOOL_DIR already exists, no need install again \033[0m"
fi
