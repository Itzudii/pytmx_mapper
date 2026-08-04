import pygame
from enum import Enum
from utils.dependency import get_frames
from settings import TILESIZE
from player.effect import Appear,Disappear
from player.dust_partical import DustF,DustH,DustJ,DustV
import random
from animation import Animation

class State(Enum):
    IDLE = "idle"
    RUN = "run"
    WALLJUMP = "wallJUMP"
    JUMP = "jump"
    HURT = "hurt"
    FALL = "fall"
    DJUMP = "djump"


class Player(pygame.sprite.Sprite):
    name = 'player'
    frames = None
    
    @classmethod
    def load_assets(cls):
        if cls.frames == None:

            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Main Characters\Ninja Frog\Idle (32x32).png',11)
            cls.frames['run'] = get_frames(r'assets\Main Characters\Ninja Frog\Run (32x32).png',12)
            cls.frames['wallJUMP'] = get_frames(r'assets\Main Characters\Ninja Frog\Wall Jump (32x32).png',5)
            cls.frames['jump'] = get_frames(r'assets\Main Characters\Ninja Frog\Jump (32x32).png',1)
            cls.frames['hurt'] = get_frames(r'assets\Main Characters\Ninja Frog\Hit (32x32).png',7)
            cls.frames['fall'] = get_frames(r'assets\Main Characters\Ninja Frog\Fall (32x32).png',1)
            cls.frames['djump'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6)
            cls.frames['appear'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6)
            cls.frames['desappear'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6)

    def __init__(self,bottomleft):
        super().__init__()
        Player.load_assets()

        self.direction = 1 # (-1,left)  (1,right)
        self.animation = Animation(Player.frames)

        self.rect:pygame.Rect = self.animation.image.get_rect()
        self.offset_x = TILESIZE//5
        self.rect.topleft = bottomleft
        self.rect.w -= self.offset_x*2
        self.speed = TILESIZE//6
        self.speed_dt = 0
        self.move = False

        self.iscollide_left = False
        self.iscollide_right = False

        # gravity and jump
        self.vel_y = 0
        self.gravity = .3
        self.jump_intensity = 10

        self.isjumped = False
        self.isfall = False
        self.isdoublej = False
        self.doublejumpuse = False
        
        self.is_hit = False
        self.isvisible = True
        self.hitground = False

        self.effects = pygame.sprite.Group()
        self.particals = pygame.sprite.Group()

    def draw(self,screen,camera):
        if self.isvisible and len(self.effects) == 0:
            screen.blit(self.animation.image,camera.apply_pos((self.rect.x-self.offset_x,self.rect.y)))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

        for partical in self.particals:
            partical.draw(screen,camera)

        for effect in self.effects:
            effect.draw(screen)


    def update_state(self):
        if self.is_hit:
            self.animation.set_state(State.HURT.value)
            if self.animation.isfinished:
                self.is_hit = False
        elif self.isdoublej:
            self.animation.set_state(State.DJUMP.value)
            if self.animation.isfinished:
                self.isdoublej = False
        elif self.isjumped:
            self.animation.set_state(State.JUMP.value)
        elif self.isfall:
            if self.iscollide_left or self.iscollide_right:
                self.animation.set_state(State.WALLJUMP.value)
                self.vel_y = 1
                self.doublejumpuse = False
            else:
                self.animation.set_state(State.FALL.value)
        elif not self.move:
            self.animation.set_state(State.IDLE.value)
        else:
            self.animation.set_state(State.RUN.value)

    def movement_y(self):
        self.vel_y += self.gravity
        self.rect.y += round(self.vel_y)

    def collision_check_y_axis(self,level):
        foot = self.rect.move(0, 1)

        def collision_check_y_axis_rects(rects):

            grounded = any(foot.colliderect(rect) for rect in rects)
            for rect in rects:
                if self.rect.colliderect(rect):
                    if self.isjumped:
                        self.rect.top = rect.bottom
                        self.isdoublej = False
                    else:
                        self.rect.bottom = rect.top
                        if not self.hitground:
                            self.hitground = True
                            for _ in range(5):
                                self.particals.add(DustF(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                    self.vel_y = 0
            return grounded

        def collision_check_y_axis_objs(objs):
            grounded = any(foot.colliderect(obj.rect) for obj in objs)

            for obj in objs:
                if self.rect.colliderect(obj.rect):
                    if self.isjumped:
                        self.rect.top = obj.rect.bottom
                        self.isdoublej = False
                    else:
                        self.rect.bottom = obj.rect.top
                        if not self.hitground:
                            self.hitground = True
                            for _ in range(5):
                                self.particals.add(DustF(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                    self.vel_y = 0
            return grounded

        self.isjumped = self.vel_y < 0
        grounded = any((
            collision_check_y_axis_rects(level.landblocks),
            # collision_check_y_axis_objs(level.boxs)
        ))

        self.isfall = not grounded
        if self.isfall:
            self.hitground = False

    def movement_x(self):
        self.rect.x += self.speed_dt

    def summon_partical(self):
        if len(self.particals) < 5:
            if self.move and not self.isfall:
                self.particals.add(DustH(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
            if self.iscollide_left:
                self.particals.add(DustV(self.rect.x,self.rect.bottom,random.randint(20,30)))
            elif self.iscollide_right:
                self.particals.add(DustV(self.rect.right,self.rect.bottom,random.randint(20,30)))
           
                


    def collision_check_x_axis(self,level):
        self.iscollide_right = False
        self.iscollide_left = False

        def tile_collision(block):
            if self.rect.colliderect(block):
                if self.speed_dt < 0:
                    self.rect.left = block.right
                    self.iscollide_left = True
                elif self.speed_dt > 0:
                    self.rect.right = block.left
                    self.iscollide_right = True

        # for block in level.landblocks:
        #     tile_collision(block)

        # for box in level.boxs:
        #     tile_collision(box.rect)

        for rect in level.landblocks:
            tile_collision(rect)
                

            
    def update(self,level):
        self.animation.direction = self.direction
        self.animation.update()

        self.movement_y() #y-axis movement
        self.collision_check_y_axis(level) #y-axis collision

        self.movement_x() #x-axis movement
        self.collision_check_x_axis(level) #y-axis collision

        self.update_state() 
        self.summon_partical()

        self.effects.update()
        self.particals.update()

    def event_handle(self,event):
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump()
                        self.particals.add(DustJ(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                    if event.key == pygame.K_q:
                        self.is_hit = True
                    if event.key == pygame.K_a:
                        if self.isvisible:
                            self.desappearing()
                            print('disapper')
                        else:
                            self.appearing()
                            print('apper')

                        
    def appearing(self):
        self.effects.add(Appear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = True

    def desappearing(self):
        self.effects.add(Disappear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = False

                    
    def key_handle(self,key):
        if key[pygame.K_LEFT]:
            self.left()
        elif key[pygame.K_RIGHT]:
            self.right()
        else:
            self.ideal()

    def jump(self):
        if not self.isjumped and not self.isfall:
            self.vel_y = -self.jump_intensity
            self.isjumped = True
            self.doublejumpuse = False
        elif not self.isdoublej and not self.doublejumpuse:
            self.vel_y = -self.jump_intensity
            self.isdoublej = True
            self.doublejumpuse = True

    def left(self):
        self.speed_dt = -self.speed
        self.direction = -1
        self.move = True

    def right(self):
        self.speed_dt = self.speed
        self.direction = 1
        self.move = True

    def ideal(self):
        self.move = False
        self.speed_dt = 0
