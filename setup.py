# -*- coding: utf-8 -*-

from distutils.core import setup
import setup_translate

pkg = 'Extensions.ModernWebif'
setup (name = 'enigma2-plugin-extensions-modernwebif',
	description = 'Webinterface for your reciver',
	cmdclass = setup_translate.cmdclass,
)
