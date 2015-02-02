http://www.codeskulptor.org/#user16_uHirnUSGPQzI3mF_0.py

# Mini-project #8 - RiceRocks
# Based on Asteroids template for Introduction to Python

import simplegui
import math
import random

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
level = 1
rockcount = 10  
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# Art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# Debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_brown.png")

# Nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# Splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# Asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")

# Animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# Sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
ship_explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/ship_explosion.mp3")
ship_explosion_sound.set_volume(1)

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = 0
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        self.forward = angle_to_vector(self.angle)
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        if self.thrust:
            self.vel[0] += self.forward[0] * .1
            self.vel[1] += self.forward[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            self.image_center = [135, 45]
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            self.image_center = [45, 45]
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missile_group
        missile_pos = [self.pos[0] + self.radius * self.forward[0], self.pos[1] + self.radius * self.forward[1]]
        missile_vel = [self.vel[0] + 6 * self.forward[0], self.vel[1] + 6 * self.forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            self.image_center[0] = self.image_center[0] + self.age * self.image_size[0]
            self.image_center = [self.image_center[0], self.image_center[1]]
            if self.image == ship_explosion_image:
                image_destsize = [self.image_size[0] * 4, self.image_size[1] * 4]
            else:
                image_destsize = self.image_size
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, image_destsize, self.angle)
            explosion_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
    
    def collide(self, obj):
        if dist(self.pos, obj.pos) < (self.radius + obj.radius):
            return True
        else:
            return False
  
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
def click(pos):
    global started, my_ship, rock_group, missile_group, explosion_group, lives, score, level, rockcount
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set()
        missile_group = set()
        explosion_group = set()
        lives = 3
        score = 0
        level = 1
        rockcount = 10
        soundtrack.rewind()
        soundtrack.play()

def draw(canvas):
    global time, started, lives, score, level
    
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    canvas.draw_text("LIVES", [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("SCORE", [680, 50], 22, "White", "sans-serif")
    canvas.draw_text("LEVEL", [50, 550], 22, "White", "sans-serif")
    canvas.draw_text(str(lives), [50, 80], 25, "White", "monospace")
    canvas.draw_text(str(score), [680, 80], 25, "White", "monospace")
    canvas.draw_text(str(level-1), [50, 580], 25, "White", "monospace")
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if started:
        my_ship.draw(canvas)
        my_ship.update()
    
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        
        num = group_collide(rock_group, my_ship)
        if num > 0:
            lives -= 1
        numb = group_group_collide(rock_group, missile_group)
        if numb > 0:
            score += numb
    
    if lives <= 0:
        started = False

def rock_spawner():
    global rock_group, my_ship, level, time, started, rockcount, score
    if (score > rockcount) and started:
        level += 1
        rockcount += 10
    ls = level * 0.5
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * ls - (ls / 2), random.random() * ls - (ls / 2)]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if dist(a_rock.pos, my_ship.pos) > ((a_rock.radius + my_ship.radius) * 2) and len(rock_group) < 13 and started:
        rock_group.add(a_rock)
        
def process_sprite_group(a_set, canvas):
    aa_set = set(a_set)
    for i in aa_set:
        i.draw(canvas)
        if i.update():
            a_set.remove(i)
        
def group_collide(a_set, obj):
    global explosion_group
    collisioncount = 0
    aa_set = set(a_set)
    for i in aa_set:
        if i.collide(obj):
            a_set.remove(i)
            collisioncount += 1
            if obj == my_ship:
                a_explosion = Sprite(my_ship.pos, [0, 0], 0, 0, ship_explosion_image, explosion_info)
                explosion_group.add(a_explosion)
                ship_explosion_sound.play()
            else:
                a_explosion = Sprite(i.pos, [0, 0], 0, 0, explosion_image, explosion_info)
                explosion_group.add(a_explosion)
    return collisioncount

def group_group_collide(b_set, a_set):
    global explosion_group
    collisioncount = 0
    aa_set = set(a_set)
    for i in aa_set:
        num = group_collide(b_set, i)
        if num > 0:
            a_set.remove(i)
            collisioncount += 1
    return collisioncount
            
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

timer.start()
frame.start()