-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 22 jan. 2024 à 09:32
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
-- Base de données : `transsim`
--

-- --------------------------------------------------------

--
-- Structure de la table `autorisation`
--

DROP TABLE IF EXISTS `autorisation`;
CREATE TABLE IF NOT EXISTS `autorisation` (
  `numeroAutorisation` int NOT NULL AUTO_INCREMENT,
  `idBanque` int UNSIGNED NOT NULL,
  `dateAutorisation` date NOT NULL,
  `montantTransaction` int NOT NULL,
  PRIMARY KEY (`numeroAutorisation`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- --------------------------------------------------------

--
-- Structure de la table `banque`
--

DROP TABLE IF EXISTS `banque`;
CREATE TABLE IF NOT EXISTS `banque` (
  `idBanque` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `nomBanque` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`idBanque`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- --------------------------------------------------------

--
-- Structure de la table `cartebancaire`
--

DROP TABLE IF EXISTS `cartebancaire`;
CREATE TABLE IF NOT EXISTS `cartebancaire` (
  `numeroCarte` int NOT NULL AUTO_INCREMENT COMMENT 'numéro de la carte',
  `idCompte` int NOT NULL COMMENT 'id du compte associé à la carte',
  `dateExpiration` date DEFAULT NULL COMMENT 'Format : YYYY-MM-DD\r\ndate d''expiration de la carte\r\n',
  `estValide` tinyint(1) DEFAULT NULL COMMENT 'validité de la carte',
  `codePin` int NOT NULL COMMENT 'code PIN de la carte pour les paiement via TPE, retraits...',
  `cryptogramme` int NOT NULL COMMENT 'cryptogramme visuel pour les paiements en ligne',
  PRIMARY KEY (`numeroCarte`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- --------------------------------------------------------

--
-- Structure de la table `comptebancaire`
--

DROP TABLE IF EXISTS `comptebancaire`;
CREATE TABLE IF NOT EXISTS `comptebancaire` (
  `idCompte` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'clé primaire d''un compte',
  `idBanque` int UNSIGNED NOT NULL COMMENT 'id de la banque associé au compte',
  `nom` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'nom de l''utilisateur',
  `prenom` varchar(128) COLLATE utf8mb3_bin DEFAULT NULL COMMENT 'prénom de l''utilisateur',
  `solde` int DEFAULT NULL COMMENT 'solde du compte en banque',
  PRIMARY KEY (`idCompte`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

-- --------------------------------------------------------

--
-- Structure de la table `tpe`
--

DROP TABLE IF EXISTS `tpe`;
CREATE TABLE IF NOT EXISTS `tpe` (
  `numeroTransaction` int NOT NULL AUTO_INCREMENT,
  `idBanque` int UNSIGNED NOT NULL,
  `numeroAutorisation` int NOT NULL,
  PRIMARY KEY (`numeroTransaction`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
