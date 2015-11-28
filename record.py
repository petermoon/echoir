import sys
import re

received = r"^received"
receiver = r"^receiver"
pulse = r"^pulse:"
space = r"^space:"

lastword = ''
signals = []

for line in sys.stdin:
    words = line.strip().split(' ')
    
    if re.search(received, words[0]) or re.search(receiver, words[0]):
        continue
    words[1] = int(words[1])
    if re.search(space, words[0]) and words[1] == 152917:
        continue

    word = re.sub(pulse, 'pulse', words[0])
    word = re.sub(space, 'space', word)

    if lastword == word:
        item = signals.pop()
        item[1] = item[1] + words[1]
        signals.append(item)
    elif lastword == '' and word == 'space':
        continue
    else:
        signals.append([word, words[1]])
    lastword = word

for i in range(len(signals)):
    if i < len(signals) - 1 or signals[i][0] != 'space':
        print("{} {}".format(*signals[i]))
