"""AIESL Assignment 2: Cryptarithmetic Puzzle Solver"""

import itertools


def main():
    keyword_count = int(input("Enter number of input keywords: "))
    keywords = []
    for i in range(keyword_count):
        keyword = input(f"Enter input keyword {i + 1}: ")
        keywords.append(keyword)
    sum_keyword = input("Enter the output keyword: ")
    operation = input("Enter the operation (e.g., '+'): ")

    letters = set("".join(keywords) + sum_keyword)
    digits = range(10)
    found = False

    for perm in itertools.permutations(digits, len(letters)):
        sol = dict(zip(letters, perm))
        if any(sol[keyword[0]] == 0 for keyword in keywords) or sol[sum_keyword[0]] == 0:
            continue
        words = []
        total_input = 0
        for keyword in keywords:
            word = 0
            for i, letter in enumerate(keyword):
                word = word * 10 + sol[letter]
            words.append(word)
            if total_input == 0:
                total_input = word
            elif operation == '+':
                total_input += word
            elif operation == '-':
                total_input -= word
            elif operation == '*':
                total_input *= word
            elif operation == '/':
                total_input /= word
        output = 0
        for i, letter in enumerate(sum_keyword):
            output = output * 10 + sol[letter]
        if total_input == output:
            print(f"{' + '.join(keywords)} = {sum_keyword}")
            print(' + '.join(map(str, words)), '=', output)
            found = True

    if not found:
        print("No solution found.")


if __name__ == "__main__":
    main()
