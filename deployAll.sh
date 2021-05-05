#!/bin/bash

aws="aws"
ibm="ibm"

function deploy {
    provider=$1
    echo Deploying for $provider
    pushd . > /dev/null
    cd $provider
    bash deploy.sh
    popd > /dev/null
}


provider=`dialog --checklist "Choose cloud providers to deploy to ..." 0 60 0 \
 $aws "" on\
 $ibm "" off 3>&1 1>&2 2>&3`
dialog --clear
clear
echo "Staring deployment process..."

for p in $provider
do
  deploy $p
done
