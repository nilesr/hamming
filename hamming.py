import math, random, sys, base64
length = int(sys.argv[1])
use_lines = int(sys.argv[2]) == 1
lines = []
def isparity(pos):
    return pos.count("1") == 1
blen = math.ceil(math.log2(length)) # 4
bpos = [bin(length - i)[2:].rjust(blen, "0") for i in range(length)]
ppos = [isparity(x) for x in bpos]
slen = ppos.count(False) # 7
lines.append("{},{} code".format(length, slen))
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
lines.append(" ".join(bpos))
lines.append(" ".join([str(x).rjust(blen, " ") for x in bits]))
if use_lines:
    for i in range(length)[::-1]:
        line = ""
        if not ppos[i]: continue
        inline = False
        guarded_bit = bpos[i].find("1")
        for j in range(i):
            if bpos[j][guarded_bit] == "1":
                pc = "─" if inline else " "
                uc = "┴" if inline else "└"
                for i in range(guarded_bit):
                    line += pc
                line += uc
                for i in range(blen - guarded_bit):
                    line += "─"
                inline = True
            else:
                if inline:
                    line += "─────"
                else:
                    line += "     "
        for i in range(guarded_bit):
            line += "─"
        line += "┘"
        lines.append(line)
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
    lines.append("Bit in position " + bin(pos)[2:].rjust(blen, "0") + " is invalid")
else:
    lines.append("All bits were valid")
lines = "\n".join(lines)
print(base64.b64encode(lines.encode("utf-8")).decode("ascii")) # python 2 compat hackery
