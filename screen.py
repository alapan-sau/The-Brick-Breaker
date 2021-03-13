import numpy as np
import time
import sys
from color import bg, fg, reset

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
                     self._board[i][j]=bg.blue+' '+reset
                # Left and Right Wall
                elif(j==0 or j==self._width-1):
                    self._board[i][j]=bg.blue+' '+reset


    def place_object(self, obj):
        pos,size,speed = obj.get_dimension()
        structure = obj.get_structure()

        for i in range(pos[1],pos[1]+size[1]):
            for j in range(pos[0],pos[0]+size[0]):
                self._board[i][j] = structure[i-pos[1]][j-pos[0]]

    def blink_screen(self):
        self.reset_screen()
        self.render_screen()
        time.sleep(0.1)

    def game_won(self, score):

        print("\033[2J") # clear the screen!!
        print("\033[0;0H")
        message = '''
              __     __          __          ___       _       __
              \ \   / /          \ \        / (_)     | |   _  \ \\
               \ \_/ /__  _   _   \ \  /\  / / _ _ __ | |  (_)  | |
                \   / _ \| | | |   \ \/  \/ / | | '_ \| |       | |
                 | | (_) | |_| |    \  /\  /  | | | | |_|   _   | |
                 |_|\___/ \__,_|     \/  \/   |_|_| |_(_)  (_)  | |
                                                                /_/
                '''



        print("\n\n\n\n\n\n\n\n\n")
        print(fg.green + message + reset)
        print("\n\n\n\n\n\n\n\n\n\n")
        print("The Score is ", score)
        sys.exit(0)

    def game_lost(self, score):
        print("\033[2J") # clear the screen!!
        print("\033[0;0H")
        message = '''
                __     __           ___              __    _         __
                \ \   / /           | |             | |   | |   _   / /
                 \ \_/ /__  _   _   | |     ___  ___| |_  | |  (_) | |
                  \   / _ \| | | |  | |    / _ \/ __| __| | |      | |
                   | | (_) | |_| |  | |___| (_) \__ \ |_  |_|   _  | |
                   |_|\___/ \__,_|  |______\___/|___/\__| (_)  (_) | |
                                                                    \_\\
        '''

        print("\n\n\n\n\n\n\n\n\n")
        print(fg.red + message + reset)
        print("\n\n\n\n\n\n\n\n\n\n")
        print("The Score is ", score)
        sys.exit(0)