import bisect

# Split into pairs
def create_pairs (a):

  # Create local stores for use
  split_array = [];
  temp_array = [];

  for num, value in enumerate(a, start=1):
    temp_length = len(temp_array)
    if temp_length == 1:
      temp_array.append(value)
      split_array.append(temp_array)
      temp_array = []
    elif len(split_array) * 2 == len(a) - 1:
      split_array.append(value)
    elif temp_length == 0:
      temp_array.append(value)

    #count += 1

  return split_array

# Sort all the pairs
def sort_each_pair (split_array):

  for pair in split_array:
    # compare values in each pair and sort
    if len(pair) != 1 and (pair[0] > pair[1]):
      temp = pair[0]
      pair[0] = pair[1]
      pair[1] = temp;

  return split_array

# build utility functions for recursive insertion sort by highest value in pair
def insert(element, A, n):
  if n < 0:
    A[0] = element
  elif element[1] >= A[n][1]:
    if n == len(A)-1:
      A.append(element)
    else:
      A[n+1] = element
  else:
    if n == len(A)-1:
      A.append(A[n])
    else:
      A[n+1] = A[n]
      insert(element, A, n-1)

# entry function to recusrively sort pairs by their higher value
def insertion_sort_pairs(A, n):
  if n < 1:
    return A
  else:
    insertion_sort_pairs(A, n-1)
    insert(A[n], A, n-1)

# Recursive function to generate nth Jacobsthal number
def jacobsthal(n):
    # first base case
    if (n == 0):
        return 0

    # second base case
    if (n == 1):
        return 1

    # recurse!
    return jacobsthal(n - 1) + 2 * jacobsthal(n - 2)

# Built a sequence of valid jacobsthal numbers, given an array length
def build_jacob_insertion_sequence (array):
    # Store some variables, set some up for returning
    array_len = len(array)
    end_sequence = []
    jacob_index = 3 # The first one that matters

    # Loop through and create the sequence
    while jacobsthal(jacob_index) < array_len -1 :
        end_sequence.append(jacobsthal(jacob_index))
        jacob_index += 1

    # Return it for user
    return end_sequence

# Recursively sort the larger set of elements into sorted set
def sort_by_larger_value(sorted_split_array):

  # Grab the length
  length = len(sorted_split_array)

  ## recursively sort the pairs by largest element
  insertion_sort_pairs(sorted_split_array, (len(sorted_split_array) -1))


# Create Sequence
def create_s(sorted_split_array, straggler, print_comparision_estimation):

  # Placeholders for the key sequences
  S = []
  pend = []

  # Comparison Counter
  comparisions_made = 0

  # Split the pairs into the main sequences.
  for pair in sorted_split_array:
    # Add the larger elements into 'main'
    S.append(pair[1])
    # add smaller elements into 'pend'
    pend.append(pair[0])

  # Insert the first element in S -- we know it's the smallest, since it
  # was already sorted smaller in the first pairing
  S.insert(0, pend[0])

  # Now, we need to build an insertion sequence, taking advantage of the
  # Jacobsthal number set

  # Store some placeholders
  iterator = 0 # We already added one
  jacobindex = 3 # Start at three, since we already inserted 1 and we can skip the beginning of this sequence
  indexSequence = [1] # Index sequence for reporting purposes (and sanity)
  last = "default" # Not the most elegant solution, but store a string so we know when if the last sequence entry was a Jacobsthal number

  # build the valid jacobsthal sequence, then we can fill in the rest
  jacob_insertion_sequence = build_jacob_insertion_sequence(pend)

  # iterate through the rest of 'pend'
  while iterator <= len(pend):

      # if we have a valid jacobsthal index, let's use it!
      if len(jacob_insertion_sequence) != 0 and last != "jacob":
          indexSequence.append(jacob_insertion_sequence[0])
          item = pend[jacob_insertion_sequence[0] - 1]
          # Now pop it off
          jacob_insertion_sequence.pop(0)
          last = "jacob"
      else:
          # Else, let's fill it with what's remaining most efficently
          # First, make sure the jacob number wasn't already used
          if (iterator in indexSequence):
              iterator += 1
          item = pend[iterator - 1]
          indexSequence.append(iterator)
          last = "not-jacob"
          # Increment our iterators
          iterator += 1
          jacobindex += 1

      # we now have the most optimal item to insert (with the least comparisons!).
      # lets use bisect to get the insertion point
      insertion_point = bisect.bisect(S, item, 0, len(S))

      # then insert it into S!
      S.insert(insertion_point, item)

      # Update comparisions counter
      comparisions_made += 2

  # If an odd numbered array was given, we took off the straggler in the beginning
  # We now binary search insert the entire array for this one, following the algo.
  if straggler:
    insertion_point = bisect.bisect(S, straggler, 0, len(S))
    S.insert(insertion_point, straggler)
    comparisions_made += 2

  if print_comparision_estimation:
      print("Approximate Comparisions Made:")
      print(comparisions_made)

  return S

# # #
# Ford-Johnson Merge-Insertion Sort
# Implementation in Python
#
# Input: Provide an array of non-repeating integers that you wish to be sorted
# Output: Sorted array
# # #
def merge_insertion_sort (A):
    # Print out Given Array, for clarity
    print("Starting Array:")
    print(A)

    # Determine if it's odd numbered... if so, take off a straggler
    hasStraggler = len(A) % 2 != 0

    if hasStraggler:
        straggler = A.pop(len(A) -1)
    else:
        straggler = False

    # Then Split Array into Pairs
    split_array = create_pairs(A);

    # Sort each pair of elements
    sorted_split_array = sort_each_pair(split_array)

    # Recursively sort the pairs by their largest element
    sort_by_larger_value(sorted_split_array)

    # Create main and pend sequences and merge insertion sort
    S = create_s(sorted_split_array, straggler, True)

    # Print it to the user
    print("Sorted Array:")
    print(S)

    # Return it to the user
    return S
