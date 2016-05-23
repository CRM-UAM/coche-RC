# coding: utf-8
from __future__ import print_function

import os
import sys
import pygame
import Pyro4

from GUI import GUIModel

framerate = 60
controls = {'up': pygame.K_w, 'down': pygame.K_s,
            'right': pygame.K_d, 'left': pygame.K_a, 'brake': pygame.K_SPACE}
#controls = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'brake': pygame.K_SPACE}


def display_text(screen, text, x, y):
    # initialize font; must be called after 'pygame.init()' to avoid 'Font
    # not Initialized' error
    #font = pygame.font.SysFont("monospace", 15)

    # render text
    font = pygame.font.SysFont("monospace", 15)
    size = font.size(text)
    label = font.render(text, 1, (255, 255, 0))

    # borramos el doble hacia la derecha, para eliminar restos
    screen.subsurface((x, y, size[0] * 2, size[1])).fill((0, 0, 0))

    screen.blit(label, (x, y))
    pygame.display.update()


def display_image(screen, image, x, y):
    screen.blit(image, (x, y))
    pygame.display.update()


def display_dict(surf, d_im, d_pos):
    for k, i in d_im.items():
        surf.blit(i, d_pos[k])
    pygame.display.update()


def car_control(rccar):

    try:
        pygame.init()
        #pygame.mouse.set_visible(False)

        # tamaño de la pantalla
        size = (pygame.display.Info().current_w - 30,
                pygame.display.Info().current_h - 20)

        screen = pygame.display.set_mode(size)

        pygame.display.set_caption(
            'Plataformas para Sistemas Empotrados - 2015/2016')

        clock = pygame.time.Clock()

        # flechas de colores
        y_arr = pygame.image.load('img/arrows/128/yellow_arrow.png').convert()
        r_arr = pygame.image.load('img/arrows/128/red_arrow.png').convert()

        a_size = y_arr.get_size()[0]

        a_left = pygame.image.load('img/arrows/128/gray_arrow.png').convert()
        a_up = pygame.transform.rotate(a_left, -90)
        a_right = pygame.transform.rotate(a_up, -90)
        a_down = pygame.transform.rotate(a_right, -90)
        p_arrows = {
            'left': (0, a_size),
            'right': (2 * a_size, a_size),
            'up': (a_size, 0),
            'down': (a_size, 2 * a_size)
        }

        # centro de la pantalla
        #a_x, a_y = tuple(x // 2 for x in size)
        a_x, a_y = 50 + (1.5 * a_size), size[1] - (1.5 * a_size) - 50
        # surface auxiliar para pintar las flechas de colores
        a_control = pygame.display.get_surface().subsurface(
            (a_x - (1.5 * a_size), a_y - (1.5 * a_size), 3 * a_size, 3 * a_size))

        #####

        arrow_size = '128'
        arrows = {
            'blue': 'img/arrows/' + arrow_size + '/blue_arrow.png',
            'gray': 'img/arrows/' + arrow_size + '/gray_arrow.png',
            'green': 'img/arrows/' + arrow_size + '/green_arrow.png',
            'red': 'img/arrows/' + arrow_size + '/red_arrow.png',
            'white': 'img/arrows/' + arrow_size + '/white_arrow.png',
            'yellow': 'img/arrows/' + arrow_size + '/yellow_arrow.png'
        }

        images = {
            'base': 'img/car/base.png',
            'wheels': {
                'blue': 'img/car/wheel/blue.png',
                'gray': 'img/car/wheel/gray.png',
                'green': 'img/car/wheel/green.png',
                'red': 'img/car/wheel/red.png',
                'white': 'img/car/wheel/white.png',
                'yellow': 'img/car/wheel/yellow.png'
            }
        }

        w_pos = {
            'tl': (-280, 280),
            'tr': (280, 280),
            'bl': (-280, 1000),
            'br': (280, 1000)
        }

        model_surf = screen.subsurface(700, 0, size[0] - 700, size[1])
        model = GUIModel(model_surf, images, w_pos)

        #####
        angle = 0.0
        speed = 0.0
        color = 'gray'
        done = False
        while not done:

            i_arrows = {'left': a_left, 'right': a_right,
                        'up': a_up, 'down': a_down}

            pressed = pygame.key.get_pressed()

            alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
            ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

            for event in pygame.event.get():

                # determine if X was clicked, or Ctrl+W or Alt+F4 was used
                if event.type == pygame.QUIT:
                    done = True

                if event.type == pygame.KEYDOWN:
                    if ctrl_held and event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        done = True

            if pressed[controls['up']] and pressed[controls['down']]:
                forward = 0
                i_arrows['up'] = pygame.transform.rotate(r_arr, -90)
                i_arrows['down'] = pygame.transform.rotate(r_arr, 90)

                # TODO: mantenemos velocidad??
                color = 'green'

            elif pressed[controls['down']]:
                forward = -1
                i_arrows['down'] = pygame.transform.rotate(y_arr, 90)

                # TODO: aceleramos marcha atras
                speed = rccar.backward()
                color = 'blue'

            elif pressed[controls['up']]:
                forward = 1
                i_arrows['up'] = pygame.transform.rotate(y_arr, -90)

                # TODO: aceleramos
                speed = rccar.forward()
                color = 'yellow'

            else:
                forward = 0

                # TODO: accion por defecto
                color = 'gray'
                rccar.decelerate()

            if pressed[controls['left']] and pressed[controls['right']]:
                steer = "keep"
                i_arrows['left'] = r_arr
                i_arrows['right'] = pygame.transform.rotate(r_arr, 180)

                # TODO: mantenemos direccion??

            elif pressed[controls['left']]:
                steer = "left"
                i_arrows['left'] = y_arr

                # TODO giramos a la izquierda
                angle = rccar.turn_left()

            elif pressed[controls['right']]:
                steer = "right"
                i_arrows['right'] = pygame.transform.rotate(y_arr, 180)

                # TODO giramos a la derecha
                angle = rccar.turn_right()

            else:
                steer = "straight"

                # TODO accion por defecto
                angle = rccar.straight()

            if pressed[controls['brake']]:

                # TODO frenamos
                rccar.brake()
                color = 'red'

            #print("forward: {}, steer: {}".format(forward, steer))
            display_text(
                screen, "forward: {}".format(forward), 100, 100)
            display_text(
                screen, "steer: {}".format(steer), 100, 120)

            display_dict(a_control, i_arrows, p_arrows)

            model.update(color, angle)

            clock.tick(framerate)

        pygame.quit()

    except KeyboardInterrupt:
        pygame.quit()


def main():

    ip = '192.168.12.2'
    #ip = 'localhost'
    try:
        rccar = Pyro4.Proxy("PYRO:rccar@" + ip + ":55555")

    #    if rccar.start():
    #        car_control(rccar)
    #    else:
    #        print("El coche ya tiene un piloto. No lo vuelvas loco.")
    #        sys.exit(0)
        car_control(rccar)
    except Pyro4.errors.CommunicationError as c:
        print("Error al conectar con el coche. ¿Está encendido?")
    # except:

    #    rccar.brake()
    else:
        rccar.brake()

if __name__ == '__main__':
    import Pyro4.util

    sys.excepthook = Pyro4.util.excepthook
    main()
