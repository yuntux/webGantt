<!--
Rapport d'Impact de Synchronisation :
- Changement de version : Brouillon Initial → 1.0.0
- Principes modifiés :
  - [PRINCIPLE_1_NAME] → Architecture Entièrement Locale & Fichier Unique
  - [PRINCIPLE_2_NAME] → Parité avec GanttProject
  - [PRINCIPLE_3_NAME] → Interface Utilisateur Efficace
  - [PRINCIPLE_4_NAME] → Stockage de Données JSON Découplé
  - [PRINCIPLE_5_NAME] → Sélection Directe des Données depuis l'UI
- Sections ajoutées : Architecture & Pile Technologique, Flux de Développement & de Révision
- Sections supprimées : Aucune
- Modèles nécessitant des mises à jour :
  - .specify/templates/plan-template.md (⚠ en attente)
  - .specify/templates/spec-template.md (⚠ en attente)
  - .specify/templates/tasks-template.md (⚠ en attente)
- TODOs de suivi : Aucun
-->

# Constitution webGantt

## Principes Fondamentaux

### I. Architecture Entièrement Locale & Fichier Unique
L'application DOIT être entièrement contenue dans un seul fichier (combinant HTML, CSS et JS) pour assurer la portabilité et la facilité de distribution. Elle DOIT s'exécuter complètement localement dans le navigateur sans nécessiter de serveur backend ni de dépendances externes à l'exécution.

### II. Parité avec GanttProject
L'ensemble des fonctionnalités de base DOIT correspondre aux capacités de GanttProject. Cela inclut la création de tâches, la gestion des dépendances, la planification et le rendu de diagrammes de Gantt clairs et précis.

### III. Interface Utilisateur Efficace
L'interface utilisateur DOIT privilégier l'efficacité, la réactivité et l'ergonomie. Les interactions doivent être simplifiées pour permettre aux utilisateurs de construire et de modifier des diagrammes de Gantt rapidement sans friction inutile.

### IV. Stockage de Données JSON Découplé
Les données de l'application NE DOIVENT PAS être codées en dur ou stockées exclusivement dans le stockage local du navigateur pour une persistance à long terme. Toutes les données du projet DOIVENT être stockées dans un fichier JSON standard séparé, garantissant la portabilité et l'interopérabilité des données.

### V. Sélection Directe des Données depuis l'UI
L'application DOIT fournir une interface graphique intégrée pour sélectionner, charger et enregistrer directement le fichier de données JSON depuis le système de fichiers local de l'utilisateur.

## Architecture & Pile Technologique

L'application sera construite en utilisant des technologies web standards :
- HTML5 pour la structure
- CSS Vanilla ou framework minimal pour le style
- JavaScript Vanilla pour la logique et l'interactivité
- API File System Access ou balise `<input type="file">` standard et liens de téléchargement pour la gestion des fichiers locaux.
- Aucune étape de compilation ou de regroupement n'est strictement requise pour l'artefact final, car l'objectif est un fichier unique contenu.

## Flux de Développement & de Révision

- Toute modification DOIT maintenir la contrainte de sortie en un seul fichier.
- Les nouvelles fonctionnalités DOIVENT être testées pour les performances et l'efficacité de l'interface utilisateur.
- Les structures de données dans le fichier JSON DOIVENT rester rétrocompatibles ou fournir un chemin de migration explicite si le schéma change.

## Gouvernance

Cette Constitution remplace toutes les autres pratiques.
Les amendements nécessitent de la documentation, une approbation et une justification claire. Toutes les "pull requests" ou modifications de code doivent vérifier la conformité avec la contrainte de fichier unique et les principes fondamentaux énoncés ci-dessus.

**Version** : 1.0.0 | **Ratifiée** : 2026-07-27 | **Dernière Modification** : 2026-07-27
