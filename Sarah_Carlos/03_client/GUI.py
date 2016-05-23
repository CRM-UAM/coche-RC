# coding: utf-8
from __future__ import print_function

import pygame


class GUICursors(object):

    def __init__(self, surface, images):
        """
        images = {
            'blue': 'img/car/wheel/blue_arrow.png',
            'gray': 'img/car/wheel/gray_arrow.png',
            'green': 'img/car/wheel/green_arrow.png',
            'red': 'img/car/wheel/red_arrow.png',
            'white': 'img/car/wheel/white_arrow.png',
            'yellow': 'img/car/wheel/yellow_arrow.png'
        }
        """

        def resize(img, factor):
            sx, sy = (int(factor * x) for x in img.get_size())
            return pygame.transform.smoothscale(img, (sx, sy))

        _scale = surface.get_size()[1] / \
            pygame.image.load(images['red']).convert().get_size()[1] * 0.9
        self.arrows = {k: resize(pygame.image.load(v).convert(), _scale)
                       for k, v in images.items()}

        self.center = surface.get_rect().center
        self.pos = {
            'left': None,
            'right': None,
            'up': None,
            'down': None
        }

    def display(self, colors):
        """
        colors = {
            'left': 'color',
            'right': 'color',
            'up': 'color',
            'down': 'color'
        }
        """
        pass


class GUIModel(object):

    def __init__(self, surface, images, positions):
        """
        images = {
            'base': 'img/car/silueta.png',
            'wheels': {
                'blue': 'img/car/wheel/blue_arrow.png',
                'gray': 'img/car/wheel/gray_arrow.png',
                'green': 'img/car/wheel/green_arrow.png',
                'red': 'img/car/wheel/red_arrow.png',
                'white': 'img/car/wheel/white_arrow.png',
                'yellow': 'img/car/wheel/yellow_arrow.png'
            }
        }
        """

        def resize(img, factor):
            sx, sy = (int(factor * x) for x in img.get_size())
            return pygame.transform.smoothscale(img, (sx, sy))

        self.surface = surface
        self.center = surface.get_rect().center

        base = pygame.image.load(images['base']).convert_alpha()
        _scale = surface.get_size()[1] / base.get_size()[1] * 0.9

        self.base = resize(base, _scale)

        self.wheels = {k: resize(pygame.image.load(v).convert_alpha(), _scale)
                       for k, v in images['wheels'].items()}

        self.positions = {k: (int(v[0] * _scale), int(v[1] * _scale))
                          for k, v in positions.items()}

    def _center_on(self, image, x, y):
        sx, sy = self.center
        ix, iy = image.get_size()

        tx = x - ix // 2
        ty = y - iy // 2
        return tx, ty

    def _display_image(self, image, x, y):
        self.surface.blit(image, (x, y))

    def update(self, color, angle):

        # reset the surface to black
        self.surface.fill((0, 0, 0))

        x, y = self._center_on(self.base, *self.center)
        self._display_image(self.base, x, y)

        # estas giran
        # tl
        tl = self.positions['tl']
        rot = pygame.transform.rotate(self.wheels[color], angle)
        x, y = self._center_on(rot, self.center[0] + tl[0], tl[1])
        self._display_image(rot, x, y)

        # tr
        tr = self.positions['tr']
        rot = pygame.transform.rotate(self.wheels[color], angle)
        x, y = self._center_on(rot, self.center[0] + tr[0], tr[1])
        self._display_image(rot, x, y)

        # estas no giran
        # bl
        bl = self.positions['bl']
        x, y = self._center_on(
            self.wheels[color], self.center[0] + bl[0], bl[1])
        self._display_image(self.wheels[color], x, y)

        # br
        br = self.positions['br']
        x, y = self._center_on(
            self.wheels[color], self.center[0] + br[0], br[1])
        self._display_image(self.wheels[color], x, y)

        pygame.display.update()
