# Implementation Plan: GanttProject Features Parity

**Branch**: `001-ganttproject-features` | **Date**: 2026-07-27 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-ganttproject-features/spec.md`

## Résumé

Implémenter les fonctionnalités principales de GanttProject (tâches, dépendances, ressources, lignes de base) dans webGantt, une application web entièrement locale contenue dans un fichier HTML unique, gérant ses données via un fichier externe au format natif de GanttProject (`.gan`, qui est du XML).

## Technical Context

**Language/Version**: HTML5, CSS3, Vanilla JavaScript (ES6+)

**Primary Dependencies**: Aucune dépendance externe requise au runtime (conformément à l'architecture fichier unique). API File System Access pour la gestion de fichiers.

**Storage**: Fichier système local via sélection de fichier `.gan` (XML) (pas de backend).

**Testing**: Tests End-to-End via Playwright (pour valider le DOM et les interactions graphiques complexes du diagramme de Gantt) en environnement de dev.

**Target Platform**: Navigateurs web modernes (Chrome, Firefox, Safari, Edge).

**Project Type**: Application web locale à fichier unique (Single-file web application).

**Performance Goals**: Rendu du diagramme de Gantt pour 500 tâches en moins d'1 seconde.

**Constraints**: L'application DOIT tenir dans un seul fichier final combinant HTML, CSS et JS. Aucune requête réseau au runtime.

**Scale/Scope**: Projets jusqu'à 500 tâches (scénario de test).

## Constitution Check

*GATE: Passed*

- **Fully Local & Single-File Architecture**: Respecté, aucun backend, tout en un fichier.
- **GanttProject Parity**: Respecté, le plan couvre les tâches, dépendances, jalons et ressources.
- **Efficient User Interface**: Respecté (Vanilla JS garantit des perfs optimales si bien écrit).
- **Stockage de Données Découplé** : Respecté, l'architecture prévoit l'API File System Access pour gérer le fichier `.gan` externe.
- **Direct Data Selection from UI**: Respecté.

## Project Structure

### Documentation (this feature)

```text
specs/001-ganttproject-features/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

### Source Code (repository root)

```text
/
└── webGantt.html        # Le livrable final (fichier unique HTML+CSS+JS)
```

**Structure Decision**: La constitution impose une application contenue dans un seul fichier. Tout le code source sera organisé au sein de `webGantt.html` avec des sections `<style>` et `<script>` distinctes pour la maintenabilité.
