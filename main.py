import pygame
import os
import random
from pygame.sprite import Sprite
pygame.init()

width, height = 400,600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60
run = True

class Player_Bullets(Sprite):
    def  __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load('png/laserRedShot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (15,20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.vel = 5
    def update(self):
        self.rect.y -= self.vel
        if self.rect.y < 0 :
            self.kill()


class PlayerShip(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('png/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.bottom = height-65
        self.vel = 5

    def update(self):
        keystat = pygame.key.get_pressed()
        if keystat[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.vel
        if keystat[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x-=self.vel
        if self.rect.left > width:
            self.rect.right = 0
    def shoot(self):
        bullets = Player_Bullets(self.rect.centerx, self.rect.top)
        sprites.add(bullets)
        bullet.add(bullets)

class Enemy_Bullet(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.image.load('png/laserGreenShot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.vel = 5
        self.rect.x = x
        self.rect.top = y
    def update(self):
        self.rect.y += self.vel
        if self.rect.y > height:
            self.kill()
class Meteor(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('png/meteorBig.png').convert_alpha()
        self.image =  pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.run_time = 100
        self.run = self.run_time
        self.vel = 4
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
    def rotate(self):
        self.rot = (self.rot + self.rot_speed) / 360
        new_image = pygame.transform.rotate(self.image, self.rot)
        old_center = self.rect.center
        self.image_ = new_image
        self.rect = self.image_.get_rect()
        self.rect.center = old_center
    def update(self):
        self.rect.y += self.vel
        self.rotate()
        if self.rect.top > height:
            self.kill()

class EnemyShip_Meteor(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('png/enemyShip.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = 0
        self.enemy_state = {'ATTACK_MODE':'ATTACK','RUN_MODE':'RUN'}
        self.state = self.enemy_state['RUN_MODE']
        self.bullet_time_max = 60
        self.bullet_time = self.bullet_time_max
        self.bullet_group = pygame.sprite.Group()
        self.x_vel = 0
        self.y_vel = random.randrange(2,5)
        self.enemy_bullet_group = pygame.sprite.Group()
        self.point = 2
        
    def ATTACK_MODE(self):
        self.y_vel = 0
        while self.x_vel == 0:
            self.x_vel = random.randrange(-4, 4)
        if self.bullet_time == 0:
            self.shoot()
            self.bullet_time = self.bullet_time_max
        else:
            self.bullet_time -= 1
        if self.rect.left < 0:
            self.x_vel *= -1
        elif self.rect.right > width:
            self.x_vel *= -1
    def RUN_MODE(self):
        if self.rect.bottom >150:
            self.state = self.enemy_state['ATTACK_MODE']
        
    def shoot(self):
        enemy_bullet = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
        self.enemy_bullet_group.add(enemy_bullet)
        sprites.add(enemy_bullet)
        enemy_bullet_group.add(enemy_bullet)
        

    def update(self):
        self.bullet_group.update()
        if self.state == 'ATTACK':
            self.ATTACK_MODE()
        elif self.state == 'RUN':
            self.RUN_MODE()
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
    def test(self):
        score = ScoreBoard()
        score.update_score()

        
        

class Star(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((2,2))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(10, width)
        self.rect.y = 0
        self.color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        self.star_vel = random.randrange(1,5)  
        self.image.fill(self.color)
    def update(self):
        self.rect.y += self.star_vel
        

class Background(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.star_sprite = pygame.sprite.Group()
        self.run_time = 150
        self.run = self.run_time
        self.meteor_group = pygame.sprite.Group()
    def update(self):
        self.image.fill((0,0,10))
        star = Star()
        self.star_sprite.add(star)
        self.star_sprite.draw(screen)
        self.star_sprite.update()
        for star in self.star_sprite:
            if star.rect.top > height:
                self.star_sprite.remove(star)

        if self.run == 0:
            meteor = Meteor()
            self.meteor_group.add(meteor)
            sprites.add(meteor)
            self.run = self.run_time
        else:
            self.run -=1

class Health_Heart(Sprite):
    def __init__(self):
        super(Health_Heart, self).__init__()
        self.image = pygame.image.load('png/Heart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = height - self.rect.height - 20
    def update(self):
        pass


class Health(Sprite):
    def __init__(self):
        super(Health, self).__init__()
        self.w = 100
        self.color = (0,255,0)
        self.image = pygame.Surface((self.w, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left = 40
        self.rect.y = height - self.rect.height - 25
    def update(self, health):
        self.w -= health
        if self.w < 70:
            self.color = (255,255,0)
        if self.w <40:
            self.color = (255,0,0)
        self.image = pygame.Surface((self.w, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.left = 40
        self.rect.y = height - self.rect.height - 25
        if self.w == 0:
            self.w = 100
            self.color = (0,255,0)
            


class ScoreBoard(Sprite):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.score = 0
        self.color = (255,255,255)
        self.font = pygame.font.Font(None, 15)
        self.image = self.font.render(str(f'Score: {self.score}'), True, self.color, None)
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.width - 10
        self.rect.y = height - self.rect.height - 15

    def update(self, point):
        self.score += point
        self.image = self.font.render(str(f'Score: {self.score}'), True, self.color, None)
        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.width - 10
        self.rect.y = height - self.rect.height - 15

    def update_score(self):
        pass
class GameStat(Sprite):
    def __init__(self):
        super(GameStat, self).__init__()
        self.image = pygame.image.load('png/HUD.png')
        self.image = pygame.transform.scale(self.image, (width, 50))
        self.rect = self.image.get_rect()
        self.rect.y = height - self.rect.height - 5
        self.health_bar = Health()
        self.hit_count = 0
        self.health_group = pygame.sprite.Group()
        self.player_score = 0
        self.score_board = ScoreBoard()
        self.score_group = pygame.sprite.Group()
        self.health_icon = Health_Heart()
        self.icon_group = pygame.sprite.Group()

    def update(self):
        self.health_group.add(self.health_bar)
        self.icon_group.add(self.health_icon)
        self.score_group.add(self.score_board)
        self.health_group.draw(screen)
        self.icon_group.draw(screen)
        self.score_group.draw(screen)
    def update_score(self, point):
        self.score_group.update(point)
    def update_health(self, health):
        self.health_group.update(health)



sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
game_stat = pygame.sprite.Group()

stat = GameStat()
game_stat.add(stat)
bg = Background()
sprites.add(bg)
for i in range(2):
    enemy = EnemyShip_Meteor()
    sprites.add(enemy)
    enemy_group.add(enemy)

ship = PlayerShip()
sprites.add(ship)
while run:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                ship.shoot()
    bullet_hit = pygame.sprite.groupcollide(bullet, enemy_group, True, True)
    for hits, enemy_ in bullet_hit.items():
        enemy = EnemyShip_Meteor()
        sprites.add(enemy)
        enemy_group.add(enemy)
        for item in enemy_:
            stat.update_score(2)
    meteor_hit = pygame.sprite.groupcollide(bullet, bg.meteor_group, True, True)
    for hits, meteors in meteor_hit.items():
        for item in meteors:
            stat.update_score(1)
            
    hit = pygame.sprite.spritecollide(ship, enemy_bullet_group, True)
    for item in hit:
        stat.update_health(10)
    hits = pygame.sprite.spritecollide(ship, bg.meteor_group, True)
    for hit in hits:
        stat.update_health(20)
    sprites.draw(screen)
    game_stat.draw(screen)
    game_stat.update()
    sprites.update()
    pygame.display.update()

pygame.quit()