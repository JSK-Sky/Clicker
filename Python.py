import pygame
import os
import json

from math import sqrt

def charger_sauvegarde():
    if os.path.exists("sauvegarde.json"):
        with open("sauvegarde.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def sauvegarder_sauvegarde(donnees):
    with open("sauvegarde.json", "w") as file:
        json.dump(donnees, file, indent=4)

sauvegarde = charger_sauvegarde()

score = sauvegarde.get("score", 0)
scoreTotal = sauvegarde.get("scoreTotal", 0)
scoreMax = sauvegarde.get("scoreMax", 0)
nombreClick = sauvegarde.get("nombreClick", 0)
scoreParClick = sauvegarde.get("scoreParClick", 1)
scoreParSecond = sauvegarde.get("scoreParSecond", 0)
gameTime = sauvegarde.get("gameTime", 0)

upgrade1Nombre = sauvegarde.get("upgrade1Nombre", 0)
upgrade1Prix = sauvegarde.get("upgrade1Prix", 50)
upgrade2Nombre = sauvegarde.get("upgrade2Nombre", 0)
upgrade2Prix = sauvegarde.get("upgrade2Prix", 200)
upgrade3Nombre = sauvegarde.get("upgrade3Nombre", 0)
upgrade3Prix = sauvegarde.get("upgrade3Prix", 500)
upgrade4Nombre = sauvegarde.get("upgrade4Nombre", 0)
upgrade4Prix = sauvegarde.get("upgrade4Prix", 1000)
upgrade5Nombre = sauvegarde.get("upgrade5Nombre", 0)
upgrade5Prix = sauvegarde.get("upgrade5Prix", 2500)
upgrade6Nombre = sauvegarde.get("upgrade6Nombre", 0)
upgrade6Prix = sauvegarde.get("upgrade6Prix", 5000)

pygame.init()
font = pygame.font.Font(None, 25)
if upgrade4Nombre > 0:
    screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
else:
    screen = pygame.display.set_mode((1200, 700))
x, y = screen.get_size()
clock = pygame.time.Clock()

dossier = r"frames"
fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]

last_update_time = pygame.time.get_ticks()

actualImage = 0
running = True

clickSound = pygame.mixer.Sound("sons/ClickSound.WAV")
clickSound.set_volume(0.1)

buySound = pygame.mixer.Sound("sons/BuySound.WAV")
buySound.set_volume(0.5)

backgroundMusic = pygame.mixer.Sound("sons/Music_BackGround.MP3")
backgroundMusic.set_volume(0.05)

exit_bouton = pygame.Rect(x-20-round(x/1920*100), 20, round(x/1920*100), round(x/1920*100))

upgradeZones = {}

note_y_offset = 0
note_jump_strength = 15
note_gravity = 2 

def afficher_texte(Surface, texte, font, x, y, couleur=(255, 255, 255)):
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    Surface.blit(texte_surface, texte_rect)

def distance(x1,y1,x2,y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

def draw_update_button(Surface, Nom, Nombre, Price, x, y, updateId):
    rectOrange = pygame.Rect(x, y, 300, 50)
    rectBlack = pygame.Rect(x-3, y-3, 306, 56)
    anglesOrange = 10
    anglesBlack = 13
    pygame.draw.rect(Surface, "black", rectBlack, width=0, border_radius=0, border_top_left_radius=anglesBlack, border_top_right_radius=anglesBlack, border_bottom_left_radius=anglesBlack, border_bottom_right_radius=anglesBlack)
    pygame.draw.rect(Surface, "orange", rectOrange, width=0, border_radius=0, border_top_left_radius=anglesOrange, border_top_right_radius=anglesOrange, border_bottom_left_radius=anglesOrange, border_bottom_right_radius=anglesOrange)
    afficher_texte(screen, f"{Nom} : {Nombre} ({Price}$)", font, x+150, y+25)
    
    upgradeZones[updateId] = rectOrange

while running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            x, y = event.w, event.h
            screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)
            exit_bouton = pygame.Rect(x-20-round(x/1920*100), 20, round(x/1920*100), round(x/1920*100))
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_bouton.collidepoint(event.pos):
                running = False
                if upgrade1Nombre > 0:
                    clickSound.play()
            if distance(event.pos[0],event.pos[1],x/2,y/2) < (round(x/1920*256)/2)*1.35:
                nombreClick += 1
                score+=scoreParClick
                scoreTotal+=scoreParClick
                if upgrade5Nombre > 0:
                    note_y_offset = -note_jump_strength
                if upgrade1Nombre > 0:
                    clickSound.play()
            for i in range(len(upgradeZones)):
                if upgradeZones[i].collidepoint(event.pos):
                    if i == 0 and score >= upgrade1Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade1Prix
                        upgrade1Prix = round(upgrade1Prix*1.25)
                        upgrade1Nombre += 1
                        scoreParSecond += 2
                    if i == 1 and score >= upgrade2Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade2Prix
                        upgrade2Prix = round(upgrade2Prix*1.3)
                        upgrade2Nombre += 1
                        scoreParSecond += 5
                    if i == 2 and score >= upgrade3Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade3Prix
                        upgrade3Prix = round(upgrade3Prix*2)
                        upgrade3Nombre += 1
                        scoreParClick += 4
                    if i == 3 and score >= upgrade4Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade4Prix
                        upgrade4Prix = round(upgrade4Prix*1.1)
                        if upgrade4Nombre == 0:
                            screen = pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
                        upgrade4Nombre += 1
                        scoreParSecond += 10
                    if i == 4 and score >= upgrade5Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade5Prix
                        upgrade5Prix = round(upgrade5Prix*1.1)
                        upgrade5Nombre += 1
                        scoreParSecond += 50
                    if i == 5 and score >= upgrade6Prix:
                        if upgrade1Nombre > 0:
                            buySound.play()
                        score -= upgrade6Prix
                        upgrade6Prix = round(upgrade6Prix*1.1)
                        upgrade6Nombre += 1
                        scoreParClick += 20
    if upgrade2Nombre > 0 and backgroundMusic.get_num_channels() == 0:
        backgroundMusic.play(-1)
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time >= 1000:
        score += scoreParSecond
        gameTime += 1
        scoreTotal += scoreParSecond
        last_update_time = current_time
    if score > scoreMax:
        scoreMax = score
    if upgrade3Nombre > 0:
        image_path = os.path.join(dossier, fichiers[actualImage])
    else:
        image_path = "frames/frame_0.PNG"
    BackGroundImage = pygame.image.load(image_path)
    BackGroundImage = pygame.transform.scale(BackGroundImage, (x, y))
    screen.fill((0, 0, 0))
    screen.blit(BackGroundImage, (0, 0))
    
    
    quitGameImage = pygame.image.load("images/Quit_game.PNG")
    quitGameImage = pygame.transform.scale(quitGameImage, (round(x/1920*100), round(x/1920*100)))
    screen.blit(quitGameImage, (x-20-round(x/1920*100), 20))
    
    pygame.draw.circle(screen, "black", (x/2,y/2), (round(x/1920*256)/2)*1.35)
    pygame.draw.circle(screen, "orange", (x/2,y/2), (round(x/1920*256)/2)*1.3)
    
    afficher_texte(screen, f"Score: {score}", font, x/2, y/2 + round(x/1920*256)/2 + round(x/25))
    afficher_texte(screen, f"Score par seconde: {scoreParSecond}", font, x/2, y/2 + round(x/1920*256)/2 + round(x/25) + 20)
    afficher_texte(screen, f"Score par click: {scoreParClick}", font, x/2, y/2 + (round(x/1920*256)/2) + round(x/25) + 40)
        
    musicNoteImage = pygame.image.load("images/Music_Note.PNG")
    musicNoteImage = pygame.transform.scale(musicNoteImage, (round(x/1920*256), round(x/1920*256)))
    note_y_offset += note_gravity
    note_y_offset = min(0, note_y_offset)
    screen.blit(musicNoteImage, (x / 2 - (round(x / 1920 * 256) / 2), y / 2 - (round(x / 1920 * 256) / 2) + note_y_offset))
    
    if upgrade6Nombre > 0:
        rect_white = pygame.Rect(x - 420, y - 100 - y/2, 400, 200)
        rect_black = pygame.Rect(x - 420 - 3, y - 100 - y/2 - 3, 406, 206)
        pygame.draw.rect(screen, (0, 0, 0), rect_black, border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), rect_white, border_radius=15)
        
        font_titre = pygame.font.Font(None, 30)
        afficher_texte(screen, "Statistiques", font_titre, x - 420 + 400 / 2, y - 70 - y/2, (0, 0, 0))
        
        afficher_texte(screen, f"Score total : {scoreTotal}", font, x - 220, y -30 - y/2, (0, 0, 0))        
        afficher_texte(screen, f"Score max : {scoreMax}", font, x - 220, y - y/2, (0, 0, 0))        
        afficher_texte(screen, f"Nombre de click : {nombreClick}", font, x - 220, y + 30 - y/2, (0, 0, 0))
        
        hours = gameTime // 3600
        minutes = (gameTime % 3600) // 60
        seconds = gameTime % 60
        afficher_texte(screen, f"Temps de jeu : {hours}h {minutes}m {seconds}s", font, x - 220, y + 60 - y/2, (0, 0, 0))

    
    draw_update_button(screen, "(+2 Score/s) Curseur", upgrade1Nombre, upgrade1Prix, 75, 100, 0)
    if upgrade1Nombre > 3:
        draw_update_button(screen, "(+5 Score/s) Musique", upgrade2Nombre, upgrade2Prix, 75, 175, 1)
    if upgrade2Nombre > 3:
        draw_update_button(screen, "(+4 Score/click) Fond", upgrade3Nombre, upgrade3Prix, 75, 250, 2)
    if upgrade3Nombre > 3:
        draw_update_button(screen, "(+10 Score/s) Fenêtre", upgrade4Nombre, upgrade4Prix, 75, 325, 3)
    if upgrade4Nombre > 3:
        draw_update_button(screen, "(+50 Score/s) Note", upgrade5Nombre, upgrade5Prix, 75, 400, 4)
    if upgrade5Nombre > 3:
        draw_update_button(screen, "(+20 Score/click) Stats", upgrade6Nombre, upgrade6Prix, 75, 475, 5)
    
    
    pygame.display.flip()
    actualImage += 1
    if actualImage >= len(fichiers):
        actualImage = 0
        x, y = screen.get_size()

    
sauvegarde["score"] = score
sauvegarde["scoreTotal"] = scoreTotal
sauvegarde["scoreMax"] = scoreMax
sauvegarde["nombreClick"] = nombreClick
sauvegarde["scoreParClick"] = scoreParClick
sauvegarde["scoreParSecond"] = scoreParSecond
sauvegarde["gameTime"] = gameTime

sauvegarde["upgrade1Nombre"] = upgrade1Nombre
sauvegarde["upgrade1Prix"] = upgrade1Prix
sauvegarde["upgrade2Nombre"] = upgrade2Nombre
sauvegarde["upgrade2Prix"] = upgrade2Prix
sauvegarde["upgrade3Nombre"] = upgrade3Nombre
sauvegarde["upgrade3Prix"] = upgrade3Prix
sauvegarde["upgrade4Nombre"] = upgrade4Nombre
sauvegarde["upgrade4Prix"] = upgrade4Prix
sauvegarde["upgrade5Nombre"] = upgrade5Nombre
sauvegarde["upgrade5Prix"] = upgrade5Prix
sauvegarde["upgrade6Nombre"] = upgrade6Nombre
sauvegarde["upgradePrix"] = upgrade6Prix

sauvegarder_sauvegarde(sauvegarde)
pygame.quit()
