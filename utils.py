def calculate_score(work, lost, social, entertainment, target, completed):
    score = 0
    socialEnt = soc_ent(social, entertainment) / 10  # 4
    completion = completed / target  # 4
    determination = work / lost  # 2

    score = (4 * socialEnt) + (4 * completion) + (2 * determination)

    if (score > 10):
        score = 10
    else:
        score = score

    return score


def soc_ent(social, entertainment):
    temp = social + entertainment

    if (temp == 0):
        return 10
    if (0 < temp <= 15):
        return 8
    if (16 < temp <= 30):
        return 7
    if (31 < temp <= 45):
        return 6
    if (46 < temp <= 60):
        return 5
    if (60 < temp <= 75):
        return 4
    if (76 < temp <= 90):
        return 3
    if (90 < temp <= 120):
        return 2
    if (120 < temp):
        return 1


print(soc_ent(15, 30)/10)
