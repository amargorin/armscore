
def set_pair(final = 0):
    state = 0
    r = None
    b = None
    for line in match:
        if line['act']:
            if state == 1:
                if (line['group'] == r['group']) or final:
                    b = line
                    break
            if state == 0:
                r = line
                state = 1
    return r, b