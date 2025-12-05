import sys
import math
from collections import deque

INF = 10**18  # ezt csak biztonsági konstansként tartom, de itt alig kell


def egcd(a, b):
    """iteratív euklideszi kiterjesztett algoritmus, hogy legyen inverzünk mod m."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0  # a = gcd, x0*a + y0*b_eredeti = gcd


def modinv(a, m):
    """visszaadom a moduláris inverzt mod m, feltéve hogy gcd(a,m) = 1."""
    g, x, _ = egcd(a, m)
    # itt biztosan g == 1, ha jól hívjuk
    return x % m


def elevators_intersect(x1, y1, x2, y2, F):
    """
    eldöntöm, hogy a két lift megáll-e valaha ugyanazon az emeleten a [0, F-1] tartományban.
    lift1: y1, y1+x1, y1+2*x1, ...
    lift2: y2, y2+x2, y2+2*x2, ...
    """
    g = math.gcd(x1, x2)
    diff = y2 - y1

    # ha a két számtani sorozat kongruenciái eleve összeegyeztethetetlenek, nincs közös emelet
    if diff % g != 0:
        return False
        
    # megoldjuk: y1 + x1 * t ≡ y2 (mod x2)
    x1p = x1 // g
    x2p = x2 // g
    diffp = diff // g  # ez lehet negatív is, de a mod aritmetika lekezeli

    inv = modinv(x1p, x2p)  # x1p * inv ≡ 1 (mod x2p)
    t0 = (diffp * inv) % x2p  # egy konkrét megoldás t-re, 0 <= t0 < x2p

    f0 = y1 + x1 * t0  # ez egy konkrét közös megálló mindkét liftnek
    lcm = x1 * x2p     # a további közös emeletek lépésköze (lcm(x1,x2))

    low = max(y1, y2)     # ennél kisebb emelettel nem foglalkozunk
    hi = F - 1            # az épület teteje

    # ha ez a konkrét megoldás már kint van az épületből, akkor megnézzük, elvileg lejjebb lehetne-e,
    # de mivel a sorozat f0 + k*lcm, k>=0, ha f0 > hi, akkor minden további is > hi
    if f0 > hi:
        return False

    # itt f0 <= hi, de lehet hogy f0 < low, azaz túl „alacsony” a max(y1,y2)-hez képest
    if f0 < low:
        # olyan k-t keresek, hogy f = f0 + k*lcm >= low
        k = (low - f0 + lcm - 1) // lcm
        f = f0 + k * lcm
    else:
        f = f0

    # ha sikerült olyan közös emeletet találni, ami az épületen belül van, akkor van él a két lift között
    return f <= hi


def elevator_serves_floor(x, y, floor):
    """eldöntöm, hogy a (x,y) lift megáll-e a floor emeleten."""
    if floor < y:
        return False
    return (floor - y) % x == 0


# itt beolvasom az összes számot a bemenetből
data = sys.stdin.read().strip().split()
if not data:
    sys.exit(0)

it = iter(data)
T = int(next(it))

for case in range(1, T + 1):
    # F = emeletek száma, E = liftek száma, A,B = honnan hova akarom vinni a bútort
    F = int(next(it))
    E = int(next(it))
    A = int(next(it))
    B = int(next(it))

    elevators = []  # (x, y) párokat tárolok
    for _ in range(E):
        X = int(next(it))
        Y = int(next(it))
        elevators.append((X, Y))

    # ha ugyanazon az emeleten van az iroda „elvileg”, akkor nem kell mozgatni semmit
    if A == B:
        print("It is possible to move the furniture.")
        continue

    # megnézem, mely liftek szolgálják ki az A és B emeletet
    start_lifts = []
    serves_B = [False] * E

    for i, (x, y) in enumerate(elevators):
        if elevator_serves_floor(x, y, A):
            start_lifts.append(i)
        if elevator_serves_floor(x, y, B):
            serves_B[i] = True

    # ha A-n nincs egyetlen lift sem, akkor a bútor el sem tud indulni
    if not start_lifts:
        print("The furniture cannot be moved.")
        continue

    # ha már az induló liftek közül valamelyik megáll B-n is, akkor kész vagyunk
    possible = any(serves_B[i] for i in start_lifts)
    if possible:
        print("It is possible to move the furniture.")
        continue

    # gráfot építek a liftekből: él akkor van, ha van közös emelet az adott két lift között
    adj = [[] for _ in range(E)]
    for i in range(E):
        x1, y1 = elevators[i]
        for j in range(i + 1, E):
            x2, y2 = elevators[j]
            if elevators_intersect(x1, y1, x2, y2, F):
                adj[i].append(j)
                adj[j].append(i)

    # bfs a start_lifts halmazból: megnézem, el tudok-e jutni olyan liftig, ami kiszolgálja B-t
    from collections import deque
    q = deque()
    visited = [False] * E

    for s in start_lifts:
        visited[s] = True
        q.append(s)

    found = False
    while q and not found:
        u = q.popleft()
        if serves_B[u]:
            found = True
            break
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)

    if found:
        print("It is possible to move the furniture.")
    else:
        print("The furniture cannot be moved.")
