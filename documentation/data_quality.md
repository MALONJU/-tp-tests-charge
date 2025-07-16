# 1. Qualité des Données

## 1.1 Types de Données Manipulées

Ce document identifie les types de données manipulées par notre plateforme BuyYourKawa, leurs formats, contraintes et normes appliquées.

### Tableau des Types de Données

| Champ               | Type    | Contraintes                             | Norme/Format            |
|---------------------|---------|----------------------------------------|-------------------------|
| client_id           | UUID    | non null, unique                       | RFC 4122               |
| name                | string  | non null, min 2 chars, max 100 chars   | UTF-8                  |
| email               | string  | non null, regex validation             | RFC 5322               |
| phone               | string  | non null, regex validation             | E.164 (format international) |
| created_at          | datetime| non null, auto-generated               | ISO 8601               |
| updated_at          | datetime| non null, auto-updated                 | ISO 8601               |
| street              | string  | non null, max 200 chars                | UTF-8                  |
| city                | string  | non null, max 100 chars                | UTF-8                  |
| zip                 | string  | non null, max 20 chars                 | Alphanumérique         |
| country             | string  | non null, max 100 chars                | ISO 3166-1             |

## 1.2 Formats d'Échange et Encodage

### API REST

- **Format de requête/réponse**: JSON
- **Encodage**: UTF-8
- **Content-Type**: application/json

### Exemple de Payload

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+33123456789",
  "address": {
    "street": "123 Rue Example",
    "city": "Paris",
    "zip": "75000",
    "country": "France"
  }
}
```

## 1.3 Validation et Conformité

### Niveau API

- Validation automatique via Pydantic/FastAPI
- Sanitisation des entrées avant stockage
- Transformation des formats (ex: numéros de téléphone en format E.164)

### Niveau Base de Données

- Contraintes d'intégrité (clés primaires, clés étrangères)
- Indexes pour optimisation des requêtes
- Triggers pour maintenir created_at/updated_at
