import os, sys
import pygame as pg
from shapes import Shapes
from piece import *

pg.init()
pg.display.set_caption('ttris')
size = (block_size*15, block_size*20)
clor = 100,100,100,100
speed = 10
level = 0
left_right = 0
time_delay = 600
screen = pg.display.set_mode(size)

shapes = Shapes()
b = Board(screen)
all_pieces = {}

new_piece = Piece(shapes.get_random_shape(), screen, shapes.get_random_color(), size, b)
all_pieces[new_piece] = [level, left_right] #0-line 1-column
time_init = pg.time.get_ticks()
time_left = pg.time.get_ticks()
time_right = pg.time.get_ticks()
screen.fill((0,0,0))
b.draw_board()
all_pieces[new_piece] = new_piece.draw(level, left_right)
pg.display.update()
level += b.block_size()
pg.key.set_repeat(600)
keep_div = 1

while 1:
    screen.fill((0,0,0))
    b.draw_board()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    time_now = pg.time.get_ticks()
    keys = pg.key.get_pressed()

    if time_now - time_left > 200 and keys[pg.K_SPACE]:
        all_pieces[new_piece] = new_piece.next_form(all_pieces[new_piece][0], all_pieces[new_piece][1])#all_piece[piece][0]/[1]
        time_left = time_now

    '''
    if new_piece.left_bound(all_pieces[new_piece][0], all_pieces[new_piece][1]) and keys[pg.K_LEFT] and time_now - time_left > 600:
            left_right -= b.block_size()
            time_left = time_now

        elif new_piece.right_bound(all_pieces[new_piece][0], all_pieces[new_piece][1]) and keys[pg.K_RIGHT] and time_now - time_right > 600:
            left_right += b.block_size()
            time_right = time_now
    '''
    if new_piece.left_bound(all_pieces[new_piece][0], all_pieces[new_piece][1]) and keys[pg.K_LEFT] and time_now - time_left > 600:
        all_pieces[new_piece][1] -= b.block_size()
        time_left = time_now

    elif new_piece.right_bound(all_pieces[new_piece][0], all_pieces[new_piece][1]) and keys[pg.K_RIGHT] and time_now - time_right > 600:
        all_pieces[new_piece][1] += b.block_size()
        time_right = time_now

    elif not new_piece.placed(all_pieces[new_piece][0], all_pieces[new_piece][1]) and time_now - time_init > 600:
        screen.fill((0,0,0))
        b.draw_board()
        #draw all the pieces on the board and set the left_right and level for the actual piece
        #all_pieces[new_piece][1] = left_right
        for piece in all_pieces:
            _level, _left_right = all_pieces[piece][0], all_pieces[piece][1]
            all_pieces[piece] = piece.draw(_level, _left_right)
        if not new_piece.placed(all_pieces[new_piece][0], all_pieces[new_piece][1]):
            all_pieces[new_piece][0] += b.block_size()
        time_init = time_now
        pg.display.update()
    
    elif keys[pg.K_DOWN]:
        keep_div = time_init - time_init // 20
        time_init = time_now // keep_div

    if new_piece.placed(all_pieces[new_piece][0], all_pieces[new_piece][1]):
        if all_pieces[new_piece][0] == all_pieces[new_piece][1] == 0:
            break# end game
        if new_piece.occupied(all_pieces[new_piece][0], all_pieces[new_piece][1]):
            all_pieces[new_piece][0] -= block_size
        b.place_piece(new_piece, all_pieces[new_piece][0], all_pieces[new_piece][1])
        new_piece = Piece(shapes.get_random_shape(), screen, shapes.get_random_color(), size, b)
        level, left_right = 0, 0
        all_pieces[new_piece] = [level, left_right]
        pg.time.delay(300)
        b.check_full_lines(all_pieces)
