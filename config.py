import pygame
#Initial
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
    "ui_bg": (0, 0, 0),
    "text_2&4": (0, 0, 0),
    "text_rest": (255, 255, 255)
}

# Größe des Spielfeldes
width = 4  #  Felder breit
length = 4  # Felder hoch
size = 100  # 1 Block ist 100 Pixel breit und hoch
size_in_between = 10  #Abstand zwischen allen Blöcken, sowie zwischen block und rand
xextra = 0

yextra = 0
yextra_top = size+size//2+3*size_in_between

xmax = width * size + xextra + size_in_between * (
    width + 1)  # x-Koordinate des rechten Randes
ymax = yextra_top +length * size + yextra + size_in_between * (
    length + 1)  # y-Koordinate des unteneren Randes

homeWidth = 720
homeHeight = 615
overworldWidth = 711
overworldHeight = 550
goWidth=702
goHeight=600
siegWidth=702
siegHeigth=600


running = True

# Spiel
board = []

#UI init
ui_bg_box=pygame.Surface((1,1))
ui_bg_pos= (0,0)

score_txt_box=pygame.Surface((1,1))
score_txt_pos = (0,0)

score_box=pygame.Surface((1,1))
score_pos = (0,0)

level_info_box=pygame.Surface((1,1))
level_info_pos=(0,0)

level_goal_box=pygame.Surface((1,1))
level_goal_pos=(0,0)


#default fuer Richtung. Up-0,Right-1,Down-2,Left-3
direction = -1

#prüft ob Spielfeld verändert wurde
changed = True
score = 0
tilerect = pygame.Rect(size_in_between, size_in_between, size, size)
#default status.
status = "homeInit"
best_level=0

#---------------------------------------------------------
tile_list = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
current_level=0
gamemode=""
maxWertTile = 2048
levelGoalText="TestTest, langer Text und so."
max_moves_per_move = -1

#Dictionary der pygame surfaces der Tiles. wird beim status gameInit -> setuptiles() initialisiert.
tile_surfaces = {}










#Bilder-import-----------------
startscreen_original = pygame.image.load("assets/images/startscreen.jpg")
overworld1_original = pygame.image.load("assets/images/levelselect1.PNG")
overworld2_original = pygame.image.load("assets/images/levelselect2.PNG")
gameover1_original = pygame.image.load("assets/images/gameover1.JPG")
win1_original = pygame.image.load("assets/images/win1.JPG")
lock_original = pygame.image.load("assets/images/lock.png")
face1_original = pygame.image.load("assets/images/face1.png")

bilder = {
    "startscreen": pygame.transform.scale(startscreen_original, (homeWidth, homeHeight)),
    "overworld1":  overworld1_original,
    "overworld2":  overworld2_original,
    "gameover1":   gameover1_original,
    "win1":        win1_original,
    "lock":        lock_original,
    "face1":       face1_original
}



#Mausklick-positionen
r_siz = 49
clickpos_levelselect1 = [
    (pygame.Rect(0 * r_siz + 5, 4 * r_siz + 5, r_siz, r_siz), "Level1"),
    (pygame.Rect(2 * r_siz + 5, 3 * r_siz + 5, r_siz, r_siz), "Level2"),
    (pygame.Rect(4 * r_siz + 5, 5 * r_siz + 5, r_siz, r_siz), "Level3"),
    (pygame.Rect(6 * r_siz + 5, 5 * r_siz + 5, r_siz, r_siz), "Level4"),
    (pygame.Rect(8 * r_siz + 5, 4 * r_siz + 5, r_siz, r_siz), "Level5"),
    (pygame.Rect(7 * r_siz + 5, 2 * r_siz + 5, r_siz, r_siz), "Level6"),
    (pygame.Rect(5 * r_siz + 5, 1 * r_siz + 5, r_siz, r_siz), "Level7"),
    (pygame.Rect(7 * r_siz + 5, 0 * r_siz + 5, r_siz, r_siz), "Level8"),
    (pygame.Rect(10 * r_siz + 5, 0 * r_siz + 5, r_siz, r_siz), "Level9"),
    (pygame.Rect(11 * r_siz + 5, 2 * r_siz + 5, r_siz, r_siz), "Level10"),
    (pygame.Rect(11 * r_siz + 5, 4 * r_siz + 5, r_siz, r_siz), "Level11"),
    (pygame.Rect(11 * r_siz + 5, 6 * r_siz + 5, r_siz, r_siz), "Level12"),
    (pygame.Rect(8 * r_siz + 5, 7 * r_siz + 5, r_siz, r_siz), "Level13"),
    (pygame.Rect(5 * r_siz + 5, 7 * r_siz + 5, r_siz, r_siz), "Level14"),
    (pygame.Rect(3 * r_siz + 5, 9 * r_siz + 5, r_siz, r_siz), "Level15"),
    (pygame.Rect(6 * r_siz + 5, 10 * r_siz + 5, r_siz, r_siz), "Level16"),
    (pygame.Rect(9 * r_siz + 5, 9 * r_siz + 5, r_siz, r_siz), "Level17"),
    (pygame.Rect(11 * r_siz + 5, 9 * r_siz + 5, r_siz, r_siz), "Level18"),
    (pygame.Rect(13 * r_siz + 5, 10 * r_siz + 5, r_siz, r_siz), "Level19"),
    (pygame.Rect(13 * r_siz + 5, 7 * r_siz + 5, r_siz, r_siz), "Level20"),
    (pygame.Rect(14 * r_siz + 3, 10 * r_siz + 4, r_siz,
                 r_siz), "Levelselect2"),
]


#Levels----------------------------------------------------------------------------------------
level1={
    "size"            : 100,
    "size_in_between" : 10,
    "gamemode"        : "maxTile",
    "maxTile"         : 128, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 128 Tile.",
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[0, 0, 2],
                         [0, 0, 0],
                         [2, 0, 0]
                         ]
}

level2={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 256, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 256 Tile.",
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[0, 0, 2, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [2, 0, 0, 0]
                         ]
}

level3={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 512, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 512 Tile.",
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[0, 0, 2, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [2, 0, 0, 0]
                         ]
}

level4={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 1024, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 1024 Tile.",
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[0, 0, 2, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [2, 0, 0, 0]
                         ]
}

level5={
    "size"            : 80,
    "size_in_between" : 8,
    "gamemode"        : "maxTile",
    "maxTile"         : 2048, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 2048 Tile.",
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[0, 0, 2, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [2, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]
                         ]
}

levels={
    1 : level1,
    2 : level2,
    3 : level3,
    4 : level4,
    5 : level5
}


