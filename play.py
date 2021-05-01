from input import input_to
import os
import numpy as np
import time
from screen import Screen
from Objects import Bomb, Bullet, ExplodingBrick, Fast_Ball, Fire_Ball, Multiply_ball, Paddle, Shoot_Paddle, Thru_ball, UFO, UnBrick
from Objects import Ball
from Objects import Brick
from Objects import Expand_paddle
from Objects import Shrink_paddle
from Objects import Paddle_grab
from Objects import RainbowBrick
import input
from input  import Get
import sys
import game_layout
from color import *

import simpleaudio as sa


KEYS = ['a','d']

class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        cols = int(cols)

        if(rows < 32 or cols < 128):
            print("Increase Terminal Screen Size!!")
            sys.exit(0)

        self._floor = int(0.1*(int(rows)))-4
        self._margin = int(0.4*(int(rows)))
        self._height = int(rows) - self._floor-4
        self._width = int(cols) - self._margin
        self._screen = Screen(self._height, self._width)
        self._time = time.time()
        self._counter=0
        self._rem_time=0
        self._fireball=0

        self._lives = 15
        self._score = 0
        self._level = 0
        size = game_layout.size
        left = game_layout.left
        top = game_layout.top

        self._frame = game_layout.frame
        self._power_frame = game_layout.power_frame
        self._brick_strength_frame = game_layout.brick_strength_frame

        self._brick_movement_time = 10

        self.make_layout()

    ############## KEYBOARD INTERRUPT ########################

    def handle_keyboard_interrupt(self):
        get = Get()
        ch = input_to(get.__call__)
        if ch in KEYS:
            self._paddle.move(ch)
            # if(self._level==2):
            #     self._ufo.move(ch)
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

        elif(ch == 'l'):
            self.level_up()

    ################ COLLISIONS ################################

    def handle_paddle_ball_collision(self,ball,paddle):
        paddle_pos,paddle_size,paddle_speed = paddle.get_dimension()
        ball_pos,ball_size,ball_speed = ball.get_dimension()

        if(ball_pos[0] >= paddle_pos[0] and ball_pos[0] < paddle_pos[0] + paddle_size[0]):
            if( (ball_pos[1]+1 <= paddle_pos[1] and ball_pos[1]+1 + ball_speed[1] > paddle_pos[1]) ):
                # collision happened!!

                import os
                os.system("afplay ./assets/paddle_ball_audio.wav &")

                ball.paddle_collision(ball_pos[0]-paddle_pos[0] - int(paddle_size[0]/2))


                #check the brick have to go down or not besd on time
                if(time.time() - self._level_time > 60):
                    for brick in self._bricks:
                        brick.move_down(self)


    def handle_ball_brick_collision(self,ball,brick):

        if(not(brick.is_visible())):
            return
        brick_pos,brick_size,brick_speed = brick.get_dimension()
        ball_pos,ball_size,ball_speed = ball.get_dimension()


        # horizontal collision
        if(ball_pos[1] == brick_pos[1]):

            # ball from left
            if(ball_pos[0]< brick_pos[0] and ball_pos[0]+ball_speed[0]+1 >=brick_pos[0]):
                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                os.system("afplay ./assets/paddle_ball_audio.wav &")


                if(self._fireball==1):
                    brick.thru_ball_collision(self,old_ball_speed)
                    game.explode_neighbour(brick_pos, brick_size, brick_speed)

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]-1
                    new_ball_pos[1] = ball_pos[1]


                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = ball_speed[0]
                    new_ball_speed[1] = -ball_speed[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)


                elif(ball.is_thru()):
                    brick.thru_ball_collision(self,old_ball_speed)
                else:
                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = -ball_speed[0]
                    new_ball_speed[1] = ball_speed[1]

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]-1
                    new_ball_pos[1] = ball_pos[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self, old_ball_speed)

            # ball from right
            if(ball_pos[0] > brick_pos[0]+brick_size[0] and ball_pos[0]+ball_speed[0] <= brick_pos[0]+brick_size[0]):

                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                os.system("afplay ./assets/paddle_ball_audio.wav &")

                if(self._fireball==1):
                    brick.thru_ball_collision(self,old_ball_speed)
                    game.explode_neighbour(brick_pos, brick_size, brick_speed)

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]+1
                    new_ball_pos[1] = ball_pos[1]

                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = -ball_speed[0]
                    new_ball_speed[1] = ball_speed[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)

                elif(ball.is_thru()):
                    brick.thru_ball_collision(self,old_ball_speed)
                else:
                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = -ball_speed[0]
                    new_ball_speed[1] = ball_speed[1]


                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]+1
                    new_ball_pos[1] = ball_pos[1]

                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self, old_ball_speed)

        # vertical collison
        if (ball_pos[0]+1  >= brick_pos[0] and ball_pos[0] <= brick_pos[0]+brick_size[0]):

            # ball from top
            if(ball_pos[1]+1 < brick_pos[1] and ball_pos[1]+1+ball_speed[1] >= brick_pos[1]):


                os.system("afplay ./assets/paddle_ball_audio.wav &")

                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                if(self._fireball==1):
                    brick.thru_ball_collision(self,old_ball_speed)
                    game.explode_neighbour(brick_pos, brick_size, brick_speed)

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]
                    new_ball_pos[1] = ball_pos[1]-1


                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = ball_speed[0]
                    new_ball_speed[1] = -ball_speed[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)

                elif(ball.is_thru()):
                    brick.thru_ball_collision(self,old_ball_speed)
                else:
                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = ball_speed[0]
                    new_ball_speed[1] = -ball_speed[1]

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]
                    new_ball_pos[1] = ball_pos[1]-1

                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self, old_ball_speed)

            # ball from bottom
            if(ball_pos[1] >= brick_pos[1]+1 and ball_pos[1]+ball_speed[1] < brick_pos[1]+1):


                os.system("afplay ./assets/paddle_ball_audio.wav &")

                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]


                if(self._fireball==1):
                    brick.thru_ball_collision(self,old_ball_speed)
                    game.explode_neighbour(brick_pos, brick_size, brick_speed)

                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]
                    new_ball_pos[1] = ball_pos[1]+1


                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = ball_speed[0]
                    new_ball_speed[1] = -ball_speed[1]
                    ball.brick_collision(new_ball_pos, new_ball_speed)

                elif(ball.is_thru()):
                    brick.thru_ball_collision(self,old_ball_speed)
                else:
                    new_ball_speed = np.array([0,0])
                    new_ball_speed[0] = ball_speed[0]
                    new_ball_speed[1] = -ball_speed[1]



                    new_ball_pos = np.array([0,0])
                    new_ball_pos[0] = ball_pos[0]
                    new_ball_pos[1] = ball_pos[1]+1

                    ball.brick_collision(new_ball_pos, new_ball_speed)
                    brick.ball_collision(self, old_ball_speed)

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
                if(0 < power_up_type <= 2 or power_up_type == 7):
                    power_up.activate(self._paddle)
                    if(power_up_type==7):
                        self._rem_time = 10
                elif(power_up_type <= 5):
                    for ball in self._balls:
                        power_up.activate(ball)
                elif(power_up_type==6):
                    power_up.activate(self)
                elif (power_up_type == 8):
                    power_up.activate(self)


    def handle_paddle_bomb_collision(self, bomb):

        paddle_pos,paddle_size,paddle_speed = self._paddle.get_dimension()
        bomb_pos,bomb_size,bomb_speed = bomb.get_dimension()

        if(bomb_pos[0] >= paddle_pos[0] and bomb_pos[0] < paddle_pos[0] + paddle_size[0]):
            if( (bomb_pos[1]+1 <= paddle_pos[1] and bomb_pos[1]+1 + bomb_speed[1] > paddle_pos[1]) ):
                # collision happened!!

                os.system("afplay explosion.mp3 &")
                self.new_life()


    def handle_bullet_brick_collision(self,bullet,brick):

        if(not(brick.is_visible())):
            return
        brick_pos,brick_size,brick_speed = brick.get_dimension()
        bullet_pos,bullet_size,bullet_speed = bullet.get_dimension()


        # vertical collison
        if (bullet_pos[0]+1  >= brick_pos[0] and bullet_pos[0] <= brick_pos[0]+brick_size[0]):

            # bullet from bottom
            if(bullet_pos[1] >= brick_pos[1]+1 and bullet_pos[1]+bullet_speed[1] < brick_pos[1]+1):

                bullet.brick_collision()
                brick.ball_collision(self, np.array([0,-1]))
                self._bullets.remove(bullet)

    def handle_ufo_ball_collision(self,ball):

        ufo_pos,ufo_size,ufo_speed = self._ufo.get_dimension()
        ball_pos,ball_size,ball_speed = ball.get_dimension()


        # horizontal collision
        if(ball_pos[1] == ufo_pos[1]):

            # ball from left
            if(ball_pos[0]< ufo_pos[0] and ball_pos[0]+ball_speed[0]+1 >=ufo_pos[0]):
                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                new_ball_speed = np.array([0,0])
                new_ball_speed[0] = -ball_speed[0]
                new_ball_speed[1] = ball_speed[1]

                new_ball_pos = np.array([0,0])
                new_ball_pos[0] = ball_pos[0]-1
                new_ball_pos[1] = ball_pos[1]
                ball.brick_collision(new_ball_pos, new_ball_speed)
                self._ufo.ball_collision()

                os.system("afplay boss_hit.mp3 &")
            # ball from right
            if(ball_pos[0] > ufo_pos[0]+ufo_size[0] and ball_pos[0]+ball_speed[0] <= ufo_pos[0]+ufo_size[0]):
                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                new_ball_speed = np.array([0,0])
                new_ball_speed[0] = -ball_speed[0]
                new_ball_speed[1] = ball_speed[1]


                new_ball_pos = np.array([0,0])
                new_ball_pos[0] = ball_pos[0]+1
                new_ball_pos[1] = ball_pos[1]

                ball.brick_collision(new_ball_pos, new_ball_speed)
                self._ufo.ball_collision()
                os.system("afplay boss_hit.mp3 &")
        # vertical collison
        if (ball_pos[0]+1  >= ufo_pos[0] and ball_pos[0] <= ufo_pos[0]+ufo_size[0]):

            # ball from top
            if(ball_pos[1]+1 < ufo_pos[1] and ball_pos[1]+1+ball_speed[1] >= ufo_pos[1]):
                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                new_ball_speed = np.array([0,0])
                new_ball_speed[0] = ball_speed[0]
                new_ball_speed[1] = -ball_speed[1]

                new_ball_pos = np.array([0,0])
                new_ball_pos[0] = ball_pos[0]
                new_ball_pos[1] = ball_pos[1]-1

                ball.brick_collision(new_ball_pos, new_ball_speed)
                self._ufo.ball_collision()
                os.system("afplay boss_hit.mp3 &")
            # ball from bottom
            if(ball_pos[1] >= ufo_pos[1]+1 and ball_pos[1]+ball_speed[1] < ufo_pos[1]+1):
                old_ball_speed = np.array([0,0])
                old_ball_speed[0] = ball_speed[0]
                old_ball_speed[1] = ball_speed[1]

                new_ball_speed = np.array([0,0])
                new_ball_speed[0] = ball_speed[0]
                new_ball_speed[1] = -ball_speed[1]



                new_ball_pos = np.array([0,0])
                new_ball_pos[0] = ball_pos[0]
                new_ball_pos[1] = ball_pos[1]+1

                ball.brick_collision(new_ball_pos, new_ball_speed)
                self._ufo.ball_collision()
                os.system("afplay boss_hit.mp3 &")

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


    def handle_paddle_shoot(self):
        if self._paddle._cannon == 1:
            if(self._counter%3 ==0):
                os.system('afplay fire.mp3 &')
                self._bullets.append(Bullet(list(self._paddle._pos),[1,1], [0,-1], [self._width, self._height]))
                self._bullets.append(Bullet(list(self._paddle._pos + np.array([self._paddle._size[0]-1, 0])),[1,1], [0,-1], [self._width, self._height]))


    def handle_ufo_bomb(self):
        if(self._level == 2 and self._ufo.get_health()):
            if(self._counter%40 ==0):
                ufo_pos,ufo_size,ufo_speed = self._ufo.get_dimension()
                self._bombs.append(Bomb([ufo_pos[0]+3, ufo_pos[1]],[1,1], [0,1], [self._width, self._height]))


    def handle_brick_respawn(self):
        if self._level==2 and self._ufo.get_health()==5 and self._ufo._weak_one:
            size = game_layout.size
            self._ufo._weak_one = 0
            for i in range(0, len(game_layout.weak_one)):
                self._bricks.append(Brick(game_layout.weak_one[i],[size,1],[0,0],[self._width,self._height],1,None))

        if self._level==2 and self._ufo.get_health()==2 and self._ufo._weak_two:
            size = game_layout.size
            self._ufo._weak_two = 0
            for i in range(0, len(game_layout.weak_two)):
                self._bricks.append(Brick(game_layout.weak_two[i],[size,1],[0,0],[self._width,self._height],1,None))
    ################ LIFE - SCORE ###################

    def increase_score(self, num):
        self._score = self._score + num


    def new_life(self):

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_activated()):
                if(0 < power_up.get_type() <= 2 or power_up.get_type() == 7):
                    power_up.deactivate(self._paddle)
                elif(power_up.get_type() <= 5):
                    for ball in self._balls:
                        power_up.deactivate(ball)
                elif(power_up.get_type() == 6):
                    power_up.deactivate(self)

        self._screen.blink_screen()

        self._lives = self._lives - 1
        if(self._lives == 0):
            self.over()
        self._paddle = Paddle([int(self._width/2)-6, self._height-1],[13,1],[0,0], [self._width,self._height])
        self._balls = []
        self._balls.append(Ball([int(self._width/2)-1, self._height-2],[1,1],[0,0], [self._width,self._height], True))
        self._rem_time = 0
    ################### BONUS ##############################

    def explode_neighbour(self, pos, size,speed):

        os.system("afplay ./assets/explosion.mp3 &")
        for brick in self._bricks:
            brick_pos,brick_size,brick_speed = brick.get_dimension()

            if(not brick.is_visible()):
                continue
            elif(pos[0] == brick_pos[0]):
                if(pos[1]+size[1] == brick_pos[1] or pos[1]-size[1] == brick_pos[1]):
                    brick.thru_ball_collision(self,speed)

            elif(pos[1] == brick_pos[1]):
                if(pos[0]+size[0] == brick_pos[0] or pos[0]-size[0] == brick_pos[0]):
                    brick.thru_ball_collision(self,speed)

            elif((pos[0]+size[0] == brick_pos[0] or pos[0]-size[0] == brick_pos[0]) and (pos[1]+size[1] == brick_pos[1] or pos[1]-size[1] == brick_pos[1])):

                brick.thru_ball_collision(self,speed)

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


        for bullet in self._bullets:
            self._screen.place_object(bullet)

        if(self._level==2 and self._ufo.get_health()):
            self._screen.place_object(self._ufo)

            for bomb in self._bombs:
                self._screen.place_object(bomb)

    def move_items(self):
        for ball in self._balls:
            if(ball.move()):
                self._balls.remove(ball)
            if(len(self._balls) == 0 ):
                self.new_life()

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_visible()):
                if(power_up.move()):
                    self._power_ups.remove(power_up)

        for bullet in self._bullets:
            if(bullet.move()):
                self._bullets.remove(bullet)


        if self._level == 2 and self._ufo.get_health():
            paddle_pos,paddle_size,paddle_speed = self._paddle.get_dimension()
            self._ufo.set_ufo_pos(np.array([paddle_pos[0], 4]))

            for bomb in self._bombs:
                if (bomb.move()):
                    self._bombs.remove(bomb)

    def handle_collisions(self):
        for ball in self._balls:
            self.handle_paddle_ball_collision(ball, self._paddle)

        for brick in self._bricks:
            for ball in self._balls:
                self.handle_ball_brick_collision(ball,brick)

            for bullet in self._bullets:
                self.handle_bullet_brick_collision(bullet,brick)

        for power_up in self._power_ups:
            if(power_up != None and power_up.is_visible()):
                self.handle_paddle_power_up_collision(self._paddle,power_up)

        if self._level == 2:
            if(self._ufo.get_health()):
                for ball in self._balls:
                    self.handle_ufo_ball_collision(ball)

            for bomb in self._bombs:
                self.handle_paddle_bomb_collision(bomb)

    def handle_power_up_timings(self):
        for power_up in self._power_ups:
            # if(power_up != None and power_up.is_visible()):
                # self._screen.place_object(power_up)

            if(power_up != None and power_up.is_activated()):
                if(time.time() - power_up.get_time()< 10 and power_up.get_type() == 7):
                    self._rem_time = 10 - int(time.time() - power_up.get_time())
                if(time.time() - power_up.get_time() > 10):
                    if(0< power_up.get_type() <=2 or power_up.get_type() == 7):
                        power_up.deactivate(self._paddle)
                        if(power_up.get_type() == 7):
                            self._rem_time=0
                    elif(power_up.get_type() <= 5):
                        for ball in self._balls:
                            power_up.deactivate(ball)
                    elif(power_up.get_type() == 6):
                        power_up.deactivate(self)
                    elif (power_up.get_type() == 8):
                        power_up.deactivate(self)

    def handle_rainbow_bricks(self):
        for rainbow in self._bricks:
            rainbow.change_color_strength()



    def handle_power_up_accelaration(self):
        for power_up in self._power_ups:
            if(power_up!=None):
                if(self._counter%2==0):
                    power_up.accelarate()

    def check_level_up(self):
        if (self._level < 2):
            for brick in self._bricks:
                if(brick.is_visible()):
                    return
            self.level_up()
        else:
            # for brick in self._bricks:
            #     if(brick.is_visible()):
            #         return
            if self._ufo.get_health():
                return
            self.level_up()




    def make_layout(self):

        size = 13
        left = size * 2 - 5
        top = 5
        self._level_time = time.time()
    #set the componets
        self._paddle = Paddle([int(self._width/2)-6, self._height-1],[13,1],[0,0], [self._width,self._height])
        self._balls = []
        self._balls.append(Ball([int(self._width/2)-1, self._height-2],[1,1],[0,0], [self._width,self._height], True))
        self._bricks = []
        self._power_ups = []
        self._bullets = []

        for i in range(0, len(self._power_frame[self._level])):
            p_type = self._power_frame[self._level][i]
            if(p_type==0):
                self._power_ups.append(None)
            elif(p_type==1):
                self._power_ups.append(Expand_paddle(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif(p_type==2):
                self._power_ups.append(Shrink_paddle(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif(p_type==3):
                self._power_ups.append(Paddle_grab(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif(p_type==4):
                self._power_ups.append(Thru_ball(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif(p_type==5):
                self._power_ups.append(Fast_Ball(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif(p_type==6 ):
                self._power_ups.append(Multiply_ball(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif (p_type==7):
                self._power_ups.append(Shoot_Paddle(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))
            elif (p_type == 8):
                self._power_ups.append(Fire_Ball(self._frame[self._level][i]+np.array([3,0]),[1,1],[0,0],[self._width,self._height]))



        for i in range(0, len(self._frame[self._level])):
            if(self._brick_strength_frame[self._level][i]< 0):
                self._bricks.append(ExplodingBrick(self._frame[self._level][i],[size,1],[0,0],[self._width,self._height],-self._brick_strength_frame[self._level][i],self._power_ups[i]))
            elif(self._brick_strength_frame[self._level][i]):
                if(self._brick_strength_frame[self._level][i]>3):
                    self._bricks.append(RainbowBrick(self._frame[self._level][i],[size,1],[0,0],[self._width,self._height],2,self._power_ups[i]))
                else:
                    self._bricks.append(Brick(self._frame[self._level][i],[size,1],[0,0],[self._width,self._height],self._brick_strength_frame[self._level][i],self._power_ups[i]))
            else:
                self._bricks.append(UnBrick(self._frame[self._level][i],[size,1],[0,0],[self._width,self._height],100,self._power_ups[i]))

        if(self._level ==2):
            self._ufo = UFO([int(self._width/2)-6, self._height-5],[13,1],[0,0], [self._width,self._height])
            self._bombs=[]
            os.system("afplay boss.wav &")


    def level_up(self):
        self._level = self._level+1
        if(self._level <= 2):
            self.make_layout()
        else:
            self._screen.game_won(game._score)
            sys.exit(0)


    def over(self):
            self._screen.game_lost(self._score)
            sys.exit()

    def increment_counter(self):
        self._counter = self._counter+1

    ############# RUN ################################
    def run(self):
        while 1:
            self.increment_counter()
            self._screen.clean()
            self.handle_keyboard_interrupt()
            self._screen.reset_screen()
            self.handle_collisions()
            self.check_level_up()
            self.move_items()
            self.place_items()
            self.handle_power_up_timings()
            self._screen.render_screen()
            self.handle_rainbow_bricks()
            self.handle_power_up_accelaration()
            self.handle_paddle_shoot()
            self.handle_ufo_bomb()
            self.handle_brick_respawn()


            if(self._rem_time > 0):
                print("LIVES: ",self._lives,"TIME: ",int(time.time()-self._time),"SCORE: ",self._score," SHOOT TIME LEFT: ",self._rem_time,"     ")
            else:
                print("LIVES: ",self._lives,"TIME: ",int(time.time()-self._time),"SCORE: ",self._score,"                                           ")
            if(self._level==2 and self._ufo.get_health()):
                health = ""
                for i in range(0,self._ufo.get_health()):
                    health = health+bg.red+" "+reset +bg.red+" "+reset
                print("HEALTH: ",health, "      ", end="")

game = Game()
game.run()


