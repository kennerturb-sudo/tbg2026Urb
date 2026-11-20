
@'
import pygame
import random
import math
import json
import os

pygame.init()

# NEON SURVIVOR - FULL GAME

W, H = 1100, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("NEON SURVIVOR")
clock = pygame.time.Clock()

BG = (7, 9, 23)
WHITE = (245, 250, 255)
CYAN = (0, 235, 255)
PURPLE = (175, 65, 255)
RED = (255, 55, 85)
GREEN = (60, 255, 140)
YELLOW = (255, 220, 60)

title_font = pygame.font.SysFont("arial", 64, bold=True)
big_font = pygame.font.SysFont("arial", 44, bold=True)
font = pygame.font.SysFont("arial", 25, bold=True)
small = pygame.font.SysFont("arial", 17)

SAVE = "neon_save.json"

def load_best():
    try:
        with open(SAVE) as f:
            return json.load(f).get("best", 0)
    except:
        return 0

best = load_best()

state = "menu"
player = pygame.Vector2(W/2, H/2)
health = 100
score = 0
wave = 1
enemies = []
bullets = []
particles = []
pickups = []

shoot_time = 0
spawn_time = 0
dash_time = 0
dash_cooldown = 0
hurt_time = 0
boss_spawned = False

stars = [
    (random.randrange(W), random.randrange(H))
    for _ in range(120)
]

class Particle:
    def __init__(self, pos, color):
        self.pos = pygame.Vector2(pos)
        angle = random.random() * math.tau
        speed = random.randint(50, 250)
        self.vel = pygame.Vector2(
            math.cos(angle)*speed,
            math.sin(angle)*speed
        )
        self.life = random.uniform(.25, .65)
        self.maximum = self.life
        self.color = color
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt

    def draw(self):
        if self.life > 0:
            r = max(1, int(self.size*self.life/self.maximum))
            pygame.draw.circle(screen, self.color,
                (int(self.pos.x), int(self.pos.y)), r)

def explosion(pos, color, amount=15):
    for _ in range(amount):
        particles.append(Particle(pos, color))

class Enemy:
    def __init__(self, kind=None):
        side = random.randrange(4)
        if side == 0:
            pos = (random.randrange(W), -30)
        elif side == 1:
            pos = (random.randrange(W), H+30)
        elif side == 2:
            pos = (-30, random.randrange(H))
        else:
            pos = (W+30, random.randrange(H))

        self.pos = pygame.Vector2(pos)
        self.boss = kind == "boss"

        if self.boss:
            self.radius = 38
            self.hp = 35 + wave*5
            self.speed = 65 + wave*2
            self.color = PURPLE
            self.maximum = self.hp
        else:
            roll = random.random()
            if roll < .6:
                self.radius = 15
                self.hp = 2
                self.speed = 105 + wave*5
                self.color = RED
            elif roll < .85:
                self.radius = 10
                self.hp = 1
                self.speed = 180 + wave*5
                self.color = YELLOW
            else:
                self.radius = 23
                self.hp = 6
                self.speed = 65 + wave*3
                self.color = PURPLE
            self.maximum = self.hp

    def update(self, dt):
        direction = player-self.pos
        if direction.length():
            direction = direction.normalize()
        self.pos += direction*self.speed*dt

    def draw(self):
        p = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, self.color, p, self.radius+6, 2)
        pygame.draw.circle(screen, self.color, p, self.radius)
        pygame.draw.circle(screen, WHITE, p, max(3, self.radius//4))

        if self.boss:
            width = 70
            pygame.draw.rect(screen, RED,
                (p[0]-width//2, p[1]-self.radius-15, width, 6))
            pygame.draw.rect(screen, GREEN,
                (p[0]-width//2, p[1]-self.radius-15,
                 width*self.hp/self.maximum, 6))

class Bullet:
    def __init__(self, pos, direction):
        self.pos = pygame.Vector2(pos)
        self.vel = direction*700
        self.life = 1.4

    def update(self, dt):
        self.pos += self.vel*dt
        self.life -= dt

    def draw(self):
        p = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, CYAN, p, 8)
        pygame.draw.circle(screen, WHITE, p, 3)

class Pickup:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.life = 12

    def update(self, dt):
        self.life -= dt

    def draw(self):
        p = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(screen, GREEN, p, 13, 3)
        pygame.draw.line(screen, GREEN,
            (p[0]-7,p[1]), (p[0]+7,p[1]), 3)
        pygame.draw.line(screen, GREEN,
            (p[0],p[1]-7), (p[0],p[1]+7), 3)

def reset():
    global player, health, score, wave
    global enemies, bullets, particles, pickups
    global shoot_time, spawn_time
    global dash_time, dash_cooldown, hurt_time
    global boss_spawned

    player = pygame.Vector2(W/2, H/2)
    health = 100
    score = 0
    wave = 1
    enemies = []
    bullets = []
    particles = []
    pickups = []
    shoot_time = 0
    spawn_time = 0
    dash_time = 0
    dash_cooldown = 0
    hurt_time = 0
    boss_spawned = False

def text(msg, f, color, y):
    img = f.render(msg, True, color)
    screen.blit(img, (W//2-img.get_width()//2, y))

def background():
    screen.fill(BG)
    for x in range(0, W, 50):
        pygame.draw.line(screen, (17,24,43), (x,0), (x,H))
    for y in range(0, H, 50):
        pygame.draw.line(screen, (17,24,43), (0,y), (W,y))
    for x,y in stars:
        pygame.draw.circle(screen, (65,80,110), (x,y), 2)

def draw_player():
    p = (int(player.x), int(player.y))
    pygame.draw.circle(screen, (0,60,85), p, 32)
    pygame.draw.circle(screen, CYAN, p, 22, 3)
    pygame.draw.circle(screen, (30,155,210), p, 15)
    pygame.draw.circle(screen, WHITE, p, 6)

    direction = pygame.Vector2(pygame.mouse.get_pos())-player
    if direction.length():
        direction = direction.normalize()
        end = player+direction*32
        pygame.draw.line(screen, WHITE, p,
            (int(end.x),int(end.y)), 3)

def draw_ui():
    screen.blit(font.render("SCORE: "+str(score), True, WHITE), (25,18))
    screen.blit(small.render("WAVE "+str(wave), True, PURPLE), (27,53))
    screen.blit(small.render("BEST: "+str(best), True, CYAN), (W-150,25))

    pygame.draw.rect(screen, (45,35,55), (25,H-45,230,18), border_radius=8)
    pygame.draw.rect(screen, RED,
        (25,H-45,230*health/100,18), border_radius=8)

    screen.blit(small.render("HEALTH "+str(health), True, WHITE),
        (25,H-72))

    color = GREEN if dash_cooldown <= 0 else (80,80,100)
    pygame.draw.circle(screen, color, (W-48,H-45), 17, 3)
    screen.blit(small.render("DASH", True, WHITE), (W-90,H-83))

def save_record():
    global best
    if score > best:
        best = score
        with open(SAVE, "w") as f:
            json.dump({"best":best},f)

running = True

while running:
    dt = min(clock.tick(60)/1000, .033)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and state in ("menu","over"):
                reset()
                state = "play"

            elif event.key == pygame.K_ESCAPE:
                if state == "play":
                    state = "pause"
                elif state == "pause":
                    state = "play"
                elif state == "over":
                    state = "menu"

            elif event.key == pygame.K_SPACE and state == "play":
                if dash_cooldown <= 0:
                    dash_time = .2
                    dash_cooldown = 2

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "play":
                pass

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()[0]

    if state == "menu":
        background()
        text("NEON SURVIVOR", title_font, CYAN, 145)
        text("SURVIVE THE APOCALYPSE", small, WHITE, 235)
        text("PRESS ENTER TO PLAY", font, GREEN, 345)
        text("WASD - MOVE    MOUSE - AIM", small, WHITE, 435)
        text("LEFT CLICK - SHOOT    SPACE - DASH", small, WHITE, 470)
        text("ESC - PAUSE", small, WHITE, 505)
        text("BEST SCORE: "+str(best), font, PURPLE, 560)

    elif state == "pause":
        background()
        text("PAUSED", title_font, YELLOW, 260)
        text("PRESS ESC TO CONTINUE", font, WHITE, 360)

    elif state == "play":

        # Movement
        move = pygame.Vector2(0,0)
        if keys[pygame.K_w]: move.y -= 1
        if keys[pygame.K_s]: move.y += 1
        if keys[pygame.K_a]: move.x -= 1
        if keys[pygame.K_d]: move.x += 1

        if move.length():
            move = move.normalize()

        speed = 300
        if dash_time > 0:
            dash_time -= dt
            speed = 850

        player += move*speed*dt
        player.x = max(20,min(W-20,player.x))
        player.y = max(20,min(H-20,player.y))

        dash_cooldown = max(0,dash_cooldown-dt)
        hurt_time = max(0,hurt_time-dt)

        # Shooting
        shoot_time -= dt
        if mouse and shoot_time <= 0:
            direction = pygame.Vector2(pygame.mouse.get_pos())-player
            if direction.length():
                direction = direction.normalize()
                bullets.append(Bullet(player+direction*22,direction))
                explosion(player+direction*22,CYAN,3)
                shoot_time = .14

        # Waves and enemies
        new_wave = 1+score//200
        if new_wave != wave:
            wave = new_wave
            boss_spawned = False

        if wave % 5 == 0 and not boss_spawned:
            enemies.append(Enemy("boss"))
            boss_spawned = True

        spawn_time -= dt
        if spawn_time <= 0:
            enemies.append(Enemy())
            spawn_time = max(.25,1.1-wave*.045)

        for e in enemies:
            e.update(dt)

        for b in bullets:
            b.update(dt)

        # Bullet collisions
        for b in bullets[:]:
            for e in enemies[:]:
                if b.pos.distance_to(e.pos) < e.radius+7:
                    e.hp -= 1
                    if b in bullets:
                        bullets.remove(b)
                    explosion(b.pos,CYAN,4)

                    if e.hp <= 0:
                        explosion(e.pos,e.color,20)
                        enemies.remove(e)
                        score += 100 if e.boss else 10

                        if random.random() < .18 or e.boss:
                            pickups.append(Pickup(e.pos))
                    break

        # Player damage
        for e in enemies:
            if e.pos.distance_to(player) < e.radius+17:
                if hurt_time <= 0 and dash_time <= 0:
                    health -= 15
                    hurt_time = .8
                    explosion(player,RED,15)

        if health <= 0:
            health = 0
            state = "over"
            save_record()

        # Pickups
        for p in pickups[:]:
            p.update(dt)
            if p.pos.distance_to(player) < 30:
                health = min(100,health+25)
                pickups.remove(p)
                explosion(player,GREEN,18)
            elif p.life <= 0:
                pickups.remove(p)

        bullets = [b for b in bullets if b.life > 0 and
                   -30 < b.pos.x < W+30 and -30 < b.pos.y < H+30]

        # Particles
        for p in particles:
            p.update(dt)
        particles = [p for p in particles if p.life > 0]

        # Draw
        background()

        for p in pickups:
            p.draw()
        for b in bullets:
            b.draw()
        for e in enemies:
            e.draw()
        for p in particles:
            p.draw()

        if hurt_time <= 0 or int(hurt_time*12)%2 == 0:
            draw_player()

        draw_ui()

    elif state == "over":
        background()
        for p in particles:
            p.update(dt)
            p.draw()
        text("GAME OVER", title_font, RED, 190)
        text("FINAL SCORE: "+str(score), big_font, WHITE, 300)
        text("BEST SCORE: "+str(best), font, CYAN, 365)
        text("PRESS ENTER TO PLAY AGAIN", font, GREEN, 440)
        text("ESC - MAIN MENU", small, WHITE, 500)

    pygame.display.flip()

pygame.quit()
