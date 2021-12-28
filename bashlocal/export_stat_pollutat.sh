#!/bin/bash

#Extract pollutants data from specific stations and pollutants for the year 2015

for i in PED UIZ MER TLA SAG SFE AJM #List of acronims of desired stations
do
    mkdir -p ../datos/contaminantes/2015/$i

    for j in O3 PM10 PM2.5 #List of pollutants
    do

        echo "** Extrayendo datos de $j la estación $i **"

grep $i ../datos/contaminantes/2015/contaminantes_2015.CSV | grep $j > ../datos/contaminantes/2015/${i}/${i}_${j}_2015.csv
    done
done

echo "** DONE **"
