import os
import sys


def error_decorator(func):
    def wrapper(x1, y1, x2, y2, canvas):
        # error processing
        if canvas is None:
            raise Exception('Create canvas first')

        y1, y2 = y1 if y1 < y2 else y2, y2 if y2 > y1 else y1
        x1, x2 = x1 if x1 < x2 else x2, x2 if x2 > x1 else x1

        if y1 <= 0 or y2 > len(canvas)-2:
            raise Exception('Y coordinate error')
        if x1 <= 0 or x2 > len(canvas[1])-2:
            raise Exception('X coordinate error')
        # func start
        return func(x1, y1, x2, y2, canvas)

    return wrapper


def process(line, canvas):
    line = line.split()
    if line[0] == "C":
        line = [int(x) for x in line[1:]]
        return create(*line)

    elif line[0] == "L" or line[0] == "R":
        params = [int(x) for x in line[1:]]
        params.append(canvas)
        if line[0] == "L":
            return line_func(*params)
        else:
            return rectangle(*params)

    elif line[0] == "B":
        line.append(canvas)
        return fill(*line[1:])

    else:
        raise Exception("Bad file arguments or unknown command")


def create(x1, y1):

    if x1 <= 0 or y1 <= 0:
        raise Exception("Coordinates should be greater than 0")

    border = ["-" for _ in range(x1+2)]
    body = [["|"]+[" " for _ in range(x1)]+["|"] for i in range(y1)]
    body.insert(0, border)
    body.append(border)
    return body


@error_decorator
def line_func(x1, y1, x2, y2, canvas):

    if x1 != x2 and y1 != y2:
        raise Exception('Only horizontal or vertical lines are supported')

    for row in range(y1, y2+1):
        for column in range(x1, x2+1):
            canvas[row][column] = "x"

    return canvas


@error_decorator
def rectangle(x1, y1, x2, y2, canvas):

    for row in range(y1, y2+1):
            if row == y1 or row == y2:
                canvas[row][x1:x2+1] = ["x" for _ in canvas[row][x1:x2+1]]

            else:
                canvas[row][x1] = "x"
                canvas[row][x2] = "x"

    return canvas


def fill(x1, y1, color, canvas):
    x1, y1 = int(x1), int(y1)
    if x1 < 1 or y1 < 1:
        raise Exception('Coordinates error')
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
            for x3, y3 in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (point_x+x3, point_y+y3) not in cache:
                    if canvas[point_y+y3][point_x+x3] == replace_point:
                        cache.add((point_x+x3, point_y+y3))
                        stack.append((point_x+x3, point_y+y3))
    return canvas

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    input_dir = basedir + '/input/'
    input_file = input_dir + "input.txt"
    result = None

    with open(input_file, 'r') as f:
        with open('output.txt', 'w+') as f1:
            for line in f:
                result = process(line, result)
                for res in result:
                    f1.writelines("".join(res)+"\n")

    print("Job is done, look at new output!")
