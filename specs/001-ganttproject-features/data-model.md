# Phase 1: Data Model

Le modèle de données représente le contenu du fichier XML (extension `.gan`) qui sera lu et écrit par webGantt. Il est aligné avec le schéma formel `ganttproject.xsd` généré à partir de `XmlSerializer.kt`.

## Entités Principales

### Project (Projet)
L'élément racine `<project>` possède des attributs globaux :
- `name`, `company`, `webLink`, `version`, `locale`, etc.
Il contient les sections enfants : `<description>`, `<view>`, `<calendars>`, `<tasks>`, `<resources>`, `<allocations>`, `<vacations>`, `<previous>` (lignes de base), `<roles>`.

### Task (Tâche)
Correspond aux balises `<task>` dans la section `<tasks>`.
- **Attributs XML** : 
  - `id` (Int) : Identifiant unique de la tâche.
  - `uid` (String) : Identifiant unique interne.
  - `name` (String) : Nom ou titre de la tâche.
  - `start` (String, format YYYY-MM-DD) : Date de début prévue.
  - `duration` (Int) : Durée en jours.
  - `complete` (Int, 0-100) : Pourcentage d'avancement.
  - `meeting` (Boolean) : Indique si la tâche est un jalon (durée = 0).
  - `color`, `shape`, `priority`, `webLink`, `expand` : Propriétés visuelles et métadonnées.
- **Enfants** :
  - `<notes>` : Description textuelle de la tâche.
  - `<depend>` : Les dépendances de cette tâche.
  - `<customproperty>` : Propriétés personnalisées.
  - `<task>` : Sous-tâches (structure récursive pour le WBS).

### Dependency (Dépendance)
Correspond aux balises `<depend>` sous une `<task>`.
- `id` (Int) : ID de la tâche cible (qui dépend de la tâche courante).
- `type` (String) : Type de contrainte. Ex: `"FS"` (Finish-to-Start).
- `difference` (Int) : Décalage/lag temporel.
- `hardness` (String) : Dureté de la contrainte ("Strong", "Rubber").

### Resource (Ressource)
Correspond aux balises `<resource>` dans la section `<resources>`.
- `id` (Int) : Identifiant unique de la ressource.
- `name` (String) : Nom de la personne ou de l'actif.
- `function` (String) : Rôle ou fonction (doit correspondre à un ID défini dans `<roles>`).
- `contacts`, `phone` : Informations de contact.

### Allocation (Affectation)
Correspond aux balises `<allocation>` dans la section `<allocations>`.
- `task-id` (Int) : ID de la tâche concernée.
- `resource-id` (Int) : ID de la ressource assignée.
- `function` (String) : Rôle pour cette assignation spécifique.
- `load` (Float) : Charge de travail (ex: 100.0).
- `responsible` (Boolean) : Indique le coordinateur de la tâche.

## Contrat de Structure
Le document formel décrivant toutes les contraintes de ce modèle est désormais le fichier `assets/ganttproject.xsd`. Le fichier `contracts/project-schema.json` (qui définissait l'ancienne structure JSON) est obsolète et peut être ignoré.
