from pygame import *
from random import *  
mixer.init()
font.init()

win,lose = font.SysFont('Verdana',80).render('WIN!!!',True,(255,255,255)),font.SysFont('Verdana',80).render('LOSE!!!',True,(255,250,250))

class gameSprite(sprite.Sprite):

    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))

class Player(gameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >=5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 620:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,10,20,15)
        bullets.add(bullet)

class Bullet(gameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() 

total = 0
miss = 0 
class Enemy(gameSprite):
    def update(self):
        xEnemyRandom = randint(80,400)
        self.rect.y += self.speed
        global miss
        if self.rect.y >= 620:
            self.rect.y = 0
            self.rect.x = xEnemyRandom
            miss = miss + 1
mw = display.set_mode((700,500))
display.set_caption('Шутер')
galaxy = transform.scale(
    image.load('galaxy.jpg'),
    (700,500)
)
sprite_rocket = Player('rocket.png',5,400,80,100,5)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,5):
    xEnemyRandom = randint(80,400)
    monster = Enemy('ufo.png',xEnemyRandom,-40,80,50,randint(1,3))
    monsters.add(monster)
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
game = True
finish = False
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                fire_sound.play()
                sprite_rocket.fire()
    if not finish:
        mw.blit(galaxy,(0,0))
        totalIns = font.Font(None,40).render('Счёт:'+str(total),True,(180,180,180))
        misIns = font.Font(None,40).render('Пропущено:'+str(miss),True,(180,180,180))
        mw.blit(totalIns,(10,80))
        mw.blit(misIns,(10,40))
        sprite_rocket.reset()
        sprite_rocket.update()
        monsters.update()
        bullets.update()
        bullets.draw(mw)
        monsters.draw(mw)
        collideB_M = sprite.groupcollide(bullets,monsters,True,True)
        for c in collideB_M:
            total = total + 1 
            xEnemyRandom = randint(80,620)
            monster = Enemy('ufo.png',xEnemyRandom,-40,80,50,randint(1,3))
            monsters.add(monster)
        if sprite.spritecollide(sprite_rocket,monsters,True) or miss >= 3:
            mw.blit(lose,(200,200))
            finish = True
        if total >= 10:
            mw.blit(win,(200,200))
            finish = True
        display.update()
    clock.tick(40)