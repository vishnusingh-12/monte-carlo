def get_msd_old(ions, steps):
    msd = []
    for i in range(steps):
        sm = 0
        for j in ions:
            for k in range(steps):
                dx = j.position_list[i + k][0] - j.position_list[k][0]
                dy = j.position_list[i + k][1] - j.position_list[k][1]
                dr2 = dx ** 2 + dy ** 2
                sm = sm + dr2
        msd.append(sm / (steps * len(ions)))
    return msd
