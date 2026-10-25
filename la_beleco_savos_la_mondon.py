#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
la_beleco_savos_la_mondon.py — « La beleco savos la mondon »
=============================================================

OBJECTIF
--------
Une œuvre art-science en trois zones (gauche — centre — droite) qui montre
E8 comme le PONT RÊVÉ entre les deux grandes théories de la physique du
XXe siècle :

  - la MÉCANIQUE QUANTIQUE (le monde de l'infiniment petit — particules,
    niveaux d'énergie discrets, incertitude) ;
  - la RELATIVITÉ GÉNÉRALE (le monde de l'infiniment grand — l'espace-temps
    courbé par la masse, la gravité).

Au centre, le mandala des 240 racines de E8 (voir mandala_e8/mandala.py
pour la construction et les vérifications mathématiques complètes,
reproduites ici de façon autonome) est présenté avec son centre
volontairement VIDE, fidèle à la géométrie réelle du système de racines :
dans la théorie des cordes HÉTÉROTIQUE, le groupe de jauge E8 × E8
apparaît naturellement comme la symétrie interne des 16 dimensions
internes compactifiées, et c'est l'une des rares pistes connues qui tente
de marier la mécanique quantique (les cordes vibrent selon les règles de
la mécanique quantique) et la relativité générale (la théorie des cordes
contient toujours un graviton, la particule de la gravité, dans son
spectre). Le lien entre le mandala et les panneaux latéraux reste, lui,
stylisé en corde vibrante — un seul fil continu et
symétrique (voir dessiner_demi_fil) : c'est là que le motif de la corde
subsiste dans l'image, comme liaison plutôt que comme occupant du centre.

CADRAGE HONNÊTE — ceci est une QUÊTE, pas un fait établi
----------------------------------------------------------
Réconcilier la mécanique quantique et la relativité générale est le plus
grand problème non résolu de la physique théorique. La théorie des cordes
hétérotique (E8 × E8) est l'une des pistes rêvées vers cette unification —
mathématiquement d'une grande beauté (E8 est le plus grand groupe de Lie
exceptionnel simple, et sa structure impose des contraintes extrêmement
fortes et élégantes), mais à ce jour AUCUNE prédiction de la théorie des
cordes n'a été confirmée expérimentalement. Le titre de cette œuvre,
« La beleco savos la mondon » (« La beauté sauvera le monde », en
espéranto — citation de Dostoïevski, prêtée au prince Mychkine dans
L'Idiot), est donc à prendre comme un vœu, une espérance esthétique, pas
comme une thèse scientifique établie. Le cartouche en bas de l'image le
rappelle explicitement, en anglais, pour quiconque regarde l'image sans
avoir lu ce docstring.

CONTENU
-------
  - CENTRE : les 240 racines de E8, projetées sur le plan de Coxeter
    (construction exacte, vérifiée par assertions : 240 racines, norme² =
    2). Le centre de la projection reste VIDE, fidèle à la géométrie
    réelle : aucune racine n'occupe le milieu, seuls des anneaux
    concentriques de racines équidistantes entourent un centre nu.
  - GAUCHE : la mécanique quantique rendue reconnaissable SANS AUCUN TEXTE
    — le pictogramme universel de l'atome (noyau + 3 orbites elliptiques
    identiques, tournées de 60° et qui se croisent, avec des électrons),
    et quelques quanta lumineux discrets dispersés autour.
  - DROITE : la relativité générale rendue reconnaissable SANS AUCUN TEXTE
    — la grille d'espace-temps déformée radialement autour d'une masse
    sphérique en son centre exact (voir deplacement_radial : chaque nœud
    de la grille est tiré vers la masse d'une quantité qui ne dépend que
    de sa distance à elle, identique dans toutes les directions), une
    planète en orbite excentrique, et un rayon de lumière qui se courbe en
    passant près de la masse (la lentille gravitationnelle, l'une des
    preuves historiques de la théorie — l'éclipse de 1919).
  - PONTS : deux liaisons stylisées en cordes vibrantes (enveloppe en
    sinus, nulle aux deux extrémités — comme une corde de guitare
    fixée aux deux bouts) relient le bord du mandala central au cœur de
    chacun des deux panneaux latéraux.

Le seul texte affiché SUR l'image est le titre en espéranto, en Zapfino
(calligraphie fluide) : les deux physiques doivent être reconnaissables
par l'image seule, sans aucune étiquette (voir README.md pour le cadrage
"quête, pas fait établi"). La palette couvre
maintenant tout le spectre visible (mandala en dégradé "hsv", points avec
un léger glow), chaque panneau reprenant le même accent or vif pour son
objet central (noyau, masse), en écho au centre — et le fil vibrant qui
relie le mandala aux deux panneaux en garde lui aussi un léger reflet
(voir COULEUR_FIL_CENTRE). Ce docstring et les commentaires du code sont
en français.
"""

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
from itertools import combinations, product


# ============================================================================
# 1. CONFIGURATION
# ============================================================================

DOSSIER_SORTIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
FICHIER_PNG = os.path.join(DOSSIER_SORTIE, "Sophia_MAI_artwork.png")
FICHIER_SVG = os.path.join(DOSSIER_SORTIE, "Sophia_MAI_artwork.svg")

DPI = 300
LARGEUR_POUCES = 18.71   # 18.71 x 300 = 5613 px  (ratio A-series 1,414 = sqrt(2), A3 paysage)
HAUTEUR_POUCES = 13.23   # 13.23 x 300 = 3969 px

# --- Couleurs — « tout le spectre » : palette vive et saturée,
# qui couvre l'ensemble du spectre visible (y compris le vert — la
# vert), avec le mandala
# central en dégradé arc-en-ciel complet (colormap cyclique "hsv") et un
# léger effet de glow sur ses 240 points (voir dessiner_panneau_e8). Le
# noyau (gauche) et la masse (droite) gardent volontairement le même
# accent or vif, pour que l'œil comprenne qu'ils jouent le même rôle dans
# leur panneau respectif — le centre du mandala E8, lui, reste vide (voir
# dessiner_panneau_e8). -------------------------------------------------------
COULEUR_FOND = "#050510"
COULEUR_TITRE = "#F4F4FF"

PALETTE_MANDALA = "hsv"                 # cyclique, tout le spectre (rouge -> jaune -> vert -> cyan -> bleu -> magenta)
COULEUR_ACCENT_CENTRAL = "#FFC400"      # or vif — noyau et masse : le même "rôle" dans leurs panneaux
COULEUR_ARETES_MANDALA = "#D6D6FF"

COULEUR_NOYAU = COULEUR_ACCENT_CENTRAL
COULEUR_ORBITES = "#8A3FFC"             # violet vif, orbites elliptiques de l'atome
COULEUR_ELECTRON = "#FF1464"            # magenta-rouge vif, électrons

COULEUR_MASSE = COULEUR_ACCENT_CENTRAL
COULEUR_GRILLE_ESPACE = "#1E6FFF"       # bleu vif, grille d'espace-temps
COULEUR_PLANETE = "#00E676"             # vert vif, corps en orbite
COULEUR_LUMIERE = "#FFEE00"             # jaune vif, rayon de lumière courbé (lentille gravitationnelle)

# --- Le fil vibrant central (voir section 7) : un seul dégradé, partagé
# par les deux moitiés (gauche et droite), de l'accent or (près du centre)
# vers la teinte des arêtes du mandala (près des bords) — c'est l'« écho »
# discret de la couleur du centre dans les deux liens. -----------------------
COULEUR_FIL_CENTRE = tuple(0.55 * np.array(to_rgb(COULEUR_ACCENT_CENTRAL))
                            + 0.45 * np.array(to_rgb(COULEUR_ARETES_MANDALA)))
COULEUR_FIL_BORD = COULEUR_ARETES_MANDALA

# --- Police du titre — le seul texte de l'image : une écriture calligraphiée,
# plus « poétique » que la police par défaut, cohérente avec la citation
# de Dostoïevski qu'il porte. ------------------------------------------------
POLICE_TITRE = "Zapfino"


# ============================================================================
# 2. CONSTRUCTION EXACTE DES 240 RACINES DE E8 (autonome, cf. mandala_e8)
# ============================================================================

def generer_racines_e8():
    """
    Génère les 240 racines du système de racines E8, en dimension 8 :
      - 112 racines ±e_i ± e_j (i < j) ;
      - 128 racines (±1/2)^8 à nombre PAIR de signes moins.
    Retourne un tableau numpy (240, 8). Reprise directe de la construction
    de mandala_e8/mandala.py, pour que ce projet reste autonome.
    """
    racines = []
    for i, j in combinations(range(8), 2):
        for si, sj in product([1.0, -1.0], repeat=2):
            v = np.zeros(8)
            v[i], v[j] = si, sj
            racines.append(v)
    for signes in product([1.0, -1.0], repeat=8):
        if signes.count(-1.0) % 2 == 0:
            racines.append(0.5 * np.array(signes))
    return np.array(racines)


def verifier_racines(racines):
    """Vérifie : exactement 240 racines en dimension 8, toutes de norme² = 2."""
    assert racines.shape == (240, 8), f"Attendu 240 racines en dim 8, obtenu {racines.shape}"
    normes2 = np.sum(racines ** 2, axis=1)
    assert np.allclose(normes2, 2.0, atol=1e-9), "Toutes les racines doivent avoir une norme² = 2"


def racines_simples_e8():
    """Les 8 racines simples de E8 (convention de Bourbaki) — sert à construire un élément de Coxeter."""
    e = np.eye(8)
    a1 = 0.5 * (e[0] - e[1] - e[2] - e[3] - e[4] - e[5] - e[6] + e[7])
    a2 = e[0] + e[1]
    a3 = e[1] - e[0]
    a4 = e[2] - e[1]
    a5 = e[3] - e[2]
    a6 = e[4] - e[3]
    a7 = e[5] - e[4]
    a8 = e[6] - e[5]
    return np.array([a1, a2, a3, a4, a5, a6, a7, a8])


def element_coxeter(racines_simples):
    """Produit des 8 réflexions associées aux racines simples : un élément de Coxeter de E8."""
    c = np.eye(8)
    for alpha in racines_simples:
        c = (np.eye(8) - np.outer(alpha, alpha)) @ c
    return c


def base_plan_coxeter(c, h=30):
    """Base orthonormée (u, v) du plan de Coxeter, sur lequel c agit comme une rotation d'angle 2π/h."""
    valeurs_propres, vecteurs_propres = np.linalg.eig(c)
    cible = np.exp(2j * np.pi / h)
    idx = np.argmin(np.abs(valeurs_propres - cible))
    vecteur = vecteurs_propres[:, idx]
    u = np.real(vecteur)
    v = np.imag(vecteur)
    u = u / np.linalg.norm(u)
    v = v - np.dot(v, u) * u
    v = v / np.linalg.norm(v)
    return u, v


def projeter_sur_plan(racines, u, v):
    """Projection des racines 8D sur le plan (u, v) -> coordonnées (x, y)."""
    return racines @ u, racines @ v


def calculer_aretes_courtes(racines):
    """Paires de racines à distance minimale (√2, les 56 voisines de chaque racine) — réseau fin du mandala."""
    gram = racines @ racines.T
    normes2 = np.sum(racines ** 2, axis=1)
    dist2 = np.clip(normes2[:, None] + normes2[None, :] - 2 * gram, 0, None)
    distances = np.sqrt(dist2)
    distance_min = distances[distances > 1e-9].min()
    masque = np.isclose(distances, distance_min, atol=1e-6)
    i_idx, j_idx = np.where(np.triu(masque, k=1))
    return i_idx, j_idx


# ============================================================================
# 3. PETITS UTILITAIRES DE RENDU (lueur, glow) — réutilisés dans les 3 panneaux
# ============================================================================

def dessiner_lueur(ax, x, y, rayon, couleur, zorder=5, n_couches=5, alpha_max=0.16):
    """Un point lumineux : halo dégradé (plusieurs disques semi-transparents) + cœur plein."""
    for k in range(n_couches, 0, -1):
        r = rayon * k / n_couches
        a = alpha_max * (1 - k / (n_couches + 1))
        ax.add_patch(Circle((x, y), r, color=couleur, alpha=a, linewidth=0, zorder=zorder))
    ax.add_patch(Circle((x, y), rayon * 0.30, color=couleur, alpha=0.95, linewidth=0, zorder=zorder + 1))


# ============================================================================
# 4. PANNEAU CENTRE — E8 : le mandala
# ============================================================================

def dessiner_tendrille(ax, rayon_ring, angle_deg, portee=0.42, couleur=COULEUR_ARETES_MANDALA,
                       n_points=80, zorder=2.5):
    """
    Une tendrille fine et semi-transparente qui part de l'anneau extérieur
    du mandala (rayon_ring) et s'étire vers l'extérieur, comme un
    prolongement du réseau de racines vers un panneau voisin. Dessinée
    avec clip_on=False : elle déborde volontairement des limites de l'axe,
    pour visuellement "tendre le bras" vers le panneau latéral, dans
    l'espace vide entre les panneaux.
    """
    a0 = np.radians(angle_deg)
    t = np.linspace(0, 1, n_points)
    rayon_t = rayon_ring * (1 + portee * t)
    ondulation = np.radians(5) * np.sin(2 * np.pi * t)   # léger gauchissement organique
    angle_t = a0 + ondulation
    x = rayon_t * np.cos(angle_t)
    y = rayon_t * np.sin(angle_t)

    points = np.stack([x, y], axis=1).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    alphas = 0.30 * (1 - t[:-1])   # s'estompe vers la pointe
    couleurs = np.tile(np.array([*to_rgb(couleur)]), (len(segments), 1))
    couleurs = np.concatenate([couleurs, alphas[:, None]], axis=1)

    lignes = LineCollection(segments, colors=couleurs, linewidths=1.0, zorder=zorder, capstyle="round")
    lignes.set_clip_on(False)
    ax.add_collection(lignes)


def dessiner_panneau_e8(ax, x, y, i_idx, j_idx):
    """
    Le mandala des 240 racines de E8, projeté sur le plan de Coxeter. Le
    centre de la projection reste volontairement VIDE : conformément à la
    géométrie réelle de E8, les 240 racines sont toutes à la même distance
    de l'origine (norme² = 2) et forment des anneaux concentriques autour
    d'un centre que rien n'occupe — aucune racine, aucun point, aucun motif
    ne doit être ajouté au milieu, cela contredirait la structure du système
    de racines.

    Quelques tendrilles fines partent symétriquement de l'anneau extérieur
    vers la gauche et vers la droite (voir dessiner_tendrille), comme un
    prolongement discret du réseau de racines en direction des deux
    panneaux latéraux.

    le fil vibrant central traverse maintenant VISUELLEMENT
    le mandala (voir dessiner_traversee_mandala), passant derrière le
    réseau d'un côté et devant de l'autre, toujours sans rien poser au
    centre exact.
    """
    ax.set_facecolor(COULEUR_FOND)
    ax.set_aspect("equal")
    ax.axis("off")

    rayons = np.hypot(x, y)
    rayon_min, rayon_max = rayons.min(), rayons.max()
    marge = rayon_max * 1.14
    ax.set_xlim(-marge, marge)
    ax.set_ylim(-marge, marge)

    valeurs_couleur = (np.arctan2(y, x) + np.pi) / (2 * np.pi)
    cmap = plt.get_cmap(PALETTE_MANDALA)

    # Réseau fin d'arêtes (les 56 plus proches voisins de chaque racine)
    segments = np.stack([
        np.stack([x[i_idx], y[i_idx]], axis=1),
        np.stack([x[j_idx], y[j_idx]], axis=1),
    ], axis=1)
    couleurs_aretes = cmap((valeurs_couleur[i_idx] + valeurs_couleur[j_idx]) / 2)
    ax.add_collection(LineCollection(segments, colors=couleurs_aretes,
                                      linewidths=0.22, alpha=0.32, zorder=2))

    # Les 240 racines, avec un léger effet de glow : deux passes plus
    # grandes et plus transparentes en dessous, de la même couleur que
    # chaque point, pour un halo lumineux, avant le disque net du dessus.
    for taille_mult, alpha in [(7, 0.05), (3.5, 0.12)]:
        ax.scatter(x, y, c=valeurs_couleur, cmap=PALETTE_MANDALA, s=17 * taille_mult,
                   alpha=alpha, zorder=3, linewidths=0)
    ax.scatter(x, y, c=valeurs_couleur, cmap=PALETTE_MANDALA, s=17,
               zorder=4, edgecolors="white", linewidths=0.2)

    # Tendrilles symétriques, 3 de chaque côté, prolongeant le réseau vers
    # les deux panneaux latéraux (voir docstring).
    for angle_deg in (160, 180, 200):
        dessiner_tendrille(ax, rayon_max, angle_deg)
    for angle_deg in (-20, 0, 20):
        dessiner_tendrille(ax, rayon_max, angle_deg)

    # Traversée visible du fil central : passe derrière le réseau à
    # gauche, devant à droite, sans rien poser exactement au centre (voir
    # dessiner_traversee_mandala). Les points renvoyés servent à placer
    # des impulsions lumineuses cohérentes avec le reste du fil.
    pts_traversee_gauche, pts_traversee_droite = dessiner_traversee_mandala(ax, marge, COULEUR_FIL_CENTRE)

    return rayon_min, rayon_max, pts_traversee_gauche, pts_traversee_droite


# ============================================================================
# 5. PANNEAU GAUCHE — mécanique quantique (sans texte : icônes seules)
# ============================================================================
#
# Un motif universellement reconnu, sans avoir besoin d'aucune légende : le
# symbole de l'atome — un noyau entouré de 3 orbites elliptiques
# identiques, tournées de 60° les unes par rapport aux autres, qui se
# croisent (c'est le pictogramme "atomique" standard, utilisé partout dans
# le monde).

def dessiner_atome(ax, echelle=1.0):
    """Le pictogramme universel de l'atome : noyau + 3 orbites elliptiques croisées + électrons."""
    theta = np.linspace(0, 2 * np.pi, 300)
    a, b = 0.95 * echelle, 0.40 * echelle   # demi-grand axe, demi-petit axe (ellipse commune aux 3 orbites)

    electrons_a_placer = []
    for k, angle_deg in enumerate((0, 60, 120)):
        phi = np.radians(angle_deg)
        ex = a * np.cos(theta)
        ey = b * np.sin(theta)
        # rotation de l'ellipse d'un angle phi
        x_rot = ex * np.cos(phi) - ey * np.sin(phi)
        y_rot = ex * np.sin(phi) + ey * np.cos(phi)
        ax.plot(x_rot, y_rot, color=COULEUR_ORBITES, linewidth=2.0, alpha=0.8, zorder=3)

        # un électron lumineux posé sur cette orbite, décalé pour ne pas s'aligner
        t_e = 0.35 + 0.5 * k
        ex_pt, ey_pt = a * np.cos(t_e), b * np.sin(t_e)
        electrons_a_placer.append((
            ex_pt * np.cos(phi) - ey_pt * np.sin(phi),
            ex_pt * np.sin(phi) + ey_pt * np.cos(phi),
        ))

    for ex, ey in electrons_a_placer:
        dessiner_lueur(ax, ex, ey, rayon=0.075 * echelle, couleur=COULEUR_ELECTRON, zorder=6, alpha_max=0.32)

    # Le noyau, au centre — même or que la corde du panneau central
    dessiner_lueur(ax, 0, 0, rayon=0.20 * echelle, couleur=COULEUR_NOYAU, zorder=6, alpha_max=0.24)


def dessiner_panneau_quantique(ax):
    """
    Le quantique rendu reconnaissable sans aucun texte : l'atome seul.
    Cadrage symétrique (xlim = ylim), comme les deux autres panneaux, pour
    que l'atome soit centré et de taille cohérente avec le mandala et la
    grille d'espace-temps.
    """
    ax.set_facecolor(COULEUR_FOND)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)

    dessiner_atome(ax, echelle=1.15)


# ============================================================================
# 6. PANNEAU DROITE — relativité générale (grille d'espace-temps courbée)
# ============================================================================

def deplacement_radial(x, y, cx=0.0, cy=0.0, amplitude=3.5, echelle=0.38):
    """
    Rapproche le point (x, y) de la masse en (cx, cy) par une COMPRESSION
    RADIALE localisée : son rayon r (distance à la masse) devient
    r / (1 + amplitude / ((r/échelle)² + 1)). Ce facteur ne dépend que de
    r, donc la déformation est rigoureusement identique dans toutes les
    directions. Le terme (r/échelle)² fait décroître la compression en
    1/r² au-delà de "échelle" : le puits est donc bien LOCALISÉ (fortement
    creusé tout près de la masse, presque plat au bord de la grille),
    plutôt que de rétrécir toute la grille de façon quasi uniforme.

    C'est un puits gravitationnel vu de dessus (et non plus un "drap" vu
    de côté). Une simple soustraction vectorielle ferait dépasser le
    centre aux points les plus proches et replierait la grille sur
    elle-même (un artefact en « fleur ») ; la compression multiplicative
    ci-dessous garantit un rayon toujours positif et croissant avec r,
    donc jamais de repli.
    """
    dx, dy = x - cx, y - cy
    r = np.hypot(dx, dy)
    r_non_nul = np.where(r < 1e-9, 1e-9, r)
    facteur = 1.0 / (1.0 + amplitude / ((r_non_nul / echelle) ** 2 + 1.0))
    r_nouveau = r_non_nul * facteur
    return cx + dx / r_non_nul * r_nouveau, cy + dy / r_non_nul * r_nouveau


def dessiner_grille_espace_temps(ax, demi_etendue=1.55, n_lignes=15, n_echant=220):
    """
    La grille d'espace-temps : deux familles de lignes (u = cste, v = cste),
    chaque point étant tiré vers la masse centrale par deplacement_radial —
    un bol symétrique, centré sur la masse, pas un "drap" vu de côté.
    """
    bornes = np.linspace(-demi_etendue, demi_etendue, n_lignes)
    fin = np.linspace(-demi_etendue, demi_etendue, n_echant)

    for u0 in bornes:
        x, y = deplacement_radial(np.full_like(fin, u0), fin)
        ax.plot(x, y, color=COULEUR_GRILLE_ESPACE, linewidth=0.95, alpha=0.68, zorder=2)
    for v0 in bornes:
        x, y = deplacement_radial(fin, np.full_like(fin, v0))
        ax.plot(x, y, color=COULEUR_GRILLE_ESPACE, linewidth=0.95, alpha=0.68, zorder=2)


def dessiner_orbite(ax, a=1.15, b=0.76, couleur=COULEUR_PLANETE, zorder=5):
    """
    Trajectoire elliptique excentrique d'un corps en orbite, déplacée par
    la même fonction radiale que la grille (deplacement_radial) : une
    traînée qui s'estompe, plus un corps lumineux à son extrémité.
    """
    phi = np.linspace(np.radians(15), np.radians(345), 260)
    u, v = a * np.cos(phi), b * np.sin(phi)
    x, y = deplacement_radial(u, v)

    points = np.stack([x, y], axis=1).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    alphas = np.linspace(0.05, 0.85, len(segments))
    couleurs = np.tile(np.array([*to_rgb(couleur)]), (len(segments), 1))
    couleurs = np.concatenate([couleurs, alphas[:, None]], axis=1)
    ax.add_collection(LineCollection(segments, colors=couleurs, linewidths=2.0, zorder=zorder))

    dessiner_lueur(ax, x[-1], y[-1], rayon=0.085, couleur=couleur, zorder=zorder + 1, alpha_max=0.3)


def deviation_lumiere(x, centre=0.0, largeur=0.55, amplitude=0.5):
    """Déviation (en y) d'un rayon lumineux qui passe à l'abscisse x, à distance |x - centre| de la masse."""
    return -amplitude / (1.0 + ((x - centre) / largeur) ** 2)


def dessiner_rayon_lumiere(ax, y0=0.88, couleur=COULEUR_LUMIERE, zorder=7):
    """
    Un rayon de lumière qui traverse le panneau en ligne quasi droite, mais
    se courbe visiblement en passant près de la masse centrale — la
    lentille gravitationnelle, l'une des preuves historiques (éclipse de
    1919) de la relativité générale.
    """
    x = np.linspace(-1.6, 1.6, 300)
    y = y0 + deviation_lumiere(x)

    for lw, a in [(5.5, 0.10), (3.2, 0.20)]:
        ax.plot(x, y, color=couleur, linewidth=lw, alpha=a, zorder=zorder - 1, solid_capstyle="round")
    ax.plot(x, y, color=couleur, linewidth=1.7, alpha=0.92, zorder=zorder, solid_capstyle="round")
    ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-8], y[-8]),
                arrowprops=dict(arrowstyle="-|>", color=couleur, lw=1.7, alpha=0.92), zorder=zorder)


def dessiner_panneau_relativite(ax):
    """La grille d'espace-temps, creusée symétriquement autour d'une masse centrale, avec orbite et lentille gravitationnelle."""
    ax.set_facecolor(COULEUR_FOND)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)

    dessiner_grille_espace_temps(ax)
    dessiner_orbite(ax)
    dessiner_rayon_lumiere(ax)

    # Le corps massif central, exactement au centre de la grille : le puits
    # se creuse symétriquement tout autour de lui (voir deplacement_radial).
    dessiner_lueur(ax, 0, 0, rayon=0.20, couleur=COULEUR_MASSE, zorder=6, alpha_max=0.28)

    return 0.0


# ============================================================================
# 7. FIL VIBRANT CENTRAL — un seul lien symétrique, avec impulsions lumineuses
# ============================================================================

def point_bord_axes(ax, cote, fraction_y=0.5):
    """Point (en coordonnées figure) au milieu du bord gauche ou droit d'un panneau."""
    pos = ax.get_position()
    y = pos.y0 + fraction_y * (pos.y1 - pos.y0)
    x = pos.x0 if cote == "gauche" else pos.x1
    return np.array([x, y])


def point_donnee_vers_figure(fig, ax, x_donnee, y_donnee):
    """Convertit un point en coordonnées de données d'un axe donné vers des coordonnées figure (0-1)."""
    return fig.transFigure.inverted().transform(ax.transData.transform((x_donnee, y_donnee)))


def _degrade_rgba(couleur_proche, couleur_lointaine, t, alpha):
    """Tableau de couleurs RGBA, interpolées linéairement entre deux couleurs le long de t (dans [0, 1])."""
    c1 = np.array(to_rgb(couleur_proche))
    c2 = np.array(to_rgb(couleur_lointaine))
    couleurs = c1[None, :] + (c2[None, :] - c1[None, :]) * t[:, None]
    alphas = np.full(len(t), alpha)
    return np.concatenate([couleurs, alphas[:, None]], axis=1)


def dessiner_demi_fil(ax_overlay, point_centre, point_bord, couleur_proche, couleur_lointaine,
                       n_oscillations=4.5, amortissement=2.6, amplitude=0.017, n_points=300, zorder=3):
    """
    Une moitié du fil vibrant central : une SINUSOÏDE AMORTIE (l'amplitude
    est maximale près du centre E8 et s'éteint progressivement vers le
    panneau latéral), plutôt que l'onde stationnaire (nulle aux deux
    bouts) de unuigo.py — pour suggérer un flux qui émane du centre,
    plutôt qu'une corde simplement tendue entre deux points fixes.

    Les deux appels (gauche et droite, depuis construire_figure) utilisent
    exactement les mêmes couleur_proche/couleur_lointaine, n_oscillations,
    amortissement, amplitude : les deux moitiés sont donc rigoureusement
    symétriques, seule la géométrie (les points de départ/arrivée) diffère.

    Le fil est délibérément FIN (délicat) — épaisseurs et
    halos réduits — pour relier les panneaux
    sans dominer visuellement le reste de la composition.

    Retourne les points (pts) de la courbe, pour que l'appelant puisse y
    placer des impulsions lumineuses (voir dessiner_impulsions).
    """
    t = np.linspace(0, 1, n_points)
    base = point_centre[None, :] + t[:, None] * (point_bord - point_centre)[None, :]

    direction = point_bord - point_centre
    longueur = np.linalg.norm(direction)
    perp = np.array([-direction[1], direction[0]]) / longueur

    enveloppe = np.exp(-amortissement * t)
    deplacement = amplitude * np.sin(n_oscillations * 2 * np.pi * t) * enveloppe

    pts = base + deplacement[:, None] * perp[None, :]

    points = pts.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    t_mid = (t[:-1] + t[1:]) / 2

    for lw, a in [(2.6, 0.04), (1.5, 0.08)]:
        couleurs = _degrade_rgba(couleur_proche, couleur_lointaine, t_mid, a)
        ax_overlay.add_collection(LineCollection(segments, colors=couleurs, linewidths=lw,
                                                  zorder=zorder - 1, capstyle="round"))
    couleurs = _degrade_rgba(couleur_proche, couleur_lointaine, t_mid, 0.8)
    ax_overlay.add_collection(LineCollection(segments, colors=couleurs, linewidths=0.65,
                                              zorder=zorder, capstyle="round"))

    return pts


def dessiner_impulsions(ax_overlay, pts, couleur, n=9, zorder=6):
    """
    De petites impulsions lumineuses (perles) le long d'un demi-fil (pts,
    tel que renvoyé par dessiner_demi_fil ou dessiner_traversee_mandala,
    indexé du centre E8 vers le panneau latéral) : concentrées et
    rapprochées près du centre (indice 0), de plus en plus PETITES ET
    ESPACÉES vers le bord — l'idée d'un flux qui rayonne depuis E8.

    biais plus marqué (exposant 2.4 au lieu de 1.6) et
    perles plus petites, cohérentes avec un fil beaucoup plus fin.
    """
    n_total = len(pts)
    fractions = np.linspace(0, 1, n) ** 2.4   # biais marqué vers 0 : perles serrées près du centre
    for frac in fractions:
        idx = int(frac * (n_total - 1))
        px, py = pts[idx]
        rayon = 0.003 + 0.007 * (1 - frac)
        alpha = 0.12 + 0.50 * (1 - frac)
        for k in (3, 2, 1):
            ax_overlay.add_patch(Circle((px, py), rayon * k / 3, color=couleur,
                                        alpha=alpha * (1 - k / 4), linewidth=0, zorder=zorder))
        ax_overlay.add_patch(Circle((px, py), rayon * 0.35, color=couleur,
                                    alpha=min(alpha + 0.3, 0.95), linewidth=0, zorder=zorder + 1))


def dessiner_traversee_mandala(ax, marge, couleur, amplitude=0.045, n_oscillations=2,
                               n_points=150, vide=0.09, zorder_derriere=1.5, zorder_devant=6.5):
    """
    Le segment interne du fil, qui traverse VISUELLEMENT le mandala plutôt
    que de s'arrêter à son bord : la moitié gauche passe DERRIÈRE le
    réseau de racines (zorder sous les arêtes/points de dessiner_panneau_e8),
    la moitié droite passe DEVANT (zorder au-dessus), avec un petit "vide"
    non marqué exactement au centre (paramètre `vide`) — le centre de E8
    reste vide, sans point ni halo.

    n_oscillations est un entier : sin(n_oscillations * 2π * t) vaut donc
    exactement 0 en t=1, ce qui place naturellement l'extrémité de chaque
    moitié en (±marge, 0) — exactement le point où s'attache le demi-fil
    extérieur (voir point_bord_axes) — sans discontinuité visible.

    Retourne (pts_gauche, pts_droite), chacun indexé du vide central
    (indice 0) vers le bord du panneau (dernier indice), pour y placer des
    impulsions cohérentes avec dessiner_impulsions.
    """
    t = np.linspace(0, 1, n_points)
    onde = amplitude * np.sin(n_oscillations * 2 * np.pi * t) * t

    x_gauche = -vide - t * (marge - vide)
    pts_gauche = np.stack([x_gauche, onde], axis=1)

    x_droite = vide + t * (marge - vide)
    pts_droite = np.stack([x_droite, onde], axis=1)

    couleur_rgb = to_rgb(couleur)
    for pts, zorder in [(pts_gauche, zorder_derriere), (pts_droite, zorder_devant)]:
        points = pts.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        for lw, a in [(2.2, 0.05), (1.3, 0.09)]:
            couleurs = np.tile([*couleur_rgb, a], (len(segments), 1))
            ax.add_collection(LineCollection(segments, colors=couleurs, linewidths=lw,
                                             zorder=zorder - 0.5, capstyle="round"))
        couleurs = np.tile([*couleur_rgb, 0.75], (len(segments), 1))
        ax.add_collection(LineCollection(segments, colors=couleurs, linewidths=0.55,
                                         zorder=zorder, capstyle="round"))

    return pts_gauche, pts_droite


# ============================================================================
# 8. CONSTRUCTION DE LA FIGURE COMPLÈTE
# ============================================================================

def construire_figure():
    """
    Construit et retourne la figure matplotlib complète : 3 panneaux
    (quantique — E8 — relativité) reliés par un seul fil vibrant
    symétrique (voir section 7), avec des tendrilles issues du mandala
    (voir dessiner_tendrille). Aucun texte hormis le titre en espéranto :
    les deux physiques doivent se reconnaître par l'image seule (atome à
    gauche, puits gravitationnel + lentille à droite).
    """
    racines = generer_racines_e8()
    verifier_racines(racines)

    c = element_coxeter(racines_simples_e8())
    u, v = base_plan_coxeter(c)
    x, y = projeter_sur_plan(racines, u, v)
    i_idx, j_idx = calculer_aretes_courtes(racines)

    fig = plt.figure(figsize=(LARGEUR_POUCES, HAUTEUR_POUCES), facecolor=COULEUR_FOND)
    gs = fig.add_gridspec(
        nrows=1, ncols=3, width_ratios=[1.12, 1.0, 1.12],
        wspace=0.06,
        left=0.03, right=0.97, top=0.965, bottom=0.035,
    )

    ax_gauche = fig.add_subplot(gs[0, 0])
    ax_centre = fig.add_subplot(gs[0, 1])
    ax_droite = fig.add_subplot(gs[0, 2])

    dessiner_panneau_quantique(ax_gauche)
    _, _, pts_traversee_gauche, pts_traversee_droite = dessiner_panneau_e8(ax_centre, x, y, i_idx, j_idx)
    y_masse = dessiner_panneau_relativite(ax_droite)

    # Impulsions sur le segment qui traverse le mandala : mêmes zorder que
    # dessiner_traversee_mandala (derrière à gauche, devant à droite), pour
    # que les perles restent cohérentes avec la traversée visible du fil.
    dessiner_impulsions(ax_centre, pts_traversee_gauche, couleur=COULEUR_ACCENT_CENTRAL, n=4, zorder=1.8)
    dessiner_impulsions(ax_centre, pts_traversee_droite, couleur=COULEUR_ACCENT_CENTRAL, n=4, zorder=6.8)

    # --- Fil vibrant unique, symétrique et FIN : un seul dégradé de
    # couleur (COULEUR_FIL_CENTRE -> COULEUR_FIL_BORD), la même sinusoïde
    # amortie, la même épaisseur des deux côtés — seule la géométrie
    # diffère entre la moitié gauche (vers l'atome) et la moitié droite
    # (vers la masse). Ces deux demi-fils extérieurs se prolongent par la
    # traversée visible du mandala (voir dessiner_traversee_mandala,
    # appelée depuis dessiner_panneau_e8). Des impulsions lumineuses,
    # petites et concentrées près du centre puis de plus en plus espacées,
    # suggèrent un flux qui rayonne depuis E8 vers chaque monde. ---
    ax_overlay = fig.add_axes([0, 0, 1, 1])
    ax_overlay.set_xlim(0, 1)
    ax_overlay.set_ylim(0, 1)
    ax_overlay.axis("off")
    ax_overlay.patch.set_alpha(0.0)

    p_centre_gauche = point_bord_axes(ax_centre, "gauche")
    p_noyau = point_donnee_vers_figure(fig, ax_gauche, 0, 0)
    pts_gauche = dessiner_demi_fil(ax_overlay, p_centre_gauche, p_noyau,
                                   COULEUR_FIL_CENTRE, COULEUR_FIL_BORD)
    dessiner_impulsions(ax_overlay, pts_gauche, couleur=COULEUR_ACCENT_CENTRAL)

    p_centre_droite = point_bord_axes(ax_centre, "droite")
    p_masse = point_donnee_vers_figure(fig, ax_droite, 0, y_masse)
    pts_droite = dessiner_demi_fil(ax_overlay, p_centre_droite, p_masse,
                                   COULEUR_FIL_CENTRE, COULEUR_FIL_BORD)
    dessiner_impulsions(ax_overlay, pts_droite, couleur=COULEUR_ACCENT_CENTRAL)

    return fig


# ============================================================================
# 9. POINT D'ENTRÉE
# ============================================================================

def main():
    os.makedirs(DOSSIER_SORTIE, exist_ok=True)

    fig = construire_figure()

    fig.savefig(FICHIER_PNG, dpi=DPI, facecolor=fig.get_facecolor())
    fig.savefig(FICHIER_SVG, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"Œuvre générée :\n  - {FICHIER_PNG}\n  - {FICHIER_SVG}")


if __name__ == "__main__":
    main()
