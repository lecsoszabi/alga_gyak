# trafficn – rövidített legrövidebb út egy új kétirányú úttal
# először kiszámolom a legrövidebb utat s-ből minden csúcsba,
# majd t-be visszafelé egy visszafordított gráfon,
# aztán minden jelölt kétirányú útra megnézem, tud-e javítani az s-t út hosszán.

import sys
import heapq

INF = 10**18  # ezzel jelölöm azt, hogy egy csúcs jelenleg elérhetetlen

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)

def dijkstra(start, adj, n):
    """dijkstra algoritmussal kiszámolom a legrövidebb utat start-ból minden csúcsba."""
    dist = [INF] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

t = int(next(it))  # tesztesetek száma

out_lines = []

for _case in range(t):
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    s = int(next(it))
    t_node = int(next(it))

    # irányított gráf előre és visszafelé
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]

    for _ in range(m):
        d = int(next(it))
        c = int(next(it))
        l = int(next(it))
        adj[d].append((c, l))
        radj[c].append((d, l))

    candidates = []
    for _ in range(k):
        u = int(next(it))
        v = int(next(it))
        q = int(next(it))
        candidates.append((u, v, q))

    # legrövidebb utak s-ből, illetve t-be (visszafordított gráfon)
    dist_s = dijkstra(s, adj, n)
    dist_t = dijkstra(t_node, radj, n)

    ans = dist_s[t_node]  # kiindulásnak az eredeti legrövidebb s-t út

    # minden jelölt kétirányú útra megnézem a két irányt
    for u, v, q in candidates:
        if dist_s[u] != INF and dist_t[v] != INF:
            cand = dist_s[u] + q + dist_t[v]
            if cand < ans:
                ans = cand
        if dist_s[v] != INF and dist_t[u] != INF:
            cand = dist_s[v] + q + dist_t[u]
            if cand < ans:
                ans = cand

    # ha ans végtelen maradt, akkor semmilyen út nem létezik
    if ans >= INF:
        out_lines.append("-1")
    else:
        out_lines.append(str(ans))

sys.stdout.write("\n".join(out_lines) + "\n")
