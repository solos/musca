#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import virtkey
from keycodes import KEYCODES

__version__ = '0.0.1'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

v = virtkey.virtkey()
MAPS = {
    'left': 'h',
    'right': 'l',
    'up': 'k',
    'down': 'j',
}

DIRECTIONS = set(['left', 'right', 'up', 'down'])


class Musca(object):

    def __init__(self, config=None, **kargs):
        if config:
            self.Mod4 = config['Mod4']
            self.Mod1 = config['Mod1']
            self.Shift = config['Shift']
        else:
            self.Mod4 = 'Super_L'
            self.Mod1 = 'Alt_L'
            self.Shift = 'Shift_L'

    def enter(self, keys):
        for key in keys:
            if '+' in key:
                arr = key.split('+')
                for i in arr:
                    keycode = int(KEYCODES[i], 16)
                    v.press_keysym(keycode)
                for i in arr:
                    keycode = int(KEYCODES[i], 16)
                    v.release_keysym(keycode)
            else:
                keycode = int(KEYCODES[key], 16)
                v.press_keysym(keycode)
                v.release_keysym(keycode)

    def enter_char(self, char):
        v.press_unicode(ord(char))
        v.release_unicode(ord(char))

    def join(self, keys):
        return '+'.join(keys)

    def create(self):
        self.enter(map(self.join, [[self.Mod4, 't'], ]))

    def focus(self, direction=['left']):
        if isinstance(direction, list):
            for i in direction:
                self.focus(i)
        elif isinstance(direction, basestring):
            direc = self.MAPS[direction]
            self.enter(self.join([self.Mod4 + self.Shift + direc]))
        else:
            return

    def use(self, number):
        self.enter(map(self.join, [
            [self.Mod4, str(number)],
        ]))

    def use_next(self):
        self.enter(map(self.join, [
            [self.Mod4, 'n'],
        ]))

    def use_prev(self):
        self.enter(map(self.join, [
            [self.Mod4, 'p'],
        ]))

    def move(self, number):
        self.enter(map(self.join, [
            [self.Mod4, self.Shift, str(number)],
        ]))

    def slide(self, direction):
        if direction.lower() in DIRECTIONS:
            self.enter(map(self.join, [
                [self.Mod1, direction.capitalize()],
            ]))
        else:
            print '''direction not in ['left', 'right', 'up', 'down']'''

    def swap(self, direction='left'):
        if direction.lower() in DIRECTIONS:
            self.enter(map(self.join, [
                [self.Mod1, self.Mod4, direction.capitalize()],
            ]))
        else:
            print '''direction not in ['left', 'right', 'up', 'down']'''

    def split(self):
        self.enter(map(self.join, [
            [self.Mod4, 'h'],
        ]))

    def vsplit(self):
        self.enter(map(self.join, [
            [self.Mod4, 'v'],
        ]))


if __name__ == '__main__':
    pass
