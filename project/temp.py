bob = []
with open("playlists.txt") as f:
    line = f.readline().rstrip()
    while line:
        line = f.readline().rstrip()
        if line:
            line2 = line.split(',')
            bob.append([line2[2], line2[3]])



print(bob[0])
