#!/bin/bash

set -e
cd "$(readlink -f $(dirname "${BASH_SOURCE[0]}"))"

for host in basement office
do
    echo "Host: $host"
    mkdir -p data-$host
    rsync -aiv $host:'data-*' data-$host/
done
