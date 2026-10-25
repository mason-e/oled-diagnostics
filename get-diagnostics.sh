#!/bin/bash

var_time=$(date +"%H:%M")
var_temp=$(vcgencmd measure_temp)
var_temp=${var_temp#temp=}
var_mem_used=$(free -m | awk '/^Mem:/ {print $3}')
var_mem_total=$(free -m | awk '/^Mem:/ {print $2}')

var_cpu=$(top -bn2 | grep '%Cpu' | tail -1 | awk '{print 100 - $8 "%"}')

echo $var_time,$var_temp,$var_mem_used,$var_mem_total,$var_cpu
