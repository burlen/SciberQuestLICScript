#!/bin/bash
# (C) 2012 SciberQuest Inc.

if [[ $# != 5 ]]
then
  echo "Error: incorrect number of arguments"
  echo
  echo "Usage:"
  echo
  echo "sq-lic-driver account queue pv_install config_file time_step"
  echo
  exit
fi

ACCOUNT=$1
QUEUE=$2
export PV_INSTALL_PREFIX=$3
export SQ_DRIVER_CONFIG=$4
export SQ_TIME_STEP=$5

export PV_LIBRARY_PATH="$PV_INSTALL_PREFIX/lib/`ls $PV_INSTALL_PREFIX/lib/`"
export LD_LIBRARY_PATH="$PV_LIBRARY_PATH:$LD_LIBRARY_PATH"
export PV_PATH="$PV_INSTALL_PREFIX/bin"
export PATH="$PV_PATH:$PATH"


echo "PV_INSTALL_PREFIX=$PV_INSTALL_PREFIX"
echo "PV_LIBRARY_PATH=$PV_LIBRARY_PATH"
echo "PV_PATH=$PV_PATH"
echo "SQ_DRIVER_CONFIG=$SQ_DRIVER_CONFIG"
echo "SQ_TIME_STEP=$SQ_TIME_STEP"

qsub -A $ACCOUNT -N lic-$SQ_TIME_STEP -j y -o $HOME/lic-$SQ_TIME_STEP.out -q $QUEUE -P vis -V -pe 1way 8 -l h_rt=02:00:00 $PV_PATH/sq-lic-driver.qsub
