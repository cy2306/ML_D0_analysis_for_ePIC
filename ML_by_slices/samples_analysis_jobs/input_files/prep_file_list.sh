#!/bin/bash

# change the following two lines to get the sample you need
# D0 without machine bkg
#datadir=/volatile/eic/EPIC/RECO/25.10.3/epic_craterlake/SIDIS/D0_ABCONV/pythia8.306-1.1/10x100/q2_1/hiDiv
#prod=D0_10x100_minQ2_1_25.10.3

# DIS without machine bkg
#datadir=/volatile/eic/EPIC/RECO/25.10.0/epic_craterlake/DIS/NC/10x100/minQ2=1
#prod=DIS_10x100_minQ2_1_25.10.0

# D0 with machine bkg
#datadir=/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_Exactly1SignalPer2usFrame/SIDIS/D0_ABCONV/pythia8.306-1.1/10x100/q2_1/hiDiv
#prod=D0_10x100_minQ2_1_with_bkg_25.10.4

# DIS with machine bkg
datadir=/volatile/eic/EPIC/RECO/25.10.4/epic_craterlake/Bkg_1SignalPer2usFrame/DIS/NC/10x100/minQ2=1
prod=DIS_10x100_minQ2_1_with_bkg_25.10.4


filelistall=file.all.list
cp blank $filelistall
files=`xrdfs root://dtn-eic.jlab.org  ls $datadir`
for file in $files; do
    echo root://dtn-eic.jlab.org/$file >> $filelistall
done

split -l 20 --numeric-suffixes --suffix-length=3 $filelistall --additional-suffix=.list subList_

if [ ! -d $prod ]; then
    mkdir -pv $prod
fi
#rm $prod/*
mv $filelistall $prod
mv subList* $prod
