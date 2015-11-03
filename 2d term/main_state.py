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

    def __init__(self):
        self.x, self.y = 300, 135
        self.frame = random.randint(0, 3)
        self.image = load_image('hulk.png')
        self.total_frames = 0


    def update(self):
        self.total_frames += Hero.FRAMES_PER_ACTION * Hero.ACTION_PER_TIME
        self.frame = int(self.total_frames) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 200, 0, 200, 200, self.x, self.y)



class Background:
    def __init__(self):
        self.x, self.y = 400,300
        self.image = load_image('Background.png')

    def draw(self):
        self.image.draw(self.x, self.y)

class Block:

    def __init__(self):
        self.x, self.y = 400, 600
        self.image = load_image('block.png')

    def draw(self):
        self.image.draw(self.x, self.y)
        if(self.y > 0):
            self.y -= 10

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
    global chk
    chk = False
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                hero.x = 500
            elif event.key == SDLK_LEFT:
                hero.x = 300

def update():
    global BlockList, Block_generate_frame

    Block_generate_frame += 1

    hero.update()
    if len(BlockList) < 100 and Block_generate_frame >= 1:
        BlockList.append(Block())
        Block_generate_frame = 0
    delay(0.06)

def draw():
    global BlockList

    clear_canvas()

    background.draw()
    hero.draw()
    for block in BlockList:
        block.draw()

    update_canvas()



