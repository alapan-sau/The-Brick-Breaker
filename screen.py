import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
import time



class Screen:
    def __init__(self, height, width):
        self._height = height
        self._width = width

        # Start a screen
        self._board = np.array([['' for j in range(self._width)] for i in range(self._height)], dtype='object')
        print("\033[2J") # clear the screen!!

    def clean(self):
        self._board = np.array([['' for j in range(self._width)] for i in range(self._height)], dtype='object')
        # set cursor to beginning
        print("\033[0;0H")

        for i in range(self._height):
            for j in range(self._width):
                print(self._board[i][j], end='')
            print("")

    def render_screen(self):
        # set cursor to beginning
        print("\033[0;0H")

        for i in range(self._height):
            for j in range(self._width):
                print(self._board[i][j], end='')
            print("")


    def reset_screen(self):
        # Adjust and start a screen
        self._board = np.array([[' ' for j in range(self._width)] for i in range(self._height)], dtype='object')

        # Adjust the constant background
        #setup walls
        for i in range(self._height):
            for j in range(self._width):
                # Top wall
                if(i==0):
                     self._board[i][j]='_'
                # Left and Right Wall
                elif(j==0 or j==self._width-1):
                    self._board[i][j]='|'


    def place_object(self, obj):
        pos,size,speed = obj.get_dimension()
        structure = obj.get_structure()

        for i in range(pos[1],pos[1]+size[1]):
            for j in range(pos[0],pos[0]+size[0]):
                self._board[i][j] = structure[i-pos[1]][j-pos[0]]
