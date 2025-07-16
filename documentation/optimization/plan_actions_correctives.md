# 4. Plan d'Actions Correctives

Ce document présente les actions correctives identifiées suite aux tests de charge réalisés sur l'API BuyYourKawa.

## 4.1 Tableau des Actions Correctives

| Endpoint         | KPI Observé | Seuil    | Problème                    | Action Corrective                        | Délai |
|------------------|-------------|----------|-----------------------------|-----------------------------------------|--------|
| `/token`         | 24.58 ms    | ✓ Rapide | 100% échecs d'authentification | Vérification des identifiants et format de requête | 12h   |
| `/token`         | 100% erreurs | < 0.5%   | Authentification impossible  | Correction de la vérification d'identité + logs détaillés | 12h   |
| `/token`         | -           | -        | Problème bloquant          | Test avec utilisateurs valides et vérification config | 4h    |
| Tous endpoints   | -           | -        | Tests incomplets            | Résolution authentification avant évaluation complète | 24h   |
| Saturation CPU   | Potentielle | < 80%    | Limitation CPU possible     | Vérification ressources serveur et monitoring | 8h    |

## 4.2 Justification des Actions Correctives

### 4.2.1 Résolution des Échecs d'Authentification (`/token`)

**Problème détaillé**: 
L'authentification échoue systématiquement (100% d'erreurs) malgré des temps de réponse exceptionnellement rapides (médiane de 19ms, moyenne de 24.58ms). Cette situation bloque l'exécution des autres tests puisque l'obtention d'un token JWT valide est un prérequis pour accéder aux autres endpoints.

**Solutions proposées**:
- **Vérification des identifiants**: Confirmer que les identifiants utilisés dans le script de test correspondent à un utilisateur valide dans la base de données
- **Format de requête**: Tester des formats alternatifs (JSON vs form-data) pour les requêtes d'authentification
- **Journalisation améliorée**: Ajouter des logs détaillés pour identifier la cause précise des échecs
- **Tests manuels**: Valider le fonctionnement de l'authentification avec un outil comme Postman avant de relancer les tests de charge

**Métriques attendues après correction**:
- Taux de succès d'authentification > 99.5%
- Maintien des excellents temps de réponse actuels (< 50ms)
- Déblocage des tests sur les autres endpoints

### 4.2.2 Vérification des Ressources Système

**Problème potentiel**:
Une hypothèse importante est que la saturation du CPU pourrait être la cause des échecs d'authentification lors des tests avec 300 utilisateurs simultanés. Même si les temps de réponse sont très rapides (19ms en médiane), le système pourrait refuser des connexions ou provoquer des timeouts si les ressources serveur sont saturées.

**Solutions proposées**:
- **Monitoring des ressources** : Mettre en place une surveillance de l'utilisation CPU/mémoire pendant les tests
- **Tests progressifs** : Exécuter des tests avec un nombre croissant d'utilisateurs (10, 50, 100, 200, 300) pour identifier le seuil de saturation
- **Dimensionnement des ressources** : Si nécessaire, augmenter les ressources serveur ou optimiser le code pour réduire l'utilisation CPU

**Métriques attendues après correction**:
- Utilisation CPU sous 80% même à pleine charge
- Stabilité du système avec 300 utilisateurs simultanés

### 4.2.3 Optimisation des Requêtes GET (`/clients`) - Pour les prochains tests

**Problème à anticiper**:
Une fois l'authentification résolue, nous pourrons évaluer les performances des autres endpoints. La récupération de la liste des clients pourrait générer une forte charge sur la base de données, particulièrement lors des pics d'utilisation.

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
