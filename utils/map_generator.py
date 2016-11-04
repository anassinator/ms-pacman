import cPickle
import Queue

mapmat = []

with open("map1.csv") as f:
    for line in f:
        row = []
        for c in line.split(","):
            row.append(int(c))
        mapmat.append(row)

mapdic = {}
cellqueue = Queue.Queue()
cellqueue.put((0, 0))

while not cellqueue.empty():
    c = cellqueue.get()
    neighbors = []
    if (c[0] + 18, c[1] + 2) in mapdic.keys():
        continue
    for n in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        x = c[0] + n[0]
        y = c[1] + n[1]
        if x < 0 or y < 0 or x >= len(mapmat[0]) or y >= len(mapmat):
            continue
        elif mapmat[y][x] == 1:
            neighbors.append((x + 18, y + 2))
            if (x + 18, y + 2) not in mapdic.keys():
                cellqueue.put((x, y))

    mapdic[(c[0] + 18, c[1] + 2)] = neighbors

with open("map1.pkl", 'wb') as f:
    cPickle.dump(mapdic, f)
