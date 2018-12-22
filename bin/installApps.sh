#! /bin/sh
#
# installApps.sh
# Copyright (C) 2018 youfa.song <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.
#


echo '============= start install apk ============='
apkDir="./"
cd $apkDir
function readDir(){
    cd $apkDir
    filelist=`ls $1`
    for file in $filelist
        do
        # echo $file
            installApk $file
        done
}
function installApk(){
    file=$1
    extension="${file##*.}"
    if [ "$extension" = "apk" ]
    then
        echo "install "$file" ..."
        adb install $file
    else
        echo "Error:"$file "is not apk file."
    fi
}

readDir $apkDir
