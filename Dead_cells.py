from pygame import *
import time as tm
'''Необхідні класи'''
 
# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (wight, height)) #разом 55,55 - параметри
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

jump = False
gravity = -10
# клас-спадкоємець для спрайту-гравця (керується стрілками)    
class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < win_width-50:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_SPACE] and self.rect.y > 5:
                global gravity 
                self.rect.y += gravity
    

class Player2(Player):
    def __init__(self, filename, x=0, y=0, width=10, height=10, speed=10):
        super().__init__(filename,x,y,width,height,speed)
        self.gravity = 0.5 #гравітація (швидкість падіння вниз)
        self.jump_power = -10 #величина стрибка
        self.vel_y = 0 #швидкість руху в стрибку
    def move(self):

        
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < win_width-50:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_SPACE] and self.rect.y > 5:
                global gravity 
                self.rect.y += gravity
    def move2(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

        

    def move_arrow(self):
        self.rect.x += 2
    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            self.can_jump = False

            
#ігрова сцена:

win_width = 1200
win_height = 600
window = display.set_mode((win_width, win_height))
back = image.load('map.jpg')
#window.fill(back)
 

arrows = []
guy = Player2('guy.png',50,190,10,40,80)
enemy1 = Player2('enemy1.png', 500,200,10,60,80)
sword1 = Player('sword3.png',5000,100,10,80,80)
sword2 = Player('sword2.png',5000,100,10,80,80)
bow1 = Player('bow1.png',5000,100,10,80,80)
bow2 = Player('bow2.png',5000,100,10,80,80)
p1 = Player('platform.png', 30,200,10,200,100)
p2 = Player('platform.png', 400,250,10,200,100)
p3 = Player('platform.png', 900,250,10,200,100)


platforms = []
platforms.append(p1)
platforms.append(p2)
platforms.append(p3)


show_image_time_sword = 0  # Початковий час 
show_image_duration_sword = 20  # Тривалість 
showing_image_sword = False # Чи відображається зображення

show_image_time_bow = 0  # Початковий час 
show_image_duration_bow = 100  # Тривалість 
showing_image_bow = False # Чи відображається зображення
cooldown_time = tm.monotonic()
#прапорці, що відповідають за стан гри
game = True
clock = time.Clock()
i = 0

while game:
                
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                sword1.rect.x = guy.rect.x + 20
                sword1.rect.y = guy.rect.y - 10
                show_image_time_sword = time.get_ticks()  # час початку показу зображення
                showing_image_sword = True

            if e.button == 3:
                if tm.monotonic() - cooldown_time >= 0.8:
                    bow1.rect.x = guy.rect.x + 20
                    bow1.rect.y = guy.rect.y - 10
                    show_image_time_bow = time.get_ticks()  # час початку показу зображення
                    showing_image_bow = True
                    arrow = Player2('arrow.png',bow1.rect.x + 20 ,bow1.rect.y + 10  , 10, 60, 60)
                    arrows.append(arrow)
                    cooldown_time = tm.monotonic()
                    
    #window.fill(back)
    window.blit(back,(0,0))
    guy.reset()
    guy.move()
    guy.move2()
    guy.update()
    p1.reset()
    p2.reset()
    p3.reset()
    sword2.reset()
    sword1.reset()
    bow1.reset()
    bow2.reset()
    enemy1.reset()
    
    if guy.rect.y <= 390:
        guy.rect.y += 3

    # Перевірка, чи потрібно відображати зображення
    if showing_image_sword:
        if time.get_ticks() - show_image_time_sword < show_image_duration_sword:
            sword1.reset()  
        else:
            showing_image = False  
            sword1.rect.x = 5000
    if showing_image_bow:
        if time.get_ticks() - show_image_time_bow < show_image_duration_bow:
            bow1.reset()  
        else:
            showing_image = False  
            bow1.rect.x = 5000 

    for a in arrows:
        a.reset()
        a.move_arrow()
        if a.rect.x >= 1200:
            arrows.remove(a)
        if a.rect.colliderect(enemy1):
                enemy1.rect.y = -1000
                arrows.remove(a)

    if sword1.rect.colliderect(enemy1):
        enemy1.rect.y = -1000
   
    display.update()
    clock.tick(60)