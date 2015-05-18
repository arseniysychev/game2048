# -*- coding: utf-8 -*-
class Item(object):
    
    def __init__(self):
        self.num = 0


class Field(object):
    
    len = 2
    score = 0
    items = []
    max_item = 0
    
    def __init__(self):
        for i in range(self.len):
            self.items.append([])
            for j in range(self.len):
                item = Item()
                self.items[i].append(item.num) 
                # Серьезно ошибся! И передал значение экземпляра, а не сам экземпляр
        self.movepc()
        self.printer()
        
    def game_control(self, move):
        result = self.some_move(move)
        if result:
            self.items = result
            self.movepc()
            self.printer()
            if self.max_item == 64:
                self.event_print(3)
                return 0
            if not self.is_set_move():
                self.event_print(2)
                return 0
        else:
            self.event_print(1)
            
    def is_set_move(self):
        for val in 'daws':
            if self.some_move(val):
                return True
        return False
            
    def some_move(self, move):
        matrix_old = self.items[:]
        matrix_new = self.items[:]
        
        def rotation_matrix(matrix, direction):
            iter_list = range(self.len)
            if direction == 'r':
                # По часовой стрелке
                return \
                [[matrix[j][i] for j in iter_list] for i in iter_list[::-1]]
            elif direction == 'l':
                # Против часовой стрелки
                return \
                [[matrix[j][i] for j in iter_list[::-1]] for i in iter_list]
            elif direction == 's':
                # Симметрия по горизонтали
                return \
                [[matrix[i][j] for j in iter_list[::-1]] for i in iter_list]
            else:
                raise InvalidArgument('Неверный аргумент для функции поворота')

        if move == 'd':        
            matrix = matrix_new
            matrix_new = self.shift_rows(matrix)
        elif move == 'a':
            matrix = rotation_matrix(matrix_new, 's')
            rezult = self.shift_rows(matrix)
            matrix_new = rotation_matrix(rezult, 's')
        elif move == 'w':
            matrix = rotation_matrix(matrix_new, 'l')
            rezult = self.shift_rows(matrix)
            matrix_new = rotation_matrix(rezult, 'r')
        else:
            matrix = rotation_matrix(matrix_new, 'r')
            rezult = self.shift_rows(matrix)
            matrix_new = rotation_matrix(rezult, 'l')
            
        if matrix_old != matrix_new:
            return matrix_new
        else:
            return False
        
    def shift_rows(self, matrix):
        for i, line in enumerate(matrix):
            line = filter((lambda x: x != 0), line)
            line = self.sum_items(line)
            line = line[::-1] 
            while len(line) < self.len:
                line.append(0)
            for x in line:
                if x > self.max_item :
                    self.max_item = x
            line = line[::-1]
            matrix[i] = line
        return matrix

    def sum_items(self, list_in):
        list_out = []
        while len(list_in) > 1:
            if list_in[-1] == list_in[-2]:
                self.score += list_in[-1]*2
                list_out.append(list_in[-1]*2)
                list_in.pop()
                list_in.pop()
            else:
                list_out.append(list_in[-1])
                list_in.pop()
        if len(list_in) == 1:        
            list_out.append(list_in[0])
        return list_out[::-1]
                
    def movepc(self):
        empty_items = []
        for i, line in enumerate(self.items):
            for j, item in enumerate(line):
                if item == 0:
                    empty_items.append([i,j])
        import random
        try:
            n = random.choice(empty_items)
            self.items[n[0]][n[1]] = 2
        except IndexError:
            print 'here'
            self.event_print(2)
            return False
        
    def event_print(self, err):
        if err == 0 :
            print ('Неверное значение ввода' % ())
        elif err == 1 :
            print ('Ход не сделан. Ничего не изменилось' % ())
        elif err == 2 :
            print ('Ходы закончились ваш счет : %s' % (self.score))
        elif err == 3 :
            print ('Победа! Плитка номиналом : %d Счет : %d' % (self.max_item, self.score))

    def printer(self):
        print('Счет: %d' % (self.score))
        for i in self.items:
            for j in i:
                print ('%s' % (str(j).center(5,' '))),
            print('%s' % ('\n'))
                 

game = Field()

while True:
    try:
        x = raw_input('wsadz ').lower()
        if x not in ['a','s','d','w','z']:
            raise ValueError()
        elif x == 'z':
            break
    except ValueError:
        game.event_print(0)
    else:
        if game.game_control(x) == 0:
            break