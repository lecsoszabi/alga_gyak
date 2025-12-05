# CSES - Room Allocation
# Cél: minimális szobaszám, plusz minden vendéghez szobaszám hozzárendelése.

import sys
import heapq  # prioritási sor (min-heap) a legkorábban felszabaduló szoba követéséhez

data = sys.stdin.read().strip().split()
n = int(data[0])

# Vendégek tárolása: (érkezés, távozás, eredeti_index)
customers = []
idx = 1
for i in range(n):
    a = int(data[idx])
    b = int(data[idx + 1])
    idx += 2
    customers.append((a, b, i))

# Érkezési nap szerint rendezzük a vendégeket
customers.sort(key=lambda x: x[0])

# Heap elemei: (távozási_nap, szobaszám)
rooms_heap = []

# Eredmény tömb: minden vendég eredeti sorrendben kap egy szobaszámot
answer = [0] * n

# Eddig használt szobák száma (maximum értéke lesz a válasz k)
room_count = 0

for a, b, original_index in customers:
    # Felszabadult-e olyan szoba, ahol a vendég távozási napja < új vendég érkezési napja?
    # (Szöveg szerint csak akkor lehet újra használni, ha távozási_nap < érkezési_nap.)
    if rooms_heap and rooms_heap[0][0] < a:
        # Legkorábban felszabadult szoba újrafelhasználása
        _, room_id = heapq.heappop(rooms_heap)
    else:
        # Új szoba nyitása
        room_count += 1
        room_id = room_count

    # Ezt a szobát hozzárendeljük az aktuális vendéghez
    answer[original_index] = room_id

    # Szoba új távozási nappal vissza a heap-be
    heapq.heappush(rooms_heap, (b, room_id))

# Először a minimális szobaszám
print(room_count)
# Utána minden vendég szobaszáma az eredeti bemeneti sorrendben
print(" ".join(map(str, answer)))