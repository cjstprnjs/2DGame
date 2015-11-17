import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

hero = None
font = None
chk = False

BlockList = []
Block_generate_frame = 0

class Hero:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    LEFT_ATTACK, RIGHT_ATTACK, DEATH_L, DEATH_R = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 325, 85
        self.frame = random.randint(0, 3)
        self.image_LEFT = load_image('hulk_L.png')
        self.image_RIGHT = load_image('hulk_R.png')
        self.image_DEATH = load_image('death_L.png')
        self.image_DEATH = load_image('death_R.png')
        self.state = self.LEFT_ATTACK
        self.total_frames = 0

    def handle_event(self, event):
        if(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.state = self.LEFT_ATTACK
            self.x = 325
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.state = self.RIGHT_ATTACK
            self.x = 475

    def update(self,frame_time):
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME
        self.frame = int(self.total_frames) % 4


    def draw(self):
        #공격모션
        if self.state == self.LEFT_ATTACK :
            self.image_LEFT.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)
        if self.state == self.RIGHT_ATTACK:
            self.image_RIGHT.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y)
        # 죽었을때
        if self.state == self.DEATH_L:
            self.image_DEATH_L.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y - 20)
        if self.state == self.DEATH_R:
            self.image_DEATH_R.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y - 20)

class Background:
    def __init__(self):
        self.x, self.y = 400,300
        self.image = load_image('Background.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class StaminaBar:
    def __init__(self):
        self.x, self.y = 400 , 600
        self.image = load_image()

class Block:

    MOVE_PER_TIME = 200

    BASIC_BLOCK, LEFT_BLOCK, RIGHT_BLOCK = 0, 1, 2

    def __init__(self):
        self.x, self.y = 400, 700
        self.image_basic = load_image('block_pice.png')
        self.image_LEFT = load_image('block_L.png')
        self.image_RIGHT = load_image('block_R.png')
        self.block_num = random.randint(0,2)

    def draw(self):
        #블럭 3종류
        if (self.block_num == 0):
            self.image_basic.draw(self.x, self.y)
        if (self.block_num == 1):
            self.image_LEFT.draw(self.x,self.y)
        if (self.block_num == 2):
            self.image_RIGHT.draw(self.x,self.y)

    def update(self,frame_time, post_block_y):
        self.y -= frame_time * self.MOVE_PER_TIME
        if(self.y < post_block_y + 50):
            self.y = post_block_y + 50
    #블럭 지우기





    def block_get_Y(self):
        return self.y




def enter():
    global hero, background

    background = Background()
    hero = Hero()

def exit():
    global hero, blcok, background

    del(hero)
    del(background)

def pause():
    pass

def resume():
    pass

def handle_events():
    global chk, hero
    chk = False
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                hero.handle_event(event)
            elif event.key == SDLK_LEFT:
                hero.handle_event(event)

def update(frame_time):
    global BlockList, Block_generate_frame
    #블록들
    Block_generate_frame += frame_time
    post_block_y = 0
    block_index = 0
    for block in BlockList:
        block_index += 1
        if(block_index == 1):
            block.update(frame_time, 20)
        else:
            block.update(frame_time, post_block_y)

        post_block_y = block.block_get_Y()


    hero.update(frame_time)
    if len(BlockList) < 12 and Block_generate_frame >= 0.25:
        BlockList.append(Block())
        Block_generate_frame = 0

        print(frame_time)

    delay(0.06)

def draw():
    global BlockList

    clear_canvas()

    background.draw()
    hero.draw()
    for block in BlockList:
        block.draw()

    update_canvas()



