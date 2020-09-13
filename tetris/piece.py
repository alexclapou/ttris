import pygame as pg
import operator
import numpy as np

block_size = 30

class Board(object):
    def __init__(self, screen):
        self.screen = screen
        self.board = [[0 for i in range(10)]for j in range(20)]
        self.score = 0

    def get_board(self):
        return self.board

    def draw_board(self):
        for i in range(5, block_size):
           for j in range(block_size):
               pg.draw.rect(self.screen, (250, 250, 250), pg.Rect(block_size*i, block_size*j, block_size, block_size), 1)

    def block_size(self):
        return block_size

    def delete_piece(self, all_pieces, piece, lines_to_delete):
        for coord in lines_to_delete:
            row, column = coord
            self.board[row][column] = 0

    def empty_line(self, all_pieces, line_index):#TODO delete what s under
        pieces_to_delete = []
        for piece in list(all_pieces):
            #check if a piece is on the line we want to empty, if it has a block on that line, erase it from list
            y = 0
            piece_deleted = False
            for line in piece.get_shape():
                x = block_size*8
                for character in line:
                    if character == 'O':
                        if (y+all_pieces[piece][0])//30 == line_index:
                            piece_deleted = True
                        x += block_size
                y += block_size
            if piece_deleted:
                lines_to_delete = piece.get_coordinates(all_pieces[piece][0], all_pieces[piece][1])
                self.delete_piece(all_pieces, piece, lines_to_delete)
                pieces_to_delete.append(piece)
        for piece_to_delete in pieces_to_delete:
            all_pieces.pop(piece_to_delete, None)

    def pieces_down(self, all_pieces):
        for piece in sorted(all_pieces, key=all_pieces.get, reverse=True):
            lines_to_delete = piece.get_coordinates(all_pieces[piece][0], all_pieces[piece][1])
            self.delete_piece(all_pieces, piece, lines_to_delete)
            while not piece.placed(all_pieces[piece][0]+block_size, all_pieces[piece][1]):
                all_pieces[piece][0] += block_size
            self.place_piece(piece, all_pieces[piece][0], all_pieces[piece][1])

    def check_full_lines(self, all_pieces):
        line = 0
        for line_index, line in reversed(list(enumerate(self.board))):
            if len(set(line)) == 1 and line[0] == 1: # if one 
                self.empty_line(all_pieces, line_index)
                self.pieces_down(all_pieces)

    def place_piece(self, piece, line_piece, column_piece):
        shape = piece.get_shape()
        y = 0
        for line in shape:
            x = block_size*8
            for character in line:
                if character == 'O':
                    self.board[(y+line_piece)//30][(x+column_piece)//30-5]=1
                x += block_size
            y += block_size


class Piece(object):
    def __init__(self, shape, screen, color, size, board):
        self.current_shape = 0
        self.shapes = shape
        self.shape = self.shapes[self.current_shape]
        self.screen = screen
        self.color = color
        self.size = size
        self.min_left = self.screen.get_size()[0]
        self.max_right = 0
        self.max_bottom = 0
        self.board = board.get_board()

    def get_final_column_value(self, row, column, op):
        keep_column_move_leftside = column
        while self.occupied(row, keep_column_move_leftside):
            keep_column_move_leftside = op(keep_column_move_leftside, block_size)
        return keep_column_move_leftside


    def change_coordinates(self, row, column):
        y = 0
        right_bound = 0
        left_bound = 9
        lines = []
        for line in self.shape:
            x = block_size*8
            for character in line:
                if character == 'O':
                    while (y+row)//30 > 19:
                        row -= block_size
                    right_bound = max(right_bound, (x+column)//30-5)
                    left_bound = min(left_bound, (x+column)//30-5)
                x += block_size
            lines.append((y+row)//30)
            y += block_size
        while left_bound < 0:
            left_bound += 1
            column += block_size
        while right_bound > 9:
            right_bound -= 1
            column -= block_size
        try_right = self.get_final_column_value(row, column, operator.add)
        try_left = self.get_final_column_value(row, column, operator.sub)
        if abs(try_right - column) < abs(try_left - column):
            column = try_right
        else:
            column = try_left
        while self.occupied(row, column):
            row -= block_size
        return [row, column]

    def next_form(self, row, column):
        self.current_shape += 1
        self.shape = self.shapes[self.current_shape % 4]
        return self.change_coordinates(row, column)

    def get_coordinates(self, line_piece, column_piece):
        coord = set()
        y = 0
        for line in self.shape:
            x = block_size*8
            for character in line:
                if character == 'O':
                    coord.add(((y+line_piece)//30, (x+column_piece)//30-5))
                x += block_size
            y += block_size
        return coord

    def get_shape(self):
        return self.shape

    def get_color(self):
        return self.color

    def get_height(self):
        height = 0
        for line in self.shape:
            O_char = False
            for character in line:
                if character == 'O':
                    O_char = True
            if O_char:
                height += 1
        return height

    def draw(self, speedy, left_right):
        y = 0
        self.min_left = self.screen.get_size()[0]
        self.max_right = 0

        for line in self.shape:
            x = block_size*8
            #need a varaible for getting coordinates
            for character in line:
                if character == 'O':
                    sec_rectangle = pg.Rect(x+left_right, y+speedy,block_size,block_size)
                    self.min_left = min(x+left_right, self.min_left)
                    self.max_right = max(x+left_right+block_size, self.max_right)
                    self.max_bottom = y+speedy
                    self.screen.fill(self.color, sec_rectangle)
                    main_rectangle = pg.draw.rect(self.screen, (255,255,255), sec_rectangle, 1)
                x += block_size
            y += block_size
        return [speedy, left_right]

    def occupied(self, line_piece, column_piece):
        y = 0

        for line in self.shape:
            x = block_size*8
            #need a varaible for getting coordinates
            for character in line:
                if character == 'O':
                    if (y+line_piece)//30 > 19:
                        return True
                    if self.board[(y+line_piece)//30][(x+column_piece)//30-5] == 1: #5 number of black squares
                        return True
                x += block_size
            y += block_size
        return False

    def left_bound(self, line, column):
        return self.min_left > block_size*5 and not self.occupied(line, column)

    def right_bound(self, line, column):
        return self.max_right < self.screen.get_size()[0] and not self.occupied(line, column)

    def get_bottom_point(self):
        return self.max_bottom

    def get_right_point(self):
        return self.max_right

    def get_left_point(self):
        return self.min_left

    def placed(self, line, column):
        return not block_size + self.max_bottom < self.screen.get_size()[1] or self.occupied(line, column)
