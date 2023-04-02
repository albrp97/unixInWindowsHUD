import pygame, os, time
from globalVars import *
import platform
import psutil
import time
import wmi
import subprocess

pygame.init()

pygame.display.set_icon(pygame.image.load('files/IconTerminal.png'))
os.environ['SDL_VIDEO_WINDOW_POS'] = "865,100"
screen = pygame.display.set_mode((830, 400), pygame.HWSURFACE)
pygame.display.set_caption("HANKA TERMINAL")

japFont=pygame.font.Font("./files/mplus-1mn-bold.ttf", 16)
engFont=pygame.font.Font("./files/JetBrainsMono-Regular.ttf", 16)

def colorOnText(text,colora,colorb,x,line,japanese=False):
    text=str(text)
    if japanese:
        y=int(5+25*line-1)
        pygame.draw.rect(screen,colorb,pygame.Rect(x-1,y,2+14*len(text),24))
        label = japFont.render(text, True, colora)
        screen.blit(label, (x, y))
    else:
        y=int(5+25*line)
        pygame.draw.rect(screen,colorb,pygame.Rect(x-1,y,2+10*len(text),24))
        label = engFont.render(text, True, colora)
        screen.blit(label, (x, y))

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

def color_gradient(start_color, end_color, steps):
    # Extract the RGB values of the start and end colors
    start_rgb = start_color.r, start_color.g, start_color.b
    end_rgb = end_color.r, end_color.g, end_color.b

    # Calculate the step size for each RGB component
    step_size = [(end - start) / steps for start, end in zip(start_rgb, end_rgb)]

    # Generate a list of colors representing the gradient between start and end colors
    gradient_colors = [pygame.Color(int(start_rgb[0] + step_size[0] * i),
                                int(start_rgb[1] + step_size[1] * i),
                                int(start_rgb[2] + step_size[2] * i)) for i in range(steps)]

    return gradient_colors

hankaHash=['#####    #####       #####     #####       ##### #####    ######      #####',
           '#####    #####      #######    ######      ##### #####   ######      #######',
           '#####    #####     #########   #######     ##### ##### ######       #########',
           '##############    ##### #####  ########    ##### ##########        ##### #####',
           '##############   #####   ##### ##########  ##### ###########      #####   #####',
           '#####    #####  #####     ########## ##### ##### ###### ######   #####     #####',
           '#####    ##### #####       #########  ########## #####   ###### #####       #####',
           '#####    ##########         ########   ######### #####    ##########         #####'
           ]

colorScheme=[red,orange,yellow,green,cyan,blue,violetLight,violet]
gradient=colorScheme

def system_info():
    # Get operating system name and version
    os_name = platform.system()
    os_version = '11'
    
    # Get kernel version
    kernel_version = platform.version().split('.')[1:]
    kernel_version='.'.join(kernel_version)
    kernel_version='.'+kernel_version
    
    # Get current time and uptime
    current_time = time.strftime('%Y-%m-%d %H:%M')
    uptime_seconds = psutil.boot_time()
    uptime = time.time() - uptime_seconds
    uptime_str = str(round(uptime/3600, 2)) + ' hours'
    
    wmi_obj = wmi.WMI()

    mem_info_gpu = psutil.virtual_memory()
    mem_total_mem = mem_info_gpu.total
    
    ram_speed = None
    for mem_module in wmi_obj.Win32_PhysicalMemory():
        if ram_speed is None:
            ram_speed = mem_module.Speed
        elif mem_module.Speed > ram_speed:
            ram_speed = mem_module.Speed

    drivesName=[]
    drives = psutil.disk_partitions()
    for drive in drives:
        drivesName.append(str(drive.device))
    drivesName=' '.join(drivesName)
    
    # Combine all the information into a list of strings
    info_list = [f'{os_name} {os_version}',
                 f'{kernel_version}',
                 f'{current_time}',
                 f'{uptime_str}',
                 f'AMD R7 3700X 8c/16t @ 3.6 GHz',
                 f'{round(mem_total_mem/1024**3)} GB @ {round(ram_speed/1000,1)} GHz',
                 f'NVIDIA RTX 2080 SUPER 8 GB',
                 drivesName
                 ]
    
    return info_list

def update_system_info(info_list):
    current_time = time.strftime('%Y-%m-%d %H:%M')
    uptime_seconds = psutil.boot_time()
    uptime = time.time() - uptime_seconds
    uptime_str = str(round(uptime/3600, 2)) + ' hours'
    info_list[2]=f'{current_time}'
    info_list[3]=f'{uptime_str}'

info_list = system_info()

running = True
draw = True

inText = ""
ghostText=""
keyColor=white
palabrasClave=["exit","track",'quit','timer']

def paint():
    screen.fill(black)

    # MAIN TITLE
    font = "./files/mplus-1mn-bold.ttf"
    myfont = pygame.font.Font(font, 22)
    label = myfont.render("    人   I   知   能   や   ボ   ロ   ツ   ト   エ   学", True, cyan)
    screen.blit(label, (70, 2))
    colorGradient=color_gradient(cyan,white,8)
    for i in range(len(colorGradient)):
        write(hankaHash[i],colorGradient[i],5,1+i)
        myfont = pygame.font.Font("./files/JetBrainsMono-Regular.ttf", 24)
    label = myfont.render("     R    O    B    O    T    I    C    S", True, white)
    screen.blit(label, (70, 225))
    

    # SEPARATOR
    pygame.draw.line(screen, grey, (5, 260), (825, 260))
    pygame.draw.line(screen, grey, (415, 270), (415, 360))
    pygame.draw.line(screen, grey, (5, 370), (825, 370))

    # SysFetch
    write('ラタパ:',violetLight,5,10.5,japanese=True)
    write('カーネル:',violetLight,5,11.5,japanese=True)
    write('ゲンザイノジコク:',violetLight,5,12.5,japanese=True)
    write('いろあわせ:',violetLight,5,13.5,japanese=True)

    write(f'{info_list[0]}{info_list[1]}',white,410,10.5,righPad=True)
    write(info_list[2],white,410,11.5,righPad=True)
    write(info_list[3],white,410,12.5,righPad=True)
    # write(info_list[3],white,410,13.5,righPad=True)

    write('プロセッサー:',violetLight,420,10.5,japanese=True)
    write('メモリー:',violetLight,420,11.5,japanese=True)
    write('グラフィックス:',violetLight,420,12.5,japanese=True)
    write('ドライブ:',violetLight,420,13.5,japanese=True)

    write(info_list[4],white,825,10.5,righPad=True)
    write(info_list[5],white,825,11.5,righPad=True)
    write(info_list[6],white,825,12.5,righPad=True)
    write(info_list[7],white,825,13.5,righPad=True)

    # COLOR SCHEME
    startColor=227
    interval=20
    for color in gradient:
        pygame.draw.line(screen, color, (startColor, 354), (startColor+interval, 354),width=5)
        startColor+=interval+3
    write('いろあわせ:',violetLight,5,13.5,japanese=True)
    # INPUT
    colorOnText(" Ghost@HANKA~",black,cyan,0,14.8)
    write(inText,keyColor,135,14.8)
    write(ghostText,grey,135,14.8)
    write('|',greyLigth, 130+10*len(inText),14.8)

    pygame.display.update()
ht=0
while running:
    if pygame.event.peek(pygame.KEYDOWN) or pygame.event.peek(pygame.QUIT) or draw:
        event = pygame.event.wait()
        if draw:
            update_system_info(info_list)
            paint()
            draw = False
        if event.type == pygame.KEYDOWN:
            draw=True
            if len(pygame.key.name(event.key)) == 1:
                inText += pygame.key.name(event.key)
            elif pygame.key.name(event.key) == "backspace":
                inText = inText[:-1]
            elif pygame.key.name(event.key) == "space":
                inText += " "
            elif pygame.key.name(event.key) == "return":
                # todo ejecutar
                if inText=="exit" or inText=='quit':
                    running = False
                elif inText == "track":
                    subprocess.Popen(["python", "runTrack.py"])
                elif inText == "timer":
                    subprocess.Popen(["python", "runTimer.py"])
                inText=''
            elif pygame.key.name(event.key) == "escape":
                inText = ""

            keyColor=white
            if len(inText)>0:
                for clave in palabrasClave:
                    ghostText = ""
                    # todo make most used commands counter
                    if len(inText)<=len(clave) and inText==clave[0:len(inText)]:
                        keyColor=blue
                        for i in range(len(inText)):
                            ghostText+=" "
                        ghostText+=clave[len(inText):]
                        break
                if pygame.key.name(event.key) == "tab":
                    inText = clave
                    ghostText=""
            else:
                ghostText = ""
        elif event.type == pygame.QUIT:
            running = False
    else:
        time.sleep(0.05)  # Add a 10ms delay to reduce CPU load
        ht+=1
        update_system_info(info_list)
        if ht==500:
            draw=True
            ht = 0

with open('files/screen_positions_timer.txt', 'w') as f:
    pass

