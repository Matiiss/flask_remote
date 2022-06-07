import pyautogui as pag

pag.FAILSAFE = False


def mouse_up(args):
    amount = int(args[0])
    pag.move(0, -amount)


def mouse_down(args):
    amount = int(args[0])
    pag.move(0, amount)


def mouse_right(args):
    amount = int(args[0])
    pag.move(amount, 0)


def mouse_left(args):
    amount = int(args[0])
    pag.move(-amount, 0)


def mouse_press(args):
    pag.click(button=args[0])


def write(args):
    pag.write(args[0])


def press(args):
    pag.press(args[0])


actions_dct = {'mouse_u': mouse_up, 'mouse_d': mouse_down,
               'mouse_r': mouse_right, 'mouse_l': mouse_left,
               'mouse_press': mouse_press, 'write': write,
               'press': press}
