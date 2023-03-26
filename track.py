import pygame
from datetime import datetime
from rich.theme import Theme
import json, os, time

pygame.init()

black = pygame.Color("#2E3440")
grey = pygame.Color("#4C566A")
greyLigth = pygame.Color("#D8DEE9")
white = pygame.Color("#ECEFF4")
red = pygame.Color("#BF616A")
orange = pygame.Color("#D08770")
yellow = pygame.Color("#EBCB8B")
green = pygame.Color("#A3BE8C")
violet = pygame.Color("#B48EAD")
violetLight = pygame.Color("#afa4ee")
blueDark = pygame.Color("#5E81AC")
blue = pygame.Color("#81A1C1")
cyan = pygame.Color("#88C0D0")

#TODO get exact coordinate
os.environ['SDL_VIDEO_WINDOW_POS'] = "600,100"
screen = pygame.display.set_mode((500, 600), pygame.HWSURFACE)
pygame.display.set_caption("TRACK")

screen.fill(black)
pygame.display.update()

# initial values
income = 0
living_expenses = 0
leisure_expenses = 0

savings = 0

expected_living = 0
expected_leisure = 0
expected_savings = 0

remaining_living = 0
remaining_leisure = 0
remaining_savings = 0

accommulated_leisure=0
accommulated_savings=0

file_date = ""
last_saved_date=""

mode="nothing"
graphData = [0]
x_axis=[]

# calculate expected expenses
def calculate():
    global expected_living, expected_leisure, expected_savings, remaining_leisure, remaining_living, savings, remaining_savings, accommulated_savings,accommulated_leisure,income,living_expenses,leisure_expenses,last_saved_date,file_date, graphData,x_axis
    
    living_ratio=0.1
    save_ratio=3/5
    
    expected_living = income * living_ratio
    expected_leisure = income * (1-living_ratio) * (1-save_ratio)
    expected_savings = income * (1-living_ratio) * save_ratio

    all_expenses=living_expenses+leisure_expenses
    savings = (income - all_expenses)*save_ratio
    remaining_savings=savings-expected_savings
    
    remaining_living = expected_living-living_expenses
    remaining_leisure = (income - all_expenses)*(1-save_ratio)

    if file_date=="":
        file_date = datetime.now().strftime("%Y-%m")

    # graphData[int(datetime.now().strftime("%m"))]=remaining_leisure+savings
    graphData=[]
    graphData.append(savings+remaining_leisure)
    x_axis=[]
    x_axis.append(datetime.now().strftime("%m"))
    for file in reversed(sorted(os.listdir("./trackFiles"))):
        with open("./trackFiles/"+file,"r") as inf:
            data=json.load(inf)
        if file.split(".")[0]!=datetime.now().strftime("%Y-%m"):
            graphData.append(data["savings"]+data["remaining_leisure"])
            x_axis.append(file.split(".")[0].split("-")[1])

    if len(graphData) > 11:
        graphData=graphData[0:11]
        x_axis=x_axis[0:10]

def getColor(variable,expectedValue):
    outColor=white
    if variable<=0:
        outColor=red
    elif expectedValue*.25 > variable:
        outColor=yellow
    return outColor

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

def write(text,color=white,x=0,line=0,japanese=False,righPad=False):
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

def import_data(read_file_date):
    global income, living_expenses, leisure_expenses, savings
    global expected_living, expected_leisure, expected_savings
    global remaining_living, remaining_leisure, remaining_savings
    global accommulated_leisure, accommulated_savings, file_date, last_saved_date

    # Load data from file
    filename = f"./trackFiles/{read_file_date}.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)

        # Set variable values from data
        income = data["income"]
        living_expenses = data["living_expenses"]
        leisure_expenses = data["leisure_expenses"]
        savings = data["savings"]
        expected_living = data["expected_living"]
        expected_leisure = data["expected_leisure"]
        expected_savings = data["expected_savings"]
        remaining_living = data["remaining_living"]
        remaining_leisure = data["remaining_leisure"]
        remaining_savings = data["remaining_savings"]
        accommulated_leisure = data["accommulated_leisure"]
        accommulated_savings = data["accommulated_savings"]
        file_date = data["file_date"]
        last_saved_date = data["last_saved_date"]

def initiateData():
    global accommulated_leisure,accommulated_savings
    if datetime.now().strftime("%Y-%m")+".json" in os.listdir("./trackFiles"):
        import_data(datetime.now().strftime("%Y-%m"))
    accommulated_leisure=0
    accommulated_savings=0
    for file in sorted(os.listdir("./trackFiles")):
        with open("./trackFiles/"+file,"r") as inf:
            data=json.load(inf)
        if file.split(".")[0]!=datetime.now().strftime("%Y-%m"):
            accommulated_leisure+=data["remaining_leisure"]
            accommulated_savings+=data["savings"]
        for file in sorted(os.listdir("./trackFiles")):
            with open("./trackFiles/"+file,"r") as inf:
                data=json.load(inf)

def scale_values(max_val, length):
    """
    Scales values between max_val and min_val and returns an array of specified length.
    """
    temp=max_val/length
    step=temp
    out=[]
    for i in range(length):
        out.append(round(temp))
        temp+=step
    out.reverse()
    return out

def export_data():    
    # Create dictionary of variables
    global last_saved_date
    last_saved_date=datetime.now().strftime('%d-%m-%Y')

    data = {
        "income": income,
        "living_expenses": living_expenses,
        "leisure_expenses": leisure_expenses,
        "savings": savings,
        "expected_living": expected_living,
        "expected_leisure": expected_leisure,
        "expected_savings": expected_savings,
        "remaining_living": remaining_living,
        "remaining_leisure": remaining_leisure,
        "remaining_savings": remaining_savings,
        "accommulated_leisure": accommulated_leisure,
        "accommulated_savings": accommulated_savings,
        "file_date": file_date,
        "last_saved_date": last_saved_date
    }
    
    # Export data as JSON
    filename = f"./trackFiles/{file_date}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

initiateData()


running = True
draw = True
mode = ""
number = ""

def paint():
    global screen, mode,number,graphData,x_axis
    screen.fill(black)
    # -----------
    # welcome info
    # -----------

    # title
    colorOnText("Ghost@HANKA~",black,cyan,5,0)
    write("細胞間",green,135,0,True)
    write("人工知能内",cyan,190,0,True)
    # current date and last saved date

    pygame.draw.line(screen, grey, (5, 40), (495, 40))

    write(f"{datetime.now().strftime('%d-%m-%Y')} - ",cyan,5,2)
    if last_saved_date!="":
        write('-',cyan,115,2)
        write(last_saved_date,yellow,135,2)
        write('(保存する)',cyan,245,2,True)

    # -----------
    # balance table
    # -----------

    # separator
    pygame.draw.line(screen, grey, (5, 90), (495, 90))

    # title
    write('日常状況',cyan,5,4,True)
    colorOnText(file_date,black,violet,80,4)
    write(':',cyan,152,4)

    # column 1
    write('カテゴリ',blue,25,5.5,True)
    if mode=='income':
        colorOnText('Income',black,cyan,25,7)
    else:
        write('Income',white,25,7)
    if mode=='living':
        colorOnText('Living',black,cyan,25,8)
    else:
        write('Living',white,25,8)
    if mode=='leisure':
        colorOnText('Leisure',black,cyan,25,9)
    else:
        write('Leisure',white,25,9)
    write('Savings',white,25,10)

    # column 2
    write('金額',blue,190,5.5,True,True)
    write(str(round(income,2)),white,190,7,righPad=True)
    write(str(round(living_expenses,2)),white,190,8,righPad=True)
    write(str(round(leisure_expenses,2)),white,190,9,righPad=True)
    write(str(round(savings,2)),white,190,10,righPad=True)

    # column 3
    write('予想',blue,285,5.5,True,True)
    write('番号なし',violet,285,7,True,righPad=True)
    write(str(round(expected_living,2)),white,285,8,righPad=True)
    write(str(round(expected_leisure,2)),white,285,9,righPad=True)
    write(str(round(expected_savings,2)),white,285,10,righPad=True)

    # column 4
    write('残り',blue,380,5.5,True,True)
    remaining=round((income-living_expenses-leisure_expenses),2)
    write(str(remaining),getColor(remaining,income),380,7,righPad=True)
    write(str(round(remaining_living,2)),getColor(remaining_living,expected_living),380,8,righPad=True)
    write(str(round(remaining_leisure,2)),getColor(remaining_leisure,expected_leisure),380,9,righPad=True)
    write('番号なし',violet,380,10,True,righPad=True)

    # column 5
    write('蓄積',blue,475,5.5,True,True)
    write('番号なし',violet,475,7,True,righPad=True)
    write('番号なし',violet,475,8,True,righPad=True)
    write(str(round(accommulated_leisure,2)),white,475,9,righPad=True)
    write(str(round(accommulated_savings,2)),white,475,10,righPad=True)

    # table lines
    pygame.draw.line(screen, greyLigth, (105, 170), (105, 285))
    pygame.draw.line(screen, greyLigth, (200, 170), (200, 285))
    pygame.draw.line(screen, greyLigth, (295, 170), (295, 285))
    pygame.draw.line(screen, greyLigth, (390, 170), (390, 285))
    pygame.draw.line(screen, greyLigth, (20, 170), (480, 170),width=3)

    # -----------
    # accomulated table
    # -----------

    # separator
    pygame.draw.line(screen, grey, (5, 310), (495, 310))

    # title
    write('グラフの保存',cyan,5,13,True)
    write(':',cyan,100,13)

    # graph
    nScaled=7

    # import random
    # for i in range(10):
    #     graphData.append(random.randint(0,max(graphData)))
    # x_axis=['03','02','01','12','11','10','09','08','07','06','05','04','03','02','01']
    # if len(graphData) > 11:
    #     graphData=graphData[0:11]
    #     x_axis=x_axis[0:10]

    y_axis=scale_values(max(graphData),nScaled)

    for j in range(nScaled):
        write(y_axis[j],white,70,14.5+j,righPad=True)
    for i in range(len(x_axis)):
        write(x_axis[i],white,90+40*i,21.5)
        try:
            pygame.draw.line(screen, violetLight, (98+40*i, 535-round(graphData[i]/min(y_axis),1)*23), (98+40*i, 535),width=10)
        except:
            pygame.draw.line(screen, violetLight, (98+40*i, 535-round(graphData[i]/1,1)*23), (98+40*i, 535),width=10)
    pygame.draw.line(screen, grey, (85, 537), (475, 537),width=3)

    # -----------
    # input
    # -----------

    # separator
    pygame.draw.line(screen, grey, (5, 570), (495, 570))

    # instructions
    if mode=='':
        colorOnText(' 選択を選択:',black,cyan,0,23,True)
        write(number,white,105,23)
    elif mode=='income':
        colorOnText(' インプット収入:',black,yellow,0,23,True)
        write(number,white,135,23)
    elif mode=='living':
        colorOnText(' 生活費入力:',black,violet,0,23,True)
        write(number,white,105,23)
    elif mode == 'leisure':
        colorOnText(' 余暇費の入力:',black,violetLight,0,23,True)
        write(number,white,120,23)
    elif mode == 'save':
        colorOnText(' 保存しますか [y/n]:',black,green,0,23,True)
        colorOnText('   ',black,black,165,23,True)
        write(number,white,170,23)
    elif mode=='load':
        colorOnText(' 入力日付 (例: 2022-01):',black,red,0,23,True)
        colorOnText('         ',black,black,200,23,True)
        write(number,white,205,23)

    # input
    

    pygame.display.update()


calculate()
paint()
while running:
    if pygame.event.peek(pygame.KEYDOWN) or pygame.event.peek(pygame.QUIT) or draw:
        event = pygame.event.wait()
        if draw:
            calculate()
            paint()
            draw = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "i":
                mode = "income"
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "v":
                mode = "living"
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "g":
                mode = "leisure"
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "s":
                mode = "save"
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "l":
                mode = "load"
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "c":
                mode = ""
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "backspace":
                number = number[:-1]
                draw = True
            elif pygame.key.name(event.key) == "return":
                if mode=='income':
                    income+=float(number)
                elif mode=='living':
                    living_expenses+=float(number)
                elif mode=='leisure':
                    leisure_expenses+=float(number)
                elif mode=='save' and number=='y':
                    export_data()
                elif mode=='load':
                    import_data(number)
                mode = ""
                number = ""
                draw = True
            elif pygame.key.name(event.key) == "q":
                running=False
            else:
                number += pygame.key.name(event.key)
                draw = True
            # print(pygame.key.name(event.key))
            # pygame.display.update()
        elif event.type == pygame.QUIT:
            running = False
    else:
        time.sleep(0.05)  # Add a 10ms delay to reduce CPU load

