# Tâches : Parité des fonctionnalités de GanttProject

**Entrée** : Documents de conception de `/specs/001-ganttproject-features/`

**Prérequis** : plan.md (requis), spec.md (requis pour les récits utilisateurs), research.md, data-model.md, contracts/

**Organisation** : Les tâches sont regroupées par récit utilisateur (User Story) pour permettre une implémentation et des tests indépendants de chaque récit. Étant donné l'architecture "fichier unique" (Single-file), presque tous les développements se feront au sein de `webGantt.html`. Les tâches ne sont donc pas parallélisables (absence de tag `[P]`) pour éviter les conflits de fusion sur ce même fichier, sauf pour les tests.

## Phase 1 : Configuration (Infrastructure Partagée)

**Objectif** : Initialisation du projet et structure de base

- [x] T001 Initialiser la structure de fichier unique avec le boilerplate HTML5 de base dans `webGantt.html`
- [x] T002 Ajouter la disposition de base CSS Grid/Flexbox pour la vue scindée (UI-001) dans `webGantt.html`
- [x] T003 Ajouter le conteneur de la barre d'outils supérieure (UI-003) dans `webGantt.html`
- [x] T004 Implémenter les variables CSS pour le mode clair/sombre et la logique de basculement (UI-004) dans `webGantt.html`

---

## Phase 2 : Fondations (Prérequis Bloquants)

**Objectif** : Infrastructure de base qui DOIT être terminée avant que N'IMPORTE QUEL récit utilisateur puisse être implémenté

**⚠️ CRITIQUE** : Aucun travail sur les récits utilisateurs ne peut commencer tant que cette phase n'est pas terminée

- [x] T005 Implémenter la logique du Gestionnaire d'État (State Manager) pour gérer les données XML du projet (tâches, dépendances, ressources) dans `webGantt.html`
- [x] T006 Implémenter la logique de l'API File System Access pour ouvrir/sauvegarder le fichier `.gan` (XML) du projet (FR-007) dans `webGantt.html`

**Point de contrôle** : Fondation prête - l'implémentation des récits utilisateurs peut maintenant commencer

---

## Phase 3 : Récit Utilisateur 1 - Planification du Projet de base & Tâches (Priorité : P1) 🎯 MVP

**Objectif** : Les utilisateurs peuvent créer et organiser une structure de découpage du travail avec des tâches, des sous-tâches et des jalons pour structurer leur projet.

**Test Indépendant** : Peut être testé en ajoutant une hiérarchie de tâches et en s'assurant qu'elles s'affichent correctement dans le modèle de données et l'interface utilisateur.

### Implémentation pour le Récit Utilisateur 1

- [x] T007 [US1] Créer le modèle de l'entité Tâche (Task) et la logique d'analyse dans `webGantt.html`
- [x] T008 [US1] Implémenter la logique de rendu du tableau de données WBS dans le volet gauche dans `webGantt.html`
- [x] T009 [US1] Implémenter la logique de rendu de base de la frise chronologique du diagramme de Gantt dans le volet droit dans `webGantt.html`
- [x] T010 [US1] Ajouter la fonctionnalité de l'interface utilisateur pour créer, modifier et supprimer des tâches et sous-tâches (FR-001) dans `webGantt.html`
- [x] T011 [US1] Ajouter la fonctionnalité pour définir visuellement et logiquement des jalons (FR-002) dans `webGantt.html`
- [x] T012 [US1] Implémenter le défilement synchronisé entre le tableau de gauche et la frise de droite (UI-002) dans `webGantt.html`

**Point de contrôle** : À ce stade, le Récit Utilisateur 1 doit être entièrement fonctionnel et testable indépendamment

---

## Phase 4 : Récit Utilisateur 2 - Dépendances des tâches & Planification (Priorité : P1)

**Objectif** : Les utilisateurs peuvent lier des tâches en utilisant des dépendances (par exemple, Fin-à-Début) afin que la planification se mette à jour automatiquement en fonction des contraintes.

**Test Indépendant** : Peut être entièrement testé en créant deux tâches, en les liant, et en déplaçant la première tâche pour voir la seconde se déplacer.

### Implémentation pour le Récit Utilisateur 2

- [x] T013 [US2] Analyser et stocker les métadonnées de dépendances des tâches (FS, FF, SS, SF) dans `webGantt.html`
- [x] T014 [US2] Dessiner visuellement les lignes/flèches de dépendance entre les barres de tâches sur le SVG du Gantt dans `webGantt.html`
- [x] T015 [US2] Implémenter la logique de décalage automatique en cascade lors du déplacement temporel d'une tâche (FR-003) dans `webGantt.html`

**Point de contrôle** : À ce stade, les Récits Utilisateurs 1 ET 2 doivent tous deux fonctionner indépendamment

---

## Phase 5 : Récit Utilisateur 3 - Gestion des ressources & Allocation (Priorité : P2)

**Objectif** : Les utilisateurs peuvent définir un pool de ressources (membres de l'équipe) et les affecter à des tâches spécifiques pour suivre les responsabilités et les charges de travail.

**Test Indépendant** : Peut être testé en ajoutant des ressources au projet et en les affectant aux tâches.

### Implémentation pour le Récit Utilisateur 3

- [x] T016 [US3] Créer la logique des entités Ressource et Affectation (Assignment) dans `webGantt.html`
- [x] T017 [US3] Implémenter l'interface (modale/panneau) pour créer un pool de ressources (FR-004) dans `webGantt.html`
- [x] T018 [US3] Implémenter l'interface pour affecter des ressources aux tâches (FR-005) dans `webGantt.html`
- [x] T019 [US3] Afficher le nom des ressources affectées sur les barres de tâches du diagramme de Gantt dans `webGantt.html`

**Point de contrôle** : Toutes les fonctionnalités de base sont opérationnelles

---

## Phase 6 : Récit Utilisateur 4 - Lignes de base (Baselines) & Suivi de progression (Priorité : P3)

**Objectif** : Les utilisateurs peuvent enregistrer une ligne de base du projet et suivre l'avancement actuel par rapport au plan d'origine.

**Test Indépendant** : Peut être testé en enregistrant une ligne de base, en modifiant les dates, et en vérifiant que les marqueurs de la ligne de base restent inchangés.

### Implémentation pour le Récit Utilisateur 4

- [x] T020 [US4] Implémenter la logique de sauvegarde des lignes de base du projet dans le Gestionnaire d'État dans `webGantt.html`
- [x] T021 [US4] Implémenter le rendu visuel des marqueurs de ligne de base sur le diagramme de Gantt dans `webGantt.html`
- [x] T022 [US4] Ajouter la fonctionnalité pour définir le pourcentage d'avancement sur les tâches (FR-008) dans `webGantt.html`
- [x] T023 [US4] Afficher le pourcentage d'avancement visuellement à l'intérieur des barres de tâches dans `webGantt.html`

**Point de contrôle** : Tous les récits utilisateurs doivent maintenant être fonctionnels indépendamment

---

## Phase 7 : Finalisation & Considérations Transversales (Polish & Cross-Cutting)

**Objectif** : Améliorations qui affectent plusieurs récits utilisateurs

- [x] T024 [P] Créer un fichier de test basique E2E Playwright pour valider le cycle complet (chargement du fichier `example.gan`, modification dans le DOM, et sauvegarde) dans `tests/e2e.test.js`
- [x] T025 Exécuter manuellement les scénarios de validation du fichier quickstart.md
- [x] T026 Nettoyage de code et refactoring dans `webGantt.html`
- [x] T027 [US5] Distinguer l'action d'enregistrement (écrasement) et de téléchargement, avec avertissement en cas de modifications non sauvegardées.
- [x] T028 [US4] Ajouter une interface modale complète pour gérer les lignes de bases : lister, supprimer, créer et choisir la ligne active.

---

## Phase 8 : Interface Utilisateur Avancée & Parité Desktop (Priorité : P1/P2)

**Objectif** : Atteindre l'ergonomie et la richesse fonctionnelle de GanttProject (barres d'outils complètes, arborescence interactive, zooms, filtres).

- [x] T029 [US5] Implémenter le modèle de sélection de tâches (multisélection), avec surbrillance WBS et Gantt.
- [x] T030 [US5] Ajouter les boutons WBS Indenter (flèche droite) et Désindenter (flèche gauche) avec leurs règles précises de grisage/désactivation en fonction du parent. Modifier l'arborescence XML (`parent`).
- [x] T031 [US5] Ajouter les boutons WBS Monter (flèche haut) et Descendre (flèche bas) avec leurs règles de grisage (vérification de l'existence d'un frère au-dessus/en-dessous).
- [x] T032 [US5] Ajouter les boutons WBS Lier (maillon) et Délier (maillon brisé). "Lier" crée les dépendances 2 à 2 en séquence. Gérer les conditions de grisage (même parent, reliées ou non).
- [x] T033 [US5] Ajouter le bouton Filtre (Entonnoir) ouvrant une liste de 4 boutons radio (Non terminées, Aujourd'hui, En retard, En cours) pour filtrer le rendu.
- [x] T034 [US5] Ajouter le bouton Colonnes (Engrenage) pour afficher/masquer dynamiquement les attributs du WBS.
- [x] T035 [US5] Modifier l'algorithme "Ajouter Tâche" : insertion juste en dessous de la sélection courante, partageant le même parent (ou racine si rien n'est sélectionné).
- [x] T036 [US5] Rendre le WBS pliable/dépliable : icônes chevrons (v) et (>) conditionnelles sur les parents, cachant/affichant les sous-tâches.
- [x] T037 [US5] Ajouter un bouton pour afficher/masquer le chemin critique sur le Gantt.
- [x] T038 [US5] Implémenter la bordure splitter (resize) entre le paneau gauche et droit.
- [x] T039 [US5] Implémenter les boutons chevron gauche/droit pour masquer complètement / réafficher le panneau gauche d'un seul clic.
- [x] T040 [US5] En-tête du Gantt : Boutons "Zoom avant" (allongement rectangles) et "Zoom arrière" (rétrécissement rectangles).
- [x] T041 [US5] En-tête du Gantt : Affichage de l'échelle du temps (graduation évoluant : jour, semaine, mois, trimestre, semestre, année) couplée au niveau de zoom.
- [x] T042 [US5] Implémenter le système d'historique (Annuler / Rétablir) avec une pile d'état de profondeur 100.
- [x] T043 [US5] Implémenter le presse-papiers complet : Copier, Couper, Coller appliqués aux tâches sélectionnées.
- [ ] T044 [US5] Implémenter la fonctionnalité d'Impression spécifique au Gantt.
- [ ] T045 [P] Mettre à jour `tests/e2e.test.js` pour inclure la vérification des nouvelles fonctionnalités d'IHM complexes.
- [x] T046 [US5] Implémenter le calcul automatique des bornes temporelles (début, fin, durée) pour les tâches parentes en fonction de leurs enfants.

---

## Dépendances & Ordre d'Exécution

### Dépendances des Phases

- **Configuration (Phase 1)** : Aucune dépendance - peut commencer immédiatement
- **Fondations (Phase 2)** : Dépend de la fin de la Configuration - BLOQUE tous les récits utilisateurs
- **Récits Utilisateurs (Phase 3+)** : Tous dépendent de la fin de la phase des Fondations
- **Finalisation (Dernière Phase)** : Dépend de l'achèvement de tous les récits utilisateurs souhaités

### Dépendances des Récits Utilisateurs

- **Récit Utilisateur 1 (P1)** : Peut commencer après les Fondations (Phase 2)
- **Récit Utilisateur 2 (P1)** : Peut commencer après le Récit Utilisateur 1 (nécessite la frise chronologique visuelle du Gantt pour tracer les flèches)
- **Récit Utilisateur 3 (P2)** : Peut commencer après les Fondations, s'appuie sur l'existence des tâches du Récit Utilisateur 1
- **Récit Utilisateur 4 (P3)** : Peut commencer après le Récit Utilisateur 1

### Opportunités de Parallélisation

- Du fait de l'architecture "fichier unique" (`webGantt.html`), les tâches d'implémentation doivent idéalement être effectuées de manière **séquentielle** pour éviter les conflits d'édition sur le même fichier.
- Le test E2E (T024) peut être fait en parallèle (`[P]`) une fois le fichier de base en place.

---

## Stratégie d'Implémentation

### MVP en Premier (Récit Utilisateur 1 Seulement)

1. Terminer la Phase 1 : Configuration
2. Terminer la Phase 2 : Fondations (CRITIQUE)
3. Terminer la Phase 3 : Récit Utilisateur 1
4. **STOP et VALIDATION** : Tester le Récit Utilisateur 1 de façon indépendante

### Livraison Incrémentale

1. Terminer Configuration + Fondations → Fondation prête
2. Ajouter le Récit Utilisateur 1 → Tester de façon indépendante → Déployer/Démo (MVP !)
3. Ajouter le Récit Utilisateur 2 → Tester de façon indépendante → Déployer/Démo
4. Ajouter le Récit Utilisateur 3 → Tester de façon indépendante → Déployer/Démo
5. Ajouter le Récit Utilisateur 4 → Tester de façon indépendante → Déployer/Démo
