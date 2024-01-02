import pygame
import timer
#Initial
colors = {
    "0_none": (192, 180, 165),
    "2_player": (238, 228, 218),
    "4_player": (237, 224, 200),
    "8_player": (242, 177, 121),
    "16_player": (245, 149, 99),
    "32_player": (246, 124, 95),
    "64_player": (246, 94, 59),
    "128_player": (237, 207, 114),
    "256_player": (237, 204, 97),
    "512_player": (237, 200, 80),
    "1024_player": (237, 197, 63),
    "2048_player": (237, 194, 46),


    "2_enemy": (218, 250, 220),
    "4_enemy": (176, 229, 179),
    "8_enemy": (137, 242, 121),
    "16_enemy": (122, 223, 91),
    "32_enemy": (86, 213, 85),
    "64_enemy": (44, 173, 43),
    "128_enemy": (139, 183, 230),
    "256_enemy": (113, 173, 238),
    "512_enemy": (80, 148, 220),
    "1024_enemy": (43, 128, 217),
    "2048_enemy": (18, 121, 230),

    "-1_wall": (110, 109, 108),
    "-1_duplicate":(0,0,0),
    "-1_halve":(0,0,0),


    "bg": (187, 173, 160),
    "ui_bg": (0, 0, 0),
    "text_2&4": (0, 0, 0),
    "text_rest": (255, 255, 255)
}
#timers
timer_set=False


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
siegHeight=600


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
best_level=15


#---------------------------------------------------------
tile_list = ["0_none", "2_player", "4_player", "8_player", "16_player", "32_player", "64_player", "128_player", "256_player", "512_player", "1024_player", "2048_player",
                       "2_enemy", "4_enemy", "8_enemy", "16_enemy", "32_enemy", "64_enemy", "128_enemy", "256_enemy", "512_enemy", "1024_enemy", "2048_enemy",
             "-1_wall", "-1_duplicate"]
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
face_big_enemy_original = pygame.image.load("assets/images/face_big_enemy.png")

bilder = {
    "startscreen": pygame.transform.scale(startscreen_original, (homeWidth, homeHeight)),
    "overworld1":  overworld1_original,
    "overworld2":  overworld2_original,
    "gameover1":   gameover1_original,
    "win1":        win1_original,
    "lock":        lock_original,
    "face1":       face1_original,
    "face_enemy":  face_big_enemy_original
}



#Mausklick-positionen
r_siz = 49
clickpos_levelselect1 = [
    (pygame.Rect(0 * r_siz + 5, 4 * r_siz + 5, r_siz, r_siz), "Level01"),
    (pygame.Rect(2 * r_siz + 5, 3 * r_siz + 5, r_siz, r_siz), "Level02"),
    (pygame.Rect(4 * r_siz + 5, 5 * r_siz + 5, r_siz, r_siz), "Level03"),
    (pygame.Rect(6 * r_siz + 5, 5 * r_siz + 5, r_siz, r_siz), "Level04"),
    (pygame.Rect(8 * r_siz + 5, 4 * r_siz + 5, r_siz, r_siz), "Level05"),
    (pygame.Rect(7 * r_siz + 5, 2 * r_siz + 5, r_siz, r_siz), "Level06"),
    (pygame.Rect(5 * r_siz + 5, 1 * r_siz + 5, r_siz, r_siz), "Level07"),
    (pygame.Rect(7 * r_siz + 5, 0 * r_siz + 5, r_siz, r_siz), "Level08"),
    (pygame.Rect(10 * r_siz + 5, 0 * r_siz + 5, r_siz, r_siz), "Level09"),
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


template_tile_dic={
    "tile_numb" : 0,
    "fraction"  : "none",
    "type"      : "none",

}
#Levels----------------------------------------------------------------------------------------
level01={
    "size"            : 100,
    "size_in_between" : 10,
    "gamemode"        : "maxTile",
    "maxTile"         : 128, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 128 Tile.",
    "chance_enemy_spawn": 0,
    "chance_duplicate_spawn": 0,
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand

    "board"           : [[{}, {}, {}],
                         [{}, {}, {}],
                         [{}, {}, {}]
                         ],
    "preset_tiles"    : {(2,0):{"tile_numb" : 2,
                                "fraction"  : "player",
                                "type"      : "none"},

                         (0,2):{"tile_numb" : 4,
                                "fraction"  : "player",
                                "type"      : "none"}
                         }
}

level02={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 256, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 256 Tile.",
    "chance_enemy_spawn": 0,
    "chance_duplicate_spawn": 0,
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[{}, {}, {}, {}],
                         [{}, {}, {}, {}],
                         [{}, {}, {}, {}],
                         [{}, {}, {}, {}]
                         ],
    "preset_tiles"    : {(2,0):{"tile_numb" : 2,
                                "fraction"  : "player",
                                "type"      : "none"},
                         (0,3):{"tile_numb" : 4,
                                "fraction"  : "player",
                                "type"      : "none"}
                             }
}

level03={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 512, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 512 Tile.",
    "chance_enemy_spawn": 0,
    "chance_duplicate_spawn": 0,
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[{}, {}, {}, {}],
                         [{}, {}, {}, {}],
                         [{}, {}, {}, {}],
                         [{}, {}, {}, {}]
                         ],
    "preset_tiles"    : {(2,0):{"tile_numb" : 2,
                                "fraction"  : "player",
                                "type"      : "none"},
                         (0,3):{"tile_numb" : 2,
                                "fraction"  : "player",
                                "type"      : "none"}
                             }
}

level04={
    "size"            : 90,
    "size_in_between" : 9,
    "gamemode"        : "maxTile",
    "maxTile"         : 1024, #only, if gamemode == "maxTile
    "level_text"      : "Erreiche das 1024 Tile.",
    "chance_enemy_spawn": 0,
    "chance_duplicate_spawn": 0,
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[{}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}]
                         ],
    "preset_tiles": {(2, 0): {"tile_numb": 2,
                              "fraction": "player",
                              "type"      : "none"},
                     (1, 3): {"tile_numb": 2,
                              "fraction": "player",
                              "type"      : "none"}
                     }
}

level05={
    "size"            : 80,
    "size_in_between" : 8,
    "gamemode"        : "maxTile",
    "maxTile"         : 1024, #only, if gamemode == "maxTile"
    "level_text"      : "Erreiche das 1024 Tile. Achtung: Gegner!",
    "chance_enemy_spawn":30,
    "chance_duplicate_spawn": 0,
    "max_moves_per_move"    : 1, #-1 ist default -> bis zum Rand
    "board"           : [[{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}]
                         ],
    "preset_tiles": {(3, 0): {"tile_numb": 4,
                              "fraction": "player",
                              "type"      : "none"},
                     (1, 3): {"tile_numb": 2,
                              "fraction": "player",
                              "type"      : "none"},
                     (3, 3): {"tile_numb": 4,
                              "fraction": "enemy",
                              "type"      : "none"}
                     }

}


level06={
    "size"            : 80,
    "size_in_between" : 8,
    "gamemode"        : "maxTile",
    "maxTile"         : 1024, #only, if gamemode == "maxTile"
    "level_text"      : "Erreiche das 1024 Tile. Achtung: Wände!",
    "chance_enemy_spawn":25,
    "chance_duplicate_spawn":1,
    "max_moves_per_move": 1, #-1 ist default -> bis zum Rand
    "board"           : [[{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}],
                         [{}, {}, {}, {}, {}, {}]
                         ],
    "preset_tiles": {(4, 0): {"tile_numb": 4,
                              "fraction": "player",
                              "type"      : "none"},
                     (5, 2): {"tile_numb": 2,
                              "fraction": "player",
                              "type"      : "none"},
                     (3, 1): {"tile_numb": 4,
                              "fraction": "enemy",
                              "type"      : "none"},

                     (4, 2): {"tile_numb": -1,
                              "fraction": "none",
                              "type":"wall"},
                     (4, 3): {"tile_numb": -1,
                              "fraction": "none",
                              "type": "wall"},
                     (5, 3): {"tile_numb": -1,
                              "fraction": "none",
                              "type": "wall"},
                     (0,1): {"tile_numb": -1,
                              "fraction": "none",
                              "type": "duplicate"}
                     }
}

levels={
    1 : level01,
    2 : level02,
    3 : level03,
    4 : level04,
    5 : level05,
    6 : level06
}



