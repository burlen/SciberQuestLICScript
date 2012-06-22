#!/bin/bash

if [ $# -ne 1 ]
then
  echo 'Error: wrong number of arguments.'
  echo
  echo 'usage:'
  echo
  echo 'install.sh /path/to/install/at'
  echo
  exit 1
fi

PREFIX=$1
WD=`pwd`

echo "installing to $PREFIX..."

cp -v sq-lic-driver.py $PREFIX
cp -v sq-lic-driver.sh $PREFIX
cp -v sq-lic-driver-all.sh $PREFIX
cp -v all_idl_cmaps.xml $PREFIX
cp -v all_mpl_cmaps.xml $PREFIX

for d in `find $PREFIX -type d -name 'paraview-3.*' | grep lib`
do
  echo "configuring $d..."
  cd $d
  cd ..
  cd ..
  ln -s $PREFIX/sq-lic-driver.py bin/sq-lic-driver.py
  ln -s $PREFIX/sq-lic-driver.py bin/sq-lic-driver.sh
  ln -s $PREFIX/sq-lic-driver-longhorn.qsub bin/sq-lic-driver.qsub
done
cd $WD
echo "done!"
