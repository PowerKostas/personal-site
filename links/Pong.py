import pygame,sys,random
from ctypes import windll
    
#General Setup
windll.shcore.SetProcessDpiAwareness(1)
pygame.mixer.pre_init(22050,-16,2,1)
pygame.mixer.init(22050,-16,2,1)
pygame.init()
clock=pygame.time.Clock()

#Window Setup
width=1600
height=900
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong.')

ball=pygame.Rect(width/2-15,height/2-15,30,30)
paddle_1=pygame.Rect(10,height/2-90,30,180)
paddle_2=pygame.Rect(width-40,height/2-90,30,180)
bg_color=pygame.Color('grey12')
light_grey=(200,200,200)

#Menu Visuals
pong_font=pygame.font.Font('freesansbold.ttf', 100)
sinmul_font=pygame.font.Font('freesansbold.ttf',72)
single_box=pygame.Rect(250,395,500,105)
multi_box=pygame.Rect(850,395,500,105)
easy_box=pygame.Rect(250,300,500,105)
medium_box=pygame.Rect(850,300,500,105)
hard_box=pygame.Rect(250,600,500,105)
impossible_box=pygame.Rect(850,600,500,105)
play_again_box=pygame.Rect(250,420,500,105)
main_menu_box=pygame.Rect(850,420,500,105)

#Score
score_font=pygame.font.Font('freesansbold.ttf',64)

#Sound
score_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/whistle.mp3')
score_sound.set_volume(0.5)
bong_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/bong.mp3')
bong_sound.set_volume(0.9)
close_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/close.mp3')
close_sound.set_volume(0.5)
open_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/open.mp3')
celebration_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/celebration.mp3')
losing_sound=pygame.mixer.Sound('C:/Users/Kostas/Desktop/Codes/Pong/sounds/losing.mp3')
losing_sound.set_volume(4.0)
pygame.mixer.music.load('C:/Users/Kostas/Desktop/Codes/Pong/sounds/main.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

paddle_1_speed=0 
paddle_2_speed=0

def quit(i):
    if i.type==pygame.QUIT:
        pygame.quit()
        sys.exit()
    if i.type==pygame.KEYDOWN:
        if i.key==pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

def up_down_both(i):
    global paddle_1_speed,paddle_2_speed
    #This checks for the specific button
    if i.type==pygame.KEYDOWN:
        #This checks for the specific button (This continues adding indefinetely*)
        if i.key==pygame.K_w:
            paddle_1_speed-=6
        if i.key==pygame.K_s:
            paddle_1_speed+=6
        if i.key==pygame.K_UP:
            paddle_2_speed-=6
        if i.key==pygame.K_DOWN:
            paddle_2_speed+=6
    #This checks if any button has been released (*Till it's released here where it stops)
    if i.type==pygame.KEYUP:
        if i.key==pygame.K_w:
            paddle_1_speed+=6
        if i.key==pygame.K_s:
            paddle_1_speed-=6
        if i.key==pygame.K_UP:
            paddle_2_speed+=6
        if i.key==pygame.K_DOWN:
            paddle_2_speed-=6                              
    return paddle_1_speed,paddle_2_speed

def up_down_1(i):
    global paddle_1_speed
    if i.type==pygame.KEYDOWN:
        if i.key==pygame.K_w:
            paddle_1_speed-=6
        if i.key==pygame.K_s:
            paddle_1_speed+=6
    if i.type==pygame.KEYUP:
        if i.key==pygame.K_w:
            paddle_1_speed+=6
        if i.key==pygame.K_s:
            paddle_1_speed-=6                            
    return paddle_1_speed

def up_down_ai(ball_speed_y,old_ball_speed,new_ball_speed):
    global paddle_2_speed
    if ball_speed_y<0:
        paddle_2_speed-=6
    else:
        paddle_2_speed+=6
    if old_ball_speed-new_ball_speed==0:
        paddle_2_speed+=6
    return paddle_2_speed

def multi_menu(game_type,frames):
    while True:
        for i in pygame.event.get():
            quit(i)
            if i.type==pygame.MOUSEBUTTONDOWN:
                if easy_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game(5,5,game_type,frames)
                if medium_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game(7,7,game_type,frames)
                if hard_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game(9,9,game_type,frames)
                if impossible_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game(11,11,game_type,frames)
                if back_rect.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    return
            
        pygame.display.flip()
        clock.tick(120)
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        back_text=sinmul_font.render('Back',False,light_grey)
        back_rect=screen.blit(back_text,(10,828.5))
        if back_rect.collidepoint(mouse_pos):
            back_text=sinmul_font.render('Back',False,'darkgrey')
            back_rect=screen.blit(back_text,(10,828.5))
        ball_speed_text=pong_font.render('Ball Speed',False,light_grey)
        screen.blit(ball_speed_text,(535,50))
        if easy_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'dodgerblue4',easy_box)
        else:
            pygame.draw.rect(screen,light_grey,easy_box)
        if medium_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgreen',medium_box)
        else:
            pygame.draw.rect(screen,light_grey,medium_box)
        if hard_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkorange4',hard_box)
        else:
            pygame.draw.rect(screen,light_grey,hard_box)
        if impossible_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'red4',impossible_box)
        else:
            pygame.draw.rect(screen,light_grey,impossible_box)
        easy_text=sinmul_font.render('Slow',False,'cadetblue')
        screen.blit(easy_text,(410,320))
        medium_text=sinmul_font.render('Medium',False,'chartreuse4')
        screen.blit(medium_text,(962,320))
        hard_text=sinmul_font.render('Fast',False,'orange3')
        screen.blit(hard_text,(425,620))
        impossible_text=sinmul_font.render('Impossible',False,'red3')
        screen.blit(impossible_text,(908,620))

def single_menu():
    while True:
        for i in pygame.event.get():
            quit(i)
            if i.type==pygame.MOUSEBUTTONDOWN:
                if easy_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    multi_menu(1,80)
                if medium_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    frames=120
                    multi_menu(1,160)
                if hard_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    multi_menu(1,240)
                if impossible_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    frames=480
                    multi_menu(1,frames)
                if back_rect.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    return

        pygame.display.flip()
        clock.tick(120)
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        difficulties_text=pong_font.render('Difficulties',False,light_grey)
        screen.blit(difficulties_text,(525,50))
        if easy_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'dodgerblue4',easy_box)
        else:
            pygame.draw.rect(screen,light_grey,easy_box)
        if medium_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgreen',medium_box)
        else:
            pygame.draw.rect(screen,light_grey,medium_box)
        if hard_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkorange4',hard_box)
        else:
            pygame.draw.rect(screen,light_grey,hard_box)
        if impossible_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'red4',impossible_box)
        else:
            pygame.draw.rect(screen,light_grey,impossible_box)
        easy_text=sinmul_font.render('Easy',False,'cadetblue')
        screen.blit(easy_text,(414,320))
        medium_text=sinmul_font.render('Medium',False,'chartreuse4')
        screen.blit(medium_text,(962,320))
        hard_text=sinmul_font.render('Hard',False,'orange3')
        screen.blit(hard_text,(413,620))
        impossible_text=sinmul_font.render('Impossible',False,'red3')
        screen.blit(impossible_text,(908,620))
        back_text=sinmul_font.render('Back',False,light_grey)
        back_rect=screen.blit(back_text,(10,828.5))
        if back_rect.collidepoint(mouse_pos):
            back_text=sinmul_font.render('Back',False,'darkgrey')
            back_rect=screen.blit(back_text,(10,828.5))

def winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner):
    while True:
        for i in pygame.event.get():
            quit(i)
            if i.type==pygame.MOUSEBUTTONDOWN:
                if play_again_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game(ball_speed_x,ball_speed_y,game_type,frames)
                if main_menu_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    main_menu()
        
        pygame.display.flip()
        clock.tick(120)
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        winning_text=pong_font.render(winner+' won!',False,light_grey)
        if game_type==1 and (paddle_2_score==3 or paddle_2_score==5):
            screen.blit(winning_text,(424,50))
        else:
            screen.blit(winning_text,(470,50))
        if play_again_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgrey',play_again_box)
        else:
            pygame.draw.rect(screen,light_grey,play_again_box)
        if main_menu_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgrey',main_menu_box)
        else:
            pygame.draw.rect(screen,light_grey,main_menu_box)
        play_again_text=sinmul_font.render('Play Again',False,'grey12')
        screen.blit(play_again_text,(311,441))
        play_again_text=sinmul_font.render('Main Menu',False,'grey12')
        screen.blit(play_again_text,(905,441))

def game(ball_speed_x,ball_speed_y,game_type,frames):
    global paddle_1_speed,paddle_2_speed,paddle_1_score,paddle_2_score
    count=0
    paddle_1_score=0
    paddle_2_score=0
    paddle_1_speed=0
    paddle_2_speed=0
    random_num=90
    x=25
    if game_type==1:
        if ball_speed_x==11 and ball_speed_x==-11:
            x=30
    while True:
        count+=1
        if count==2:
            pygame.time.wait(2100)
            ball_speed_x*=random.choice([-1,1])
            ball_speed_y*=random.choice([-1,1])
        if game_type==1:
            for i in pygame.event.get():
                quit(i)
                paddle_1_speed=up_down_1(i)
    
           
            paddle_1.y+=paddle_1_speed
            if count % frames==0 and frames!=0:
                random_num+=random.choice((1,2,3,4,5,6,7,8,9,10))
            paddle_2.y=ball.centery-random_num

        else:
            for i in pygame.event.get():
                quit(i)
                paddle_1_speed,paddle_2_speed=up_down_both(i)

            paddle_1.y+=paddle_1_speed
            paddle_2.y+=paddle_2_speed
        
        #Visuals
        screen.fill(bg_color)
        score_text_1=score_font.render(f"{paddle_1_score}",False,light_grey)
        screen.blit(score_text_1,(700,25))
        score_text_2=score_font.render(f"{paddle_2_score}",False,light_grey)
        screen.blit(score_text_2,(864,25))
        pygame.draw.rect(screen,light_grey,paddle_1)
        pygame.draw.rect(screen,light_grey,paddle_2)
        pygame.draw.ellipse(screen,light_grey,ball)
        pygame.draw.aaline(screen,light_grey,(width/2,0),(width/2,height))

        #To Refresh
        pygame.display.flip()
        clock.tick(120)

        #Animation Of Ball
        ball.x+=ball_speed_x
        ball.y+=ball_speed_y

        #Collisions (remember y is reversed,δηλαδή η κορυφή είναι 0 και ο πάτος 900)
        if ball.top<=0 or ball.bottom>=height:
            pygame.mixer.Sound.play(bong_sound)
            ball_speed_y*=-1
        if ball.right>=width:
            pygame.mixer.Sound.play(score_sound)
            ball.center=(width/2,height/2)
            paddle_1.center=(x,height/2)
            paddle_2.center=(width-x,height/2)
            ball_speed_x*=random.choice([-1,1])
            ball_speed_y*=random.choice([-1,1])
            paddle_1_score+=1
            random_num=90
            winner='Player 1'
            pygame.time.wait(2100)
        if ball.left<=0:
            pygame.mixer.Sound.play(score_sound)
            ball.center=(width/2,height/2)
            paddle_1.center=(x,height/2)
            paddle_2.center=(width-x,height/2)
            ball_speed_x*=random.choice([-1,1])
            ball_speed_y*=random.choice([-1,1])
            paddle_2_score+=1
            random_num=90
            if game_type==2:
                winner='Player 2'
            else:
                winner='Computer'
            pygame.time.wait(2100)
            
        #Don't worry about this
        if ball.colliderect(paddle_1) and ball_speed_x<0:
            pygame.mixer.Sound.play(bong_sound)
            if abs(ball.left-paddle_1.right)<10:
                ball_speed_x*=-1
            elif abs(ball.bottom-paddle_1.top)<10 and ball_speed_y>0:
                ball_speed_y*=-1
            elif abs(ball.top-paddle_1.bottom)<10 and ball_speed_y<0:
                ball_speed_y*=-1
        if ball.colliderect(paddle_2) and ball_speed_x>0:
            pygame.mixer.Sound.play(bong_sound)
            if abs(ball.right-paddle_2.left)<10:
                ball_speed_x*=-1
            elif abs(ball.bottom-paddle_2.top)<10 and ball_speed_y>0:
                ball_speed_y*=-1
            elif abs(ball.top-paddle_2.bottom)<10 and ball_speed_y<0:
                ball_speed_y*=-1
        
        if paddle_1.top<=2:
            paddle_1.top=2
        if paddle_1.bottom>=height-2:
            paddle_1.bottom=height-2
        if paddle_2.top<=2:
            paddle_2.top=2
        if paddle_2.bottom>=height-2:
            paddle_2.bottom=height-2
        
        if game_type==2:
            if paddle_1_score==5 or paddle_2_score==5:
                pygame.mixer.Sound.play(celebration_sound)
                winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner)
        else:
            if (ball_speed_x==5 or ball_speed_x==-5) or (ball_speed_x==7 or ball_speed_x==-7):
                if paddle_1_score==3:
                    pygame.mixer.Sound.play(celebration_sound)
                    winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner)
                elif paddle_2_score==3:
                    pygame.mixer.Sound.play(losing_sound)
                    winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner)
            else:
                if paddle_1_score==5:
                    pygame.mixer.Sound.play(celebration_sound)
                    winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner)
                elif paddle_2_score==5:
                    pygame.mixer.Sound.play(losing_sound)
                    winning_screen(ball_speed_x,ball_speed_y,game_type,frames,winner)

def main_menu():
    while True:
        #Refresh
        pygame.display.flip()
        clock.tick(120)

        #Visuals
        screen.fill('grey12')
        mouse_pos=pygame.mouse.get_pos()
        exit_text=sinmul_font.render('Exit',False,light_grey)
        exit_rect=screen.blit(exit_text,(1445,827.5))
        if exit_rect.collidepoint(mouse_pos):
            exit_text=sinmul_font.render('Exit',False,'darkgrey')
            exit_rect=screen.blit(exit_text,(1445,827.5))
        if single_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgrey',single_box)
        else:
            pygame.draw.rect(screen,light_grey,single_box)
        if multi_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen,'darkgrey',multi_box)
        else:
            pygame.draw.rect(screen,light_grey,multi_box)
        pong_text=pong_font.render('Pong',False,light_grey)
        pong_rect=screen.blit(pong_text,(671,52))
        single_text=sinmul_font.render('Singleplayer',False,'grey12')
        screen.blit(single_text,(272,414))
        multi_text=sinmul_font.render('Multiplayer',False,'grey12')
        screen.blit(multi_text,(900,415))
        
        for i in pygame.event.get():
            quit(i)
            if i.type==pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(close_sound)
                    pygame.time.wait(600)
                    pygame.quit()
                    sys.exit()
                if multi_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game_type=2
                    multi_menu(game_type,0)
                if single_box.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(open_sound)
                    game_type=1
                    single_menu()
                if pong_rect.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(bong_sound)

while True:
    main_menu()