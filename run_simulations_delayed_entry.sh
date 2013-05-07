#!/bin/bash

#  experiment for adversary inserting relays after user's guard selection
# 1/1/2013 00:00:00 timestamp: 1356998400

BASE_DIR=/home/ajohnson/research/pathsim.git

TOT_PROCESSES=20
PARALLEL_PROCESSES=10
DATE_RANGE=2012-11--2013-03
OUTPUT=2
ADV_GUARD_BW=288115
ADV_EXIT_BW=76282
ADV_TIME=1356998400
NUM_ADV_GUARDS=1
USERMODEL=typical
NUM_SAMPLES=5000
TRACEFILE=$BASE_DIR/in/users2-processed.traces.pickle
PATH_ALG=tor

EXP_NAME=$USERMODEL.$DATE_RANGE.$ADV_GUARD_BW-$NUM_ADV_GUARDS-$ADV_EXIT_BW-$ADV_TIME-adv
NSF_DIR=$BASE_DIR/out/network-state/slim/ns-$DATE_RANGE
OUT_DIR=$BASE_DIR/out/simulate/$EXP_NAME

mkdir -p $OUT_DIR
i=1
while [ $i -le $TOT_PROCESSES ]
do
j=1
	while [[ $j -lt $PARALLEL_PROCESSES && $i -lt $TOT_PROCESSES ]]
	do
	# start these in parallel
    	(time pypy pathsim.py simulate $NSF_DIR $NUM_SAMPLES $TRACEFILE $USERMODEL $OUTPUT $ADV_GUARD_BW $ADV_EXIT_BW $ADV_TIME $NUM_ADV_GUARDS $PATH_ALG) 2> $OUT_DIR/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$i.time 1> $OUT_DIR/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$i.out &
	j=$(($j+1))
    	i=$(($i+1))
	done
# wait for this one to finish
(time pypy pathsim.py simulate $NSF_DIR $NUM_SAMPLES $TRACEFILE $USERMODEL $OUTPUT $ADV_GUARD_BW $ADV_EXIT_BW $ADV_TIME $NUM_ADV_GUARDS $PATH_ALG) 2> $OUT_DIR/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$i.time 1> $OUT_DIR/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$i.out
i=$(($i+1))
done
