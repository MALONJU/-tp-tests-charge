# Documentation des Modèles de Données

## Modèle Client

| Champ         | Type   | Contraintes              | Norme      |
|---------------|--------|--------------------------|------------|
| id            | string | optionnel, unique        | UUID v4    |
| name          | string | requis                   |            |
| email         | string | requis, format email     | RFC 5322   |
| phone         | string | requis, format téléphone | E.164      |
| address       | object | requis                   |            |
| created_at    | datetime| optionnel                | ISO 8601   |
| updated_at    | datetime| optionnel                | ISO 8601   |

## Modèle Address

| Champ         | Type   | Contraintes              | Norme      |
|---------------|--------|--------------------------|------------|
| street        | string | requis                   |            |
| city          | string | requis                   |            |
| zip           | string | requis, format code postal |            |
| country       | string | requis                   | ISO 3166-1 |

## Points Critiques de l'API

### Endpoints Sensibles
1. `/token` - Authentification
   - Méthode : POST
   - Risque : Accès non autorisé
   - Importance : Critique

2. `/clients` - Gestion des clients
   - Méthodes : GET (liste), POST (création)
   - Risque : Fuite de données, création non contrôlée
   - Importance : Élevée

3. `/clients/{id}` - Client spécifique
   - Méthodes : GET (lecture), PUT/PATCH (mise à jour), DELETE
   - Risque : Modification/suppression non autorisée
   - Importance : Élevée
