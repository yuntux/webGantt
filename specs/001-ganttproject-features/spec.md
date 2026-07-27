# Spécification de la fonctionnalité : Parité des fonctionnalités de GanttProject

**Branche de la fonctionnalité** : `[001-ganttproject-features]`

**Créé le** : 2026-07-27

**Statut** : Brouillon

**Entrée** : Description de l'utilisateur : "parcours le web pour comprendre ce que fais l'application GanttProject"

## Scénarios Utilisateur & Tests *(obligatoire)*

### Récit Utilisateur 1 - Planification du Projet de base & Tâches (Priorité : P1)

Les utilisateurs peuvent créer et organiser une structure de découpage du travail avec des tâches, des sous-tâches et des jalons pour structurer leur projet.

**Pourquoi cette priorité** : Sans tâches de base, il n'y a pas de diagramme de Gantt. Il s'agit de la fonctionnalité fondamentale.

**Test Indépendant** : Peut être testé en ajoutant une hiérarchie de tâches et en s'assurant qu'elles s'affichent correctement dans le modèle de données et l'interface utilisateur.

**Scénarios d'acceptation** :

1. **Étant donné** un nouveau projet, **Quand** un utilisateur ajoute une tâche et une sous-tâche, **Alors** la sous-tâche est visuellement imbriquée sous la tâche parente.
2. **Étant donné** une tâche existante, **Quand** un utilisateur la marque comme jalon, **Alors** elle est représentée comme un événement de durée nulle (en forme de losange) sur le diagramme de Gantt.

---

### Récit Utilisateur 2 - Dépendances des tâches & Planification (Priorité : P1)

Les utilisateurs peuvent lier des tâches en utilisant des dépendances (par exemple, Fin-à-Début) afin que la planification se mette à jour automatiquement en fonction des contraintes.

**Pourquoi cette priorité** : Les dépendances distinguent un diagramme de Gantt d'un simple calendrier.

**Test Indépendant** : Peut être entièrement testé en créant deux tâches, en les liant, et en déplaçant la première tâche pour voir la seconde se déplacer.

**Scénarios d'acceptation** :

1. **Étant donné** la Tâche A et la Tâche B, **Quand** l'utilisateur crée un lien Fin-à-Début de A vers B, **Alors** la Tâche B ne peut pas commencer avant que la Tâche A ne soit terminée.

---

### Récit Utilisateur 3 - Gestion des ressources & Allocation (Priorité : P2)

Les utilisateurs peuvent définir un pool de ressources (membres de l'équipe) et les affecter à des tâches spécifiques pour suivre les responsabilités et les charges de travail.

**Pourquoi cette priorité** : Essentiel pour les projets d'équipe, mais la planification de base des tâches fonctionne sans cela.

**Test Indépendant** : Peut être testé en ajoutant des ressources au projet et en les affectant aux tâches.

**Scénarios d'acceptation** :

1. **Étant donné** une liste de ressources, **Quand** un utilisateur affecte une ressource à une tâche, **Alors** le nom de la ressource apparaît sur la tâche dans le diagramme.

---

### Récit Utilisateur 4 - Lignes de base (Baselines) & Suivi de progression (Priorité : P3)

Les utilisateurs peuvent enregistrer une ligne de base du projet et suivre l'avancement actuel par rapport au plan d'origine.

**Pourquoi cette priorité** : Important pour l'exécution du projet mais pas nécessaire pour la planification initiale.

**Test Indépendant** : Peut être testé en enregistrant une ligne de base, en modifiant les dates, et en vérifiant que les marqueurs de la ligne de base restent inchangés.

**Scénarios d'acceptation** :

1. **Étant donné** un projet planifié, **Quand** l'utilisateur enregistre une ligne de base et modifie la durée d'une tâche, **Alors** le diagramme visuel affiche à la fois la nouvelle durée et la ligne de base d'origine pour comparaison.

### Cas limites (Edge Cases)

- Que se passe-t-il lorsqu'un utilisateur crée une dépendance circulaire (La Tâche A dépend de B, B dépend de A) ?
- Comment le système gère-t-il les tâches affectées à une ressource qui est supprimée par la suite ?
- Que se passe-t-il si le fichier JSON importé est malformé ou s'il manque des champs obligatoires ?

## Exigences *(obligatoire)*

### Exigences Fonctionnelles

- **FR-001** : Le système DOIT permettre aux utilisateurs de créer, modifier et supprimer des tâches et des sous-tâches.
- **FR-002** : Le système DOIT permettre aux utilisateurs de définir des jalons (tâches de durée nulle).
- **FR-003** : Le système DOIT prendre en charge les dépendances de tâches, en particulier les contraintes Fin-à-Début.
- **FR-004** : Le système DOIT permettre aux utilisateurs de créer un pool de ressources.
- **FR-005** : Le système DOIT permettre d'affecter des ressources aux tâches.
- **FR-006** : Le système DOIT visualiser la chronologie du projet sous forme de diagramme de Gantt.
- **FR-007** : Le système DOIT être capable de lire, modifier et sauvegarder un fichier au format natif `.gan` (XML GanttProject). L'application DOIT se conformer strictement au schéma de référence `assets/ganttproject.xsd` et l'interface utilisateur (IHM) DOIT être capable de gérer et d'exposer **toutes** les possibilités et attributs offerts par ce fichier XSD (tâches, dépendances, ressources, affectations, lignes de base, couleurs, etc.).
- **FR-008** : L'application doit permettre la sauvegarde d'empreintes du projet (lignes de base) au sein du fichier et offrir un affichage visuel de ces références. Elle doit permettre de gérer ces lignes de base (création, suppression, sélection de la ligne active pour l'affichage). Elle doit permettre de définir et visualiser le pourcentage d'avancement des tâches (attribut `complete`).
- **FR-009** : L'application doit distinguer l'écrasement natif du fichier ("Enregistrer") du téléchargement d'une nouvelle copie ("Télécharger"). Si l'utilisateur tente de quitter la page avec des modifications non sauvegardées, une alerte système (beforeunload) doit le prévenir.

### Exigences d'Interface Graphique (IHM)

- **UI-001 (Vue scindée - Split View)** : L'interface DOIT reprendre la disposition classique de GanttProject avec une vue divisée verticalement : 
  - **Volet gauche** : Un tableau de données hiérarchique (WBS) listant les tâches, leurs dates de début, de fin et leurs durées.
  - **Volet droit** : La frise chronologique (Gantt chart) interactive avec les barres horizontales et les flèches de dépendance.
- **UI-002 (Synchronisation du défilement)** : Le défilement vertical du tableau à gauche et du diagramme à droite DOIT être parfaitement synchronisé.
- **UI-003 (Barre d'outils)** : Une barre d'outils supérieure DOIT être présente pour accéder rapidement aux actions principales (Nouveau, Ouvrir, Enregistrer, Ajouter une Tâche, Propriétés, Descendre une tâche, Remonter une tâche, Ajouter une dépendance, Supprimer une dépendance, Ajouter une ressource, Supprimer une ressource, Affecter une ressource à une tâche).
- **UI-004 (Thématisation)** : L'interface DOIT proposer un mode clair (Light Mode) et un mode sombre (Dark Mode). Le mode **clair** DOIT être activé par défaut.

### Entités Clés

- **Tâche** (Task) : Représente une unité de travail. Attributs : ID, nom, date de début, durée, avancement, est_un_jalon, id_parent.
- **Dépendance** (Dependency) : Représente un lien entre les tâches. Attributs : id_tâche_source, id_tâche_cible, type.
- **Ressource** (Resource) : Représente une personne ou un équipement. Attributs : ID, nom, rôle.
- **Affectation** (Assignment) : Associe une Ressource à une Tâche. Attributs : id_tâche, id_ressource, pourcentage_charge.

## Critères de Succès *(obligatoire)*

### Résultats Mesurables

- **SC-001** : Les utilisateurs peuvent charger un fichier de projet JSON contenant 500 tâches et afficher le diagramme de Gantt en moins de 1 seconde.
- **SC-002** : Les utilisateurs peuvent identifier clairement les dépendances des tâches et les chemins critiques sur la visualisation.
- **SC-003** : 100% des concepts de base de GanttProject (tâches, dépendances, ressources) sont pris en charge par le schéma JSON.

## Hypothèses

- Nous supposons que les dépendances standards Fin-à-Début sont suffisantes pour le MVP ; Début-à-Début, Fin-à-Fin pourront être ajoutées ultérieurement.
- L'exportation vers MS Project/PDF est hors de portée pour le MVP car l'objectif principal est une application HTML entièrement locale avec sauvegarde en JSON.
- Les diagrammes PERT et les graphiques de charge des ressources sont moins prioritaires que la vue principale du diagramme de Gantt.
