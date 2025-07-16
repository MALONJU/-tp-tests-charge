# 4. Plan d'Actions Correctives

Ce document présente les actions correctives identifiées suite aux tests de charge réalisés sur l'API BuyYourKawa.

## 4.1 Tableau des Actions Correctives

| Endpoint         | KPI Observé | Seuil    | Problème                    | Action Corrective                        | Délai |
|------------------|-------------|----------|-----------------------------|-----------------------------------------|--------|
| `/token`         | 780 ms      | < 300ms  | Temps de réponse élevé      | Optimisation de l'authentification + cache Redis | 48h   |
| `/token`         | 2% erreurs  | < 0.5%   | Échecs d'authentification   | Augmentation des timeouts et mécanisme de retry | 24h   |
| `/clients` (GET) | 350 ms      | < 250ms  | Latence base de données     | Ajout d'index + mise en cache des résultats | 36h   |
| `/clients` (POST)| 580 ms      | < 400ms  | Traitement lent des écritures | Optimisation des validations et transactions | 72h   |
| `/clients` (POST)| 4% erreurs  | < 1%     | Erreurs 500 lors des créations | Validation renforcée + gestion des exceptions | 48h   |
| `/clients/{id}`  | 0.5% erreurs| < 0.1%   | Clients non trouvés         | Amélioration de la gestion des erreurs 404 | 24h   |

## 4.2 Justification des Actions Correctives

### 4.2.1 Optimisation de l'Authentification (`/token`)

**Problème détaillé**: 
L'authentification est un goulot d'étranglement avec un temps médian de 780ms, bien au-dessus du seuil acceptable de 300ms. L'analyse des logs montre que la vérification des identifiants et la génération du token JWT sont les étapes les plus lentes.

**Solution proposée**:
- **Cache Redis pour les tokens**: Stocker temporairement les tokens JWT valides
- **Réduction de la complexité du hachage**: Ajuster le coût du bcrypt (actuellement trop élevé)
- **Optimisation de la génération JWT**: Utiliser une bibliothèque plus performante

**Métriques attendues après correction**:
- Temps de réponse médian < 200ms
- Réduction de 75% du temps CPU pour l'authentification
- Capacité d'authentification doublée

### 4.2.2 Optimisation des Requêtes GET (`/clients`)

**Problème détaillé**:
La récupération de la liste des clients prend 350ms en médiane et génère une forte charge sur la base de données, particulièrement lors des pics d'utilisation.

**Solution proposée**:
- **Indexation optimisée**: Création d'index composites sur les champs fréquemment utilisés
- **Cache Redis**: Mise en cache des résultats de requêtes fréquentes avec expiration de 5 minutes
- **Pagination optimisée**: Utilisation de cursors plutôt que d'offset pour améliorer les performances

**Métriques attendues après correction**:
- Temps de réponse médian < 150ms
- Charge CPU de la base de données réduite de 40%
- Capacité de traitement des requêtes augmentée de 60%

### 4.2.3 Amélioration des Créations de Clients (`/clients` POST)

**Problème détaillé**:
La création de nouveaux clients génère 4% d'erreurs et prend 580ms en médiane, principalement dû à des validations excessives et des contraintes d'unicité non optimisées.

**Solution proposée**:
- **Validation optimisée**: Restructuration des validations pour les exécuter en parallèle
- **Transactions optimisées**: Réduction du temps de verrouillage des tables
- **Gestion d'exceptions améliorée**: Capture précise des exceptions avec messages explicites
- **File d'attente asynchrone**: Pour les opérations lourdes comme les notifications

**Métriques attendues après correction**:
- Temps de réponse médian < 300ms
- Taux d'erreur < 0.5%
- Débit augmenté de 50%

## 4.3 Priorisation et Plan d'Implémentation

### Phase 1 (24-48h)
1. Mise en place du cache Redis pour l'authentification
2. Amélioration de la gestion des erreurs 404
3. Augmentation des timeouts pour les requêtes d'authentification

### Phase 2 (48-72h)
1. Optimisation des index de base de données
2. Mise en cache des résultats de requêtes GET
3. Validation renforcée pour les requêtes POST

### Phase 3 (72h+)
1. Implémentation de la file d'attente asynchrone
2. Optimisation complète des transactions
3. Revue globale des performances
