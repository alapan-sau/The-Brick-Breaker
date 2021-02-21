import numpy as np
import time
from color import *


class Item:
    def __init__(self,pos,size,speed,max_size):
        self._pos = np.array(pos)
        self._size = np.array(size)
        self._speed = np.array(speed)
        self._structure = np.array([[]])
        self._max_size = np.array(max_size)

    def get_dimension(self):
        return [self._pos,self._size, self._speed]

    def get_structure(self):
        return self._structure


class Paddle(Item):
    def __init__(self,pos,size,speed,max_size):
        super().__init__(pos,size,speed,max_size)
        self._structure = np.array([[fg.cyan+'I'+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0]=fg.cyan+'('+reset
        self._structure[0][self._size[0]-1]=fg.cyan+')'+reset

    def move(self,ch):
        if(ch=='d'):
            self._pos[0] = self._pos[0]+2
            if(self._pos[0]+self._size[0] >= self._max_size[0]-1):
                self._pos[0] = self._max_size[0] - self._size[0] - 1

        elif(ch=='a'):
            self._pos[0] = self._pos[0]-2
            if(self._pos[0] <= 0):
                self._pos[0] = 1

########## POWER UP functionalities ############

    def increase_size(self):
        self._size[0] = self._size[0] + 2
        self._structure = np.array([[fg.cyan+'I'+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0]=fg.cyan+'('+reset
        self._structure[0][self._size[0]-1]=fg.cyan+')'+reset

    def decrease_size(self):
        self._size[0] = self._size[0] - 2
        self._structure = np.array([[fg.cyan+'I'+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0]=fg.cyan+'('+reset
        self._structure[0][self._size[0]-1]=fg.cyan+')'+reset

class Ball(Item):
    def __init__(self,pos,size,speed,max_size,stick):
        super().__init__(pos,size,speed,max_size)
        self._structure = np.array([[fg.yellow+'o'+reset]])
        self._stick = stick
        self._paddle_grab = False
        self._thru_ball = False

    def start(self):
        if(self._stick is True):
            self._speed = np.array([0,-1])
            self._stick = False

    def move_with_paddle(self, ch):
        if(self._stick):
            #move left
            if(ch=='d'):
                self._pos[0] = self._pos[0]+2
                if(self._pos[0]+self._size[0] >= self._max_size[0]-1):
                    self._pos[0] = self._max_size[0] - self._size[0] - 2

            # move right
            elif(ch=='a'):
                self._pos[0] = self._pos[0]-2
                if(self._pos[0] <= 0):
                    self._pos[0] = self._pos[0]+2

    def move(self):
        # move the ball based on speed
        self._pos[0] = self._pos[0] + self._speed[0]
        self._pos[1] = self._pos[1] + self._speed[1]

        # WALL COLLISION CONDITIONS
        # left wall
        if(self._pos[0] <= 0 or (self._pos[0]>0 and self._pos[0]+ self._speed[0]<=0 ) ):
            # set the postion to avoid out of bound
            self._pos[0] = 1
            if(self._speed[0] < 0):
                self._speed[0] = -self._speed[0]

        # right wall
        if(self._pos[0] +1 >= self._max_size[0]-1   or (self._pos[0] < self._max_size[0]-1 and self._pos[0]+ self._speed[0] >= self._max_size[0]-1) ):
            # set the postion to avoid out of bound
            self._pos[0] = self._max_size[0]-2
            if(self._speed[0] > 0):
                self._speed[0] = -self._speed[0]

        # top wall
        if(self._pos[1] <= 1 or (self._pos[1]>1 and self._pos[1]+ self._speed[1] <=1 )):
            # set the postion to avoid out of bound
            self._pos[1] = 1
            if(self._speed[1]< 0):
                self._speed[1] = -self._speed[1]


        # bottom wall(VIRTUAL WALL)
        if(self._pos[1] >= self._max_size[1]-1):
            # set the postion to avoid out of bound
            self._pos[1] = self._max_size[1]-1
            if(self._speed[1] != 0):
                self._speed[1] = 0
                self._speed[0] = 0
                return True

        return False

    def paddle_collision(self, change_in_speed):
        self._pos[1] = self._max_size[1]-2
        if(self._paddle_grab==True):
            self._stick = True

        if(self._stick):
            self._speed = np.array([0,0])
        else:
            self._speed[1] = -self._speed[1]
            self._speed[0] = self._speed[0] + change_in_speed

    def brick_collision(self, new_pos, new_speed):
        self._pos = new_pos
        self._speed = new_speed

    ###### POWER UP functionalities ############


    def paddle_grab(self):
        self._paddle_grab = True

    def revoke_paddle_grab(self):
        self._paddle_grab = False

    def thru_ball(self):
        self._thru_ball = True

    def revoke_thru_ball(self):
        self._thru_ball = False

    def is_thru(self):
        return self._thru_ball

    def increase_speed(self):
        if(not self._stick):
            self._speed[0] = self._speed[0] * 2

    def decrease_speed(self):
        if(not self._stick):
            if(self._speed[0]>=2 or self._speed[0]<=-2):
                self._speed[0] = self._speed[0]/2

class Brick(Item):
    def __init__(self,pos,size,speed,max_size,strength,power_up):
        super().__init__(pos,size,speed,max_size)
        self._strength = strength

        self._color = ''
        if(self._strength == 3):
            self._color = fg.red
        elif(self._strength == 2):
            self._color = fg.yellow
        elif(self._strength == 1):
            self._color = fg.green


        self._structure = np.array([[ (self._color+'I'+reset )for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0] = self._color+'|'+reset
        self._structure[0][self._size[0]-1] = self._color+'|'+reset

        self._visible = 1
        self._power_up = power_up


    def ball_collision(self,game):
        self._strength = self._strength -1
        game.increase_score(1)

        if(self._strength == 3):
            self._color = fg.red
        elif(self._strength == 2):
            self._color = fg.yellow
        elif(self._strength == 1):
            self._color = fg.green

        self._structure = np.array([[ (self._color+'I'+reset )for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0] = self._color+'|'+reset
        self._structure[0][self._size[0]-1] = self._color+'|'+reset

        if(self._strength==0):
            self._visible = 0
            if(self._power_up != None):
                self._power_up.make_visible()

    def is_visible(self):
        return self._visible


    ###### POWER UP functionalities ############
    def thru_ball_collision(self,game):
        game.increase_score(self._strength)
        self._strength = 0
        if(self._strength==0):
            self._visible = 0
            if(self._power_up != None):
                self._power_up.make_visible()



class UnBrick(Brick):
    def __init__(self,pos,size,speed,max_size,strength,power_up):
        super().__init__(pos,size,speed,max_size,strength,power_up)
        self._strength = strength
        self._structure = np.array([['U' for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0] = '|'
        self._structure[0][self._size[0]-1] = '|'

        self._visible = 1
        self._power_up = power_up


    ########### Both are overloaded #############

    def ball_collision(self,game):
        return

    ## POWER UP functionalities ##
    def thru_ball_collision(self,game):
        game.increase_score(5)
        self._visible = 0
        if(self._power_up != None):
            self._power_up.make_visible()


class ExplodingBrick(Brick):
    def __init__(self,pos,size,speed,max_size,strength,power_up):
        super().__init__(pos,size,speed,max_size,strength,power_up)

        self._strength = strength

        if(self._strength == 3):
            self._color = fg.red
        elif(self._strength == 2):
            self._color = fg.yellow
        elif(self._strength == 1):
            self._color = fg.green

        self._structure = np.array([[self._color+'E'+reset for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0] = self._color+'|'+reset
        self._structure[0][self._size[0]-1] = self._color+'|'+reset

        self._visible = 1
        self._power_up = power_up



    ########### Both are overloaded #############

    def ball_collision(self,game):
        self._strength = self._strength -1
        game.increase_score(1)

        if(self._strength == 3):
            self._color = fg.red
        elif(self._strength == 2):
            self._color = fg.yellow
        elif(self._strength == 1):
            self._color = fg.green

        self._structure = np.array([[self._color+'E' for j in range(self._size[0])] for i in range(self._size[1])], dtype='object')
        self._structure[0][0] = self._color+'|'+reset
        self._structure[0][self._size[0]-1] = self._color+'|'+reset

        if(self._strength==0):
            self._visible = 0
            if(self._power_up != None):
                self._power_up.make_visible()
            game.explode_neighbour(self._pos, self._size)

    ###### POWER UP functionalities ############
    def thru_ball_collision(self,game):
        print(1)
        game.increase_score(self._strength)
        self._strength = 0
        if(self._strength==0):
            self._visible = 0
            if(self._power_up != None):
                self._power_up.make_visible()
            game.explode_neighbour(self._pos, self._size)


class Power_up(Item):
    def __init__(self,pos, size, speed, max_size, type):
        super().__init__(pos,size,speed,max_size)
        self._type = type
        self._visible = 0
        self._activated = False
        self._time = 0


    def make_visible(self):
        self._visible = 1
    def paddle_collision(self):
        self._visible = 0
    def is_visible(self):
        return self._visible
    def move(self):
        self._pos = self._pos  + self._speed

        if(self._pos[1]+self._size[1] > self._max_size[1]):
            self._pos = np.array([0,0])
            self._visible = 0

    def get_type(self):
        return self._type

    def is_activated(self):
        return self._activated


    def activate(self, paddle):
        self._visible = 0
        self._time = time.time()

    def get_time(self):
        return self._time


class Expand_paddle(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,1)
        self._structure = np.array([['+']])

    def activate(self, paddle):
        self._visible = 0
        paddle.increase_size()
        self._activated = 1
        self._time = time.time()

    def deactivate(self, paddle):
        paddle.decrease_size()
        self._activated = 0


class Shrink_paddle(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,2)
        self._structure = np.array([['-']])


    def activate(self, paddle):
        self._visible = 0
        paddle.decrease_size()
        self._activated = 1
        self._time = time.time()

    def deactivate(self, paddle):
        paddle.increase_size()
        self._activated = 0



class Paddle_grab(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,3)
        self._structure = np.array([['^']])

    def activate(self, ball):
        self._visible = 0
        ball.paddle_grab()
        self._activated = 1
        self._time = time.time()

    def deactivate(self, ball):
        ball.revoke_paddle_grab()
        self._activated = 0

class Thru_ball(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,4)
        self._structure = np.array([['!']])

    def activate(self, ball):
        self._visible = 0
        ball.thru_ball()
        self._activated = 1
        self._time = time.time()

    def deactivate(self, ball):
        ball.revoke_thru_ball()
        self._activated = 0

class Multiply_ball(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,5)
        self._structure = np.array([['*']])
        self._num_ball = 0

    def activate(self, game):
        self._visible = 0
        self._num_ball = game.get_num_ball()
        game.multiply_ball()
        self._activated = 1
        self._time = time.time()


    def deactivate(self,game):
        game.divide_ball(self._num_ball)
        self._activated = 0

class Fast_Ball(Power_up):
    def __init__(self,pos, size, speed, max_size):
        super().__init__(pos,size,speed,max_size,5)
        self._structure = np.array([['F']])

    def activate(self, ball):
        self._visible = 0
        ball.increase_speed()
        self._activated = 1
        self._time = time.time()


    def deactivate(self,ball):
        ball.decrease_speed()
        self._activated = 0