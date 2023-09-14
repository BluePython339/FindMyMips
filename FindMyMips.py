import os
import re
import random
import sys



def ToInteger(abBinary): 
    #converts a binary string to an integer
    return ord(abBinary[0]) | (ord(abBinary[1]) << 8) | (ord(abBinary[2]) << 16) | (ord(abBinary[3]) << 24)



def compute_score(base_addr, bin_strings, references):
    score = 0

    # Iterate through each dwStringOffset in aStrings
    for string_offset in bin_strings:
        # Check if the reference exists at dwStringOffset + lpBaseAddr
        if string_offset + base_addr in references:
            # Increment the score if the reference exists
            score += 1

    # Return the final score
    return score


def pick_pivot_point(filename):
    data = os.popen(f"strings -t x -n 10 {filename}").read()

    #filtering out the offset and string pairs
    re_data = re.findall(r"^\s*([0-9a-f]+)\s(.*)", data, re.MULTILINE)
    bin_strings = []
    pivots = []

    for match in re_data:
        offset = int(match[0], 16)
        bin_strings.append(offset)

        if "%d" in match[1]:
            oPivot = {
                "dwOffset": offset,
                "szString": match[1]
            }
            pivots.append(oPivot)

    pivot = pivots[random.randrange(0, len(pivots))]

    return pivot, bin_strings
    

def get_decomp(filename):
    data = os.popen(f"mips-linux-gnu-objdump -b binary -m mips -EB -D {filename}").read()

    pattern_refs = r'lui\s+([astv][0-9]+),0x([0-9a-f]*)' #finding the load upper immediate (lui)
    pattern_supp = r'addiu\s+{}\s*,{}\s*,(-?[0-9]+)' # find the add immediate (addi)
    matches_refs = list(re.finditer(pattern_refs, data))
    references = {}
    for match_ref in matches_refs:
        register, hexvalue = match_ref.groups()
        dwValueMsh = int(hexvalue, 16)
        dwOffset = match_ref.start()
        start_offset = data[dwOffset:dwOffset + 220]

        match_supp = re.search(pattern_supp.format(re.escape(register), re.escape(register)), start_offset) #attempts to find the matching addi


        if match_supp:
            dwValueLsh = int(match_supp.group(1))
            ref = (dwValueMsh << 16) + dwValueLsh
            references[ref] = True

    return references


def main(filename: str):
    pivot, bin_strings = pick_pivot_point(filename)
    references = get_decomp(filename)

    scores = {}
    for ref in references:
        base_addr = ref - pivot["dwOffset"]
        score = compute_score(base_addr, bin_strings, references)
        scores[base_addr] = score

    sorted_scores = sorted(scores, reverse=True, key=scores.get)
    print("[*] best guesses addr => score")
    for k in sorted_scores[:10]:
        print(f"{hex(k)} : {scores[k]}")



if __name__ == '__main__':
    main(sys.argv[1])
        





