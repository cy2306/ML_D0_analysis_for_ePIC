#!/bin/bash

echo ${1}
echo ${2}
echo ${3}
echo ${4}
echo ${5}

cd ${1}

/direct/eic+u/cyang/eic/eic-shell  << EOF
# root -b -q 'analysis.C("'"${2}"'","'"${3}"'")'
/eic/u/cyang/eic/Job_submission_RCF/analysis "${2}" "${3}" "${4}" "${5}"
exit
EOF
