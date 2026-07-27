# Phase 0: Research & Decisions

## Décision 1 : API d'Accès aux Fichiers
- **Décision** : Utiliser l'API File System Access (méthode `showOpenFilePicker()` et `showSaveFilePicker()`) avec un fallback classique (`<input type="file">` et lien de téléchargement `<a download>`) pour une compatibilité maximale.
- **Raisonnement** : L'API File System Access permet une expérience utilisateur fluide similaire à une application de bureau (GanttProject), permettant d'enregistrer les modifications directement dans le même fichier, comme exigé par le principe "Direct Data Selection from UI".
- **Alternatives considérées** : Exclusivement `<input type="file">`, mais cela oblige à "télécharger" un nouveau fichier à chaque sauvegarde au lieu de modifier l'original.

## Décision 2 : Rendu Graphique du Diagramme de Gantt
- **Décision** : Utiliser le rendu DOM (HTML/CSS avec CSS Grid/Flexbox et positionnement absolu pour la frise chronologique) ou un mix DOM+SVG. Le rendu DOM + SVG (SVG pour les liens de dépendance + `div` pour les barres de tâches) est choisi pour faciliter les interactions (survol, clic, drag-and-drop).
- **Raisonnement** : Le DOM natif est plus accessible, plus simple à styliser avec CSS Vanilla, et très performant pour un nombre de tâches inférieur à 1000, ce qui correspond à nos exigences de 500 tâches en moins de 1 seconde.
- **Alternatives considérées** : `<canvas>`, qui serait plus performant pour des dizaines de milliers de tâches mais complexifie drastiquement la gestion des événements (clics) et la modification du style. L'approche Canvas viole implicitement le principe "Simplicity" et la manipulation facile.
