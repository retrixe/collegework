#!/bin/bash

while [[ true ]]; do
	echo "=========="
	echo -n "Enter number 1: "
	read num1
	echo -n "Enter number 2: "
	read num2
	echo "1. Addition"
	echo "2. Subtraction"
	echo "3. Multiplication"
	echo "4. Division"
	echo "0. Exit"
	echo -n "Enter choice: "
	read choice
	result=-1
	case $choice in
	# Other options include:
	# - awk "BEGIN {print EXPR}"
	# - expr EXPR (doesn't support decimals)
	# - echo "EXPR" | bc -l (doesn't provide exit code)
	1) result=$(awk "BEGIN {print $num1 + $num2}" 2>&1);;
	2) result=$(awk "BEGIN {print $num1 - $num2}" 2>&1);;
	3) result=$(awk "BEGIN {print $num1 * $num2}" 2>&1);;
	4) result=$(awk "BEGIN {print $num1 / $num2}" 2>&1);;
	0) break;;
	*) echo Incorrect choice!;;
	esac
	if [[ $? -eq 0 ]]; then
		echo Result: $result
	else
		echo An error occurred!
		echo $result
	fi
done
