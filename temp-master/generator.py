from random import random, randint

def generate(n, m, density=0.5):
    user = []
    bs = []

    i = 1
    users_inserted = 0
    bss_inserted = 0
    done = False

    pn = 1.0 - density
    pu = 1.0 * n / (n+m) * density
    pb = 1.0 * m / (n+m) * density
    print("pn:", pn, "pu:", pu, "pb:", pb)

    while done == False:
        # Generate a random number in (0.0, 1.0]
        rand = 1 - random()
        # print("rand:", rand)
        if rand < pn:
            i += 1
            continue
        elif rand < pn + pu:
            if users_inserted < n:
                user.append(i)
                i += 1
                users_inserted += 1
                done = (users_inserted == n) and (bss_inserted == m)
        else:
            if bss_inserted < m:
                bs.append(i)
                i += 1
                bss_inserted += 1
                done = (users_inserted == n) and (bss_inserted == m)

    print("bs= " + str(bs))
    print("user= " + str(user))
    print("Expected width:", 1.0*(m+n)/density)
    print("Actual width:", max(user[-1], bs[-1]) - min(user[0], bs[0]))

def generate_even(n, m, density=0.5, d=None):
    user = []
    bs = []

    users_inserted = 0
    done = False

    fbs = randint(2, 100)
    if d == None:
        d = 1.0 * (m+n) / density / m
        d = max(2, int(d))
    bs = [fbs + d*k for k in range(0, m)]
    print("bs = ", bs)

    LL = max(1, fbs-d+1)
    UL = bs[-1] + d - 1
    pu = 1.0 * n / (n+m) * density
    aps = [x for x in range(LL, UL+1) if (x%d) != (fbs%d)]

    j = 0
    while(done == False):
        rand = random()
        if rand < pu and users_inserted < n:
            user.append(aps[j])
            users_inserted += 1
            done = (users_inserted == n)
            del aps[j]
            j = j % len(aps)
        else:
            j = (j+1) % len(aps)

    print("user = ", user)
    print("Expected width:", 1.0*(m+n)/density)
    print("Actual width:", max(user[-1], bs[-1]) - min(user[0], bs[0]))

# Check if every 2 BSs have a user in between them.
def check(user, bs):
    sorted_user = sorted(user)
    sorted_bs = sorted(bs)
    valid = True
    bs1 = -1
    bs2 = -1
    for j in range(len(sorted_bs) - 1):
        for u in sorted_user:
            if u > sorted_bs[j] and u < sorted_bs[j+1]:
                break
            if u == sorted_user[-1]:
                valid = False
                bs1, bs2 = sorted_bs[j], sorted_bs[j+1]

    if valid == True:
        print("The given users and bss are VALID.")
    else:
        print("The given users and bss are INVALID.")
        print("There are no users between basestations " + str(bs1) + " and " + str(bs2) + " .")
