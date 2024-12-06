#!/bin/bash
START=1
END=25
for day in $(seq $START $END); do

    mkdir -p "Day$day"
    touch  "Day$day/solution.go"
    touch  "Day$day/solution.cpp"
    touch  "Day$day/solution.lua"
done



