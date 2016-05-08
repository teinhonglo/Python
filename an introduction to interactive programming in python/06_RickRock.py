# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

rock_group = set([])
missile_group = set([])
explosion_group = set([])

EXPLOSION_DIM = 64

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def increament_angle(self):
        self.angle_vel += ( math.pi / 45 )
    def decreament_angle(self):
        self.angle_vel -= ( math.pi / 45 )
            
    def turn_on(self, on):
        if on == True:
            self.thrust = True
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.pause()
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        missile_sound.play()
    
    def get_radius(self):
        return self.image_size[0]
    
    def get_position(self):
        return self.pos
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], 
                                           self.image_center[1]), self.image_size,
                                           self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos,
                              self.image_size, self.angle)
    
    def update(self):
        # Angle update
        self.angle += self.angle_vel
        
        # Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Velocity update-acceleration in direction of forward vector
        forward = angle_to_vector(self.angle)
        
        # Thurst update
        if self.thrust :
            self.vel[0] += forward[0] * .1
            self.vel[1] += forward[1] * .1
        
        # Friction update
        c = .01
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
    
# Sprite class
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
    
    def get_radius(self):
        return self.image_size[0]
    
    def get_position(self):
        return self.pos
    
    def collide(self, other_object):
        if math.sqrt((self.pos[0] - other_object.get_position()[0]) ** 2 + 
                     (self.pos[1] - other_object.get_position()[1]) ** 2 ) <= self.image_size[0] / 2 + other_object.get_radius()  / 2:
            
            return True
        else:
            return False
    
    def draw(self, canvas):
        if self.animated:
            explosion_sound.play()
            global time
            current_explosion_index = (time % EXPLOSION_DIM) // 1
            current_explosion_center = [self.image_center[0] + self.image_size[0] * current_explosion_index,
                                        self.image_center[1]]
            canvas.draw_image(self.image, current_explosion_center, 
                              self.image_size, self.pos, self.image_size, self.angle)
            time += 0.2
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # increase age
        self.age += .3
        
        if self.age >= self.lifespan:
            return False
        else:
            return True

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        
def draw(canvas):
    global time, lives, score, rock_group, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Live : " + str(lives), [WIDTH / 13, HEIGHT / 10], 40, "White")
    canvas.draw_text("Score : " + str(score), [WIDTH * 10 / 13, HEIGHT / 10], 40, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    # a_missile.update()
    
    # draw splash screen if not started
    if started:
        soundtrack.play()
        # check collision
        if group_collide(rock_group, my_ship) :
            lives -= 1
            
        group_group_collide(missile_group, rock_group)

    else:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    if lives <= 0:
        soundtrack.rewind()
        started = False
        rock_group = set([])
        lives = 3
        score = 0

def key_down_handler(key):
    # key down 'left' and 'right' to change the angle
    if key == simplegui.KEY_MAP['left']:
        my_ship.decreament_angle()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increament_angle()
    
    # key down 'up' to acceleration
    if key == simplegui.KEY_MAP['up']:
        my_ship.turn_on(True)
    # key down 'space' to shoot missile
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def key_up_handler(key):
    # stop change the angle
    if key == simplegui.KEY_MAP['left']:
        my_ship.increament_angle()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decreament_angle()
        
    # stop acceleration    
    if key == simplegui.KEY_MAP['up']:
        my_ship.turn_on(False)
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, score
    rock_pos = [random.randrange(10, WIDTH - 10),
                random.randrange(10, HEIGHT - 10)]
    
    while dist(rock_pos ,my_ship.get_position()) < 90:
        rock_pos = [random.randrange(10, WIDTH - 10),
                    random.randrange(10, HEIGHT - 10)]
    
    rock_vel = [(random.random() * .8 - .3) * score / 5,
                (random.random() * .8 - .3) * score / 5]
    rock_ang = 0
    rock_ang_vel = random.random() * .2 - .1
    
    if started:
        if len(rock_group) < 12:
            rock_group.add(Sprite(rock_pos, rock_vel, rock_ang, rock_ang_vel, asteroid_image,
                                  asteroid_info))

# process rock and missle
def process_sprite_group(sprite, canvas):
    for item in set(sprite):
        if not item.update():
            sprite.remove(item)
        else:
            item.draw(canvas)
            
# collide with group and one object(rock, other)        
def group_collide(group, other_object):
    global explosion_group
    isCollide = False
    for each_item in set(group):
        if each_item.collide(other_object):
            group.remove(each_item)
            explosion_group.add(Sprite(each_item.get_position(), [0,0], 0, 0, explosion_image, explosion_info))
            isCollide = True
            
    return isCollide

# collide with group and group(missile and rock)        
def group_group_collide(first_group, second_group):
    global score
    for each_item in set(first_group):
        if group_collide(second_group, each_item):
            score += 1
            first_group.remove(each_item)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
