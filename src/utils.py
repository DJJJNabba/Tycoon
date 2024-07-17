def pathfind(start, end):
    # Simplified pathfinding for grid movement
    path = []
    current = start
    while current != end:
        if current[0] < end[0]:
            current = (current[0] + 1, current[1])
        elif current[0] > end[0]:
            current = (current[0] - 1, current[1])
        elif current[1] < end[1]:
            current = (current[0], current[1] + 1)
        elif current[1] > end[1]:
            current = (current[0], current[1] - 1)
        path.append(current)
    return path
