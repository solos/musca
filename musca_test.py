#!/usr/bin/env python
# -*- coding: utf-8 -*-


from musca import Musca


def test():
    musca = Musca()
    musca.use(8)
    musca.create()
    musca.vsplit()
    musca.split()
    import time
    time.sleep(0.2)
    musca.enter('ssh server')
    musca.slide('right')
    musca.create()
    musca.slide('down')
    musca.create()
    musca.split()
    musca.slide('right')
    musca.create()
    musca.vsplit()
    musca.slide('down')
    musca.create()

if __name__ == '__main__':
    test()
