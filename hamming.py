import math, random, sys
length = 11 + random.randint(0, 1)

def isparity(pos):
    return pos.count("1") == 1
blen = math.ceil(math.log2(length)) # 4
bpos = [bin(length - i)[2:].rjust(blen, "0") for i in range(length)]
ppos = [isparity(x) for x in bpos]
slen = ppos.count(False) # 7
print("{},{} code".format(length, slen))
bits = []
# generate bits or parity bits
for i in range(length):
    if ppos[i]:
        this_bpos = bpos[i]
        guarded_bit = this_bpos.find("1")
        count = 0;
        for j in range(i):
            if bpos[j][guarded_bit] == "1":
                count += bits[j]
        parity = count & 1
        bits.append(parity)
    else:
        bits.append(random.randint(0, 1))
# fuck with it
bits[random.randint(0, length - 1)] = random.randint(0, 1)
# print out bits
print(" ".join(bpos))
print(" ".join([str(x).rjust(blen, " ") for x in bits]))
for i in range(length)[::-1]:
    if not ppos[i]: continue
    inline = False
    guarded_bit = bpos[i].find("1")
    for j in range(i):
        if bpos[j][guarded_bit] == "1":
            pc = "─" if inline else " "
            uc = "┴" if inline else "└"
            for i in range(guarded_bit):
                sys.stdout.write(pc)
            sys.stdout.write(uc)
            for i in range(blen - guarded_bit):
                sys.stdout.write("─")
            inline = True
        else:
            if inline:
                sys.stdout.write("─────")
            else:
                sys.stdout.write("     ")
    for i in range(guarded_bit):
        sys.stdout.write("─")
    sys.stdout.write("┘\n")
# begin verification
invalid = []
for i in range(length):
    if not ppos[i]: continue
    guarded_bit = bpos[i].find("1")
    count = 0
    for j in range(i):
        if bpos[j][guarded_bit] == "1":
            count += bits[j]
    parity = count & 1
    valid = parity == bits[i]
    if not valid:
        invalid.append(i)
#print(invalid)
if len(invalid) > 0:
    pos = 0
    for invpos in invalid:
        pos |= int(bpos[invpos], 2)
    print("Bit in position " + bin(pos)[2:].rjust(blen, "0") + " is invalid")
else:
    print("All bits were valid")
