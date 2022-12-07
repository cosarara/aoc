def walk(inp):
    tree = {'size': 0, 'dirs': {}}
    pwd = []
    node = tree # ref inside tree
    for line in inp.strip().split('\n'):
        parts = line.strip().split()
        #print('parts', parts)
        if parts[0] == '$':
            if parts[1] == 'cd':
                path = parts[2]
                if path == '/':
                    pwd = []
                elif path == '..':
                    pwd.pop()
                else:
                    pwd.append(path)
                node = tree
                for p in pwd:
                    node = node['dirs'][p]
        else:
            size, name = parts
            if size == 'dir':
                node['dirs'][name] = {'size': 0, 'dirs': {}}
            else:
                size = int(size)
                tmp = tree
                tmp['size'] += size
                for p in pwd:
                    tmp = tmp['dirs'][p]
                    tmp['size'] += size
        #print(tree)
        #print(pwd, node)
    return tree

def result(node, max, name='/'):
    x = []
    if node['size'] >= max:
        x.append((node['size'], name))
    for cname, cnode in node['dirs'].items():
        x += result(cnode, max, cname)
    return x

ex = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def free(inp):
    total = 70000000
    required = 30000000
    tree = walk(inp)
    used = tree['size']
    #print('used space:', used)
    free = total-used
    #print('free space:', free)
    must_free = required-free
    #print('must free:', must_free)
    return min(result(tree, must_free))

assert free(ex) == (24933642, 'd')
with open('input') as f:
    print(free(f.read()))
