import pygame, os, time
from globalVars import *

pygame.init()


# Define constants for file name and possible screen positions
pygame.display.set_icon(pygame.image.load('files/IconTimer.png'))
SCREEN_FILE = 'files/screen_positions_timer.txt'
POSSIBLE_POSITIONS = ['10,1310', '420,1310', '10,1150','420,1150']

def get_screen_position():
    # Read screen positions from file, or create file if it doesn't exist
    if not os.path.exists(SCREEN_FILE):
        with open(SCREEN_FILE, 'w') as f:
            pass
    with open(SCREEN_FILE, 'r') as f:
        positions = [line.strip() for line in f.readlines()]

    # Find the first available position from the possible positions list
    for position in POSSIBLE_POSITIONS:
        if position not in positions:
            return position
    
    # If all positions are taken, return None
    return None

def set_screen_position(position):
    # Append the position to the file
    with open(SCREEN_FILE, 'a') as f:
        f.write(f'{position}\n')
    # Set the SDL_VIDEO_WINDOW_POS environment variable to the screen position
    os.environ['SDL_VIDEO_WINDOW_POS'] = position

def clear_screen_position(position):
    # Remove the position from the file
    with open(SCREEN_FILE, 'r') as f:
        positions = [line.strip() for line in f.readlines()]
    positions.remove(position)
    with open(SCREEN_FILE, 'w') as f:
        for position in positions:
            f.write(f'{position}\n')

# os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
position = get_screen_position()
if position is None:
    exit()

set_screen_position(position)

screen = pygame.display.set_mode((400, 120), pygame.HWSURFACE)
pygame.display.set_caption("TIMER")

japFont=pygame.font.Font("./files/mplus-1mn-bold.ttf", 16)
engFont=pygame.font.Font("./files/JetBrainsMono-Regular.ttf", 26)

def write(text, color=white,x=0,line=0,japanese=False,righPad=False):
    text=str(text)
    if japanese:
        y=int(5+25*line-1)
        if righPad:
            screen.blit(japFont.render(text,True,color),(x-16*len(text),y))
        else:
            screen.blit(japFont.render(text,True,color),(x,y))
    else:
        y=int(5+25*line)
        if righPad:
            screen.blit(engFont.render(text,True,color),(x-10*len(text),y))
        else:
            screen.blit(engFont.render(text,True,color),(x,y))

start_time = None
time_limit = None
time_left = 0
# play_sound = False

sound = pygame.mixer.Sound('files/sound.wav')

running = True
draw = True
inText = ""

soundPlaying=False

def start_timer(minutes, seconds):
    global start_time,time_limit
    start_time = time.time()
    time_limit = minutes * 60 + seconds
    # time_left = time_True

def display_time():
    global time_left
    minutes = int(time_left / 60)
    seconds = int(time_left % 60)
    # if len(str(minutes))==1:
    time_text = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
    write(time_text,violetLight,160,1)

def paint():
    global inText
    screen.fill(black)
    pygame.draw.line(screen, grey, (5, 80), (395, 80),width=5)
    if time_left > 0:
        display_time()
        pygame.draw.line(screen, cyan, (5, 80), (round(5 + ((time_left - 0) / (time_limit - 0)) * (395 - 5)), 80),width=5)
    else:
        ghostText='10:00'
        if len(inText)==1:
            inText='0'+inText
        elif len(inText)>1 and inText[2] !=':':
            inText=inText[1:]
        write(inText,violet,160,1)
        ghostText=ghostText[len(inText):]
        for i in range(len(inText)):
            ghostText=' '+ghostText
        write(ghostText,grey,160,1)
        pygame.draw.line(screen, cyan, (5, 80), (395, 80),width=5)
        if soundPlaying:
            pygame.draw.line(screen, red, (5, 80), (395, 80),width=5)

    pygame.display.update()

while running:
    sleepTime=0.05
    if start_time is not None:
        time_left = time_limit - (time.time() - start_time)
        sleepTime=0.01
        if time_left<=0:
            start_time=None
            pygame.mixer.init()
            pygame.mixer.music.load("files/sound.wav")
            pygame.mixer.music.play(-1)
            soundPlaying=True
            inText=''
        draw=True

    if pygame.event.peek(pygame.KEYDOWN) or pygame.event.peek(pygame.QUIT) or draw:        
        if draw:
            paint()
            draw = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                draw=True
                if pygame.key.name(event.key) == "space":
                    if soundPlaying:
                        pygame.mixer.quit()
                        soundPlaying=False
                    else:
                        inText += ":"
                elif pygame.key.name(event.key) == "backspace":
                    inText=inText[:-1]
                elif pygame.key.name(event.key) == "c":
                    inText=''
                    start_time=None
                elif pygame.key.name(event.key) == "q":
                    running=False
                elif pygame.key.name(event.key) == "tab":
                    if len(inText)==0:
                        inText='00:'
                    else:
                        inText+=':00'
                elif pygame.key.name(event.key) == "return":
                    # todo ejecutar
                    if inText=='':
                        inText='10:00'
                    minutes, seconds = map(int, inText.split(':'))
                    start_timer(minutes,seconds)
                    inText=''
                else:
                    inText += pygame.key.name(event.key)
            elif event.type == pygame.QUIT:
                running = False
    
    time.sleep(sleepTime)  # Add a 10ms delay to reduce CPU load
try:
    clear_screen_position(position)
except:
    pass