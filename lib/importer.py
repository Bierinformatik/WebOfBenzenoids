

def bec_to_hex_list(bec):
    """
    Return list of hexagons in a benzenoid defined by a given BEC.
    """
    male_neigh = [(0, 1), (1, 0), (-1, 0)]
    female_neigh = [(1, 0), (0, -1), (-1, 0)]

    def is_male_vertex(vx, vy):
        return (vx + vy) % 2 == 0

    if bec == '6':  # Benzene is an exception.
        return [(0, 0)]

    vert_lines = {}

    vx, vy = 0, 0
    dir = 0
    for c in bec:
        for i in range(int(c)):
            # print(vx, vy)
            # Make a step.
            if is_male_vertex(vx, vy):
                if dir == 0:
                    # We are on the left of hexagon ((vx - vy) // 2, vy).
                    hx, hy = (vx - vy) // 2, vy
                    if hy not in vert_lines:
                        vert_lines[hy] = [hx]
                    else:
                        vert_lines[hy].append(hx)
                vx += male_neigh[dir][0]
                vy += male_neigh[dir][1]
            else:
                if dir == 1:
                    # We are on the left of hexagon ((vx - vy + 1) // 2, vy - 1).
                    hx, hy = (vx - vy + 1) // 2, vy - 1
                    if hy not in vert_lines:
                        vert_lines[hy] = [hx]
                    else:
                        vert_lines[hy].append(hx)
                vx += female_neigh[dir][0]
                vy += female_neigh[dir][1]
                dir = (dir + 1) % 3
        # We arrived at a 3-valent vertex.
        dir = (dir - 1 + 3) % 3
    # print(vx, vy)

    hex_list = []

    for hy, lst in vert_lines.items():
        lst.sort()
        assert len(lst) % 2 == 0
        for i in range(0, len(lst) - 1, 2):
            left, right = lst[i], lst[i+1]
            for k in range(left, right):
                hex_list.append((hy, k))

    return hex_list

if __name__ == '__main__':
    code = '53335111'
    print(bec_to_hex_list(code))

