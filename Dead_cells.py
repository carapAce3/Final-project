from pygame import *
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

            
#ігрова сцена:
back = (200, 255, 255)  #колір фону (background)
win_width = 1200
win_height = 600
window = display.set_mode((win_width, win_height))
back = image.load('map.jpg')
#window.fill(back)
 
guy = Player('guy.png',50,390,10,40,80)
sword = Player('sword.png',50,100,10,40,80)
bow = Player('bow.png',50,100,10,40,80)
platform = GameSprite('platform.png', 30,460,10,200,100)
platforms = []
platforms.append(platform)





#прапорці, що відповідають за стан гри
game = True
clock = time.Clock()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                print('')
                
    #window.fill(back)
    window.blit(back,(0,0))
    guy.reset()
    platform.reset()
    guy.move()
    if guy.rect.y <= 390:
        guy.rect.y += 3


    


    #if sprite.collide_rect(guy,platform):
        #guy.rect.y += 1
        #guy.rect.y -= 1
   
    display.update()
    clock.tick(60)