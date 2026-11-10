count = int(input("How many Fibonacci numbers? "))

first, second = 0, 1
for _ in range(max(0, count)):
	print(first, end=" ")
	first, second = second, first + second

print()
