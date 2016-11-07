def color(arrows):
    """Given arrows, return the minimum number of colors required to color
    them."""
    # Debugged
    # An arrow is specified as (tail, head) pair.

    colors_used = 0
    left_arrows_rj = larj = {}
    right_arrows_rj = rarj = {}
    coloring = {}

    # Sort the arrows in left-to-right order of their left end points.
    arrows.sort(key=lambda x: min(x[0], x[1]))
    # print("arrows", arrows)
    for ai in arrows:
        colors = []
        for c in range(1, colors_used+1):
            if ai[0] < ai[1]:
                if rarj[c] < ai[0] and larj[c] < ai[1]:
                    colors.append(c)
            if ai[1] < ai[0]:
                if rarj[c] < ai[1] and larj[c] < ai[1]:
                    colors.append(c)
        # print("colors_used", colors_used)
        # print("arrow", ai, "colors", colors)

        if colors != []:
            rjs = [max(larj[c], rarj[c]) for c in colors]
            color_for_ai = cfai = colors[rjs.index(max(rjs))]
            coloring[ai] = cfai

            if ai[0] < ai[1] and rarj[cfai] < ai[1]:
                rarj[cfai] = ai[1]
            if ai[1] < ai[0] and larj[cfai] < ai[0]:
                larj[cfai] = ai[0]
        else:
            colors_used += 1
            coloring[ai] = colors_used
            if ai[0] < ai[1]:
                rarj[colors_used] = ai[1]
                larj[colors_used] = -1
            if ai[1] < ai[0]:
                larj[colors_used] = ai[0]
                rarj[colors_used] = -1
    # print("larj", larj, "rarj", rarj)
    return colors_used

if __name__ == '__main__':
    arrows = [(3,10), (1,5), (14,11), (9,12), (8,4)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 3
    print()

    arrows = [(1,3), (4,6), (8,11), (12,19)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 1
    print()

    arrows = [(3,1), (6,4), (8,11), (19,12)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 1
    print()

    arrows = [(2,5), (4,7), (6,9), (8,11)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 2
    print()

    arrows = [(5,2), (7,4), (9,6), (11,8)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 2
    print()

    arrows = [(8,5), (7,10)]
    print("arrows:", arrows)
    colors = color(arrows)
    print('Colors used:', colors)
    assert colors == 1
    print()
