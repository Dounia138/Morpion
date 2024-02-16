# IA en utilisant l'algo MINMAX

import pygame
import sys

pygame.init()


TAILLE_CASE = 80
LARGEUR, HAUTEUR = 4, 4
LARGEUR_ECRAN = LARGEUR * TAILLE_CASE
HAUTEUR_ECRAN = HAUTEUR * TAILLE_CASE
COULEUR_FOND = (255, 255, 255)
COULEUR_LIGNES = (0, 0, 0)
COULEUR_JOUEUR = (0, 0, 255)
COULEUR_IA = (255, 0, 0)

ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Morpion 4x4")


# IA
class IA:
    def __init__(self, symbole):
        self.symbole = symbole
        self.profondeur_max = 3

    def jouer_coup(self, plateau):
        meilleur_score = float("-inf")
        meilleur_coup = None
        alpha = float("-inf")
        beta = float("inf")

        for x in range(LARGEUR):
            for y in range(HAUTEUR):
                if plateau[y][x] == " ":
                    plateau[y][x] = self.symbole
                    score = self.minimax(plateau, False, alpha, beta, 1)
                    plateau[y][x] = " "

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)

                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break

        plateau[meilleur_coup[1]][meilleur_coup[0]] = self.symbole

    def minimax(self, plateau, maximisant, alpha, beta, profondeur):
        if self.verifier_victoire("X", 4):
            return -1
        elif self.verifier_victoire("O", 4):
            return 1
        elif all(cellule != " " for ligne in plateau for cellule in ligne):
            return 0
        elif profondeur == self.profondeur_max:
            return 0

        if maximisant:
            meilleur_score = float("-inf")
            for x in range(LARGEUR):
                for y in range(HAUTEUR):
                    if plateau[y][x] == " ":
                        plateau[y][x] = "O"
                        score = self.minimax(
                            plateau, False, alpha, beta, profondeur + 1
                        )
                        plateau[y][x] = " "
                        meilleur_score = max(score, meilleur_score)
                        alpha = max(alpha, score)
                        if alpha >= beta:
                            return meilleur_score
            return meilleur_score
        else:
            meilleur_score = float("inf")
            for x in range(LARGEUR):
                for y in range(HAUTEUR):
                    if plateau[y][x] == " ":
                        plateau[y][x] = "X"
                        score = self.minimax(plateau, True, alpha, beta, profondeur + 1)
                        plateau[y][x] = " "
                        meilleur_score = min(score, meilleur_score)
                        beta = min(beta, score)
                        if alpha >= beta:
                            return meilleur_score
            return meilleur_score

    def verifier_victoire(self, symbole, alignement):
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

                if all(
                    plateau[j + k][i + alignement - 1 - k] == symbole
                    for k in range(alignement)
                ):
                    return True

        return False


plateau = [[" " for _ in range(LARGEUR)] for _ in range(HAUTEUR)]


def afficher_plateau():
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            pygame.draw.rect(
                ecran,
                COULEUR_FOND,
                (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE),
            )
            pygame.draw.rect(
                ecran,
                COULEUR_LIGNES,
                (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE),
                1,
            )
            if plateau[y][x] == "X":
                pygame.draw.line(
                    ecran,
                    COULEUR_JOUEUR,
                    (x * TAILLE_CASE, y * TAILLE_CASE),
                    ((x + 1) * TAILLE_CASE, (y + 1) * TAILLE_CASE),
                    2,
                )
                pygame.draw.line(
                    ecran,
                    COULEUR_JOUEUR,
                    ((x + 1) * TAILLE_CASE, y * TAILLE_CASE),
                    (x * TAILLE_CASE, (y + 1) * TAILLE_CASE),
                    2,
                )
            elif plateau[y][x] == "O":
                pygame.draw.circle(
                    ecran,
                    COULEUR_IA,
                    (
                        x * TAILLE_CASE + TAILLE_CASE // 2,
                        y * TAILLE_CASE + TAILLE_CASE // 2,
                    ),
                    TAILLE_CASE // 2 - 2,
                )


# Fonction principale
def jouer_morpion():
    tour_joueur = True
    ia = IA("O")

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
                    if plateau[y][x] == " ":
                        plateau[y][x] = "X"
                        tour_joueur = False

        afficher_plateau()
        pygame.display.flip()

        if not tour_joueur:
            ia.jouer_coup(plateau)
            tour_joueur = True

        if ia.verifier_victoire("O", 4):
            print("L'IA a gagné !")
            pygame.quit()
            sys.exit()
        elif ia.verifier_victoire("X", 4):
            print("Félicitations ! Vous avez gagné !")
            pygame.quit()
            sys.exit()
        elif all(cellule != " " for ligne in plateau for cellule in ligne):
            print("Match nul !")
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    jouer_morpion()
