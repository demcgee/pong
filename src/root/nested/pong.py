'''
Created on May 7, 2017

@author: daniellemcgee
'''

import pygame
from pygame.locals import *

class Pong(object):
    def __init__(self, screensize):
        
        self.screensize = screensize
        
        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)
        
        self.radius = 8
        
        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)
        
        self.color = (100,100,255)
        
        self.direction = [1,1]
        
        self.speedx = 4
        self.speedy = 6
        #CODE TASK: change speed/radius as game progresses to make it harder
        #CODE BONUS: adjust ratio of x and y speeds to make it harder
        
        self.hit_edge_left = False
        self.hit_edge_right = False
        
    def update(self, player_paddle, ai_paddle):
        
        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy
        
        self.rect.center = (self.centerx, self.centery)
        
        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1
        
        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True
            
        #CODE TASK: Change the direction of the pong, based on where
        #it hits the paddles (Hint: Check the center points of each)
        
        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1
    
    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)
        
class AIPaddle(object):
    def __init__(self, screensize):
        self.screen_size = screensize
        
        self.centerx = 5
        self.centery = int(screensize[1]*0.5)
        
        self.height = 100
        self.width = 10
        
        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)
        
        self.color = (255,100,100)
        
        #CODE TASK: Adjust size of AI paddle for difficulty
        
        self.speed = 3
    
    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed
        
        self.rect.center = (self.centerx, self.centery)
        
    def render (self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
        
class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screen_size = screensize
        
        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)
        
        self.height = 100
        self.width = 10
        
        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)
        
        self.color = (100,255,100)
        
        #CODE TASK: Adjust size of Player paddle for difficulty
        
        self.speed = 3
        self.direction = 0
    
    def update(self):
        self.centery += self.direction*self.speed
        
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom == 0:
            self.rect.bottom = self.screensize[1]-1
        
    def render (self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

def main():
    pygame.init()
    
    screensize = (640, 480)
    
    screen = pygame.display.set_mode(screensize)
    
    clock = pygame.time.Clock()
    
    pong = Pong(screensize)
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)
    
    running = True
    
    while running:
        #fps limiting/reporting phase
        clock.tick(64)
        
        #event handling phase
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0
                    
        
        #object updating phase
        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)
        
        #CODE TASK: make some text on the screen over everything else saying
        #you won/lost and then exit on keypress
        #CODE BONUS: allow restarting of the game (Hint: You can recreate the
        #Pong/Paddle objects the same way we made them initially 
        if pong.hit_edge_left:
            print ('You Won')
            running = False
        elif pong.hit_edge_right:
            print ('You Lost')
            running = False
        
        #rendering phase
        screen.fill((255,255,255))
        
        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)
        
        pygame.display.flip()
    
    pygame.quit()

main()