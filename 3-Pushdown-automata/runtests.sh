#!/bin/bash

num_tests=$(ls -l testovi | grep -c ^d)

for i in $(seq 1 $num_tests)  # iterate over the number of test cases
do
    dir=$(printf "%02d\n" $i)
    echo "Test $dir"

    res=$(python SimPa.py < "testovi/test$dir/primjer.in" | diff "testovi/test$dir/primjer.out" -)
    if [ "$res" != "" ]
    then
        echo "FAIL $res"
    else
        echo "OK"
    fi
done