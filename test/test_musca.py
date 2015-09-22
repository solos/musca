#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/..' % current)

from musca import Musca
import musca
import unittest
from mock import patch, call
from musca import KEYCODES


class MuscaTests(unittest.TestCase):

    def base_16_keycode(self, input):
        return int(KEYCODES[input], 16)

    def assert_in_press_release(self, keys):
        press_list = self.vk.return_value.press_keysym.call_args_list
        release_list = self.vk.return_value.release_keysym.call_args_list
        for expected in keys:
            self.assertIn(call(self.base_16_keycode(expected)),
                          press_list)
            self.assertIn(call(self.base_16_keycode(expected)),
                          release_list)
            self.assertEqual(len(press_list), 2)
            self.assertEqual(len(release_list), 2)

    def setUp(self):
        self.vk_patcher = patch("musca.virtkey.virtkey", autospec=True)
        self.vk = self.vk_patcher.start()
        self.musca = Musca()

    def tearDown(self):
        self.vk_patcher.stop()

    def test_version(self):
        self.assertIsNotNone(musca.__version__, '0.0.2')

    def test_enter(self):
        self.musca.use(8)
        self.assert_in_press_release((str(8), self.musca.Mod4))

    def test_enter_char(self):
        self.musca.enter_char('c')
        self.assertTrue(self.vk.return_value.press_unicode.call_args,
                        call(ord('c')))
        self.assertTrue(self.vk.return_value.release_unicode.call_args,
                        call(ord('c')))

    # def test_focus(self):
    #     from musca import MAPS
    #     self.musca.MAPS = MAPS
    #     self.musca.focus(["left"])

    def test_split(self):
        self.musca.split()
        self.assert_in_press_release(("h", self.musca.Mod4))

    def test_vsplit(self):
        self.musca.vsplit()
        self.assert_in_press_release(("v", self.musca.Mod4))

    def test_create(self):
        self.musca.create()
        self.assert_in_press_release(('t', self.musca.Mod4))

    def test_use(self):
        self.musca.use(1)
        self.assert_in_press_release(('1', self.musca.Mod4))

    def test_use_next(self):
        self.musca.use_next()
        self.assert_in_press_release(('n', self.musca.Mod4))

    def test_use_prev(self):
        self.musca.use_prev()
        self.assert_in_press_release(('p', self.musca.Mod4))

    def test_slide(self):
        for direction in ['left', 'right', 'up', 'down']:
            self.vk.return_value.press_keysym.reset_mock()
            self.vk.return_value.release_keysym.reset_mock()
            self.musca.slide(direction)
            self.assert_in_press_release((direction.capitalize(),
                                          self.musca.Mod1))
        #  Test invalid direction

        with patch("sys.stdout") as fake_stdout:
            self.musca.slide("hulahoop")
            fake_stdout.assert_has_calls([call.write("direction not in ['left', 'right', 'up', 'down']"),
                                          call.write("\n")])
if __name__ == '__main__':
    unittest.main(verbosity=2)
