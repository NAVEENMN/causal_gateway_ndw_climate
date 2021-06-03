#!/bin/sh
i=0
while [ $i -ne 5 ]
do
        i=$(($i+1))
        echo "$i"
done
curl --url https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/surface/slp.1948.nc --output /Volumes/ext_data/ncep/slp.1948.nc