import pygame
import math
import time
import pygame.gfxdraw
import random
import copy

POINT_SIZE = 5
LINE_THICKNESS = 6
W = 1000
H = 400
GAME_SPEED = 30
clDkYellow = (200, 200, 0)
clYellow = (255, 255, 0)
clBlack = (0, 0, 0)
clGreen = (0, 255, 0)
clRed = (255, 0, 0)
clGray = (120, 120, 120)
LMB = 1
RMB = 3
MODE_NONE = 0
MODE_NEW_LINE = 1
MODE_DRAG = 2
MODE_RUN = 100
X = 0
Y = 1
CAR_COUNT = 10
# CAR_STOP = 0CAR_MOVE = 1

params = {
    "points": [],
    "highlight": None,  # coordinates of highlighted point
    "selection": None,  # index of selected point
    "mode": MODE_NONE,
    "drag": None,
}


class Car:
    graph = None

    @staticmethod
    def initialize_static_var(g):
        Car.graph = g

    @staticmethod
    def get_random_point():
        segment = random.randrange(len(Car.graph["s"]))
        segm_pos = random.random()
        p1 = Car.graph["s"][segment][0]
        p2 = Car.graph["s"][segment][1]
        p1 = Car.graph["p"][p1]
        p2 = Car.graph["p"][p2]
        p = [p1[0] + (p2[0] - p1[0]) * segm_pos, p1[1] + (p2[1] - p1[1]) * segm_pos]
        return {"xy": p, "segment": segment}

    def make_route(self, dest):
        # делаем маршрут от текущей до параметра
        tg = copy.deepcopy(Car.graph)
        # убираем текущую, делаем из неё 2 отрезка во временном графе
        ps = tg["s"].pop(self.pos["segment"])

        tg["s"].append((len(tg["p"]), ps[0]))
        tg["s"].append((len(tg["p"]), ps[1]))
        tg["p"].append(self.pos["xy"])

        # убираем конечную, делаем из неё 2 отрезка во временном графе
        if self.pos["segment"] < dest["segment"]:
            dest["segment"] -= 1

        ps = tg["s"].pop(dest["segment"])
        tg["s"].append((len(tg["p"]), ps[0]))
        tg["s"].append((len(tg["p"]), ps[1]))
        tg["p"].append(self.pos["xy"])
        pass

    def tick(self):
        if len(self.stops) > 0:
            self.queue = self.make_route(self.stops.pop(0))

    def __init__(self):
        self.pos = Car.get_random_point()
        # self.angle = 0.0        # self.charge = 100.0

        self.queue = []  # текущий маршурт
        self.stops = []  # запланированные точки останова

        self.stops.append(Car.get_random_point())
        self.tick()
        self.route = self.make_route()

    def __str__(self):
        return f"pos:{self.pos} angle:{self.angle}"


def get_dist(pt1, pt2) -> float:
    return math.sqrt(math.pow(pt1[X] - pt2[X], 2) + math.pow(pt1[Y] - pt2[Y], 2))


def prepare_action(params: dict):

    def segment_intersect(start1, end1, start2, end2):
        epsilon = 0.1

        # проверяем, не лежат ли точки очень рядом
        if get_dist(start1, start2) < epsilon:
            return None
        if get_dist(start1, end2) < epsilon:
            return None
        if get_dist(end1, start2) < epsilon:
            return None
        if get_dist(end1, end2) < epsilon:
            return None

        #  Рассчитать коэффициенты уравнений прямых, содержащих отрезки
        A1 = end1[Y] - start1[Y]
        B1 = start1[X] - end1[X]
        C1 = A1 * start1[X] + B1 * start1[Y]

        A2 = end2[Y] - start2[Y]
        B2 = start2[X] - end2[X]
        C2 = A2 * start2[X] + B2 * start2[Y]

        #  Рассчитать определитель
        det = A1 * B2 - A2 * B1

        # Если определитель равен нулю, отрезки параллельны или совпадают
        if det == 0:
            return None

        #  Найти координаты точки пересечения
        intersect_x = (B2 * C1 - B1 * C2) / det
        intersect_y = (A1 * C2 - A2 * C1) / det

        # Проверить, находится ли точка пересечения на отрезках
        if (
            min(start1[X], end1[X]) <= intersect_x <= max(start1[X], end1[X])
            and min(start1[Y], end1[Y]) <= intersect_y <= max(start1[Y], end1[Y])
            and min(start2[X], end2[X]) <= intersect_x <= max(start2[X], end2[X])
            and min(start2[Y], end2[Y]) <= intersect_y <= max(start2[Y], end2[Y])
        ):
            return (intersect_x, intersect_y)
        else:
            return None

    apoints = []
    tmpgraph = []
    # делаем из всех отрезков плоский список
    for line_index in range(len(params["points"])):
        pt_count = len(params["points"][line_index])
        for pt_index in range(pt_count - 1):
            apoints.append(params["points"][line_index][pt_index])
            tmpgraph.append((len(apoints) - 1, len(apoints)))
        # add last point
        apoints.append(params["points"][line_index][pt_count - 1])
        del pt_index, pt_count
    del line_index

    # проверяем каждый отрезок на возможное пересечение с другим
    # если пересекается - добавляем точку / новые 4 отрезка, старые 2 отрезка удаляем
    curr_index = 0
    while curr_index < len(tmpgraph) - 1:
        # print(f"curr: {curr_index} (total: {len(tmpgraph)}) --- ")
        cmp_index = curr_index + 1
        while cmp_index < len(tmpgraph):

            # print(f"\tcmp: {cmp_index}   {tmpgraph[curr_index]},  {tmpgraph[cmp_index]}")
            # print(f"\tcmp: {cmp_index:02}  ", end="")

            isect = segment_intersect(
                apoints[tmpgraph[curr_index][0]],
                apoints[tmpgraph[curr_index][1]],
                apoints[tmpgraph[cmp_index][0]],
                apoints[tmpgraph[cmp_index][1]],
            )

            if isect is not None:
                isect_point_index = len(apoints)
                apoints.append(isect)
                tmpgraph.append((tmpgraph[curr_index][0], isect_point_index))
                tmpgraph.append((tmpgraph[curr_index][1], isect_point_index))
                tmpgraph.append((tmpgraph[cmp_index][0], isect_point_index))
                tmpgraph.append((tmpgraph[cmp_index][1], isect_point_index))
                tmpgraph.pop(curr_index)
                tmpgraph.pop(cmp_index - 1)
                # if cmp_index > 1:
                cmp_index = curr_index + 1
                # print("\t\t", end="")
                # for zzz in range(len(tmpgraph)):
                #     print(f"{zzz}:{tmpgraph[zzz]}  ", end="")
                # print()

            else:
                cmp_index += 1

            # if isect is not None:
            #     print(f"OK ", end="")
            # else:
            #     print(" * ", end="")
            # # for zzz in range(len(tmpgraph)):
            # #     print(f"{zzz}:{tmpgraph[zzz]}  ", end="")
            # print()

        curr_index += 1

    # делаем 2 массива, один для отображения (с цветами), второй для расчётов (с обратными отрезками и расстояниями)
    # добавляем обратные отрезки в граф также добавляем дистанцию и цвет
    graph_draw = []
    graph_calc = {}
    for g in tmpgraph:
        p0 = g[0]
        p1 = g[1]
        graph_draw.append(
            {"s": p0, "e": p1, "color": (random.randint(20, 255), random.randint(10, 255), random.randint(10, 255))}
        )

        # d = get_dist(apoints[p0], apoints[p1])
        # if not (p0 in graph_calc):
        #     graph_calc[p0] = {}
        # graph_calc[p0][p1] = d
        # if not (p1 in graph_calc):
        #     graph_calc[p1] = {}
        # graph_calc[p1][p0] = d

    params.update(
        {
            "g": {
                "p": apoints,
                #   "l": graph_calc,
                "s": tmpgraph,
            },
            "draw": graph_draw,
            "cars": [],
        }
    )
    Car.initialize_static_var(params["g"])
    for c in range(CAR_COUNT):
        params["cars"].append(Car())

    for c in params["cars"]:
        print(c)
    return params


def process_mousedown(pt, button, params):
    test_point = get_point_under_mouse(pt, params["points"])
    test_line = get_line_under_mouse(pt, params["points"])
    if params["mode"] == MODE_NONE:
        if test_point is not None:
            # point under mouse detected
            if button == LMB:
                # start drag
                params["drag"] = test_point[1]
                params["mode"] = MODE_DRAG
            elif button == RMB:
                # remove point
                params["points"][test_point[1][0]].pop(test_point[1][1])
                if len(params["points"][test_point[1][0]]) == 1:
                    params["points"].pop(test_point[1][0])
        elif test_line is not None:
            # line under mouse
            params["points"][test_line[1][0]].insert(test_line[1][1] + 1, test_line[0])
        else:
            # none under mouse - start new line

            # line_count = len(params["points"])
            params["points"].append([pt, pt])
            l = len(params["points"])
            params["drag"] = [l - 1, len(params["points"][l - 1]) - 1]
            params["mode"] = MODE_NEW_LINE
    elif params["mode"] == MODE_NEW_LINE:
        params["mode"] = MODE_NONE
    return params


def process_move(pt, params):
    if params["mode"] == MODE_DRAG:
        params["points"][params["drag"][0]][params["drag"][1]] = pt
        params["highlight"] = pt

    elif params["mode"] == MODE_NONE:
        test_point = get_point_under_mouse(pt, params["points"])
        if test_point is not None:
            # point under mouse detected
            params["highlight"] = test_point[0]
        else:
            test_line = get_line_under_mouse(pt, params["points"])
            if test_line is not None:
                # line under mouse
                params["highlight"] = test_line[0]
            else:
                params["highlight"] = None

    elif params["mode"] == MODE_NEW_LINE:
        params["points"][params["drag"][0]][params["drag"][1]] = pt
        # params["drag"] = test_point[1]


def process_mouseup(pt, button, params):
    if params["mode"] == MODE_DRAG:
        params["mode"] = MODE_NONE
    return params


def get_point_under_mouse(pt, points) -> tuple:
    for line_index in range(len(points)):
        for point_index in range(len(points[line_index])):
            d = get_dist(pt, points[line_index][point_index])
            if d <= POINT_SIZE * 2:
                return (points[line_index][point_index], (line_index, point_index))
    return None


def get_line_under_mouse(p, points) -> list:

    for line_index in range(len(points)):
        for segment_index in range(len(points[line_index]) - 1):
            # shortcuts
            a = points[line_index][segment_index]
            b = points[line_index][segment_index + 1]

            if (p[X] - b[X]) * (a[X] - b[X]) + (p[Y] - b[Y]) * (a[Y] - b[Y]) <= 0:
                continue
            elif (p[X] - a[X]) * (b[X] - a[X]) + (p[Y] - a[Y]) * (b[Y] - a[Y]) <= 0:
                continue

            ax = b[X] - a[X]
            ay = b[Y] - a[Y]
            if ax == 0:
                hx = a[X]
                hy = p[Y]

            elif ay == 0:
                hx = p[X]
                hy = a[Y]
            else:
                hy = (ax * (a[Y] * (ax / ay) - a[X] + p[X]) + ay * p[Y]) / ((ax * ax / ay) + ay)
                hx = (hy - a[Y]) * (ax / ay) + a[X]

            dist = get_dist(p, (hx, hy))
            # print(f"dist: {dist}")
            if dist > 15.0:
                continue
            return ((int(hx), int(hy)), (line_index, segment_index))

    #             print(f"value: {value},result: {result}")
    #             return result
    return None


def update_screen(surf, params):
    def text_out(x, y, t, c):
        global font
        score_text = font.render("{}".format(t), True, c)
        surf.blit(score_text, (x, y))

    pygame.draw.rect(surf, clBlack, (0, 0, W, H))
    if params["mode"] == MODE_RUN:
        text_out(10, 10, "Run mode", clYellow)
        for l in params["draw"]:
            p0 = l["s"]
            p1 = l["e"]

            p0 = params["g"]["p"][p0]
            p1 = params["g"]["p"][p1]

            pygame.draw.line(surf, l["color"], p0, p1, LINE_THICKNESS)
        c = 0
        for p in params["g"]["p"]:
            text_out(p[0] + 7, p[1] - 17, f"{c}", clYellow)
            c += 1
    else:
        text_out(10, 10, "Edit mode", clYellow)
        # lines
        for line in params["points"]:

            for pt_index in range(len(line) - 1):
                pygame.draw.line(surf, clYellow, line[pt_index], line[pt_index + 1], LINE_THICKNESS)

        # points
        for line_index in range(len(params["points"])):
            for point_index in range(len(params["points"][line_index])):
                pt = params["points"][line_index][point_index]
                # color = clRed if highlight == [1, line_index, point_index] else clGreen
                # color = clRed if highlight[X] == 1 and highlight[1] == line_index and highlight[2] == point_index else clGreen
                # print(color)
                pygame.gfxdraw.filled_circle(surf, pt[X], pt[Y], POINT_SIZE, clYellow)
                pygame.gfxdraw.circle(surf, pt[X], pt[Y], POINT_SIZE, clYellow)
                text_out(pt[X] + 9, pt[Y] - 20, f"{line_index}-{point_index}", clGreen)
                # pygame.draw.circle(surf, clYellow, params["points"][line_index][point_index], POINT_SIZE)

        # text_out(10, 10, mmp, clYellow)
        # text_out(10, 30, md_mode, clYellow)
        if params["highlight"] is not None:
            pygame.gfxdraw.circle(surf, params["highlight"][X], params["highlight"][Y], POINT_SIZE, clRed)
            pygame.gfxdraw.circle(surf, params["highlight"][X], params["highlight"][Y], POINT_SIZE - 1, clRed)


def main():
    def do_save(points):
        with open("points.txt", "w") as pt_file:
            # pt_file.write("{}\n".format(len(points)))
            for line in points:
                pt_file.write("*\n")
                for pt in line:
                    pt_file.write("{},{}\n".format(pt[X], pt[Y]))

    def do_load(params):
        ptr = []
        global md_mode
        with open("points.txt", "r") as pt_file:
            while True:
                value = pt_file.readline().strip()
                if value == None or value == "" or value == "#":
                    break
                elif value == "*":
                    ptr.append([])
                    # index = len(points) - 1
                else:
                    values = [int(i) for i in value.split(",")]
                    ptr[len(ptr) - 1].append(values)

        md_mode = 0
        params["points"] = ptr
        return params

    global font

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("AUTO'S")

    # create a surface on screen
    screen = pygame.display.set_mode((W, H))
    font = pygame.font.SysFont("consola.ttf", 18)

    global params
    params = do_load(params)

    # params["mode"] == MODE_RUN
    # params = prepare_action(params)

    # xxx = get_line_under_mouse((100, 100), params["points"])

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEMOTION:
                process_move(pygame.mouse.get_pos(), params)
            elif event.type == pygame.MOUSEBUTTONUP:
                params = process_mouseup(pygame.mouse.get_pos(), event.button, params)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                params = process_mousedown(pygame.mouse.get_pos(), event.button, params)

            # check user keys press
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_F1:
                    params["mode"] = MODE_NONE
                elif event.key == pygame.K_F2:
                    params = prepare_action(params)
                    params["mode"] = MODE_RUN

                elif event.key == pygame.K_F5:
                    do_save(params["points"])
                elif event.key == pygame.K_F9:
                    params = do_load(params)
                elif event.key == pygame.K_F12:
                    debug_print(params)

        update_screen(screen, params)

        # show all drawed things to the user
        pygame.display.update()
        clock.tick(GAME_SPEED)


if __name__ == "__main__":
    main()
