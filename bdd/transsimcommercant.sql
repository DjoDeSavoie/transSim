-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 23 jan. 2024 à 16:29
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `transsimcommercant`
--

-- --------------------------------------------------------

--
-- Structure de la table `autorisationtransaction`
--

DROP TABLE IF EXISTS `autorisationtransaction`;
CREATE TABLE IF NOT EXISTS `autorisationtransaction` (
  `numeroAutorisation` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `idBanqueEmetteur` int UNSIGNED NOT NULL,
  `dateAutorisation` date NOT NULL,
  `montantAutorisation` int NOT NULL,
  PRIMARY KEY (`numeroAutorisation`),
  KEY `fk_banqueemetteur_autorisationtransaction` (`idBanqueEmetteur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `banque`
--

DROP TABLE IF EXISTS `banque`;
CREATE TABLE IF NOT EXISTS `banque` (
  `idBanque` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'identifiant de la banque, clé primaire',
  `nomBanque` varchar(128) DEFAULT NULL COMMENT 'nom de la banque',
  PRIMARY KEY (`idBanque`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cartebancaire`
--

DROP TABLE IF EXISTS `cartebancaire`;
CREATE TABLE IF NOT EXISTS `cartebancaire` (
  `numeroCarte` int NOT NULL COMMENT 'numéro de carte, les 4 premier chiffres identifient la banque, le dernier est la clé de luhn calculée d''après les chiffres précédents',
  `idCompteEmetteur` int UNSIGNED NOT NULL,
  `dateExpiration` date NOT NULL,
  `validite` tinyint(1) NOT NULL,
  `pin` int NOT NULL,
  `cryptogramme` int NOT NULL,
  PRIMARY KEY (`numeroCarte`),
  KEY `fk_comptebancaireemetteur_cartebancaire` (`idCompteEmetteur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `comptebancaireacquereur`
--

DROP TABLE IF EXISTS `comptebancaireacquereur`;
CREATE TABLE IF NOT EXISTS `comptebancaireacquereur` (
  `idCompteAcquereur` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'numéro d''identifiant du compte bancaire de l''acquéreur (commercant)',
  `idBanqueAcquereur` int UNSIGNED NOT NULL,
  `numeroCompte` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` varchar(128) NOT NULL,
  `prenom` varchar(128) NOT NULL,
  `soldeCompteAcquereur` int NOT NULL,
  PRIMARY KEY (`idCompteAcquereur`),
  KEY `fk_banque_comptebancaireacquereur` (`idBanqueAcquereur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `comptebancaireemetteur`
--

DROP TABLE IF EXISTS `comptebancaireemetteur`;
CREATE TABLE IF NOT EXISTS `comptebancaireemetteur` (
  `idCompteEmetteur` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'numéro d''identifiant du compte bancaire de l''émetteur (client)',
  `idBanqueEmetteur` int UNSIGNED NOT NULL,
  `numeroCompte` int UNSIGNED NOT NULL,
  `nom` varchar(128) NOT NULL,
  `prenom` varchar(128) NOT NULL,
  `soldeCompteEmetteur` int NOT NULL,
  PRIMARY KEY (`idCompteEmetteur`),
  KEY `fk_banque_comptebancaireemetteur` (`idBanqueEmetteur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `tpe`
--

DROP TABLE IF EXISTS `tpe`;
CREATE TABLE IF NOT EXISTS `tpe` (
  `numeroTransaction` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `idBanqueAcquereur` int UNSIGNED NOT NULL,
  `numeroAutorisation` int UNSIGNED NOT NULL,
  `montantTransaction` int NOT NULL,
  PRIMARY KEY (`numeroTransaction`),
  KEY `fk_comptebancaireacquereur_tpe` (`idBanqueAcquereur`),
  KEY `fk_autorisation_tpe` (`numeroAutorisation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `autorisationtransaction`
--
ALTER TABLE `autorisationtransaction`
  ADD CONSTRAINT `fk_banqueemetteur_autorisationtransaction` FOREIGN KEY (`idBanqueEmetteur`) REFERENCES `comptebancaireemetteur` (`idBanqueEmetteur`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `cartebancaire`
--
ALTER TABLE `cartebancaire`
  ADD CONSTRAINT `fk_comptebancaireemetteur_cartebancaire` FOREIGN KEY (`idCompteEmetteur`) REFERENCES `comptebancaireemetteur` (`idCompteEmetteur`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `comptebancaireacquereur`
--
ALTER TABLE `comptebancaireacquereur`
  ADD CONSTRAINT `fk_banque_comptebancaireacquereur` FOREIGN KEY (`idBanqueAcquereur`) REFERENCES `banque` (`idBanque`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `comptebancaireemetteur`
--
ALTER TABLE `comptebancaireemetteur`
  ADD CONSTRAINT `fk_banque_comptebancaireemetteur` FOREIGN KEY (`idBanqueEmetteur`) REFERENCES `banque` (`idBanque`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `tpe`
--
ALTER TABLE `tpe`
  ADD CONSTRAINT `fk_autorisation_tpe` FOREIGN KEY (`numeroAutorisation`) REFERENCES `autorisationtransaction` (`numeroAutorisation`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `fk_comptebancaireacquereur_tpe` FOREIGN KEY (`idBanqueAcquereur`) REFERENCES `comptebancaireacquereur` (`idBanqueAcquereur`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
