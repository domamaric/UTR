#!/bin/bash

num_tests=$(ls -l testovi | grep -c ^d)

for i in $(seq 1 $num_tests)  # iterate over the number of test cases
do
    dir=$(printf "%02d\n" $i)
    echo "Test $dir"

    res=$(python SimEnka.py < "testovi/test$dir/test.a" | diff "testovi/test$dir/test.b" -)
    if [ "$res" != "" ]
    then
        echo "FAIL $res"
    else
        echo "OK"
    fi
done
