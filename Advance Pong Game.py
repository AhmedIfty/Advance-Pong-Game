# Movement keys:
# Player 1: "w" for Up, "s" for down
# Player 2: "up arrow" for Up, "down arrow" for down
#
# Diamond color & respective powerup:
# green+red: Board size increase & decrease
# white: Board comes forward
# yellow: Middle wall
# orange: Ball Speed
# purple: Movement reverse
# blue: Board movement speed
#
# Task distribution:
# Sakib Ul Haque: 23341128
# * Ball movement & bouncing off the edge
# * Diamond generation & animation
# * GameOver & displaying final score
# * powerup: Board size increase & decrease
# * powerup: Board comes forward
#
# Iftekhar Ahmed: 21201032
# * game difficulty (easy, medium, hard) setting
# * ball bouncing off board in different direction
# * board movement using keyboard
# * powerup: Middle wall to reflect ball
# * powerup: Ball speed change
#
# Syed Mominul Quddus: 21301182
# * handeling game pause, restart & exit
# * powerup: Board Movement reverse
# * powerup: Board movement speed increase


from OpenGL.GL import *
from OpenGL.GLUT import *
import random

s_width, s_height = 1200, 500

difficulty = "medium"

# starting coordinates of the boards
board1_x = 20
board2_x = s_width - 20
board1_y = board2_y = s_height // 2
default_board_speed = 10
board1_speed = board2_speed = default_board_speed

# starting coordinates of the ball
dx = 1
dy = random.choice([1, -1])
default_ball_speed = 3
ball = [s_width // 2, s_height // 2, 5, dx, dy, default_ball_speed]  # [x, y, size, direction_x, direction_y, speed]

score = [0, 0]

flag_gameOver = False
flag_gamePaused = False


def int_FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy > 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    return zone


def convertToZero(x, y, zone):
    if zone == 1:
        X, Y = y, x
    elif zone == 2:
        X, Y = y, -x
    elif zone == 3:
        X, Y = -x, y
    elif zone == 4:
        X, Y = -x, -y
    elif zone == 5:
        X, Y = -y, -x
    elif zone == 6:
        X, Y = -y, x
    elif zone == 7:
        X, Y = x, -y
    return int(X), int(Y)


def convertToOriginal(x, y, zone):
    if zone == 1:
        X, Y = y, x
    elif zone == 2:
        X, Y = -y, x
    elif zone == 3:
        X, Y = -x, y
    elif zone == 4:
        X, Y = -x, -y
    elif zone == 5:
        X, Y = -y, -x
    elif zone == 6:
        X, Y = y, -x
    elif zone == 7:
        X, Y = x, -y
    return int(X), int(Y)


def drawPoint(x, y, size=2):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(int(x), int(y))
    glEnd()


def drawLine(x1, y1, x2, y2, size=1, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    zone = int_FindZone(x1, y1, x2, y2)
    if zone != 0:
        x1, y1 = convertToZero(x1, y1, zone)
        x2, y2 = convertToZero(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1

    for x in range(int(x1), int(x2)):
        if zone != 0:
            original_x, original_y = convertToOriginal(x, y, zone)
            drawPoint(original_x, original_y, size)
        else:
            drawPoint(x, y, size)

        if d > 0:
            d = d + incNE
            y += 1
        else:
            d = d + incE


def draw_circle(r, value, size=2, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    global screen_height, screen_width

    d = 1 - r
    x = 0
    y = r
    circle_points(x, y, value)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
            x = x + 1
        else:
            d = d + 2 * x - 2 * y + 5
            x = x + 1
            y = y - 1
        circle_points(x, y, value, size)


def circle_points(x, y, value, size=2):
    cx, cy = value[0], value[1]
    drawPoint(x + cx, y + cy, size)
    drawPoint(y + cx, x + cy, size)
    drawPoint(y + cx, -x + cy, size)
    drawPoint(x + cx, -y + cy, size)
    drawPoint(-x + cx, -y + cy, size)
    drawPoint(-y + cx, -x + cy, size)
    drawPoint(-y + cx, x + cy, size)
    drawPoint(-x + cx, y + cy, size)


# board size change variables
board1_dy = 0
board2_dy = 0


def draw_arrow():
    n = 30
    teal = (0, 0.8, 0.8)
    drawLine(n, s_height - n, 2 * n, s_height - n, 3, teal)
    drawLine(n, s_height - n, 1.5 * n, s_height - n + 10, 3, teal)
    drawLine(n, s_height - n, 1.5 * n, s_height - n - 10, 3, teal)

def draw_difficulty():
    es, ms, hs = 1, 3, 1
    if difficulty == "easy":
        es, ms, hs = 3, 1, 1
    elif difficulty == "medium":
        es, ms, hs = 1, 3, 1
    elif difficulty == "hard":
        es, ms, hs = 1, 1, 3

    draw_circle(15, ((s_width/4)-50, s_height-30), es, (0, 1.0, 0))
    draw_circle(15, (s_width/4, s_height - 30), ms, (1.0, 1.0, 0))
    draw_circle(15, ((s_width/4)+50, s_height - 30), hs, (1.0, 0, 0))

def draw_pause():
    n = 30
    amber = (1, 0.749, 0)
    if not flag_gamePaused:
        drawLine(s_width / 2 - 10, s_height - n + 10, s_width / 2 - 10, s_height - n - 10, 3, amber)
        drawLine(s_width / 2 - 20, s_height - n + 10, s_width / 2 - 20, s_height - n - 10, 3, amber)
    else:
        drawLine(s_width / 2 - 30, s_height - n + 10, s_width / 2 - 30, s_height - n - 10, 3, amber)
        drawLine(s_width / 2 - 30, s_height - n - 10, s_width / 2 - 10, s_height - n, 3, amber)
        drawLine(s_width / 2 - 30, s_height - n + 10, s_width / 2 - 10, s_height - n, 3, amber)


def draw_cross():
    n = 30
    red = (1, 0, 0)
    drawLine(s_width - n, s_height - n + 10, s_width - 2 * n, s_height - n - 10, 3, red)
    drawLine(s_width - n, s_height - n - 10, s_width - 2 * n, s_height - n + 10, 3, red)

board_dx1=0
board_dx2=0
def draw_board():
    global board1_x, board1_y, board2_x, board2_y, board_dx2, board_dx1
    x1, y1, x2, y2 = board1_x, board1_y, board2_x, board2_y

    # draw board 2
    x2+=board_dx2
    drawLine(x2, y2 + 50 + board2_dy, x2, y2 - 50 - board2_dy, 2)
    drawLine(x2, y2 - 50 - board2_dy, x2 + 10, y2 - 50 - board2_dy, 2)
    drawLine(x2 + 10, y2 - 50 - board2_dy, x2 + 10, y2 + 50 + board2_dy, 2)
    drawLine(x2, y2 + 50 + board2_dy, x2 + 10, y2 + 50 + board2_dy, 2)

    # draw board 1
    x1+=board_dx1
    drawLine(x1, y1 + 50 + board1_dy, x1, y1 - 50 - board1_dy, 2)
    drawLine(x1, y1 - 50 - board1_dy, x1 - 10, y1 - 50 - board1_dy, 2)
    drawLine(x1 - 10, y1 - 50 - board1_dy, x1 - 10, y1 + 50 + board1_dy, 2)
    drawLine(x1, y1 + 50 + board1_dy, x1 - 10, y1 + 50 + board1_dy, 2)


def draw_midLine():
    global s_width, s_height
    x, y = s_width // 2, s_height
    while y > 0:
        drawLine(x, y, x, y - 10, 2)
        y -= 20


def draw_ball():
    global ball
    x, y, radius = ball[0], ball[1], ball[2]
    draw_circle(radius, [x, y])


# Diamond Global Variables
x_diamond = s_width // 2
y_diamond = random.randint(20, s_height - 20)
color_diamond = (0, 1, 0)
diamond = random.choice(['red', 'green', 'yellow', 'purple', 'orange', 'cyan', 'white'])
if diamond == 'green':
    color_diamond = (0, 1, 0)
elif diamond == 'red':
    color_diamond = (1, 0, 0)
elif diamond == 'yellow':
    color_diamond = (1, 1, 0)
elif diamond == 'purple':
    color_diamond = (1, 0, 1)
elif diamond == 'orange':
    color_diamond = (1, 0.6, 0)
elif diamond == 'cyan':
    color_diamond = (0, 0.8, 0.8)
elif diamond == 'white':
    color_diamond = (1, 1, 1)
diamond_speed = random.choice([2, -2])


def draw_diamond(x, y):
    global color_diamond
    drawLine(x, y, x + 10, y + 10, 2, color_diamond)
    drawLine(x, y, x + 10, y - 10, 2, color_diamond)
    drawLine(x + 10, y + 10, x + 20, y, 2, color_diamond)
    drawLine(x + 10, y - 10, x + 20, y, 2, color_diamond)


def draw_midWall():
    global s_width, s_height
    if m_wall_b2 == True:
        x, y = (s_width // 2) - 10, s_height
        drawLine(x, 0, x, y, 4)
    if m_wall_b1 == True:
        x, y = (s_width // 2) + 10, s_height
        drawLine(x, 0, x, y, 4)


def generate_diamond():
    global x_diamond, y_diamond, color_diamond, diamond_speed, diamond
    x_diamond = s_width // 2
    y_diamond = random.randint(20, s_height - 20)
    diamond = random.choice(['yellow', 'orange', 'green', 'red', 'purple', 'cyan', 'white'])

    if diamond == 'green':
        color_diamond = (0, 1, 0)
    elif diamond == 'red':
        color_diamond = (1, 0, 0)
    elif diamond == 'yellow':
        color_diamond = (1, 1, 0)
    elif diamond == 'purple':
        color_diamond = (1, 0, 1)
    elif diamond == 'orange':
        color_diamond = (1, 0.6, 0)
    elif diamond == 'cyan':
        color_diamond = (0, 0.8, 0.8)
    elif diamond=='white':
        color_diamond=(1,1,1)
    diamond_speed = random.choice([2, -2])


def default_all():
    global timer_board1, timer_board2, board1_size_change, board2_size_change, board1_dy, board2_dy, \
        timer_m_wall_b1, timer_m_wall_b2, board1_yellow, board2_yellow, m_wall_b1, m_wall_b2, \
        reverse_b1, reverse_b2, timer_reverse_b1, timer_reverse_b2, \
        ball_speed_b1, ball_speed_b2, fast_b1, fast_b2, timer_ball_speed_b1, timer_ball_speed_b2, \
        more_speed_b1, more_speed_b2, timer_bat_speed_b1, timer_bat_speed_b2, default_board_speed, \
        board1_forward, board2_forward, board1_forward_timer, board2_forward_timer, board_dx1, board_dx2

    # board size powerup variable
    timer_board1 = timer_board2 = 0
    board1_size_change = board2_size_change = False
    board1_dy = board2_dy = 0

    # middle wall power up variable
    timer_m_wall_b1 = timer_m_wall_b2 = 0
    board1_yellow = board2_yellow = False
    m_wall_b1 = m_wall_b2 = False

    # reverse power up variable
    reverse_b1 = reverse_b2 = False
    timer_reverse_b1 = timer_reverse_b2 = 0

    # board speed variable
    more_speed_b1 = more_speed_b2 = False
    timer_bat_speed_b1 = timer_bat_speed_b2 = 0

    # board comes forward variable
    board1_forward = False
    board2_forward = False
    board1_forward_timer = 0
    board2_forward_timer = 0
    board_dx1 = board_dx2 = 0


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_board()
    draw_midLine()
    draw_ball()
    draw_arrow()
    draw_pause()
    draw_cross()
    draw_difficulty()
    draw_midWall()
    # gameplay()
    draw_diamond(x_diamond, y_diamond)
    glutSwapBuffers()


# board size powerup variable
timer_board1 = timer_board2 = 0
board1_size_change = board2_size_change = False

# middle wall power up variable
timer_m_wall_b1 = timer_m_wall_b2 = 0
board1_yellow = board2_yellow = False
m_wall_b1 = m_wall_b2 = False

# reverse power up variable
reverse_b1 = reverse_b2 = False
timer_reverse_b1 = timer_reverse_b2 = 0

# ball speed variable
ball_speed_b1 = ball_speed_b2 = False
fast_b1 = fast_b2 = False
timer_ball_speed_b1 = timer_ball_speed_b2 = 0

# board speed variable
more_speed_b1 = more_speed_b2 = False
timer_bat_speed_b1 = timer_bat_speed_b2 = 0

# board comes forward variable
board1_forward=False
board2_forward=False
board1_forward_timer=0
board2_forward_timer=0

def animation():
    global ball, default_ball_speed, s_width, s_height, board1_x, board1_y, board2_x, board2_y, score, flag_gameOver, \
        x_diamond, y_diamond, board1_dy, board2_dy, color_diamond, diamond_speed, \
        timer_board1, timer_board2, board1_size_change, board2_size_change, \
        timer_m_wall_b1, timer_m_wall_b2, m_wall_b1, m_wall_b2, board1_yellow, board2_yellow, \
        reverse_b1, reverse_b2, timer_reverse_b1, timer_reverse_b2, \
        ball_speed_b1, ball_speed_b2, fast_b1, fast_b2, timer_ball_speed_b1, timer_ball_speed_b2, \
        more_speed_b1, more_speed_b2, timer_bat_speed_b1, timer_bat_speed_b2, default_board_speed, board1_speed, board2_speed, \
        board1_forward, board2_forward, board1_forward_timer, board2_forward_timer, board_dx1, board_dx2

    if not flag_gamePaused:
        if not flag_gameOver:

            # ball global variables
            ball_x, ball_y, radius, ball_dx, ball_dy, ball_speed = ball[:6]
            ball_x += ball_dx * ball_speed
            ball_y += ball_dy * ball_speed
            ball[0], ball[1] = ball_x, ball_y

            # ball bouncing off y-axis
            if ball_y >= s_height or ball_y <= 0:
                ball_dy *= -1
                ball[4] = ball_dy

            # missing the ball
            if ball_x <= 0:  # by P1
                score[1] += 1
                print('======================================================')
                print(f'''Score: 
                Player1: {score[0]}
                Player2: {score[1]} ''')
                x, y =  s_width // 2, s_height // 2
                if m_wall_b2:    # ball generation handling for middle wall
                    x = (s_width // 2) - 20
                ball = [x, y, radius, 1, random.choice([1, -1]), ball_speed]

            if ball_x >= s_width:  # by P2
                score[0] += 1
                print('======================================================')
                print(f'''Score: 
                Player1: {score[0]}
                Player2: {score[1]} ''')
                x, y = s_width // 2, s_height // 2
                if m_wall_b1:   # ball generation handling for middle wall
                    x = (s_width // 2) + 20
                ball = [x, y, radius, -1, random.choice([1, -1]), ball_speed]

            # ball hitting board 1
            if board1_x - 10 + board_dx1<= ball_x <= board1_x+ board_dx1:
                if board1_y <= ball_y <= (board1_y + 50 + board1_dy):
                    ball_dx *= -1
                    ball_dy = 1
                elif (board1_y - 50 - board1_dy) <= ball_y < board1_y:
                    ball_dx *= -1
                    ball_dy = -1
                ball[3] = ball_dx
                ball[4] = ball_dy

                # ball speed feature
                if board1_y - 50 - board1_dy <= ball_y <= (board1_y + 50 + board1_dy):
                    if ball_speed_b1 == True:
                        fast_b1 = True
                    elif ball_speed_b2 == True:
                        fast_b2 = False

            # ball hitting board 2
            if board2_x +board_dx2<= ball_x <= board2_x + 10+board_dx2:
                if board2_y <= ball_y <= (board2_y + 50 + board2_dy):
                    ball_dx *= -1
                    ball_dy = 1
                elif (board2_y - 50 - board2_dy) <= ball_y < board2_y:
                    ball_dx *= -1
                    ball_dy = -1
                ball[3] = ball_dx
                ball[4] = ball_dy

                # ball speed feature
                if board2_y - 50 - board2_dy <= ball_y <= (board2_y + 50 + board2_dy):
                    if ball_speed_b2 == True:
                        fast_b2 = True
                    elif ball_speed_b1 == True:
                        fast_b1 = False

            # game over
            if score[0] == 5 or score[1] == 5:
                flag_gameOver = True
                print('======================================================')
                print(f'''Gameover! Final Score: 
                Player1: {score[0]}
                Player2: {score[1]}''')

            # middle wall, ball location confirmation
            if board1_yellow and (s_width // 2) + 15 <= ball_x <= s_width:
                m_wall_b1 = True
            elif board2_yellow and 0 <= ball_x <= (s_width // 2) - 15:
                m_wall_b2 = True

            # ball speed change
            if (ball_speed_b1 and fast_b1) or (ball_speed_b2 and fast_b2):
                ball_speed = default_ball_speed * 2
                ball[5] = ball_speed
            else:
                ball_speed = default_ball_speed
                ball[5] = ball_speed

            # board speed change
            if more_speed_b1:
                board1_speed = 50
            if more_speed_b2:
                board2_speed = 50

            # diamond animation
            x_diamond += diamond_speed

            # powerup: board 2
            if (board2_x +board_dx2<= x_diamond <= board2_x + 10+board_dx2) and (
                    board2_y - 50 - board2_dy <= y_diamond <= board2_y + 50 + board2_dy):

                # board-size
                if diamond == 'green':
                    board2_dy = 30
                    board2_size_change = True
                    timer_board2 = 0
                    generate_diamond()

                elif diamond == 'red':
                    board2_dy = -30
                    board2_size_change = True
                    timer_board2 = 0
                    generate_diamond()

                elif diamond == 'yellow':
                    board2_yellow = True
                    generate_diamond()

                elif diamond == 'purple':
                    reverse_b1 = True
                    timer_reverse_b1 = 0
                    generate_diamond()

                elif diamond == 'orange':
                    ball_speed_b2 = True
                    timer_ball_speed_b2 = 0
                    generate_diamond()

                elif diamond == 'cyan':
                    more_speed_b2 = True
                    timer_bat_speed_b2 = 0
                    generate_diamond()

                elif diamond=='white':
                    board1_forward=True
                    if board_dx1 == 0:
                        board_dx1+=200
                    generate_diamond()


            # powerup: board 1
            elif (board1_x - 10 + board_dx1<= x_diamond <= board1_x+ board_dx1) and (
                    board1_y - 50 - board1_dy <= y_diamond <= board1_y + 50 + board1_dy):
                # board-size
                if diamond == 'green':
                    board1_dy = 30
                    board1_size_change = True
                    timer_board1 = 0
                    generate_diamond()

                elif diamond == 'red':
                    board1_dy = -30
                    board1_size_change = True
                    timer_board1 = 0
                    generate_diamond()

                elif diamond == 'yellow':
                    board1_yellow = True
                    generate_diamond()

                elif diamond == 'purple':
                    reverse_b2 = True
                    timer_reverse_b2 = 0
                    generate_diamond()

                elif diamond == 'orange':
                    ball_speed_b1 = True
                    timer_ball_speed_b1 = 0
                    generate_diamond()

                elif diamond == 'cyan':
                    more_speed_b1 = True
                    timer_bat_speed_b1 = 0
                    generate_diamond()

                elif diamond=='white':
                    board2_forward=True
                    if board_dx2 == 0:
                        board_dx2-=200
                    generate_diamond()

            # time count: board-forward
            if board1_forward==True:
                board1_forward_timer+=1
                if board1_forward_timer == 1000:
                    board_dx1 = 0
                    board1_forward_timer = 0
                    board1_forward = False

            if board2_forward==True:
                board2_forward_timer+=1
                if board2_forward_timer == 1000:
                    board_dx2 = 0
                    board2_forward_timer = 0
                    board2_forward = False

            # time count: board-size
            if board2_size_change == True:
                timer_board2 += 1
                if timer_board2 == 1000:
                    board2_dy = 0
                    timer_board2 = 0
                    board2_size_change = False

            if board1_size_change == True:
                timer_board1 += 1
                if timer_board1 == 1000:
                    board1_dy = 0
                    timer_board1 = 0
                    board1_size_change = False

            # time count: middle wall
            if m_wall_b2:
                timer_m_wall_b2 += 1
                if (s_width // 2) - 10 <= ball_x:
                    ball_dx *= -1
                    ball[3] = ball_dx
                if timer_m_wall_b2 == 1200:
                    m_wall_b2 = False
                    board2_yellow = False
                    timer_m_wall_b2 = 0

            if m_wall_b1:
                timer_m_wall_b1 += 1
                if ball_x <= (s_width // 2) + 10:
                    ball_dx *= -1
                    ball[3] = ball_dx
                if timer_m_wall_b1 == 1200:
                    m_wall_b1 = False
                    board1_yellow = False
                    timer_m_wall_b1 = 0

            # time count: reverse movement
            if reverse_b2:
                timer_reverse_b2 += 1
                if timer_reverse_b2 == 800:
                    reverse_b2 = False
                    timer_reverse_b2 = 0

            if reverse_b1:
                timer_reverse_b1 += 1
                if timer_reverse_b1 == 800:
                    reverse_b1 = False
                    timer_reverse_b1 = 0

            # time count: ball speed
            if ball_speed_b1:
                timer_ball_speed_b1 += 1
                if timer_ball_speed_b1 == 1500:
                    ball_speed_b1 = False
                    fast_b1 = False
                    timer_ball_speed_b1 = 0

            if ball_speed_b2:
                timer_ball_speed_b2 += 1
                if timer_ball_speed_b2 == 1500:
                    ball_speed_b2 = False
                    fast_b2 = False
                    timer_ball_speed_b2 = 0

            # time count: bat speed #meeeee
            if more_speed_b1:
                timer_bat_speed_b1 += 1
                if timer_bat_speed_b1 == 1500:
                    more_speed_b1 = False
                    timer_bat_speed_b1 = 0
                    board1_speed = default_board_speed

            if more_speed_b2:
                timer_bat_speed_b2 += 1
                if timer_bat_speed_b2 == 1500:
                    more_speed_b2 = False
                    timer_bat_speed_b2 = 0
                    board2_speed = default_board_speed

            # regenerate diamond
            if s_width + 600 <= x_diamond <= s_width + 650 or -650 <= x_diamond <= -600:
                generate_diamond()

        glutPostRedisplay()


def special_keys(key, x, y):
    global board2_y, s_height, board1_speed, board2_speed, reverse_b1, reverse_b2

    # board movement 2
    if not flag_gameOver:
        if not reverse_b2:
            if key == GLUT_KEY_UP:
                if board2_y < s_height - 30:
                    board2_y += board2_speed
            elif key == GLUT_KEY_DOWN:
                if board2_y > +30:
                    board2_y -= board2_speed
        else:
            if key == GLUT_KEY_DOWN:
                if board2_y < s_height - 30:
                    board2_y += board2_speed
            elif key == GLUT_KEY_UP:
                if board2_y > +30:
                    board2_y -= board2_speed


def keyboardListener(key, x, y):
    global board1_y, board2_y, s_height, board1_speed, board2_speed

    if not flag_gameOver:
        if not reverse_b1:  # default controls
            if key == b'w':
                if board1_y < s_height - 30:
                    board1_y += board1_speed
            elif key == b's':
                if board1_y > 0 + 30:
                    board1_y -= board1_speed
        else:
            if key == b's':  # reversed controls
                if board1_y < s_height - 30:
                    board1_y += board1_speed
            elif key == b'w':
                if board1_y > 0 + 30:
                    board1_y -= board1_speed

def reset_all():
    global flag_gamePaused, flag_gameOver, score, ball, s_width, s_height, board1_x, board2_x, board1_y, board2_y, board1_speed, board2_speed, x_diamond, y_diamond, color_diamond, diamond_speed, default_ball_speed
    board1_x = 20
    board2_x = s_width - 20
    board1_y = board2_y = s_height // 2
    board1_speed = board2_speed = 10

    if difficulty == "easy":
        default_ball_speed = 2
    elif difficulty == "medium":
        default_ball_speed = 3
    elif difficulty == "hard":
        default_ball_speed = 4

    # starting coordinates of the ball
    dx = 1
    dy = random.choice([1, -1])
    ball = [s_width // 2, s_height // 2, 5, dx, dy,
            default_ball_speed]  # [x, y, size, direction_x, direction_y, speed]

    score = [0, 0]

    flag_gameOver = False
    flag_gamePaused = False

    default_all()  # resets all powerup variable
    generate_diamond()

def mouseListener(button, state, x, y):
    global flag_gamePaused, flag_gameOver, score, ball, s_width, s_height, board1_x, board2_x, board1_y, board2_y, board1_speed, board2_speed, x_diamond, y_diamond, color_diamond, diamond_speed, default_ball_speed, difficulty
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = s_height - y
        n = 30
        if s_height - n - 10 <= y <= s_height - n + 10:  # handles restart button
            if n <= x <= 2 * n:
                reset_all()
                print('Starting Over')

            elif (s_width/4)-50-15 <= x <= (s_width/4)-50+15:
                difficulty = "easy"
                reset_all()
                print('Starting Over in Easy mode')

            elif (s_width / 4)-15 <= x <= (s_width / 4)+15:
                difficulty = "medium"
                reset_all()
                print('Starting Over in Medium mode')

            elif (s_width / 4)+50-15 <= x <= (s_width / 4)+50+15:
                difficulty = "hard"
                reset_all()
                print('Starting Over in Hard mode')

            elif s_width / 2 - 30 <= x <= s_width / 2 - 10:  # handles pause button
                if not flag_gamePaused:
                    flag_gamePaused = True
                else:
                    flag_gamePaused = False

            elif (s_width - 2 * n <= x <= s_width - n):  # handles cross button
                print('======================================================')
                print(f'''Goodbye! Final Score: 
              Player1: {score[0]} 
              Player2: {score[1]}''')
                glutLeaveMainLoop()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(s_width, s_height)
glutCreateWindow(b"Pong Game")
glOrtho(0, s_width, 0, s_height, -1, 1)
glClearColor(0, 0, 0, 1)

glutDisplayFunc(display)
glutIdleFunc(animation)

glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(special_keys)
glutMainLoop()