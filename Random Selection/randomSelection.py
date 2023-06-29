import random
import os
print("Select a random element from a list:")
elements = set(line.strip() for line in open('./imageNames.txt'))

print("\nTrain:")
for x in range(int(len(elements) * 0.8)):
	y = random.choice(tuple(elements))
	print(y)
	elements.remove(y)

print("\nVal:")
for x in range(int(len(elements) * 0.5)):
	y = random.choice(tuple(elements))
	print(y)
	elements.remove(y)

print("\nTest:")
for x in range(len(elements)):
	y = random.choice(tuple(elements))
	print(y)
	elements.remove(y)

