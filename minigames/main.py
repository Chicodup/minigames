from random import choice
from pygame import *
import pygame_menu
init()
font.init()
font1 = font.SysFont("Arial",100,True)
font2 = font.SysFont("Arial",34,True)
game_over_text = font1.render("Game Over", True,(255,0,0))
game_win_text_over_text = font1.render("WIN", True,(0,255,0))
#mixer.init()
#mixer.music.load('chicken_song.mp3')
#mixer.music.play()
mixer_music.set_volume(0.03)
#створи вікно гри;
MAP_WIDTH, MAP_HEIGHT = 25,21.5
TILESIZE = 33
WIDTH,HEIGHT =MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE
window = display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = time.Clock()
#задай фон сцени
bg = image.load('images/Grass.png')
bg = transform.scale(bg,(MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE))
cyborg_img = image.load("images/ForestRanger.png")
player_img = image.load("images/rect.png")
wall_img = image.load("images/pine_tree_png.png")
ruins_img = image.load("images/Brown-gray_ruins1.png")
gold_img = image.load("images/clipart1898966.png")
spike_img = image.load("images/spikes2.png")
fake_img = image.load("images/clipart1898966.png")
exit_img = image.load("images/clipart1898966.png")
button_img = image.load("images/Levelreoundred-min.png")
button2_img = transform.scale(image.load("images/Levelgreen-min.png"), (70,60))
all_sprites = sprite.Group()

#створи 2 спрайти та розмісти їх на сцені
class Sprite(sprite.Sprite):
    def __init__(self,sprite_img,width,height,x,y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self,sprite_img,width,height,x,y):
        super().__init__(sprite_img,width,height,x,y)
        self.hp = 100
        self.buttons = 0
        self.speed = 3.23
        self.left = self.image
        self.right = transform.flip(self.image,True, False)
    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if (key_pressed[K_w] or key_pressed[K_UP])and self.rect.y > 0:
            self.rect.y -= self.speed
        if (key_pressed[K_s]or key_pressed[K_DOWN])and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if (key_pressed[K_a] or key_pressed[K_LEFT])and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = self.left 
        if (key_pressed[K_d]or key_pressed[K_RIGHT]) and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.image = self.right

        collide_list = sprite.spritecollide(self,walls,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
        collide_list = sprite.spritecollide(self,ruins,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
        enemy_collide = sprite.spritecollide(self,enemys,False,sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100
        fake_collide = sprite.spritecollide(self,fakes,False,sprite.collide_mask)
        if len(fake_collide) > 0:
            self.hp -= 100
        enemy_collide = sprite.spritecollide(self,poshalkikill,False,sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100
        fake_collide = sprite.spritecollide(self,spikes,False,sprite.collide_mask)
        if len(fake_collide) > 0:
            self.hp -= 100
        collide_list = sprite.spritecollide(self,buttons,False,sprite.collide_mask)
        for btn in collide_list:
            btn.image = button2_img
            buttons.remove(btn)
        collide_list = sprite.spritecollide(self,buttons,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos

            
    

class Enemy(Sprite):
    standart_speed = 2.1
    def __init__(self,sprite_img,width,height,x,y):
        super().__init__(sprite_img,width,height,x,y)
        self.damage = 1
        self.speed = 2.1
        self.leftimage = self.image
        self.rightimage = transform.flip(self.image,True,False)
        self.dir_list = ["right","left","up","down"]
        self.dir = choice(self.dir_list)
    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == "right":
            self.rect.x += self.speed
            self.image = self.rightimage
        elif self.dir == "left":
            self.rect.x -= self.speed
            self.image = self.leftimage
        elif self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed
        collide_list = sprite.spritecollide(self,walls,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.dir = choice(self.dir_list)
            self.rect.x, self.rect.y = old_pos
        collide_list = sprite.spritecollide(self,poshalkas,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.dir = choice(self.dir_list)
            self.rect.x, self.rect.y = old_pos
        collide_list = sprite.spritecollide(self,spikes,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.dir = choice(self.dir_list)
            self.rect.x, self.rect.y = old_pos
        collide_list = sprite.spritecollide(self,ruins,False,sprite.collide_mask)
        if len(collide_list) > 0:
            self.dir = choice(self.dir_list)
            self.rect.x, self.rect.y = old_pos

        

player = Player(player_img,50,50,300,300)
walls = sprite.Group()
ruins = sprite.Group()
enemys = sprite.Group()
fakes = sprite.Group()
spikes = sprite.Group()
buttons = sprite.Group()


exits = sprite.Group()
poshalkas = sprite.Group()
poshalkikill = sprite.Group()



def load_map(map_file):

    global gold,exits
    for s in all_sprites:
        if s != player:
            s.kill()

    with open(map_file) as f:
        map = f.readlines()
        x = 0
        y = 0
        for line in map:
            for symwol in line:
                if symwol == "w":
                    walls.add(Sprite(wall_img, TILESIZE,TILESIZE,x,y))
                if symwol == "r":
                    ruins.add(Sprite(ruins_img, 30,30,x,y))
                if symwol == "p":
                    player.rect.x = x
                    player.rect.y = y
                if symwol == "g":
                    gold = Sprite(gold_img, 40,40,x,y)
                if symwol == "f":
                    fakes.add(Sprite(fake_img, 40,40,x,y))
                if symwol == "s":
                    spikes.add(Sprite(spike_img, 26,26,x,y))
                if symwol == "b":
                    buttons.add(Sprite(button_img, 70,60,x,y))
                if symwol == "a":
                    exits.add(Sprite(exit_img, 40,40,x,y))
                if symwol == "n":
                    enemys.add(Enemy(wall_img, TILESIZE,TILESIZE,x,y))
                if symwol == "l":
                    enemys.add(Enemy(wall_img, 150,150,x,y))
                if symwol == "u":
                    walls.add(Sprite(cyborg_img, TILESIZE,TILESIZE,x,y))
                if symwol == "e":
                    enemys.add(Enemy(cyborg_img, TILESIZE,TILESIZE,x,y))
                x += TILESIZE
            y+=TILESIZE
            x = 0
            

load_map("map4.txt")
lvl = 4

#оброби подію «клік за кнопкою "Закрити вікно"»
run = False
finish = False
def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')
    player.speed = value
    if player.speed == 5:
        Enemy.standart_speed = 1
    if player.speed == 3.5:
        Enemy.standart_speed = 2.1
    if player.speed == 2:
        Enemy.standart_speed = 10

    for enemy in enemys:
        enemy.speed = Enemy.standart_speed

def start_the_game():
    # Do the job here !
    global run
    run = True
    menu.disable()

#завантажуємо картинку
myimage = pygame_menu.baseimage.BaseImage(
    image_path='images/Grass.png',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)
#створюємо власну тему - копію стандартної
mytheme = pygame_menu.themes.THEME_DARK.copy()
# колір верхньої панелі (останній параметр - 0 робить її прозорою)
mytheme.title_background_color=(255, 255, 255, 0) 
#задаємо картинку для фону
mytheme.background_color = myimage
menu = pygame_menu.Menu('mini', WIDTH, HEIGHT,
                       theme=mytheme)   

#user_name = menu.add.text_input("Ім'я :", default='Анонім')
menu.add.selector('Складність :', [('Hard',2), ('Normal', 3.5),('Easy', 5)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(window)

timer_text = font2.render(f"Time: 0",True,(255,255,255))
current_time = 0
total_time = 300
start_time = time.get_ticks()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            if player.hp <= 0:
                run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)

    
    window.blit(bg, (0,0))
    
    if current_time >= total_time:
        finish = True


    if player.hp <= 0:
        finish = True
    
    if lvl==4:
        collide_list = sprite.spritecollide(player,exits,False,sprite.collide_mask)
        if len(collide_list) > 0:
            if len(buttons) == 0:
                finish = True
                game_over_text = font1.render("  Перемога!", True,(0,255,0))
    else:
        if sprite.collide_mask(player,gold):
            lvl += 1
            if lvl <= 4:
                load_map(f"map{lvl}.txt")

    all_sprites.draw(window)
    window.blit(timer_text ,(10,10))
    if not finish:
        now = time.get_ticks()
        current_time = int((now - start_time)/1000)
        timer_text = font2.render(f"Time: {total_time - current_time}",True,(255,255,255))
        all_sprites.update()
    if finish:
        window.blit(game_over_text,(230,270))

    display.update()
    clock.tick(FPS)