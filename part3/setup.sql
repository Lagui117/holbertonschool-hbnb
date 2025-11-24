-- ================================================================================
-- HBnB Database Schema - SQL Script for Table Generation and Initial Data
-- ================================================================================
-- Ce script crée toutes les tables nécessaires pour l'application HBnB
-- et insère les données initiales (admin et amenities)
-- This script creates all necessary tables for the HBnB application
-- and inserts initial data (admin and amenities)
-- ===========================================================================- Suppression des tables existantes (si elles existent) pour un déploiement propre
-- Drop existing tables (if they exist) for clean deployment
DROP TABLE IF EXISTS place_amenity_association;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- ================================================================================
-- TABLE: users
-- Stocke les informations des utilisateurs (proprietaires et reviewers)
-- Stores user information (owners and reviewers)
-- ================================================================================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================================
-- TABLE: places
-- Stocke les informations des lieux/hébergements
-- Stores place/accommodation information
-- ================================================================================
CREATE TABLE places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price REAL NOT NULL DEFAULT 0.0,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ================================================================================
-- TABLE: reviews
-- Stocke les avis/commentaires sur les lieux
-- Stores reviews/comments on places
-- ================================================================================
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id INTEGER NOT NULL,
    place_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)  -- Un utilisateur ne peut reviewer un lieu qu'une seule fois
);

-- ================================================================================
-- TABLE: amenities
-- Stocke les équipements/commodités disponibles
-- Stores available amenities/facilities
-- ================================================================================
CREATE TABLE amenities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================================
-- TABLE: place_amenity_association
-- Table d'association Many-to-Many entre places et amenities
-- Many-to-Many association table between places and amenities
-- ================================================================================
CREATE TABLE place_amenity_association (
    place_id INTEGER NOT NULL,
    amenity_id INTEGER NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- ================================================================================
-- DONNÉES INITIALES / INITIAL DATA
-- ================================================================================

-- Insertion d'un utilisateur administrateur initial
-- Insert initial administrator user
-- Mot de passe: admin1234 (hashé avec bcrypt)
-- Password: admin1234 (hashed with bcrypt)
-- Hash généré avec: bcrypt.hashpw(b'admin1234', bcrypt.gensalt())
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES (
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5F1BgQCkB/uNi',  -- admin1234
    1
);

-- Insertion des équipements (amenities) de base
-- Insert basic amenities
INSERT INTO amenities (name) VALUES ('WiFi');
INSERT INTO amenities (name) VALUES ('Swimming Pool');
INSERT INTO amenities (name) VALUES ('Air Conditioning');
INSERT INTO amenities (name) VALUES ('Kitchen');
INSERT INTO amenities (name) VALUES ('Parking');
INSERT INTO amenities (name) VALUES ('TV');
INSERT INTO amenities (name) VALUES ('Heating');
INSERT INTO amenities (name) VALUES ('Washer');
INSERT INTO amenities (name) VALUES ('Dryer');
INSERT INTO amenities (name) VALUES ('Gym');

-- ================================================================================
-- FIN DU SCRIPT / END OF SCRIPT
-- ================================================================================

