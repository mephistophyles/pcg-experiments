import random
import turtle

def drunk_lightning_1(t, start=0, end=100, step=10, bias=5):
    """
    Using Brownian motion we create 2D movement towards the end goal with a bias
    :param t: turtle.Turtle object
    :param start: int
    :param end: int
    :param step: int
    :param bias: int
    :return: turtle.Turtle object
    """
    current_x = 0
    current_y = start
    t.setpos(current_x, current_y)
    new_x = 0
    new_y = 0
    while current_y < end:
        direction = random.randint(1, 4)
        if direction == 1:
            new_x = current_x - 1*step
        elif direction == 2:
            new_y = current_y + 1*step + bias
        elif direction == 3:
            new_x = current_x + 1*step
        else:
            new_y = current_y - 1*step + bias
        t.goto(new_x, new_y)
        current_x = new_x
        current_y = new_y
    return t


def bnb_lightning(t, start=0, end=100, frac=0.6, width=5, epsilon=5):
    current_x = 0
    current_y = start
    stack = []
    stack.append((current_x, current_y))
    while len(stack) > 0:
        start_pos = stack.pop()
        y_final = start_pos[1] + frac*(end + epsilon - start_pos[1]) # TODO add some variance here?
        left = random.randint(1, width)
        right = random.randint(1, width)
        t.setpos(start_pos[0], start_pos[1])
        left_pos = (left, y_final)
        right_pos = (right, y_final)
        if y_final < end:
            stack.append(left_pos)
            stack.append(right_pos)
        t.goto(left_pos[0], left_pos[1])
        t.setpos(start_pos[0], start_pos[1])
        t.goto(right_pos[0], right_pos[1])
    return t


def lsys_lightning():
    pass

if __name__ == '__main__':
    random.seed(0)
    window = turtle.Screen()
    drunk_turtle = turtle.Turtle()
    drunk_turtle.pencolor('red')
    drunk_lightning_1(drunk_turtle, 0, 300, 5, 5)
    bnb_turtle = turtle.Turtle()
    bnb_turtle.pencolor('blue')
    bnb_lightning(bnb_turtle, 0, 300, 0.4, 50, 30)
    turtle.done()
