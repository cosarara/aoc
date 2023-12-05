with open("input.txt") as f:
    content = f.read()

## parse everything
sections = content.strip('\n').split('\n\n')
seeds_flat = [int(s) for s in sections[0].split(': ')[1].strip().split()]
seeds = []
for i in range(len(seeds_flat)//2):
    seeds.append(seeds_flat[i*2:i*2+2])

print(seeds)

maps = []
titles = []
for section in sections[1:]:
    lines = section.split('\n')
    titles.append(lines[0])
    ranges = []
    for line in lines[1:]:
        dst, src, length = [int(s) for s in line.split()]
        ranges.append((dst, src, length))
    maps.append(ranges)

## calculate

def map_ranges(input, mapping, shift):
    (start_1, length_1), (start_2, length_2) = input, mapping
    end_1 = start_1+length_1
    end_2 = start_2+length_2
    # if range 2 begins inside range 1
    if start_1 <= start_2 and start_1+length_1 >= start_2:
        # we let unmapped the part before the mapping
        unmapped = [(start_1, start_2-start_1)]
        # if range 2 ends inside range 1
        if end_2 < end_1:
            # we let the end bit unmapped
            unmapped.append((end_2, end_1-end_2))
        mapped = (start_2+shift, min(end_1, end_2)-start_2)
        return mapped, unmapped

    # if range 1 begins inside range 2
    if start_2 <= start_1 and start_2+length_2 >= start_1:
        # if range 1 ends outside range 2
        if end_1 > end_2:
            mapped = (start_1+shift, end_2-start_1)
            unmapped = [(end_2, end_1-end_2)]
            return mapped, unmapped
        # range 1 ends inside range 2 (fully mapped)
        mapped = (start_1+shift, length_1)
        unmapped = []
        return mapped, unmapped
    return None

#print(ranges_overlap((79, 14), (98, 2)))
#print(ranges_overlap((75, 10), (79, 14)))

#print(maps)
def main():
    results = []
    unmapped_ranges = seeds
    output_ranges = []
    for title, map in zip(titles, maps):
        new_output_ranges = []
        for dst, src, length in map:
            shift = dst - src
            new_unmapped_ranges = []
            for range in unmapped_ranges:
                overlap = map_ranges(range, (src, length), shift)
                if overlap:
                    mapped, unmapped = overlap
                    #print('overlap between', range, (src, length))
                    #print('mapped, unmapped:', mapped, unmapped)
                    new_output_ranges.append(mapped)
                    new_unmapped_ranges += [(s, l) for (s, l) in
                                            unmapped if l]
                else:
                    new_unmapped_ranges.append(range)
            unmapped_ranges = new_unmapped_ranges
        new_output_ranges += unmapped_ranges
        print(new_output_ranges)
        unmapped_ranges = new_output_ranges

    print(new_output_ranges)
    print(min(r for r, l in new_output_ranges if l))

if __name__ == "__main__":
    main()
