#Farben
import pygame


colors = {
    0: (192, 180, 165),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "bg": (187, 173, 160),
    "text_2&4":(0,0,0),
    "text_rest":(255,255,255)
}
tile_surfaces={}
tile_list=[0,2,4,8,16,32,64,128,256,512,1024,2048]

# Größe des Spielfeldes
width = 4 #  Felder breit
length = 4 # Felder hoch
size = 100 # 1 Block ist 100 Pixel breit und hoch
size_in_between=10#Abstand zwischen allen Blöcken, sowie zwischen block und rand
xextra = 0
yextra = 100
xmax = width * size + xextra+size_in_between*(width+1)  # x-Koordinate des rechten Randes
ymax = length * size + yextra+size_in_between*(length+1)  # y-Koordinate des unteneren Randes

homeHeight= 615
homeWidth = 720
overworldHeight=550
overworldWidth=711



running = True

# Spiel
board = []

#default fuer Richtung. Up-0,Right-1,Down-2,Left-3
direction=-1
#prüft ob Spielfeld verändert wurde
changed=True

score=0
highscore=0

ui_down_rect=pygame.Rect(0,length * size+size_in_between*(length+1),width * size + xextra+size_in_between*(width+1),yextra)

tilerect = pygame.Rect(size_in_between,size_in_between,size,size)

status="homeInit"


startscreen_original=pygame.image.load("assets/images/startscreen.jpg")
overworld1_original=pygame.image.load("assets/images/levelselect1.PNG")
overworld2_original=pygame.image.load("assets/images/levelselect2.PNG")

bilder={"startscreen" : pygame.transform.scale(startscreen_original, (homeWidth, homeHeight)),
        "overworld1":overworld1_original,
        "overworld2":overworld2_original
        }



maxWertTile=2048
r_siz=48



clck_pos_lvl_11 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level11")
clck_pos_lvl_12 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level12")
clck_pos_lvl_13 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level13")
clck_pos_lvl_14 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level14")
clck_pos_lvl_15 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level15")
clck_pos_lvl_16 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level16")
clck_pos_lvl_17 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level17")
clck_pos_lvl_18 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level18")
clck_pos_lvl_19 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level19")
clck_pos_lvl_20 = (pygame.Rect(5,4*r_siz+5,r_siz,r_siz),"Level20")

lvls1=[ (pygame.Rect(0*r_siz+5,4*r_siz+5,r_siz,r_siz),"Level1"),
        (pygame.Rect(2*r_siz+5,3*r_siz+5,r_siz,r_siz),"Level2"),
        (pygame.Rect(4*r_siz+5,5*r_siz+5,r_siz,r_siz),"Level3"),
        (pygame.Rect(6*r_siz+5,5*r_siz+5,r_siz,r_siz),"Level4"),
        (pygame.Rect(8*r_siz+5,4*r_siz+5,r_siz,r_siz),"Level5"),
        (pygame.Rect(7*r_siz+5,2*r_siz+5,r_siz,r_siz),"Level6"),

        (pygame.Rect(5*r_siz + 5, 1 * r_siz + 5, r_siz, r_siz), "Level7"),
        (pygame.Rect(2*r_siz + 5, 3 * r_siz + 5, r_siz, r_siz), "Level8"),
        (pygame.Rect(2*r_siz + 5, 3 * r_siz + 5, r_siz, r_siz), "Level9"),
        (pygame.Rect(2*r_siz + 5, 3 * r_siz + 5, r_siz, r_siz), "Level10")
        ]

lvls2=[]