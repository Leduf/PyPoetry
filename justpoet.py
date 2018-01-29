import inspect, os, random, time

# directory management
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pathSource = os.path.join(path, "src")
pathWords = os.path.join(path, "wrd")

print("Loading...")

# Load 5 syllable templates
tl5 = []
with open(os.path.join(pathSource, "tl5.txt")) as f:
    tl5 = f.readlines()
tl5len = len(tl5)
for i in range(tl5len):
    tl5[i] = tl5[i].rstrip()
# Load 7 syllable templates
tl7 = []
with open(os.path.join(pathSource, "tl7.txt")) as f:
    tl7 = f.readlines()
tl7len = len(tl7)
for i in range(tl7len):
    tl7[i] = tl7[i].rstrip()
print("Templates loaded.")

# Open and load markov chain
read = []
with open(os.path.join(pathSource, "mkv.txt")) as f:
    read = f.readlines()
markov = {}
for line in read:
    temp = line.split()
    if temp[0] in markov:
        markov[temp[0]].append(temp[1].rstrip())
    else:
        markov[temp[0]] = [temp[1].rstrip()]
print("Markov loaded.")
print(len(markov))

# Open parts of speech
pos = []
with open(os.path.join(pathSource, "pos.txt")) as f:
    pos = f.readlines()
poslen = len(pos)
for i in range(poslen):
    pos[i] = pos[i].rstrip()
print("Parts of speech loaded.")

# Open and load words
sylcount = 4
wrd = [[[]]]
mwrd = [[[]]]
mkeys = markov.keys()
for i in range(poslen):
    wrdi = [[]]
    mwrdi = [[]]
    for j in range(1, sylcount + 1):
        wrdj = []
        with open(os.path.join(pathWords,
                               pos[i] + "/" + str(j) + ".txt")) as f:
            wrdj = f.readlines()
        for k in range(len(wrdj)):
            wrdj[k] = wrdj[k].rstrip()
        wrdi.append(wrdj)
        mwrdj = []
        for key in mkeys:
            if key in wrdj:
                mwrdj.append(key)
        mwrdi.append(mwrdj)
    wrdi = wrdi[1:]
    wrd.append(wrdi)
    mwrd.append(mwrdi)
wrd = wrd[1:]
print("Words loaded.")

print("Now running.\n")

# Forever loop
while True:
    # Generate template
    lines = []
    lines.append(tl5[random.randint(0, len(tl5) - 1)])
    lines.append(tl7[random.randint(0, len(tl7) - 1)])
    lines.append(tl5[random.randint(0, len(tl5) - 1)])
    # Split lines into parts
    lines2 = []
    for line in lines:
        lines2.append(line.split())
    # Make sure punctuation are their own parts
    lines = []
    for line in lines2:
        newline = []
        for part in line:
            if part[-1:] == ',':
                newline.append(part[:-1])
                newline.append(part[-1:])
            else:
                newline.append(part)
        lines.append(newline)

    # Generate poem from template
    prevpart = ""
    poem = []
    for line in lines:
        pline = ""
        lnstrt = 1
        for part in line:
            # Check Punctuation
            if part == ',':
                pline = pline.rstrip()
                pline += part + " "
            else:
                potentialpart = []
                index = pos.index(part[:-1]) + 1
                # Check markov
                #try:
                    # First word of a line
                if lnstrt:
                    potentialpart = mwrd[index][int(part[-1:])]
                # Other words of a line
                else:
                    if prevpart in markov:
                        tstlst = markov[prevpart]
                        for prt in tstlst:
                            if prt in mwrd[index][int(part[-1:])]:
                                potentialpart.append(prt)
                #except:
                #    potentialpart = []
                #    pass
                # Add randomly generated word to prevent duplicate frequency
                potentialpart.append("---")
                # Select part at random
                prevpart = random.choice(potentialpart)
                if prevpart == "---":
                    prevpart = random.choice(mwrd[index][int(part[-1:])])
                    if prevpart == "---":
                        prevpart = random.choice(wrd[index - 1][int(part[-1:]) - 1])
                # Add part to poem
                pline += str(prevpart) + " "
            lnstrt = 0
        # Format line and add it to poem
        pline = (pline.capitalize()).rstrip()
        poem.append(pline)
    outfile = open('out.txt', 'a')  # Opens out file in append mode
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    for line in poem:
        print(line)
        outfile.write(line + "\n")  # Writes input to txt file.
    outfile.close()  # Closes file.
    #time.sleep(5)
