def hash(s):
    o = 0
    for c in s:
        o += ord(c)
        o *= 17
        o %= 256
    return o

#print(hash('HASH'))
import sys
with open(sys.argv[1]) as f:
    steps = f.read().replace('\n', '').split(',')

boxes = [[] for i in range(256)]

def find_in_box(label, box):
    for i, (l, f) in enumerate(box):
        if label == l:
            return i
    return None

for step in steps:
    if '-' in step:
        label = step.rstrip('-')
        box = boxes[hash(label)]
        i = find_in_box(label, box)
        if i is not None:
            box.pop(i)

    else:
        label, num = step.split('=')
        num = int(num)
        box = boxes[hash(label)]
        i = find_in_box(label, box)
        if i is not None:
            box[i] = (label, num)
        else:
            box.append((label, num))

print(boxes)

power = 0
for boxi, box in enumerate(boxes):
    for lensi, (l, f) in enumerate(box):
        power += (boxi+1)*(lensi+1)*f
print(power)
