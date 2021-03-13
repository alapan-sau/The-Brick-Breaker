from input import input_to
import os
import numpy as np
import time
from screen import Screen
from Objects import ExplodingBrick, Fast_Ball, Multiply_ball, Paddle, Thru_ball, UnBrick
from Objects import Ball
from Objects import Brick
from Objects import Expand_paddle
from Objects import Shrink_paddle
from Objects import Paddle_grab
import input
from input  import Get
import sys
KEYS = ['a','d']

class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        cols = int(cols)

        if(rows < 32 or cols < 128):
            print("Increase Terminal Screen Size!!")
            sys.exit(0)

        self._floor = int(0.1*(int(rows)))
        self._margin = int(0.4*(int(rows)))
        self._height = int(rows) - self._floor
        self._width = int(cols) - self._margin
        self._screen = Screen(self._height, self._width)
        self._time = time.time()
        self._lives = 7
        self._score = 0

        size = 13
        left = size * 2 - 5
        top = 5
        #set the componets
        self._paddle = Paddle([int(self._width/2)-6, self._height-1],[13,1],[0,0], [self._width,self._height])
        self._balls = []
        self._balls.append(Ball([int(self._width/2)-1, self._height-2],[1,1],[0,0], [self._width,self._height], True))


        self._frame = [     [left+ size*0,top],[left+ size*5,top],

                            [left+ size*0,top+1],[left+ size*1,top+1],
                            [left+ size*4,top+1],[left+ size*5,top+1],

                            [left+ size*0,top+2],[left+ size*1,top+2],
                            [left+ size*2,top+2],[left+ size*3,top+2],
                            [left+ size*4,top+2],[left+ size*5,top+2],

                            [left+ size*1,top+3],[left+ size*2,top+3],
                            [left+ size*3,top+3],[left+ size*4,top+3],

                            [left+ size*2,top+4],[left+ size*3,top+4],

                            [left+ size*2,top+6],[left+ size*3,top+6],

                            [left+ size*1,top+7],[left+ size*2,top+7],
                            [left+ size*3,top+7],[left+ size*4,top+7],

                            [left+ size*0,top+8],[left+ size*1,top+8],
                            [left+ size*2,top+8],[left+ size*3,top+8],
                            [left+ size*4,top+8],[left+ size*5,top+8],

                            [left+ size*2,top+9],[left+ size*3,top+9]

                    ]
        self._power_frame = [   5, 0,

                                1, 2,
                                2, 1,

                                5, 0,
                                0, 0,
                                0, 0,

                                3, 3,
                                4, 4,

                                0, 0,

                                0, 0,

                                4, 3,
                                1, 2,

                                2, 3,
                                6, 6,
                                6, 6,

                                6, 2,
                        ]
        self._brick_strength_frame = [
                                1, 3,

                                2, 2,
                                3, 1,

                                2, 2,
                                2, 3,
                                3, 1,

                                1, 1,
                                1, 1,

                                3, 1,

                                2, 1,

                                2, 2,
                                0, 0,

                                -1, -2,
                                -3, -3,
                                -1, -3,

                                0, 0

                            ]

        self._bricks = []
        self._power_ups = []

        for i in range(0, len(self._power_frame)):
            p_type = self._power_frame[i]
            if(p_type==0):
                self._power_ups.append(None)
            elif(p_type==1):
                self._power_ups.append(Expand_paddle(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))
            elif(p_type==2):
                self._power_ups.append(Shrink_paddle(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))
            elif(p_type==3):
                self._power_ups.append(Paddle_grab(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))
            elif(p_type==4):
                self._power_ups.append(Thru_ball(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))
            elif(p_type==5):
                self._power_ups.append(Fast_Ball(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))
            elif(p_type==6 ):
                self._power_ups.append(Multiply_ball(self._frame[i]+np.array([3,0]),[1,1],[0,1],[self._width,self._height]))


        for i in range(0, len(self._frame)):
            if(self._brick_strength_frame[i]< 0):
                self._bricks.append(ExplodingBrick(self._frame[i],[size,1],[0,0],[self._width,self._height],-self._brick_strength_frame[i],self._power_ups[i]))
            elif(self._brick_strength_frame[i]):
                self._bricks.append(Brick(self._frame[i],[size,1],[0,0],[self._width,self._height],self._brick_strength_frame[i],self._power_ups[i]))
            else:
                self._bricks.append(UnBrick(self._frame[i],[size,1],[0,0],[self._width,self._height],100,self._power_ups[i]))

    ############## KEYBOARD INTERRUPT ########################

    def handle_keyboard_interrupt(self):
        get = Get()
        ch = input_to(get.__call__)
        if ch in KEYS:
            self._paddle.move(ch)
            # fixed
            for ball in self._balls:
                ball.move_with_paddle(ch)

        elif(ch=='q'):
            sys.exit()

        elif(ch=='s'):
            for ball in self._balls:
                ball.start()

        elif(ch == 'r'):
            self._paddle = Paddle([int(self._width/2)-4, self._height-1],[13,1],[0,0], [self._width,self._height])
            self._balls = []
            self._balls.append( Ball([int(self._width/2), self._height-2],[1,1],[0,0], [self._width,self._height],True) )



    ################ COLLISIONS ################################

    def handle_paddle_ball_collision(self,ball,paddle):
        paddle_pos,paddle_size,paddle_speed = paddle.get_dimension()
        ball_pos,ball_size,ball_speed = ball.get_dimension()

        if(ball_pos[0] >= paddle_pos[0] and ball_pos[0] < paddle_pos[0] + paddle_size[0]):
            if( (ball_pos[1]+1 <= paddle_pos[1] and ball_pos[1]+1 + ball_speed[1] > paddle_pos[1]) ):
                # collision happened!!
                ball.paddle_collision(ball_pos[0]-paddle_pos[0] - int(paddle_size[0]/2))


    def handle_ball_brick_collision(self,ball,brick):

        if(not(brick.is_visible())):
            return
        brick_pos,brick_size,brick_speed = brick.get_dimension()
        ball_pos,ball_size,ball_speed = ball.get_dimension()


        # horizontal collision
        if(ball_pos[1] == brick_pos[1]):

            # ball from left
            if(ball_pos[0]< brick_pos[0] and ball_pos[0]+ball_speed[0]+1 >=brick_pos[0]):

                if(ball.is_thru()):
                    brick.thru_ball_collision(self)
                else:
                    new_ball_speed = ball_speed
                    new_ball_speed[0] = -new_ball_speed[0]
                    new_ball_pos = ball_pos
                    new_ball_pos[0] = brick_pos[0]-1
                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self)

            # ball from right
            if(ball_pos[0] > brick_pos[0]+brick_size[0] and ball_pos[0]+ball_speed[0] <= brick_pos[0]+brick_size[0]):
                if(ball.is_thru()):
                    brick.thru_ball_collision(self)
                else:
                    new_ball_speed = ball_speed
                    new_ball_speed[0] = -new_ball_speed[0]
                    new_ball_pos = ball_pos
                    new_ball_pos[0] = brick_pos[0]+brick_size[0]

                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self)

        # vertical collison
        if (ball_pos[0]+1  >= brick_pos[0] and ball_pos[0] <= brick_pos[0]+brick_size[0]):

            # ball from top
            if(ball_pos[1]+1 < brick_pos[1] and ball_pos[1]+1+ball_speed[1] >= brick_pos[1]):

                if(ball.is_thru()):
                    brick.thru_ball_collision(self)
                else:
                    new_ball_speed = ball_speed
                    new_ball_speed[1] = -new_ball_speed[1]
                    new_ball_pos = ball_pos
                    new_ball_pos[1] = brick_pos[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self)

            # ball from bottom
            if(ball_pos[1] >= brick_pos[1]+1 and ball_pos[1]+ball_speed[1] < brick_pos[1]+1):

                if(ball.is_thru()):
                    brick.thru_ball_collision(self)
                else:
                    new_ball_speed = ball_speed
                    new_ball_speed[1] = -new_ball_speed[1]
                    new_ball_pos = ball_pos
                    new_ball_pos[1] = brick_pos[1]+1
                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self)

    def handle_paddle_power_up_collision(self, paddle, power_up):
        if(power_up==None):
            return

        if(not power_up.is_visible()):
            return

        paddle_pos,paddle_size,paddle_speed = paddle.get_dimension()
        power_up_pos,power_up_size,power_up_speed = power_up.get_dimension()

        if(power_up_pos[0] >= paddle_pos[0] and power_up_pos[0] < paddle_pos[0] + paddle_size[0]):
            if( (power_up_pos[1]+1 <= paddle_pos[1] and power_up_pos[1]+1 + power_up_speed[1] > paddle_pos[1]) ):
                # collision happened!!
                power_up_type = power_up.get_type()
                if(0 < power_up_type <= 2):
                    power_up.activate(self._paddle)
                elif(power_up_type <= 5):
                    for ball in self._balls:
                        power_up.activate(ball)
                elif(power_up_type==6):
                    power_up.activate(self)



    ######## POWER UP functionalitites ###############

    def get_num_ball(self):
        return len(self._balls)

    def multiply_ball(self):
        num_of_balls = len(self._balls)
        for i in range(0, num_of_balls):
            ball_pos,ball_size,ball_speed = self._balls[i].get_dimension()

            new_ball_pos = []
            new_ball_speed = []

            new_ball_pos.append(ball_pos[0])
            new_ball_pos.append(ball_pos[1])
            new_ball_speed.append(-ball_speed[0])
            new_ball_speed.append(-ball_speed[1])

            self._balls.append(Ball(new_ball_pos,[1,1], new_ball_speed, [self._width, self._height],False))

    def divide_ball(self, num):
        num_of_balls = len(self._balls)
        if(num_of_balls <= num):
            return
        remove_num = num_of_balls - num

        for i in range(0,remove_num):
            self._balls.remove(self._balls[i])




    ################ LIFE - SCORE ###################

    def increase_score(self, num):
        self._score = self._score + num


    def new_life(self):

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_activated()):
                if(0 < power_up.get_type() <= 2):
                    power_up.deactivate(self._paddle)
                elif(power_up.get_type() <= 5):
                    for ball in self._balls:
                        power_up.deactivate(ball)
                elif(power_up.get_type() == 6):
                    power_up.deactivate(self)

        self._screen.blink_screen()

        self._lives = self._lives - 1
        if(self._lives == 0):
            self._screen.game_lost(self._score)
            sys.exit()
        self._paddle = Paddle([int(self._width/2)-6, self._height-1],[13,1],[0,0], [self._width,self._height])
        self._balls = []
        self._balls.append(Ball([int(self._width/2)-1, self._height-2],[1,1],[0,0], [self._width,self._height], True))

    ################### BONUS ##############################

    def explode_neighbour(self, pos, size):
        for brick in self._bricks:
            brick_pos,brick_size,brick_speed = brick.get_dimension()

            if(not brick.is_visible()):
                continue
            elif(pos[0] == brick_pos[0]):
                if(pos[1]+size[1] == brick_pos[1] or pos[1]-size[1] == brick_pos[1]):
                    brick.thru_ball_collision(self)

            elif(pos[1] == brick_pos[1]):
                if(pos[0]+size[0] == brick_pos[0] or pos[0]-size[0] == brick_pos[0]):
                    brick.thru_ball_collision(self)

            elif((pos[0]+size[0] == brick_pos[0] or pos[0]-size[0] == brick_pos[0]) and (pos[1]+size[1] == brick_pos[1] or pos[1]-size[1] == brick_pos[1])):

                brick.thru_ball_collision(self)

    ################## UTILITY ####################

    def place_items(self):
        self._screen.place_object(self._paddle)

        for ball in self._balls:
            self._screen.place_object(ball)

        for brick in self._bricks:
            if(brick.is_visible()):
                self._screen.place_object(brick)

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_visible()):
                self._screen.place_object(power_up)

    def move_items(self):
        for ball in self._balls:
            if(ball.move()):
                self._balls.remove(ball)
            if(len(self._balls) == 0 ):
                self.new_life()

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_visible()):
                power_up.move()

    def handle_collisions(self):
        for ball in self._balls:
            self.handle_paddle_ball_collision(ball, self._paddle)

        for brick in self._bricks:
            for ball in self._balls:
                self.handle_ball_brick_collision(ball,brick)

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_visible()):
                self.handle_paddle_power_up_collision(self._paddle,power_up)

    def handle_power_up_timings(self):
        for power_up in self._power_ups:
            # if(power_up != None and power_up.is_visible()):
                # self._screen.place_object(power_up)

            if(power_up != None and power_up.is_activated()):
                if(time.time() - power_up.get_time() > 60):
                    if(0< power_up.get_type() <=2):
                        power_up.deactivate(self._paddle)
                    elif(power_up.get_type() <= 5):
                        for ball in self._balls:
                            power_up.deactivate(ball)
                    elif(power_up.get_type() == 6):
                        power_up.deactivate(self)

    def check_win(self):
        for brick in self._bricks:
            if(brick.is_visible()):
                return
        self._screen.game_won(game._score)


    ############# RUN ################################
    def run(self):
        while 1:
            self._screen.clean()
            self.handle_keyboard_interrupt()
            self._screen.reset_screen()
            self.handle_collisions()
            self.check_win()
            self.move_items()
            self.place_items()
            self.handle_power_up_timings()
            self._screen.render_screen()
            print("LIVES: ",self._lives,"TIME: ",int(time.time()-self._time),"SCORE: ",self._score)



game = Game()
game.run()


