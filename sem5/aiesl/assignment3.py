"""AIESL Assignment 2: Cryptarithmetic Puzzle Solver"""

import itertools

keyword1 = input("Enter the first input keyword: ")
keyword2 = input("Enter the second input keyword: ")
keyword3 = input("Enter the output keyword: ")

letters = set(keyword1 + keyword2 + keyword3)
digits = range(10)
found = False

for perm in itertools.permutations(digits, len(letters)):
    sol = dict(zip(letters, perm))
    if sol[keyword1[0]] == 0 or sol[keyword2[0]] == 0 or sol[keyword3[0]] == 0:
        continue
    word1 = 0
    for i, letter in enumerate(keyword1):
        word1 = word1 * 10 + sol[letter]
    word2 = 0
    for i, letter in enumerate(keyword2):
        word2 = word2 * 10 + sol[letter]
    output = 0
    for i, letter in enumerate(keyword3):
        output = output * 10 + sol[letter]
    if word1 + word2 == output:
        print(f"{keyword1} + {keyword2} = {keyword3}")
        print(word1, word2, output)
        found = True

if not found:
    print("No solution found.")
