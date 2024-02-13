# IA simplifié (l'IA choisit simplement la première case vide qu'elle trouve sur le plateau et place son symbole dedans)

import pygame
import sys
import random

# Initialiser Pygame
pygame.init()

# Paramètres du jeu
TAILLE_CASE = 40
LARGEUR, HAUTEUR = 16, 16
LARGEUR_ECRAN = LARGEUR * TAILLE_CASE
HAUTEUR_ECRAN = HAUTEUR * TAILLE_CASE
COULEUR_FOND = (255, 255, 255)
COULEUR_LIGNES = (0, 0, 0)
COULEUR_JOUEUR = (0, 0, 255)
COULEUR_IA = (255, 0, 0)

# Initialiser l'écran
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Morpion 16x16")

# Initialiser le plateau
plateau = [[' ' for _ in range(LARGEUR)] for _ in range(HAUTEUR)]

# Fonction pour afficher le plateau
def afficher_plateau():
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            pygame.draw.rect(ecran, COULEUR_FOND, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
            pygame.draw.rect(ecran, COULEUR_LIGNES, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
            if plateau[y][x] == 'X':
                pygame.draw.line(ecran, COULEUR_JOUEUR, (x * TAILLE_CASE, y * TAILLE_CASE), ((x + 1) * TAILLE_CASE, (y + 1) * TAILLE_CASE), 2)
                pygame.draw.line(ecran, COULEUR_JOUEUR, ((x + 1) * TAILLE_CASE, y * TAILLE_CASE), (x * TAILLE_CASE, (y + 1) * TAILLE_CASE), 2)
            elif plateau[y][x] == 'O':
                pygame.draw.circle(ecran, COULEUR_IA, (x * TAILLE_CASE + TAILLE_CASE // 2, y * TAILLE_CASE + TAILLE_CASE // 2), TAILLE_CASE // 2 - 2)

# Fonction principale
def jouer_morpion():
    tour_joueur = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tour_joueur:
                    x, y = event.pos
                    x //= TAILLE_CASE
                    y //= TAILLE_CASE
                    if plateau[y][x] == ' ':
                        plateau[y][x] = 'X'
                        tour_joueur = False

        afficher_plateau()
        pygame.display.flip()

        if not tour_joueur:
            jouer_coup_ia()
            tour_joueur = True

        if verifier_victoire('O', 4):
            print("L'IA a gagné !")
            pygame.quit()
            sys.exit()
        elif verifier_victoire('X', 4):
            print("Félicitations ! Vous avez gagné !")
            pygame.quit()
            sys.exit()
        elif all(cellule != ' ' for ligne in plateau for cellule in ligne):
            print("Match nul !")
            pygame.quit()
            sys.exit()

def jouer_coup_ia():
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if plateau[y][x] == ' ':
                plateau[y][x] = 'O'
                return

def verifier_victoire(symbole, alignement):
    for i in range(LARGEUR):
        for j in range(HAUTEUR - alignement + 1):
            if all(plateau[j + k][i] == symbole for k in range(alignement)):
                return True

    for i in range(LARGEUR - alignement + 1):
        for j in range(HAUTEUR):
            if all(plateau[j][i + k] == symbole for k in range(alignement)):
                return True

    for i in range(LARGEUR - alignement + 1):
        for j in range(HAUTEUR - alignement + 1):
            if all(plateau[j + k][i + k] == symbole for k in range(alignement)):
                return True

            if all(plateau[j + k][i + alignement - 1 - k] == symbole for k in range(alignement)):
                return True

    return False

if __name__ == "__main__":
    jouer_morpion()
