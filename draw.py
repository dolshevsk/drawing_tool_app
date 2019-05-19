import os
import sys


def process(line, canvas):
    line = line.split()
    if line[0] == "C":
        line = [int(x) for x in line[1:]]
        return create(*line)
    elif line[0] == "L" or line[0] == "R":
        line = [int(x) for x in line[1:]]
        line.append(canvas)
        if line[0] == "L":
            return line(*line)
        else:
            return rectangle(*line)
    elif line[0] == "B":
        line.append(canvas)
        return fill(*line[1:])
    else:
        print(line)
        raise Exception("Bad file arguments or unknown command")


def create(x1, y1):

    if x1 <= 0 or y1 <= 0:
        raise Exception("Coordinates should be greater than 0")
    border = ["-" for _ in range(x1+2)]
    body = [["|"]+[" " for _ in range(x1)]+["|"] for i in range(y1)]
    body.insert(0, border)
    body.append(border)
    return body


def line(x1, y1, x2, y2, canvas):

    if canvas is None:
        raise Exception('Create canvas first')
    if x1 != x2 and y1 != y2:
        raise Exception('Only horizontal or vertical lines are supported')
    y1, y2 = y1 if y1 < y2 else y2, y2 if y2 > y1 else y1
    x1, x2 = x1 if x1 < x2 else x2, x2 if x2 > x1 else x1

    if y1 <= 0 or y2 > len(canvas)-2:
        raise Exception('Y coordinate error')
    if x1 <= 0 or x2 > len(canvas[1])-2:
        raise Exception('X coordinate error')

    for row in range(y1, y2+1):
        for column in range(x1, x2+1):
            canvas[row][column] = "x"

    return canvas


def rectangle(x1, y1, x2, y2, canvas):
    y1, y2 = y1 if y1 < y2 else y2, y2 if y2 > y1 else y1
    x1, x2 = x1 if x1 < x2 else x2, x2 if x2 > x1 else x1

    if canvas is None:
        raise Exception('Create canvas first')

    for row in range(y1, y2+1):
            if row == y1 or row == y2:
                canvas[row][x1:x2+1] = ["x" for _ in canvas[row][x1:x2+1]]

            else:
                canvas[row][x1] = "x"
                canvas[row][x2] = "x"

    return canvas


def fill(x1, y1, color, canvas):
    x1, y1 = int(x1), int(y1)
    if canvas is None:
        raise Exception('Create canvas first')
    if color is None or len(str(color)) > 1:
        raise Exception('Invalid color, can be only 1 character')

    replace_point = canvas[y1][x1]
    visited = set()
    cache = set()

    stack = [(x1, y1)]
    while stack:
        point_x, point_y = stack.pop()
        if (point_x, point_y) not in visited:
            visited.add((point_x, point_y))
            canvas[point_y][point_x] = str(color)
    #  made with 2 if because check in set always O(1)
            if (point_x-1, point_y) not in cache:
                if canvas[point_y][point_x-1] == replace_point:
                    cache.add((point_x-1, point_y))
                    stack.append((point_x-1, point_y))

            if (point_x+1, point_y) not in cache:
                if canvas[point_y][point_x+1] == replace_point:
                    cache.add((point_x+1, point_y))
                    stack.append((point_x+1, point_y))

            if (point_x, point_y-1) not in cache:
                if canvas[point_y-1][point_x] == replace_point:
                    cache.add((point_x, point_y-1))
                    stack.append((point_x, point_y-1))

            if (point_x, point_y+1) not in cache:
                if canvas[point_y+1][point_x] == replace_point:
                    cache.add((point_x, point_y+1))
                    stack.append((point_x, point_y+1))

    return canvas

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    input_dir = basedir + '/input/'
    input_files = [input_dir + f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    result = None

    for file in input_files:
        with open(file, 'r') as f:
            with open(file[:-4]+'_result.txt', 'w+') as f1:
                for line in f:
                    result = process(line, result)
                    for res in result:
                        f1.writelines("".join(res)+"\n")

    print("Job is done, look at new output!")
