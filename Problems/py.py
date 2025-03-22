def number(x):
    numbers = []
    total = 0
    for i in range(1, x + 1):
        if(i % 2 != 0):
            numbers.append(i)
            total += i
    
    print(f"The natural numbers up to {x}th terms are:")
    print(*numbers)
    print(f"The sum of the natural numbers is: {total}")

# Get input from user
n = int(input("Input a number of terms: "))
number(n)

# Write a program in C++ to display n terms of natural number and their sum.
# Sample Output: