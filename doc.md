# Documentation webGantt

**webGantt** est une application web d'édition et de visualisation de diagrammes de Gantt, conçue pour être 100% compatible avec le format XML `.gan` de l'application open-source de référence GanttProject.

Cette documentation a pour but de présenter le fonctionnement global de l'application et les configurations avancées disponibles via le menu des préférences.

---



## Chapitre 1 : Introduction & Architecture de l'Application

### 1.1 Principe et Interopérabilité
**webGantt** est conçu pour fonctionner intégralement et de manière autonome au sein de votre navigateur web. Il n'utilise aucune base de données côté serveur, ce qui garantit la confidentialité totale de vos plannings. Le moteur de l'application lit, interprète, et génère directement des fichiers XML portant l'extension `.gan`.
Cette approche garantit une interopérabilité absolue avec le logiciel de bureau open-source **GanttProject** (un standard de l'industrie de la gestion de projet).

### 1.2 L'Interface Principale
La zone de travail est structurée autour d'un redimensionnement dynamique (*splitter*) :
- **À gauche (Panneau WBS)** : L'arborescence des tâches ou la liste de vos ressources. Il prend généralement 30% à 40% de l'écran.
- **À droite (Panneau Graphique)** : La ligne de temps dynamique (timeline) affichant le diagramme de Gantt ou la carte d'occupation des ressources.

### 1.3 Actions Globales de la Barre d'Outils
La barre d'outils supérieure rassemble les contrôles vitaux du cycle de vie du projet :
- **Ouvrir** : Analyse et charge instantanément un fichier `.gan` local. 
- **Sauvegarder** : Compile l'état actuel de votre écran (incluant les préférences graphiques) et déclenche le téléchargement d'un nouveau fichier XML valide.
- **Bouton Thème (Clair/Sombre)** : Alterne les variables CSS de l'application pour offrir un mode sombre profond (idéal pour réduire la fatigue visuelle) ou un mode clair classique.
- **Propriétés du Projet** : Permet de définir les métadonnées globales (Nom du projet, Entreprise, URL) ainsi que les calendriers des week-ends et jours fériés généraux qui impacteront toutes les tâches.

---

## Chapitre 2 : L'arborescence des Tâches (WBS)

La *Work Breakdown Structure* (WBS) est le tableau de bord structurel de votre projet.

### 2.1 Manipulation des Tâches
- **Ajout rapide** : Cliquez sur "Ajouter une tâche". Si une tâche est déjà sélectionnée, la nouvelle ligne s'insèrera immédiatement sous la sélection, en héritant de son parent direct. Un identifiant unique de tâche (`id`) est automatiquement généré en arrière-plan.
- **Édition directe (Inline)** : Un double-clic sur certaines colonnes (comme le Nom) permet une édition instantanée sans ouvrir les propriétés avancées.
- **Masquer le panneau** : Si vous souhaitez vous concentrer sur l'aspect calendaire, le bouton de repli (◀) situé en haut du panneau WBS permet de cacher ce dernier pour passer le diagramme de Gantt en plein écran.

### 2.2 Hiérarchisation et Structure
La barre d'outils dédiée au WBS (située au-dessus de la liste des tâches) propose des outils de déplacement structurel. Les règles de grisage (activation/désactivation) s'assurent que la structure reste logiquement cohérente.
- **Indenter (flèche droite →)** : Décale la tâche sélectionnée vers la droite. La tâche située juste au-dessus devient alors une "tâche mère" (ou résumé de phase). **Attention** : Les dates d'une tâche mère sont automatiquement calculées en fonction de ses enfants. Vous ne pouvez plus éditer manuellement les dates d'une tâche mère.
- **Désindenter (flèche gauche ←)** : Ramène la sous-tâche au niveau supérieur (soeur de son ancien parent).
- **Monter (↑) / Descendre (↓)** : Modifie l'ordre d'affichage vertical de deux tâches ayant le même parent et le même niveau de profondeur.

### 2.3 Multisélection
L'interface gère la multisélection : maintenez la touche `Ctrl` (ou `Cmd` sous Mac) pour sélectionner plusieurs tâches éparses, ou `Shift` pour sélectionner un bloc entier. Cela est particulièrement utile pour appliquer des liaisons de masse (voir Chapitre 3) ou supprimer un lot.

---

## Chapitre 3 : Diagramme de Gantt et Liens de Dépendance

Le diagramme de droite convertit vos données WBS en une représentation temporelle claire.

### 3.1 Représentations Visuelles
- **Tâches classiques** : Rectangles colorés (par défaut bleus).
- **Tâches Mères (Groupes)** : Barres noires ou foncées avec des extrémités biseautées englobant temporellement toutes leurs sous-tâches.
- **Jalons (Milestones)** : Les tâches dont la durée est de 0 jour (marquant la fin d'une phase, par exemple un rendu de livrable) sont automatiquement représentées par un losange.

### 3.2 Gestion des Dépendances (Chaînage)
Au lieu de modifier manuellement les dates de chaque tâche, l'application utilise un moteur de contraintes :
- **Lier (🔗)** : Sélectionnez chronologiquement plusieurs tâches dans le WBS à l'aide de la touche `Ctrl`. Cliquez sur "Lier" : des relations "Fin-à-Début" (FS) seront créées. La tâche B ne pourra pas démarrer avant la fin de la tâche A.
- **Délier (⛓️‍💥)** : Permet de casser toutes les relations entre les tâches actuellement sélectionnées.
*Note technique : Le moteur recalcule en temps réel l'ensemble du planning si la tâche "A" subit un retard.*

### 3.3 Contrôles Graphiques Avancés
- **Zoom (+ / -)** : Ajuste dynamiquement l'échelle temporelle (axe X). Vous pouvez passer d'une vue détaillée "Jours / Semaines" à une vue "Mois / Années" pour les projets au long cours.
- **Filtrage (Entonnoir)** : Ouvre un menu déroulant permettant d'épurer le diagramme.
  - *Non terminées* : Masque ce qui est à 100% d'avancement.
  - *À faire aujourd'hui* / *En retard* : Se base sur la date système courante pour cibler l'urgence.
- **Chemin Critique** : Activez l'icône de chemin critique pour afficher en rouge continu le chemin temporel inaltérable du projet. Toute tâche située sur ce chemin (qui n'a aucune marge de sécurité) décalera la date de livraison finale du projet si sa propre durée s'allonge.

---

## Chapitre 4 : Gestion des Ressources Humaines et Matérielles

Les ressources sont au cœur de la planification capacitaire de **webGantt**.

### 4.1 La base de Ressources
- Basculez sur l'espace "Ressources" (en bas ou onglet de vue) pour lister votre équipe.
- Ajoutez de nouvelles ressources en définissant des données de contact (Nom, Email, Téléphone).
- Vous pouvez définir un **Coût Standard** (taux horaire ou journalier) qui servira, couplé à la durée des tâches, au calcul automatisé du coût total du projet.

### 4.2 Les Rôles
Les rôles normalisent les intitulés de postes (ex: *Architecte Cloud*, *Ingénieur QA*, *Consultant Fonctionnel*).
- Ils se créent globalement via le menu **Propriétés du Projet**.
- Une fois créés, vous pouvez assigner un Rôle par défaut à chaque ressource. Cela permet de grouper l'équipe par corps de métier.

### 4.3 Jours de Congés Individuels (Calendrier de Ressource)
Outre le calendrier du projet (week-ends et jours fériés globaux), webGantt gère l'indisponibilité individuelle.
- Dans les détails d'une ressource, accédez à son **Calendrier de jours de congés**.
- Toute plage déclarée en congé suspendra le travail de cette ressource sur le Gantt. Les tâches qui lui sont affectées exclusives subiront automatiquement un allongement de leur durée réelle (saut par-dessus les congés).

---

## Chapitre 5 : Affectation, Taux de Charge et Planification

### 5.1 Affecter une ressource
Ouvrez le panneau de **Propriétés avancées de la tâche** (icône d'engrenage sur une ligne du WBS, ou double-clic).
- Dans l'onglet **Ressources**, vous pouvez sélectionner un intervenant dans la liste.
- Vous devez définir un **Taux de charge (Unités)** en pourcentage. Un taux de `100%` signifie un emploi à temps plein de l'individu sur la tâche. Un taux de `50%` indique une charge à temps partiel.
- **Responsable** : L'option "Coordinator" (Responsable) permet de désigner spécifiquement une personne (parmi celles affectées) comme chef d'orchestre de la tâche.

### 5.2 Le Diagramme d'occupation et la Surcharge
Dans le panneau des ressources, la frise chronologique n'affiche pas des tâches, mais des **barres d'occupation**.
- Ces barres cumulent mathématiquement le taux de charge d'une personne si elle est affectée à plusieurs tâches se chevauchant.
- Si le cumul des charges journalières dépasse **100%**, la barre se colore en rouge (Surcharge / *Overloaded*). Cela indique un conflit d'agenda qu'il faudra résoudre (en lissant les dates ou en réduisant le taux de charge).
- *(Note : les couleurs d'alerte, de charge normale et de sous-charge sont personnalisables dans les Préférences du Projet).*

---

## Chapitre 6 : Colonnes, Champs Personnalisés et Lignes de Base

### 6.1 Le Sélecteur de Colonnes WBS (⚙️)
La liste des tâches possède un bouton d'engrenage dans son en-tête. Il déclenche un menu contextuel permettant d'afficher ou masquer à la volée n'importe quel attribut système (Date de début, Date de fin, % d'avancement, Coût, Durée). 
*L'état d'affichage des colonnes est temporaire afin d'optimiser l'espace visuel.*

### 6.2 Les Champs Personnalisés (Custom Properties)
Si le standard ne suffit pas à votre métier, webGantt permet de créer des méta-données :
- Allez dans **Propriétés du Projet** > Onglet **Champs personnalisés**.
- Créez un champ (Ex: "Ticket Jira", "Phase de Validation", "Budget Estimé").
- Vous devez choisir un type strict : *Texte*, *Date*, *Entier*, *Booléen* ou *Double*.
- Une fois créés, ces champs apparaissent automatiquement sous forme de nouvelles colonnes dans l'arbre WBS et de nouveaux champs de saisie dans le détail de chaque tâche.

### 6.3 Lignes de Base (Baselines / Empreintes)
La planification est un métier itératif. Une fois le planning validé, vous pouvez créer une **Ligne de Base**.
- Une ligne de base effectue un "instantané" silencieux des dates prévues de toutes les tâches à l'instant T.
- Au fil du déroulement du projet, si les tâches prennent du retard, vous pourrez afficher la ligne de base sur le diagramme de Gantt. L'interface superposera (généralement en gris) le rectangle des dates d'origine sous le rectangle coloré courant, exposant visuellement le dérapage ou l'avance du planning.

---

## Chapitre 7 : Les Préférences du Projet


La fenêtre des **Préférences** permet de paramétrer finement l'affichage de l'interface, des composants du diagramme de Gantt et du planificateur de ressources. Ces préférences sont directement persistées dans votre fichier `.gan` et s'appliquent de manière portable (si le fichier est ouvert par un autre utilisateur ou sous GanttProject, la configuration graphique est conservée).

La fenêtre est divisée en trois onglets : **Général**, **Propriétés du diagramme de Gantt**, et **Propriétés du diagramme des ressources**.

### 7.1 Onglet "Général"

Cet onglet permet de contrôler l'apparence globale du logiciel (UI) ainsi que les formats régionaux (langue, format des dates).

| Nom du champ | Valeurs possibles | Effet du paramètre | XPath dans le fichier .gan |
| --- | --- | --- | --- |
| Apparence | `Plastic`, etc. | Thème visuel global de l'interface. | `//view[@id='gantt-chart']/option[@id='general.appearance']/@value` |
| Polices de l'application | Liste des polices (ex: `default`) | Définit la police de caractères utilisée pour l'UI. | `//view[@id='gantt-chart']/option[@id='general.appFont']/@value` |
| (Taille police de l'application) | `1` à `5` (entier) | Ajuste la taille du texte de l'interface graphique. | `//view[@id='gantt-chart']/option[@id='general.appFontSize']/@value` |
| Polices de base graphique | Liste des polices (ex: `default`) | Définit la police utilisée pour le dessin SVG du graphe. | `//view[@id='gantt-chart']/option[@id='general.chartFont']/@value` |
| (Taille police graphique) | `1` à `5` (entier) | Ajuste la taille du texte à l'intérieur du diagramme SVG. | `//view[@id='gantt-chart']/option[@id='general.chartFontSize']/@value` |
| Espacement des lignes du tableau | Nombre décimal (ex: `20.0`, `32`) | Modifie la hauteur (en pixels) de chaque ligne de l'arborescence (WBS) et du diagramme. | `//view[@id='gantt-chart']/option[@id='general.rowSpacing']/@value` |
| DPI | Nombre (ex: `96`) | Densité de pixels simulée pour la définition des polices et impressions. | `//view[@id='gantt-chart']/option[@id='general.dpi']/@value` |
| Langue | `fr`, `en`, etc. | Langue de localisation des mois, jours de la semaine et labels UI. | `//view[@id='gantt-chart']/option[@id='general.language']/@value` |
| Utilisez le format de date | `default` ou `custom` | Choix entre le format dicté par le système ou un format saisi manuellement. | `//view[@id='gantt-chart']/option[@id='general.dateFormatType']/@value` |
| Format de date court personnalisé | Chaîne de format (ex: `dd/MM/y`) | Syntaxe de formatage appliquée à l'affichage des dates du projet. | `//view[@id='gantt-chart']/option[@id='general.dateFormat']/@value` |
| Fichier du logo | Chemin absolu ou relatif du fichier | Logo affiché sur les rapports et l'export du projet (pour impression). | `//view[@id='gantt-chart']/option[@id='general.logo']/@value` |

### 7.2 Onglet "Propriétés du diagramme de Gantt"

Ces options modifient le comportement natif des tâches et les informations textuelles ou visuelles dessinées autour de celles-ci.

| Nom du champ | Valeurs possibles | Effet du paramètre | XPath dans le fichier .gan |
| --- | --- | --- | --- |
| Préfixe de nom de tâche | Texte libre (ex: `tâche`) | Préfixe utilisé automatiquement lors de la création d'une nouvelle tâche. | `//view[@id='gantt-chart']/option[@id='gantt.taskPrefix']/@value` |
| Format du nom pour les tâches copiées | Format tokenisé (ex: `{0}_{1}`) | Gabarit d'automatisation utilisé pour renommer une tâche dupliquée. | `//view[@id='gantt-chart']/option[@id='gantt.taskCopyFormat']/@value` |
| Nouvelle tâche | Couleur hex (ex: `#8cb6ce`) | Couleur d'arrière-plan appliquée par défaut aux nouvelles tâches créées. | `//view[@id='gantt-chart']/option[@id='gantt.newTaskColor']/@value` |
| Contrainte | `Strong` ou `Rubber` | Type de contrainte d'enchaînement par défaut. Une contrainte forte ("Strong") déplace automatiquement une tâche en cas de retard. | `//view[@id='gantt-chart']/option[@id='gantt.constraint']/@value` |
| Afficher aujourd'hui avec une ligne rouge | `yes` ou `no` | Si activé, une ligne rouge verticale barre le diagramme à la date d'aujourd'hui. | `//view[@id='gantt-chart']/option[@id='gantt.todayLine']/@value` |
| Dates de début/fin du projet | `yes` ou `no` | Si activé, marque explicitement les limites globales du projet sur l'axe calendaire. | `//view[@id='gantt-chart']/option[@id='gantt.projectDates']/@value` |
| Style d'affichage des week-ends | `default` (grisé), etc. | Définit si les week-ends et jours chômés sont hachurés, grisés, ou masqués. | `//view[@id='gantt-chart']/option[@id='gantt.weekendStyle']/@value` |
| Numérotation des semaines | `default` (ISO), etc. | Mode de numérotation utilisé dans l'en-tête de la timeline du diagramme. | `//view[@id='gantt-chart']/option[@id='gantt.weekNumbering']/@value` |
| Afficher tous les jalons | Boîte à cocher (`true` ou `false`) | Indique si les tâches d'une durée de 0 (jalons) doivent être rendues (losange) dans le SVG. | `//view[@id='gantt-chart']/option[@id='gantt.showMilestones']/@value` |
| (Détails) Au-dessus | `name`, `resources`, `progress`, `duration`, ` ` | Définit la métrique affichée *au-dessus* de la barre rectangulaire SVG de la tâche. | `//view[@id='gantt-chart']/option[@id='gantt.detailTop']/@value` |
| (Détails) En-dessous | `name`, `resources`, `progress`, `duration`, ` ` | Définit la métrique affichée *en-dessous* de la barre rectangulaire SVG de la tâche. | `//view[@id='gantt-chart']/option[@id='gantt.detailBottom']/@value` |
| (Détails) A gauche | `name`, `resources`, `progress`, `duration`, ` ` | Définit la métrique affichée *à gauche* de la barre rectangulaire SVG de la tâche. | `//view[@id='gantt-chart']/option[@id='gantt.detailLeft']/@value` |
| (Détails) A droite | `name`, `resources`, `progress`, `duration`, ` ` | Définit la métrique affichée *à droite* de la barre rectangulaire SVG de la tâche. | `//view[@id='gantt-chart']/option[@id='gantt.detailRight']/@value` |

### 7.3 Onglet "Propriétés du diagramme des ressources"

Ce troisième onglet sert à configurer le panneau inférieur de l'application (l'arbre et la timeline des ressources matérielles ou humaines), et en particulier la coloration conditionnelle liée au taux de charge hebdomadaire de ces ressources.

| Nom du champ | Valeurs possibles | Effet du paramètre | XPath dans le fichier .gan |
| --- | --- | --- | --- |
| Ressources | Couleur hex (ex: `#90b6d3`) | Couleur de fond standard des intervalles où la ressource travaille normalement (charge <= 100%). | `//view[@id='resource-table']/option[@id='res.color']/@value` |
| Ressources (surchargées) | Couleur hex (ex: `#e14436`) | Couleur d'alerte pour les périodes où la ressource est assignée à plus de 100% (conflits d'agenda). | `//view[@id='resource-table']/option[@id='res.overloadedColor']/@value` |
| Ressources (sous employées) | Couleur hex (ex: `#3bd93b`) | Couleur marquant les périodes où la ressource n'atteint pas le quota d'heures prévu (optionnel). | `//view[@id='resource-table']/option[@id='res.underloadedColor']/@value` |
| Jours de congés | Couleur hex (ex: `#ffff55`) | Couleur utilisée pour dessiner l'arrière-plan des plages d'inactivité ou de vacances signalées pour cette ressource. | `//view[@id='resource-table']/option[@id='res.vacationColor']/@value` |
