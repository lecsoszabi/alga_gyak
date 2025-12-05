# CSES - Reading Books
# Két olvasó elolvassa az összes könyvet, de ugyanazt a könyvet nem olvashatják egyszerre.
# Minimum teljes idő = max(összes idő, leghosszabb könyv kétszerese).

import sys

# Input beolvasása
data = sys.stdin.read().strip().split()
n = int(data[0])

times = []
for i in range(1, 1 + n):
    times.append(int(data[i]))

# Összes olvasási idő kiszámítása
total_time = 0
for t in times:
    total_time += t

# Leghosszabb könyv meghatározása
longest = times[0]
for t in times[1:]:
    if t > longest:
        longest = t

# Minimális lehetséges teljes idő
result = total_time
if 2 * longest > result:
    result = 2 * longest

# Eredmény kiírása
print(result)