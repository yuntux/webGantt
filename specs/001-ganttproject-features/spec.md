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
- **FR-010** : Le système DOIT fournir des outils de hiérarchie WBS et de réordonnancement :
  - **Indenter (flèche droite)** : La tâche sélectionnée (ou le groupe) devient l'enfant de la tâche la précédant. Grisé si aucune tâche ne précède dans la même fratrie. En sélection multiple, actif uniquement si toutes les tâches ont le même parent et peuvent toutes être indentées).
  - **Désindenter (flèche gauche)** : La tâche (ou le groupe) remonte d'un niveau. Grisé si niveau 1 / sans parent. En sélection multiple, actif uniquement si toutes les tâches ont le même parent et peuvent toutes être désindentées).
  - **Monter (flèche haut)** : La tâche sélectionnée (ou le groupe de tâches) monte dans la fratrie. (Grisé s'il n'y a pas de tâche supérieure avec le même parent. En sélection multiple, actif uniquement si toutes les tâches ont le même parent et peuvent toutes monter).
  - **Descendre (flèche bas)** : La tâche sélectionnée (ou le groupe de tâches) descend dans la fratrie. (Grisé s'il n'y a pas de tâche inférieure avec le même parent. En sélection multiple, actif uniquement si toutes les tâches ont le même parent et peuvent toutes descendre).
- **FR-011** : Le système DOIT permettre la liaison et déliaison multiple via des boutons dédiés opérant sur les N tâches sélectionnées :
  - **Lier (chaîne)** : Crée des dépendances 2 à 2 dans l'ordre de la liste. (Grisé si toutes les tâches sélectionnées n'ont pas le même parent).
  - **Délier (chaîne brisée)** : Supprime les dépendances entre les tâches sélectionnées. (Grisé si les tâches ne sont pas reliées).
- **FR-012** : Le système DOIT proposer un bouton (Entonnoir) avec 4 boutons radio pour filtrer :
  1. Tâches non terminées (progression < 100%).
  2. Tâches à faire aujourd'hui (progression < 100% et date de fin = aujourd'hui).
  3. Tâches en retard.
  4. Tâches en cours.
- **FR-013** : Le système DOIT proposer un bouton (Engrenage) pour afficher/masquer les colonnes du WBS.
- **FR-014** : Le WBS DOIT afficher les tâches sous forme d'arborescence pliable :
  - Chevron bas (v) : tâche dépliée. Un clic la plie et affiche un chevron droit (>).
  - Chevron droit (>) : tâche pliée. Un clic la déplie et affiche un chevron bas (v).
  - **Persistance** : L'état plié/déplié DOIT être synchronisé en temps réel avec l'attribut XML `expand="true/false"` de la tâche concernée, afin que cet état soit conservé lors de la sauvegarde et du chargement du fichier `.gan`.
  - Le diagramme de Gantt DOIT masquer dynamiquement les barres des tâches enfants lorsqu'un groupe est plié, et réaligner verticalement les tâches suivantes.
- **FR-014b** : L'ajout de tâche DOIT insérer la nouvelle tâche sous la dernière tâche sélectionnée, avec le même parent. Sans sélection, elle s'ajoute à la fin sans parent.
- **FR-015** : L'application DOIT calculer et permettre d'afficher ou masquer le chemin critique.
- **FR-016** : L'interface DOIT permettre :
  - D'élargir ou rétrécir le panneau de gauche via une bordure cliquable et glissable (splitter).
  - De masquer d'un coup le panneau de gauche (bouton chevron gauche) et de le réafficher (bouton chevron droit).
- **FR-017** : Le diagramme de Gantt (panneau de droite) DOIT intégrer :
  - Un bouton "Zoom avant" (allonge la largeur des rectangles).
  - Un bouton "Zoom arrière" (raccourcit la largeur des rectangles).
  - Une échelle de temps graduée s'adaptant au zoom (jour, semaine, mois, trimestre, semestre, année).
- **FR-018** : Le système DOIT maintenir un historique des actions (Annuler/Rétablir) avec une profondeur minimale de 100 actions.
- **FR-019** : Le système DOIT supporter les opérations de presse-papiers (Copier, Couper, Coller) sur les tâches.
- **FR-020** : Le système DOIT offrir une fonctionnalité d'impression optimisée pour le diagramme de Gantt.
- **FR-021** : Le système DOIT recalculer automatiquement les dates des tâches parentes (groupes). La date de début d'un parent correspond à la date de début la plus ancienne de ses enfants, et sa date de fin correspond à la date de fin la plus tardive de ses enfants. La durée de la tâche parente est déduite de ces bornes.

### Exigences d'Interface Graphique (IHM)

- **UI-001 (Vue scindée - Split View)** : L'interface DOIT reprendre la disposition classique de GanttProject avec une vue divisée verticalement : 
  - **Volet gauche** : Un tableau de données hiérarchique (WBS) listant les tâches, leurs dates de début, de fin et leurs durées.
  - **Volet droit** : La frise chronologique (Gantt chart) interactive avec les barres horizontales et les flèches de dépendance.
- **UI-002 (Synchronisation du défilement)** : Le défilement vertical du tableau à gauche et du diagramme à droite DOIT être parfaitement synchronisé.
- **UI-003 (Barre d'outils WBS & Gantt)** : L'en-tête du panneau de gauche (WBS) DOIT intégrer ses propres boutons (hiérarchie, filtres, colonnes, liaisons). L'en-tête du diagramme de Gantt DOIT intégrer ses contrôles de Zoom.
- **UI-004 (Thématisation)** : L'interface DOIT proposer un mode clair (Light Mode) et un mode sombre (Dark Mode). Le mode **clair** DOIT être activé par défaut.
- **UI-005 (Splitter dynamique)** : Une barre de redimensionnement interactive DOIT séparer les deux panneaux, avec des boutons de masquage rapide.
- **UI-006 (Insertion contextuelle)** : L'ajout de nouvelles tâches DOIT s'effectuer contextuellement sous la sélection active.
- **UI-007 (Indicateurs d'états)** : Les boutons nécessitant des conditions spécifiques (ex: "désindenter" sur une tâche racine) DOIVENT être grisés/désactivés visuellement.

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
