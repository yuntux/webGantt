# Documentation webGantt

**webGantt** est une application web d'édition et de visualisation de diagrammes de Gantt, conçue pour être 100% compatible avec le format XML `.gan` de l'application open-source de référence GanttProject.

Cette documentation a pour but de présenter le fonctionnement global de l'application et les configurations avancées disponibles via le menu des préférences.

---

## Chapitre 1 : Les Préférences du Projet

La fenêtre des **Préférences** permet de paramétrer finement l'affichage de l'interface, des composants du diagramme de Gantt et du planificateur de ressources. Ces préférences sont directement persistées dans votre fichier `.gan` et s'appliquent de manière portable (si le fichier est ouvert par un autre utilisateur ou sous GanttProject, la configuration graphique est conservée).

La fenêtre est divisée en trois onglets : **Général**, **Propriétés du diagramme de Gantt**, et **Propriétés du diagramme des ressources**.

### 1.1 Onglet "Général"

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

### 1.2 Onglet "Propriétés du diagramme de Gantt"

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

### 1.3 Onglet "Propriétés du diagramme des ressources"

Ce troisième onglet sert à configurer le panneau inférieur de l'application (l'arbre et la timeline des ressources matérielles ou humaines), et en particulier la coloration conditionnelle liée au taux de charge hebdomadaire de ces ressources.

| Nom du champ | Valeurs possibles | Effet du paramètre | XPath dans le fichier .gan |
| --- | --- | --- | --- |
| Ressources | Couleur hex (ex: `#90b6d3`) | Couleur de fond standard des intervalles où la ressource travaille normalement (charge <= 100%). | `//view[@id='resource-table']/option[@id='res.color']/@value` |
| Ressources (surchargées) | Couleur hex (ex: `#e14436`) | Couleur d'alerte pour les périodes où la ressource est assignée à plus de 100% (conflits d'agenda). | `//view[@id='resource-table']/option[@id='res.overloadedColor']/@value` |
| Ressources (sous employées) | Couleur hex (ex: `#3bd93b`) | Couleur marquant les périodes où la ressource n'atteint pas le quota d'heures prévu (optionnel). | `//view[@id='resource-table']/option[@id='res.underloadedColor']/@value` |
| Jours de congés | Couleur hex (ex: `#ffff55`) | Couleur utilisée pour dessiner l'arrière-plan des plages d'inactivité ou de vacances signalées pour cette ressource. | `//view[@id='resource-table']/option[@id='res.vacationColor']/@value` |
