import random
o_shape_1 = [
    '.OO.',
    '.OO.'
]

o_shape = [o_shape_1] * 4

i_shape_1 = [
        '..O.',
    '..O.',
    '..O.',
    '..O.'
]

i_shape_2 = [
        '.OOOO'
]

i_shape = [i_shape_1, i_shape_2] * 2

s_shape_1 = [
        '.OO',
        'OO.',
]

s_shape_2 = [
       '.O',
       '.OO',
       '..O'
]

s_shape_3 = [
       'O',
       'OO',
       '.O'
]

s_shape = [s_shape_1, s_shape_2, s_shape_1, s_shape_3]

z_shape_1 = [
        'OO',
        '.OO'
]

z_shape_2 = [
        '..O',
        '.OO',
        '.O.'
]

z_shape_3 = [
        '.O',
        'OO',
        'O.'
]

z_shape = [z_shape_1, z_shape_2, z_shape_1, z_shape_3]


l_shape_1 = [
    'O..',
    'OOO'
]

l_shape_2 = [
        '.OO',
        '.O',
        '.O'
]

l_shape_3 = [
        'OOO',
        '..O'
]

l_shape_4 = [
        '.O.',
        '.O.',
        'OO.'
]

l_shape = [l_shape_1, l_shape_2, l_shape_3, l_shape_4]

j_shape_1 = [
    '..O',
    'OOO'
]

j_shape_2 = [
        '.O',
        '.O',
        '.OO'
]

j_shape_3 = [
        'OOO',
        '..O'
]

j_shape_4 = [
        'OO',
        '.O',
        '.O'
]

j_shape = [j_shape_1, j_shape_2, j_shape_3, j_shape_4]

t_shape_1 = [
    '.OOO',
    '..O'
]

t_shape_2 = [
        '..O',
        '.OO',
        '..O'
]

t_shape_3 = [
    '..O',
    '.OOO'
]

t_shape_4 = [
        '..O',
        '..OO',
        '..O'
]

t_shape = [t_shape_1, t_shape_2, t_shape_3, t_shape_4]


class Shapes(object):
    def __init__(self):
        self.shapes = []
        self.colors = [[255, 70, 0],
                    [63, 135, 222],
                    [0, 255, 0],
                    [204, 137, 216],
                    [240, 213, 95],
                    [2, 8, 183],
                    [250, 217, 170]
        ]
        self.init_shapes()

    def get_random_shape(self):
        return random.choice(self.shapes)

    def get_random_color(self):
        return random.choice(self.colors)

    def get_square(self):
        return self.shapes[4]

    def init_shapes(self):
        self.shapes.append(o_shape)
        self.shapes.append(i_shape)
        self.shapes.append(s_shape)
        self.shapes.append(z_shape)
        self.shapes.append(l_shape)
        self.shapes.append(j_shape)
        self.shapes.append(t_shape)

