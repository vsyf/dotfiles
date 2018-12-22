#! /bin/sh
#
# autoBuildAOSP.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


#Usage:crontab -e to add task

######config
PROJECT_DIR=/work/MT8321_AP/
LUNCH_COMBO=full_rlk8321_tb_rc_m-eng
#if use git global
#GIT_REMOTE=origin/dev_orange_archermind
BUILD_DIR=out/target/product/rlk8321_tb_rc_m
OUT_DIR=/data/daily_build/


######sync
cd $PROJECT_DIR
repo sync -j16
#git reset --hard $GIT_REMOTE

######build
# cd $PROJECT_DIR
# source $PROJECT_DIR/build/envsetup.sh
# lunch $LUNCH_COMBO
# make clean -j8 2>&1 | tee build.log
# make -j8 2>&1 | tee build.log

######package&copy
DATE=`date +%m%d%H%M`
cd ${PROJECT_DIR}/${BUILD_DIR}
tar czvf $OUT_DIR/rlk8321_${DATE}.tar.gz *
