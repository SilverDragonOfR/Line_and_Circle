import pygame as py

py.init()

width = 600
height = 500
screen = py.display.set_mode((width, height))
text_font = py.font.Font("freesansbold.ttf", 30)


### Game variables
running = True
menu = 0
method = 1
bg_color = (0, 0, 0)
color = (255, 255, 255)
dash_length = 5
ct = 0
first_point = (-1, -1)
second_point = (-1, -1)
####

def reset_state():
    first_point = (-1, -1)
    second_point = (-1, -1)
    ct = 0
    screen.fill(bg_color)

def write_description(figure, algorithm):
    desc = text_font.render(f"{figure} - {algorithm}", True , color)
    screen.blit(desc, (10, 10))

def put_pixel(x, y):
    screen.set_at((x, height - y), color)

def draw_point(x, y):
    put_pixel(x, y)

def eight_sym_put_pixel(cx, cy, p, q):
    put_pixel(cx + p, cy + q)
    put_pixel(cx - p, cy + q)
    put_pixel(cx + p, cy - q)
    put_pixel(cx - p, cy - q)
    put_pixel(cx + q, cy + p)
    put_pixel(cx - q, cy + p)
    put_pixel(cx + q, cy - p)
    put_pixel(cx - q, cy - p)

### line algorithms
def draw_line_by_naive(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    c = y1 - x1*m
    if -1<=m<=1:
        st, en = min(x1, x2), max(x1, x2)
        for x in range(st, en+1):
            put_pixel(x, round(m*x+c))
    else:
        st, en = min(y1, y2), max(y1, y2)
        for y in range(st, en+1):
            put_pixel(round((y-c)/m), y)

def draw_line_by_bresenham(x1, y1, x2, y2, reflect_diagonal = 0, reflect_horizonal = 0):
    dx = x2-x1
    dy = y2-y1

    if dx<0:
        draw_line_by_bresenham(x2, y2, x1, y1, reflect_diagonal, reflect_horizonal)
        return
    if (-dx)<=dy<=dx:
        if dy<0:
            draw_line_by_bresenham(x1, y1, x2, -(y2-y1)+y1, 0, 1)
            return
        else:
            pass
    else:
        if dy<0:
            draw_line_by_bresenham(x1, y1, -(y2-y1)+x1, x2-x1+y1, 1, 1)
            return
        else:
            draw_line_by_bresenham(x1, y1, y2-y1+x1, x2-x1+y1, 1, 0)
            return

    i1 = 2*dy
    i2 = 2*(dy-dx)

    d = i1-dx
    y = y1
    for x in range(x1, x2+1):
        if reflect_horizonal:
            if reflect_diagonal:
                put_pixel(y-y1+x1, -(x-x1)+y1)
            else:
                put_pixel(x, -(y-y1)+y1)
        else:
            if reflect_diagonal:
                put_pixel(y-y1+x1, x-x1+y1)
            else:
                put_pixel(x, y)
        if d<0:
            d = d + i1
        else:
            d = d + i2
            y += 1
        x += 1

def draw_line_by_dashedbresenham(x1, y1, x2, y2, reflect_diagonal = 0, reflect_horizonal = 0):    
    dx = x2-x1
    dy = y2-y1

    if dx<0:
        draw_line_by_dashedbresenham(x2, y2, x1, y1, reflect_diagonal, reflect_horizonal)
        return
    if (-dx)<=dy<=dx:
        if dy<0:
            draw_line_by_dashedbresenham(x1, y1, x2, -(y2-y1)+y1, 0, 1)
            return
        else:
            pass
    else:
        if dy<0:
            draw_line_by_dashedbresenham(x1, y1, -(y2-y1)+x1, x2-x1+y1, 1, 1)
            return
        else:
            draw_line_by_dashedbresenham(x1, y1, y2-y1+x1, x2-x1+y1, 1, 0)
            return

    i1 = 2*dy
    i2 = 2*(dy-dx)

    d = i1-dx
    y = y1

    put = True
    todo = dash_length
    for x in range(x1, x2+1):
        if reflect_horizonal:
            if reflect_diagonal:
                if put:
                    put_pixel(y-y1+x1, -(x-x1)+y1)
                    todo -= 1
                    if todo==0:
                        put = False
                        todo = 5
                else:
                    todo -= 1
                    if todo==0:
                        put = True
                        todo = 5
            else:
                if put:
                    put_pixel(x, -(y-y1)+y1)
                    todo -= 1
                    if todo==0:
                        put = False
                        todo = 5
                else:
                    todo -= 1
                    if todo==0:
                        put = True
                        todo = 5
        else:
            if reflect_diagonal:
                if put:
                    put_pixel(y-y1+x1, x-x1+y1)
                    todo -= 1
                    if todo==0:
                        put = False
                        todo = 5
                else:
                    todo -= 1
                    if todo==0:
                        put = True
                        todo = 5
            else:
                if put:
                    put_pixel(x, y)
                    todo -= 1
                    if todo==0:
                        put = False
                        todo = 5
                else:
                    todo -= 1
                    if todo==0:
                        put = True
                        todo = 5

        if d<0:
            d = d + i1
        else:
            d = d + i2
            y += 1
        x += 1
###

### circle algorithms
def draw_circle_by_naive(x1, y1, x2, y2):
    r = ((x1-x2)**2 + (y1-y2)**2)**0.5
    x, y = 0, r
    while x<=y:
        eight_sym_put_pixel(x1, y1, x, round((r**2 - x**2)**0.5))
        x += 1

def draw_circle_by_bresenham(x1, y1, x2, y2):
    r = round(((x1-x2)**2 + (y1-y2)**2)**0.5)
    x, y = 0, r
    d = 3 - 2*r

    while x<=y:
        eight_sym_put_pixel(x1, y1, x, y)
        if d<0:
            d = d + 4*x + 6
        else:
            d = d + 4*x - 4*y + 10
            y -= 1
        x += 1

def draw_circle_by_midpoint(x1, y1, x2, y2):
    r = round(((x1-x2)**2 + (y1-y2)**2)**0.5)
    x, y = 0, r
    # p = (5/4) - r
    p = 1 - r

    while x<=y:
        eight_sym_put_pixel(x1, y1, x, y)
        if p<0:
            p = p + 2*x + 3
        else:
            p = p + 2*x - 2*y + 5
            y -= 1
        x += 1
###

while running:

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            x, y = py.mouse.get_pos()
            if ct==0:
                first_point = (x, height - y)
                screen.fill(bg_color)
                ct += 1
            elif ct==1:
                second_point = (x, height - y)
                screen.fill(bg_color)
                ct += 1
        if event.type == py.KEYDOWN:
            if event.key == py.K_e:
                if ct==2:
                    first_point = (-1, -1)
                    second_point = (-1, -1)
                    ct = 0
                    screen.fill(bg_color)
            if event.key == py.K_TAB:
                menu = 1 - menu
                screen.fill(bg_color)
            if event.key == py.K_1:
                method = 1
                reset_state()
            if event.key == py.K_2:
                method = 2
                reset_state()
            if event.key == py.K_3:
                method = 3
                reset_state()

    if menu==0:
        # line
        if method==1:
            # naive
            write_description("Line", "Naive")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_line_by_naive(*first_point, *second_point)
        elif method==2:
            # bresenham
            write_description("Line", "Bresenham")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_line_by_bresenham(*first_point, *second_point)
        else:
            # dashedBresenham
            write_description("Line", "DashedBresenham")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_line_by_dashedbresenham(*first_point, *second_point)
    else:
        # circle
        if method==1:
            # naive
            write_description("Circle", "Naive")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_circle_by_naive(*first_point, *second_point)
        elif method==2:
            # bresenham
            write_description("Circle", "Bresenham")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_circle_by_bresenham(*first_point, *second_point)
        else:
            # midpoint
            write_description("Circle", "Midpoint")
            if ct==1:
                draw_point(*first_point)
            elif ct==2:
                draw_circle_by_midpoint(*first_point, *second_point)

    py.display.update()

# "Ash nazg durbatuluk, ash nazg gimbatul, thrakatuluk agh burzum-ishi krimpatul"
