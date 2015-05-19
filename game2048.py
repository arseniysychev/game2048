# -*- coding: utf-8 -*-

"""
*** Игра 2048 ***

Управление:
"a" - Вправо'
"d" - Влево'
"w" - Ввех'
"s" - Вниз'
"z" - Выйти
"p" - Сохранить'
"l" - Загрузить'
"h" - Справка'

Используйте клавиши на клавиатуре, чтобы перемещать плитки.
Когда две плитки с одинаковыми цифрами соприкасаются, они сливаются в одну!
Целью игры является получение плитки номинала «2048»
"""

import pickle

import field

def help_print(): print('%s' % (__doc__))

help_print()

moves = ['a','s','d','w','z','h','l','p']

game = field.Field()

while True:
    try:
        move = raw_input('Move : ').lower()
        if move not in moves:
            raise ValueError()
        elif move == 'z':
            break
        elif move == 'h':
            help_print()
            continue
        elif move == 'p':
            filename = raw_input('Save as : ').lower()
            f = open(filename, 'w')
            pickle.dump(game, f)
            f.close()
            continue
        elif move == 'l':
            filename = raw_input('Load as : ').lower()
            f = open(filename, 'r')
            game = pickle.load(f)
            f.close()
            game.printer()
            continue
    except ValueError:
        game.event_print(0)
    else:
        if game.game_control(move) == 0:
            break