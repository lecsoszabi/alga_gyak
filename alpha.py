# acode – alphacode megoldás dinamikus programozással
# azt számoljuk meg, hányféleképpen lehet az adott számjegysorozatot betűkké visszafejteni

import sys

for line in sys.stdin:
    s = line.strip()
    if not s:
        continue
    if s == "0":
        break

    n = len(s)

    # az első karakter biztosan nem 0, mert a feladat ezt garantálja
    # dp_prev2 = dp[i-2], dp_prev1 = dp[i-1]; induláskor dp[0] = 1, dp[1] = 1
    dp_prev2 = 1
    dp_prev1 = 1

    for i in range(1, n):
        ways = 0

        # egyjegyű értelmezés: ha az aktuális számjegy nem 0, akkor átvehetem dp[i-1]-et
        if s[i] != '0':
            ways += dp_prev1

        # kétjegyű értelmezés: ha az előző+aktuális együtt 10 és 26 között van
        two = int(s[i - 1:i + 1])
        if 10 <= two <= 26:
            ways += dp_prev2

        # léptetem az ablakot: mostantól dp_prev1 lesz dp[i], dp_prev2 lesz dp[i-1]
        dp_prev2, dp_prev1 = dp_prev1, ways

    # a teljes sorozat dekódolási módjainak száma dp_prev1-ben van
    print(dp_prev1)
