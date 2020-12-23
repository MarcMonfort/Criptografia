
f = open("./2020_09_10_12_29_04_marc.monfort.Cifrado", "r")

""" 
Generate a frequency list of letters. The letter with more
occurences probably is the letter 'e' (English text).
"""
all_freq = {}

for line in f:
    for i in line:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1

sorted = {k: v for k, v in sorted(all_freq.items(), key=lambda item: item[1])}
print(str(sorted))

f = open("./2020_09_10_12_29_04_marc.monfort.Cifrado", "r")

result = open("./solved_cesar.txt", "w")

""" 
The values depends on the padding of the text.
The letter 'e' is the most common in English texts.
ord('⎰') - ord('e') = 9035

After testing with 9035, there are some letters that
still dont change, because they made a flip on the
alphabet when applying Cesar. Check which ones dont change
and use the new value for them.
ord('⎥') - ord('t') = 9009
"""

for line in f:
    n_line = ""
    for c in line:
        aux = (ord(c)-9035)
        if (aux < 70) or (aux > 122): # Range without change
            n_line = n_line + c
        elif (aux < 97):
            aux2 = (ord(c) - 9009)
            n_line = n_line + chr(aux2)
        else:
            n_line = n_line + chr(aux)
    result.write(n_line)
result.close()


# Copyright Marc Monfort


