# Documentation Technique HBnB Evolution - Part 1

## Table des Matières
1. [Introduction](#introduction)
2. [Architecture Générale](#architecture-générale)
3. [Conception du Modèle de Données](#conception-du-modèle-de-données)
4. [Flots des API](#flots-des-api)
5. [Principes de Conception](#principes-de-conception)
6. [Conclusion](#conclusion)

---

## Introduction

### Contexte du Projet
HBnB Evolution est une application de type AirBnB simplifiée développée dans le cadre d'un projet éducatif. Cette première partie (Part 1) se concentre sur la conception et la documentation technique de l'architecture du système, sans implémentation de code.

### Objectifs de la Documentation
Cette documentation sert de plan directeur pour le développement ultérieur de l'application. Elle définit :
- L'architecture en couches du système
- Les modèles de données et leurs relations
- Les interactions entre les composants
- Les flux de traitement des requêtes API

### Fonctionnalités Couvertes
L'application gère quatre entités principales :
- **Utilisateurs** : gestion des comptes, authentification
- **Lieux** : création et gestion des propriétés
- **Avis** : système de notation et commentaires
- **Commodités** : services et équipements des lieux

---

## Architecture Générale

### Pattern Architectural : Architecture en Couches

L'application suit une architecture en trois couches, séparant clairement les responsabilités :

#### 1. Couche de Présentation (Presentation Layer)
- **Responsabilité** : Gestion des interfaces utilisateur et API REST
- **Composants** : Contrôleurs API, endpoints REST, services web
- **Rôle** : Translation des requêtes externes vers la logique métier

#### 2. Couche de Logique Métier (Business Logic Layer)
- **Responsabilité** : Implémentation des règles métier et orchestration
- **Composants** : Services métier, modèles de domaine, facade
- **Rôle** : Application des règles business, validation, orchestration

#### 3. Couche de Persistance (Persistence Layer)
- **Responsabilité** : Accès et gestion des données
- **Composants** : Repositories, accès base de données
- **Rôle** : Abstraction de la persistance des données

### Pattern Facade
Le **HBnB Facade** sert de point d'entrée unique pour la communication entre la couche de présentation et la logique métier. Il :
- Simplifie les interactions complexes
- Réduit le couplage entre couches
- Centralise l'orchestration des services

**Avantages** :
- Interface unifiée pour les contrôleurs API
- Encapsulation de la complexité interne
- Facilite les tests et la maintenance

---

## Conception du Modèle de Données

### Entités Principales

#### User (Utilisateur)
```
Attributs :
- id (UUID) : Identifiant unique
- firstName (String) : Prénom
- lastName (String) : Nom de famille
- email (String) : Adresse email (unique)
- password (String) : Mot de passe hashé
- isAdmin (Boolean) : Statut administrateur
- createdAt (DateTime) : Date de création
- updatedAt (DateTime) : Date de dernière mise à jour

Méthodes :
- createUser() : Création d'un utilisateur
- updateUser() : Mise à jour du profil
- deleteUser() : Suppression du compte
- validateEmail() : Validation format email
- hashPassword() : Hachage sécurisé du mot de passe
```

#### Place (Lieu)
```
Attributs :
- id (UUID) : Identifiant unique
- title (String) : Titre du lieu
- description (String) : Description détaillée
- price (Float) : Prix par nuit
- latitude (Float) : Coordonnée latitude
- longitude (Float) : Coordonnée longitude
- createdAt (DateTime) : Date de création
- updatedAt (DateTime) : Date de dernière mise à jour

Méthodes :
- createPlace() : Création d'un lieu
- updatePlace() : Mise à jour des informations
- deletePlace() : Suppression du lieu
- validateCoordinates() : Validation des coordonnées GPS
- calculateDistance() : Calcul de distance
```

#### Review (Avis)
```
Attributs :
- id (UUID) : Identifiant unique
- rating (Integer) : Note (1-5)
- comment (String) : Commentaire textuel
- createdAt (DateTime) : Date de création
- updatedAt (DateTime) : Date de dernière mise à jour

Méthodes :
- createReview() : Création d'un avis
- updateReview() : Modification d'un avis
- deleteReview() : Suppression d'un avis
- validateRating() : Validation de la note (1-5)
```

#### Amenity (Commodité)
```
Attributs :
- id (UUID) : Identifiant unique
- name (String) : Nom de la commodité
- description (String) : Description
- createdAt (DateTime) : Date de création
- updatedAt (DateTime) : Date de dernière mise à jour

Méthodes :
- createAmenity() : Création d'une commodité
- updateAmenity() : Mise à jour
- deleteAmenity() : Suppression
```

### Relations entre Entités

1. **User ↔ Place** : Un utilisateur peut posséder plusieurs lieux (1:N)
2. **User ↔ Review** : Un utilisateur peut écrire plusieurs avis (1:N)
3. **Place ↔ Review** : Un lieu peut avoir plusieurs avis (1:N)
4. **Place ↔ Amenity** : Association plusieurs-à-plusieurs (N:N)

### Règles Métier Importantes

- **Identifiants uniques** : Tous les objets utilisent des UUID4
- **Audit trail** : Dates de création et mise à jour obligatoires
- **Contrainte Review** : Un utilisateur ne peut pas noter son propre lieu
- **Contrainte Review** : Un utilisateur = un seul avis par lieu
- **Validation email** : Format email requis et unicité

---

## Flots des API

### 1. Inscription d'Utilisateur

**Endpoint** : `POST /users`

**Flux de traitement** :
1. Réception de la requête par l'API Controller
2. Transmission au HBnB Facade
3. Traitement par User Service :
   - Validation des données (format email, longueur mot de passe)
   - Vérification unicité de l'email
   - Hachage du mot de passe
   - Génération UUID et timestamps
4. Sauvegarde via User Repository
5. Retour du résultat à travers les couches

**Gestion d'erreur** : Email déjà existant → 400 Bad Request

### 2. Création de Lieu

**Endpoint** : `POST /places`

**Flux de traitement** :
1. Authentification via middleware (validation JWT)
2. Traitement par Place Service :
   - Validation des données (coordonnées, prix)
   - Vérification de l'utilisateur propriétaire
   - Création de l'instance Place
3. Sauvegarde en base de données
4. Retour de la confirmation

**Prérequis** : Token JWT valide requis

### 3. Soumission d'Avis

**Endpoint** : `POST /places/{placeId}/reviews`

**Flux de traitement** :
1. Authentification utilisateur
2. Validation par Review Service :
   - Vérification existence du lieu
   - Contrôle que l'utilisateur n'est pas propriétaire
   - Vérification absence d'avis existant
   - Validation de la note (1-5)
3. Création et sauvegarde de l'avis

**Règles métier appliquées** :
- Pas d'auto-évaluation
- Un seul avis par utilisateur et par lieu

### 4. Récupération de la Liste des Lieux

**Endpoint** : `GET /places`

**Flux de traitement** :
1. Analyse des paramètres de requête (pagination, filtres)
2. Construction des critères de recherche
3. Récupération des lieux avec pagination
4. Enrichissement avec les commodités associées
5. Construction de la réponse paginée

**Fonctionnalités** :
- Support de la pagination (page, limit)
- Filtrage par commodités
- Comptage total pour la pagination

---

## Principes de Conception

### Principes SOLID Appliqués

#### Single Responsibility Principle (SRP)
- **UserService** : gestion exclusive des utilisateurs
- **PlaceService** : gestion exclusive des lieux
- **ReviewService** : gestion exclusive des avis
- **AmenityService** : gestion exclusive des commodités

#### Open-Closed Principle (OCP)
- Utilisation d'interfaces pour les services
- Extension possible sans modification du code existant
- Pattern Strategy applicable pour les validations

#### Liskov Substitution Principle (LSP)
- Implémentations des repositories interchangeables
- Respect des contrats d'interface

#### Interface Segregation Principle (ISP)
- Interfaces spécialisées par domaine
- Évite les dépendances inutiles

#### Dependency Inversion Principle (DIP)
- Dépendance sur les abstractions (interfaces)
- Injection de dépendance pour les repositories
- Facilite les tests unitaires

### Avantages de l'Architecture

1. **Maintenabilité** : Séparation claire des responsabilités
2. **Testabilité** : Chaque couche testable indépendamment
3. **Évolutivité** : Ajout de fonctionnalités sans régression
4. **Réutilisabilité** : Composants métier réutilisables
5. **Performance** : Optimisations possibles par couche

---

## Outils et Technologies

### Outils de Modélisation
- **Mermaid.js** : Création des diagrammes UML
- **GitHub** : Versioning et collaboration
- **Markdown** : Documentation technique

### Standards Respectés
- **UML 2.x** : Notation des diagrammes
- **REST API** : Design des endpoints
- **UUID4** : Génération d'identifiants
- **JWT** : Authentification stateless

---

## Conclusion

Cette documentation constitue la fondation technique du projet HBnB Evolution. L'architecture en couches avec pattern Facade assure une séparation claire des responsabilités et facilite la maintenance.

### Bénéfices de l'Approche

1. **Clarté architecturale** : Structure compréhensible par l'équipe
2. **Réduction du couplage** : Indépendance des couches
3. **Facilitation des tests** : Testabilité de chaque composant
4. **Évolutivité** : Ajout de fonctionnalités sans impact majeur
5. **Réutilisabilité** : Composants métier indépendants

### Étapes Suivantes

1. **Part 2** : Implémentation de l'API REST
2. **Part 3** : Intégration base de données
3. **Part 4** : Interface utilisateur frontend

### Validation et Reviews

Cette documentation doit être reviewée par :
- L'équipe de développement (Yassin Jaghmim, Guillaume Watelet)
- Le mentor technique
- QA manual review avant passage à la Part 2

---

**Auteurs** : Équipe HBnB Evolution Yassin Jaghmim, Guillaume Watelet 
**Date** : Septembre 2025  
**Version** : 1.0  
**Statut** : En attente de review
