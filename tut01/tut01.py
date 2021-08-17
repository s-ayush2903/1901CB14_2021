def meraki_helper(n):
    sz = len(n) # length of the input list
    noes = 0 # maintain counter for number of numberes that ain't Meraki

    # iterate in the entire list
    for listIndex in range(0, sz):
        poss = True # possibility is the number is meraki or not, true if yes no otherwise, default to `True`
        instance = str(n[listIndex]) # element of input list, cast to `string` for ease of iteration
        elementSize = len(instance) # length of current string in investigation
        if (elementSize == 1):
            poss = True
        else: # meraki logic
            for index in range(0, elementSize - 1):
                if (abs(int(instance[index]) - int(instance[index + 1])) != 1):
                    poss = False
                    noes += 1
                    break
        # variables to beautifully format string and avoid redundancy
        verdict = "Yes" if poss else "No"
        highlight = " NOT" if poss == False else "" 

        # Print the final result
        print("{}, {} is{} a Meraki number".format(verdict, instance, highlight))
 
    yess = sz - noes # keep it here as this is an overall result, so it'll be printed _only_ once

    print("The input list contains {} Meraki and {} Non-Meraki numbers".format(yess, noes))

# write input here
input = [2, 14, 56, 78, 98, 54, 678, 134, 789, 0, 7, 5, 123, 45, 76345, 987654321, 101210123212]

# invoke the funtion via storing test case in `input` variable
meraki_helper(input)