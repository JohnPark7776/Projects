import pygame
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 30)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20 # Rotation Velocity
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        # Bird position
        self.x = x
        self.y = y
        # Bird animation
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5 # Negative Velocity means going up or left
        self.tick_count = 0 # Keep track of when last jump
        self.height = self.y # Keep track of original position

    def move(self):
        # time/FPS
        self.tick_count += 1

        # d = displacement
        # velocity * time + 1.5 * time^2
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2 # Makes jump "fluid"

        self.y = self.y + d

        #  Makes Bird not tilt downwards until end of Jump
        if d < 0 or self.y < self.height + 50:
            # Keeps bird tilt to not exceed 25 degrees
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    # win = windows
    def draw(self, win):
        self.img_count += 1

        # Checking which img to use based on img_count
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If Bird is falling, keeps image to BIRD_IMG[1]
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # Rotates an Img on their center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # Makes mask for collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    # Space between pipes
    GAP = 200
    # Bird doesn't move, items move to bird
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        # Checks if Bird passes pipe
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # Moves pipe to the left based on velocity and FPS
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # Mask is the actual pixels within a collision box
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Finds the collision(overlap) from bird mask and bottom pipe mask
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # If does not collide, returns None
        t_point = bird_mask.overlap(top_mask, top_offset)

        # if b_point or t_point is True
        # Collision is true
        if t_point or b_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Moves 2 images of the same Base to the left
        # The moment first image leaves screen, move image behind second image
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



def draw_window(win, bird, pipes, base, score):
    # blit draws the window
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


# Main() to run game
def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(650)]

    score = 0

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    # Creates FPS
    clock = pygame.time.Clock()

    while run:
        # FPS = 30
        clock.tick(30)

        # Gets user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            left = pygame.mouse.get_pressed()

            if left:
                bird.jump()
            
        bird.move()

        # Creates Pipe as it leaves screen
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            # Adds pipe to list after leaving screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            # Creates pipe after bird passes Pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        # Adds score and creates new Pipe
        if add_pipe:
            score += 1
            pipes.append(Pipe(650))

        # Removes pipe in list
        for r in rem:
            pipes.remove(r)

        # Moves Base to make Bird seem like moving
        base.move()

        # Creates the window for the game
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()

main()