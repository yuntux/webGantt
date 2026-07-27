# Quickstart & Validation Guide

Ce guide documente la façon de valider que les fonctionnalités de type GanttProject sont implémentées correctement au sein du fichier `webGantt.html`.

## Prérequis
- Un navigateur web moderne récent (Chrome/Edge/Firefox).
- Le fichier local `webGantt.html`.

## Exécution
1. Ouvrez `webGantt.html` directement dans le navigateur en double-cliquant dessus (le protocole sera `file://`).
2. L'interface de création de diagramme de Gantt doit s'afficher.

## Scénarios de Validation de bout en bout

### 1. Test Exhaustif du Parseur XML avec `example.gan`
- **Action** : Cliquez sur le bouton "Ouvrir un projet" et sélectionnez le fichier `assets/example.gan`.
- **Résultat Attendu** : Le fichier est chargé instantanément. L'interface affiche toutes les vues, les congés, les tâches (et leurs sous-tâches, hiérarchies, notes, propriétés), les dépendances, les ressources et les lignes de base.

### 2. Création de Tâches et Dépendances
- **Action** : Modifiez le projet en ajoutant une "Tâche 1". Créez une "Tâche 2". Tirez un lien depuis la fin de "Tâche 1" vers le début de "Tâche 2" (Dépendance Fin-à-Début). Déplacez "Tâche 1" vers la droite (plus tard dans le temps).
- **Résultat Attendu** : "Tâche 2" se décale automatiquement dans le temps pour respecter la dépendance "Fin-à-Début", sans chevauchement.

### 3. Ressources
- **Action** : Allez dans l'onglet "Ressources", ajoutez "Alice". Retournez au Gantt, sélectionnez "Tâche 1" et assignez "Alice".
- **Résultat Attendu** : Le nom "Alice" s'affiche à côté de la barre de "Tâche 1".

### 4. Enregistrer sous un nouveau fichier `.gan`
- **Action** : Cliquez sur "Enregistrer sous" (ou "Enregistrer le projet").
- **Résultat Attendu** : Le navigateur vous propose de sauvegarder un nouveau fichier `.gan` (ou écrase l'existant via l'API File System Access). Le fichier généré doit être un XML valide, conforme au `ganttproject.xsd`, contenant toutes les modifications apportées (Tâches, Dépendances, Ressources). Il doit pouvoir s'ouvrir parfaitement dans GanttProject (le logiciel original).
