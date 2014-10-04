
def generateRounds(numDebaters, numRounds):
    """
    generateRounds implements the a simple lazy algorithm, guaranteeing that for
    any tournament where numRooms > 2*numRounds, every debateer will switch
    positions every round, and no debater will see another debater twice before
    outrounds. An optimal algorithm would only require numDebaters > 3*numRounds
    
    The output will be a tuple of two lists of tuples, which contain two lists,
    resulting in following structure:
    (
      [
        ([Half prop debaters in round 0], [Half prop debaters in round 0]),
        ...
        ([Half prop debaters in round n], [Half prop debaters in round n])
      ],
      [
        ([Half opp  debaters in round 0], [Half opp  debaters in round 0]),
        ...
        ([Half opp  debaters in round n], [Half opp  debaters in round n])
      ]
    )
    
    The indices of each pair of positioned debaters in each round will indicate
    their room each round, and their partner will be the person with the
    matching index.

    A simple inductive proof of the correctness of this algorithm can be seen by
    the fact that each ith quadrant outpaces the i-1th quadrant, and
    > 3*numRounds is enough that the fastest cycle will never overlap. So for
    every cycle you will never align with any other debater from any quadrant
    you have previously aligned with.
    """
    
    if (numDebaters % 4):
        print("Error! Please provide even number of teams.")
        exit()
    if (numRounds < 2):
        print("Don't use this tool for doing less than two rounds of debate. That's stupid.")
        exit()
    if (numDebaters//4 <= 2*numRounds):
        print("Warning! Having fewer rooms than 3*rounds may result in an imperfect tab.")

    numRooms = numDebaters//4
    debaters = [i for i in range(numDebaters)]

    # Split debaters into four quadrants
    a = numDebaters // 4
    b, c =  a*2, a*3
    h1, h2 = debaters[:a], debaters[a:b]
    h3, h4 = debaters[b:c], debaters[c:]

    # The 0th round will simply be whatever order they happened to be on input
    prop, opp = [(h1.copy(), h2.copy())], [(h3.copy(), h4.copy())]
    
    # For each further round, have h2-h4 cycle asyncronously.
    for i in range(numRounds-1):
        # h1 remains in the same
        # h2 cycles up 1
        head = h2.pop()
        h2.insert(0, head)
        # h3 cycles up 2
        for j in range(2):
            head = h3.pop()
            h3.insert(0, head)
        # h4 cycles up 3
        for j in range(3):
            head = h4.pop()
            h4.insert(0, head)
        # Now that they're cycled, store the this round and move on
        if (i % 2):
            prop.append((h1.copy(),h2.copy()))
            opp.append( (h3.copy(),h4.copy()))
        else:
            prop.append((h3.copy(),h4.copy()))
            opp.append( (h1.copy(),h2.copy()))

    # All rounds slotted, let's roll!
    return (prop, opp)

def saveRounds(rounds):
    """
    saveRounds takes the output from generateRounds and outputs a csv file
    that can be used to open the tab in the spreadsheet software of your
    choosing.
    """
    out = ["Room Number"]
    # Generate the header cells
    for i in range(len(rounds[0])):
        out.append("Prop 1")
        out.append("Prop 2")
        out.append("Opp  1")
        out.append("Opp  2")
        out.append("Round {n}".format(n=i+1))
    out.append('\n')
    for i in range(len(rounds[0][0][0])):
        # Print the room number
        out.append(i)
        # for each round
        for j in range(len(rounds[0])):
            # Fill columns for each room
            out.append(rounds[0][j][0][i])
            out.append(rounds[0][j][1][i])
            out.append(rounds[1][j][0][i])
            out.append(rounds[1][j][1][i])
            # Space between rounds (Round # column)
            out.append(' ')
        out.append('\n')
            
    filename = 'out.csv'
    outfile = open(filename, 'w')
    for cell in out:
        outfile.write(str(cell))
        if (cell != '\n'):
            outfile.write(',')
    outfile.close()

