# Import module
import fjmi

### Testing Utilities
import random
import time

# Function to generate arrays with random, non-repating nummbers of any length
def createArray(length):
    i = 0
    A = []
    while i < length:
        randomNumber = random.randint(0, 5000)
        if randomNumber not in A:
            A.append(randomNumber)
        i += 1
    return A

# Create an unsorted array
a = createArray(100)

# And sort it!
start_time = time.time()
fjmi.merge_insertion_sort(a)
print("Sort took", time.time() - start_time, "to run")
