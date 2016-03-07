import sys

Inf = 100000000 # orizoume: infinity = very very large integer


###################################
### leitourgies priority queue  ###
###################################

def create_queue(maxNode):
    pq = []
    for i in range(maxNode + 1):
        pq.append(-1) # -1 simainei oti o komvos i den einai sto queue

    return pq


def insert(pq, i, d):
    pq[i] = d


def update(pq, i, d):
    pq[i] = d


def extractMin(pq):
    minVal = Inf

    for node, val in enumerate(pq):
        if val != -1 and val < minVal:
            minVal = val
            minNode = node

    pq[minNode] = -1 # afairoume ton komvo
    return minNode


def size(pq):
    count = 0;
    for val in pq:
        if val != -1:
            count += 1

    return count


###################################
###    algorithmos dijkstra     ###
###################################

def dijkstra(adjacency, costs, blocked, source, dest, maxNode):
    pred = dict()
    dist = dict()

    for node in adjacency:
        pred[node] = -1 # -1 simainei pws den yparxei predecessor
        if node == source:
            dist[node] = 0
        else:
            dist[node] = Inf

    pq = create_queue(maxNode)
    insert(pq, source, dist[source])

    while size(pq) != 0:
        u = extractMin(pq)

        # ftasame!
        if u == dest:
            break

        for v in adjacency[u]:
            if dist[v] > dist[u] + costs[(u, v)]:
                dist[v] = dist[u] + costs[(u, v)]
                pred[v] = u

                if v in pq:
                    update(pq, v, dist[v])
                else:
                    insert(pq, v, dist[v])

    # dimiourgoume to monopati akolouthontas 
    # anapoda tous predecessors
    path = []
    u = dest
    while pred[u] != -1:
        path.insert(0, u)
        u = pred[u]
    path.insert(0, u)

    return path, dist[dest]


###################################
###      kyriws programma       ###
###################################

# diavasma parametrwn
if len(sys.argv) < 4:
    print("Wrong arguments")
    sys.exit()

graph_fname = sys.argv[1]
source = int(sys.argv[2])
dest = int(sys.argv[3])

if '-r' in sys.argv:
    reposition = True
else:
    reposition = False

if '-b' in sys.argv:
    blocked_fname = sys.argv[sys.argv.index('-b') + 1]
else:
    blocked_fname = None


# diavasma grafou
adjacency = dict() # edw tha kratame tis listes geitniasis gia kathe komvo
costs = dict() # edw tha kratame ta kosti gia kathe zevgos komvwn
maxNode = -1 # to xreiazomaste gia tin arxikopoiisi tis priority queue

gf = open(graph_fname, 'r')
for line in gf:
    values = line.split()
    node1 = int(values[0])
    node2 = int(values[1])
    cost = int(values[2])

    if node1 in adjacency:
        adjacency[node1].append(node2)
    else:
        adjacency[node1] = [node2]
    costs[(node1, node2)] = cost

    if node2 in adjacency:
        adjacency[node2].append(node1)
    else:
        adjacency[node2] = [node1]
    costs[(node2, node1)] = cost

    if node1 > maxNode:
        maxNode = node1
    if node2 > maxNode:
        maxNode = node2

gf.close()

# diavasma blocked
blocked = set()
if blocked_fname is not None:
    bf = open(blocked_fname, 'r')
    for line in bf:
        values = line.split()
        node1 = int(values[0])
        node2 = int(values[1])

        blocked.add((node1, node2))
        blocked.add((node2, node1))

    bf.close()

found = False
full_path = []
full_dist = 0
while not found:
    # prwta ekteloume dijkstra gia na vroume to monopati agnoontas ta blocked
    path, dist = dijkstra(adjacency, costs, blocked, source, dest, maxNode)

    found = True
    part_dist = 0 # prepei na kratame to kostos mexri na blockaristoume

    # tha elegksoume tous komvous tou monopatiou enan-enan gia blocked
    for i in range(len(path) - 1):
        if (path[i], path[i + 1]) not in blocked:
            # oxi blocked, prosthese to kostos
            part_dist += costs[(path[i], path[i + 1])]
        else:
            # blocked, diegrapse to zevgari aptis listes geitniasis
            for j in range(len(adjacency[path[i]])):
                if adjacency[path[i]][j] == path[i + 1]:
                    del adjacency[path[i]][j]
                    break
            for j in range(len(adjacency[path[i + 1]])):
                if adjacency[path[i + 1]][j] == path[i]:
                    del adjacency[path[i + 1]][j]
                    break

            if (reposition):
                # prepei na ypologistei kai to monopati epistrofis
                return_path = path[1:i + 1]
                return_path.reverse()
                full_path += path[:i] + return_path
                full_dist += part_dist * 2
            else:
                # mas noiazei mono to monopati ews edw
                full_path += path[:i]
                full_dist += part_dist
                source = path[i]
            found = False
            break

# prosthetoume to teliko monopati
full_path += path
full_dist += dist

print(full_path)
print(full_dist)
