def get_memory_score(lst):
    invalid_inputs = [] # memo of elements in @lst that are NOT integers
    memory = [] # memo of "valid" elements in @lst
    poss = True # a flag that which is False on presence of ANY invalid element in @lst
    score = 0 # score, defined as per question description

    # iterate in @lst and check validity of EACH element present in it
    for index in range(0, len(lst)):
        if (isinstance(lst[index], int) == False):
            invalid_inputs.append(lst[index])
            poss = False
    # if @poss is True, increase score by `1` for elements present in memory, if they ain't present in memory, remove the oldest element and add the current one
    if (poss):
        for ind in range(0, len(lst)):
            if (lst[ind] in memory):
                score += 1
            else:
                if (len(memory) == 5):
                    memory.pop()
                memory.append(lst[ind]) 
        return "Score: " + str(score) # return score on complete traversal
    else:
        # Display an error message on the console with some Info
        return ("Please enter a valid input list, invalid inputs detected: " + str(invalid_inputs))

input_nums = [3, 4, 5, 3, 2, 1]
print(get_memory_score(input_nums))