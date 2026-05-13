#!/bin/bash

submit=$1

if [ -z $submit ]; then
    echo "[i] Set it to submit = 0 for local test"
    submit=0
fi

##################################################
### Local test ###
##################################################
if [ $submit -eq 0 ]; then
    echo "[i] Running locally"
    # root -b -q analysis.C\(\"test.list\",\"test.output.root\"\)
    ./analysis "test.list" "test.output.root"
    exit
fi

###############################################################
### Batch production for real data using file list          ###
###############################################################

if [ $submit -eq 1 ]; then
    #config=D0_10x100_minQ2_1_25.10.3            # D0 without machine bkg
    #config=DIS_10x100_minQ2_1_25.10.0           # DIS without machine bkg
    #config=D0_10x100_minQ2_1_with_bkg_25.10.4   # D0 with machine bkg
    config=DIS_10x100_minQ2_1_with_bkg_25.10.4  # DIS with machine bkg
    
    echo "[i] Submit batch jobs for sample ${config}"
    pwd=$PWD
	
    #odir=$pwd/output
    odir=$pwd/output_$config

    logdir=$odir/log
    if [ ! -d $odir ]; then
	mkdir -pv $odir
    fi
    rm -rf $odir/*
    mkdir $logdir

    executable=job_run.sh
    cp -v ${executable} $odir/.
    #cp -v analysis.C $odir/.
    
    # Initialising Condor File
    condor_file=CondorFile_submit
    echo "" > ${condor_file}
    echo "Universe    = vanilla" >> ${condor_file}
    echo "Executable  = ${odir}/${executable}" >> ${condor_file}
    echo "GetEnv  =  True" >> ${condor_file}
    #echo "Arguments = \$(oodir) \$(inputfile) \$(outputfile) "  >> ${condor_file}
    echo "Arguments = \$(oodir) \$(inputfile) \$(outfile1) \$(outfile2) \$(outfile3)" >> ${condor_file}
    echo "request_memory = 4GB" >> ${condor_file}

    echo "log = ${logdir}/log_\$(number).log"  >> ${condor_file}
    echo "error = ${logdir}/log_\$(number).err"  >> ${condor_file}
    echo "output = ${logdir}/log_\$(number).out"  >> ${condor_file}

    echo "" >> ${condor_file}
    echo "queue number, oodir, inputfile, outfile1, outfile2, outfile3 from (" >> ${condor_file}

    # change this line as needed
    files=`ls $pwd/input_files/$config/subList*`
    count=0
    for file in $files; do
	count=$((count + 1))
        #if [ $count -ge 5 ]; then
        #	break
	#fi
	listNum=`basename ${file} | sed "s/.list//g" | cut -f 2 -d _`
	#OutFile=${odir}/output_${listNum}.root
	#echo ${listNum}, ${odir}, ${file}, ${OutFile} >> ${condor_file}
        OutFile1=${odir}/output_${listNum}.root
        OutFile2=${odir}/Signal_${listNum}.root
        OutFile3=${odir}/Bkg_${listNum}.root
        echo ${listNum}, ${odir}, ${file}, ${OutFile1}, ${OutFile2}, ${OutFile3} >> ${condor_file}
    done
    echo ")" >> ${condor_file}
    mv ${condor_file} $odir/.
    cd $odir

    #submit condor jobs
    condor_submit ${condor_file}
    cd $pwd
fi

