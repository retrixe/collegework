#!/bin/bash
echo -n Enter your language:\ 
read userlang
echo -n Enter your name:\ 
read name

case $userlang in
"Japanese") printf "Konnichiwa, $name!\n";;
"French") printf "Bonjour, $name!\n";;
"Arabic") printf "Merhaba, $name!\n";;
"Korean") printf "Annyeong, $name!\n";;
"English") printf "Hello, $name!\n";;
*) printf "Sorry, I don't know your language, but hello, $name!\n";;
esac

echo -n Enter a number:\ 
read num
if [ $num -gt 0 ]; then
	echo Number is positive!
elif [ $num -lt 0 ]; then
	echo Number is negative!
else
	echo Number is zero!
fi

for i in {1..5}; do
	echo $i \* $i = `expr $i \* $i`
	fact=1
	j=1
	while [ $j -ne $i ]; do
		j=`expr $j + 1`
		fact=`expr $fact \* $j`
	done
	echo $i! = $fact
done

#str=${str,,}
str=$name
str=$(echo $str | tr "[a-z]" "[A-Z]")
echo Lowercased string: $str
str=$(echo $str | tr "[A-Z]" "[a-z]")
echo Uppercased string: $str

echo Guess a number!
num=$RANDOM
guess=-1
while [ $guess -ne $num ]; do
	echo -n Enter your guess:\ 
	read guess
	if [ $guess -eq $num ]; then
		echo Correct answer!
	elif [ $guess -lt $num ]; then
		echo Guess higher!
	else
		echo Guess lower!
	fi
done
