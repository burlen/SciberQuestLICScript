#!/bin/bash

if [ $# -ne 6 ]
then
  echo "Error: invalid number of arguments"
  echo
  echo "sq-lic-driver-all account queue pv_install config_file in_dir out_dir script args"
  echo
  exit 0
fi

ACCOUNT=$1
QUEUE=$2
PV_INSTALL=$3
CONFIG=$4
IN=$5
OUT=$6

IN_IDS=`ls $IN/*_*.gda | cut -d_ -f2 | cut -d. -f1 | sort -g -u`
OUT_IDS=`ls $OUT/*_*.png | cut -d_ -f2 | cut -d. -f1 | sort -g -u`

trap "echo exiting; exit -1;" INT TERM

STEP=0
for IN_ID in $IN_IDS
do
  ID_FOUND=0
  for OUT_ID in $OUT_IDS;
  do
    if [ "$IN_ID" -eq "$OUT_ID" ]
    then
      ID_FOUND=1
      break
    fi
  done
  if [ "$ID_FOUND" -eq 1 ]
  then
    let STEP=$STEP+1
    continue
  fi

  OVER_LIMIT=1
  while [ "$OVER_LIMIT" -eq 1 ]
  do
    NJOBS=`qstat | wc -l`
    if [ "$NJOBS" -lt 19 ]
    then
      OVER_LIMIT=0
    fi
  done

  echo "processing $STEP $IN_ID"

  $PV_INSTALL/bin/sq-lic-driver.sh $ACCOUNT $QUEUE $PV_INSTALL $CONFIG $STEP

  let STEP=$STEP+1
done
