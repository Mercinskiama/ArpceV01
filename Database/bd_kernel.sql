-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3308
-- Généré le :  lun. 23 oct. 2023 à 12:04
-- Version du serveur :  8.0.18
-- Version de PHP :  7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `bd_kernel`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add model_ action utilisateur', 7, 'add_model_actionutilisateur'),
(26, 'Can change model_ action utilisateur', 7, 'change_model_actionutilisateur'),
(27, 'Can delete model_ action utilisateur', 7, 'delete_model_actionutilisateur'),
(28, 'Can view model_ action utilisateur', 7, 'view_model_actionutilisateur'),
(29, 'Can add model_ civilite', 8, 'add_model_civilite'),
(30, 'Can change model_ civilite', 8, 'change_model_civilite'),
(31, 'Can delete model_ civilite', 8, 'delete_model_civilite'),
(32, 'Can view model_ civilite', 8, 'view_model_civilite'),
(33, 'Can add model_ devise', 9, 'add_model_devise'),
(34, 'Can change model_ devise', 9, 'change_model_devise'),
(35, 'Can delete model_ devise', 9, 'delete_model_devise'),
(36, 'Can view model_ devise', 9, 'view_model_devise'),
(37, 'Can add model_ groupe menu', 10, 'add_model_groupemenu'),
(38, 'Can change model_ groupe menu', 10, 'change_model_groupemenu'),
(39, 'Can delete model_ groupe menu', 10, 'delete_model_groupemenu'),
(40, 'Can view model_ groupe menu', 10, 'view_model_groupemenu'),
(41, 'Can add model_ groupe permission', 11, 'add_model_groupepermission'),
(42, 'Can change model_ groupe permission', 11, 'change_model_groupepermission'),
(43, 'Can delete model_ groupe permission', 11, 'delete_model_groupepermission'),
(44, 'Can view model_ groupe permission', 11, 'view_model_groupepermission'),
(45, 'Can add model_ groupe permission utilisateur', 12, 'add_model_groupepermissionutilisateur'),
(46, 'Can change model_ groupe permission utilisateur', 12, 'change_model_groupepermissionutilisateur'),
(47, 'Can delete model_ groupe permission utilisateur', 12, 'delete_model_groupepermissionutilisateur'),
(48, 'Can view model_ groupe permission utilisateur', 12, 'view_model_groupepermissionutilisateur'),
(49, 'Can add model_ ligne regle', 13, 'add_model_ligneregle'),
(50, 'Can change model_ ligne regle', 13, 'change_model_ligneregle'),
(51, 'Can delete model_ ligne regle', 13, 'delete_model_ligneregle'),
(52, 'Can view model_ ligne regle', 13, 'view_model_ligneregle'),
(53, 'Can add model_ message', 14, 'add_model_message'),
(54, 'Can change model_ message', 14, 'change_model_message'),
(55, 'Can delete model_ message', 14, 'delete_model_message'),
(56, 'Can view model_ message', 14, 'view_model_message'),
(57, 'Can add model_ module', 15, 'add_model_module'),
(58, 'Can change model_ module', 15, 'change_model_module'),
(59, 'Can delete model_ module', 15, 'delete_model_module'),
(60, 'Can view model_ module', 15, 'view_model_module'),
(61, 'Can add model_ module over model', 16, 'add_model_moduleovermodel'),
(62, 'Can change model_ module over model', 16, 'change_model_moduleovermodel'),
(63, 'Can delete model_ module over model', 16, 'delete_model_moduleovermodel'),
(64, 'Can view model_ module over model', 16, 'view_model_moduleovermodel'),
(65, 'Can add model_ notification', 17, 'add_model_notification'),
(66, 'Can change model_ notification', 17, 'change_model_notification'),
(67, 'Can delete model_ notification', 17, 'delete_model_notification'),
(68, 'Can view model_ notification', 17, 'view_model_notification'),
(69, 'Can add model_ operationnalisation_module', 18, 'add_model_operationnalisation_module'),
(70, 'Can change model_ operationnalisation_module', 18, 'change_model_operationnalisation_module'),
(71, 'Can delete model_ operationnalisation_module', 18, 'delete_model_operationnalisation_module'),
(72, 'Can view model_ operationnalisation_module', 18, 'view_model_operationnalisation_module'),
(73, 'Can add model_ organisation', 19, 'add_model_organisation'),
(74, 'Can change model_ organisation', 19, 'change_model_organisation'),
(75, 'Can delete model_ organisation', 19, 'delete_model_organisation'),
(76, 'Can view model_ organisation', 19, 'view_model_organisation'),
(77, 'Can add model_ permission', 20, 'add_model_permission'),
(78, 'Can change model_ permission', 20, 'change_model_permission'),
(79, 'Can delete model_ permission', 20, 'delete_model_permission'),
(80, 'Can view model_ permission', 20, 'view_model_permission'),
(81, 'Can add model_ personne', 21, 'add_model_personne'),
(82, 'Can change model_ personne', 21, 'change_model_personne'),
(83, 'Can delete model_ personne', 21, 'delete_model_personne'),
(84, 'Can view model_ personne', 21, 'view_model_personne'),
(85, 'Can add model_ place', 22, 'add_model_place'),
(86, 'Can change model_ place', 22, 'change_model_place'),
(87, 'Can delete model_ place', 22, 'delete_model_place'),
(88, 'Can view model_ place', 22, 'view_model_place'),
(89, 'Can add model_ regle', 23, 'add_model_regle'),
(90, 'Can change model_ regle', 23, 'change_model_regle'),
(91, 'Can delete model_ regle', 23, 'delete_model_regle'),
(92, 'Can view model_ regle', 23, 'view_model_regle'),
(93, 'Can add model_ sous module', 24, 'add_model_sousmodule'),
(94, 'Can change model_ sous module', 24, 'change_model_sousmodule'),
(95, 'Can delete model_ sous module', 24, 'delete_model_sousmodule'),
(96, 'Can view model_ sous module', 24, 'view_model_sousmodule'),
(97, 'Can add model_ taux', 25, 'add_model_taux'),
(98, 'Can change model_ taux', 25, 'change_model_taux'),
(99, 'Can delete model_ taux', 25, 'delete_model_taux'),
(100, 'Can view model_ taux', 25, 'view_model_taux'),
(101, 'Can add model_ temp_ notification', 26, 'add_model_temp_notification'),
(102, 'Can change model_ temp_ notification', 26, 'change_model_temp_notification'),
(103, 'Can delete model_ temp_ notification', 26, 'delete_model_temp_notification'),
(104, 'Can view model_ temp_ notification', 26, 'view_model_temp_notification'),
(105, 'Can add model_ type organisation', 27, 'add_model_typeorganisation'),
(106, 'Can change model_ type organisation', 27, 'change_model_typeorganisation'),
(107, 'Can delete model_ type organisation', 27, 'delete_model_typeorganisation'),
(108, 'Can view model_ type organisation', 27, 'view_model_typeorganisation'),
(109, 'Can add model_ user sessions', 28, 'add_model_usersessions'),
(110, 'Can change model_ user sessions', 28, 'change_model_usersessions'),
(111, 'Can delete model_ user sessions', 28, 'delete_model_usersessions'),
(112, 'Can view model_ user sessions', 28, 'view_model_usersessions'),
(113, 'Can add model_ wkf_ approbation', 29, 'add_model_wkf_approbation'),
(114, 'Can change model_ wkf_ approbation', 29, 'change_model_wkf_approbation'),
(115, 'Can delete model_ wkf_ approbation', 29, 'delete_model_wkf_approbation'),
(116, 'Can view model_ wkf_ approbation', 29, 'view_model_wkf_approbation'),
(117, 'Can add model_ wkf_ condition', 30, 'add_model_wkf_condition'),
(118, 'Can change model_ wkf_ condition', 30, 'change_model_wkf_condition'),
(119, 'Can delete model_ wkf_ condition', 30, 'delete_model_wkf_condition'),
(120, 'Can view model_ wkf_ condition', 30, 'view_model_wkf_condition'),
(121, 'Can add model_ wkf_ etape', 31, 'add_model_wkf_etape'),
(122, 'Can change model_ wkf_ etape', 31, 'change_model_wkf_etape'),
(123, 'Can delete model_ wkf_ etape', 31, 'delete_model_wkf_etape'),
(124, 'Can view model_ wkf_ etape', 31, 'view_model_wkf_etape'),
(125, 'Can add model_ wkf_ historique', 32, 'add_model_wkf_historique'),
(126, 'Can change model_ wkf_ historique', 32, 'change_model_wkf_historique'),
(127, 'Can delete model_ wkf_ historique', 32, 'delete_model_wkf_historique'),
(128, 'Can view model_ wkf_ historique', 32, 'view_model_wkf_historique'),
(129, 'Can add model_ wkf_ stakeholder', 33, 'add_model_wkf_stakeholder'),
(130, 'Can change model_ wkf_ stakeholder', 33, 'change_model_wkf_stakeholder'),
(131, 'Can delete model_ wkf_ stakeholder', 33, 'delete_model_wkf_stakeholder'),
(132, 'Can view model_ wkf_ stakeholder', 33, 'view_model_wkf_stakeholder'),
(133, 'Can add model_ wkf_ transition', 34, 'add_model_wkf_transition'),
(134, 'Can change model_ wkf_ transition', 34, 'change_model_wkf_transition'),
(135, 'Can delete model_ wkf_ transition', 34, 'delete_model_wkf_transition'),
(136, 'Can view model_ wkf_ transition', 34, 'view_model_wkf_transition'),
(137, 'Can add model_ wkf_ workflow', 35, 'add_model_wkf_workflow'),
(138, 'Can change model_ wkf_ workflow', 35, 'change_model_wkf_workflow'),
(139, 'Can delete model_ wkf_ workflow', 35, 'delete_model_wkf_workflow'),
(140, 'Can view model_ wkf_ workflow', 35, 'view_model_wkf_workflow'),
(141, 'Can add model_ employe', 36, 'add_model_employe'),
(142, 'Can change model_ employe', 36, 'change_model_employe'),
(143, 'Can delete model_ employe', 36, 'delete_model_employe'),
(144, 'Can view model_ employe', 36, 'view_model_employe'),
(145, 'Can add model_ document_archivage', 37, 'add_model_document_archivage'),
(146, 'Can change model_ document_archivage', 37, 'change_model_document_archivage'),
(147, 'Can delete model_ document_archivage', 37, 'delete_model_document_archivage'),
(148, 'Can view model_ document_archivage', 37, 'view_model_document_archivage'),
(149, 'Can add Etiquette', 38, 'add_model_tag'),
(150, 'Can change Etiquette', 38, 'change_model_tag'),
(151, 'Can delete Etiquette', 38, 'delete_model_tag'),
(152, 'Can view Etiquette', 38, 'view_model_tag'),
(153, 'Can add Lien partagé', 39, 'add_model_document_partage'),
(154, 'Can change Lien partagé', 39, 'change_model_document_partage'),
(155, 'Can delete Lien partagé', 39, 'delete_model_document_partage'),
(156, 'Can view Lien partagé', 39, 'view_model_document_partage'),
(157, 'Can add Catégorie d\'étiquette', 40, 'add_model_categorie_tag'),
(158, 'Can change Catégorie d\'étiquette', 40, 'change_model_categorie_tag'),
(159, 'Can delete Catégorie d\'étiquette', 40, 'delete_model_categorie_tag'),
(160, 'Can view Catégorie d\'étiquette', 40, 'view_model_categorie_tag'),
(161, 'Can add Dossier', 41, 'add_model_dossier'),
(162, 'Can change Dossier', 41, 'change_model_dossier'),
(163, 'Can delete Dossier', 41, 'delete_model_dossier'),
(164, 'Can view Dossier', 41, 'view_model_dossier'),
(165, 'Can add Document', 42, 'add_model_document'),
(166, 'Can change Document', 42, 'change_model_document'),
(167, 'Can delete Document', 42, 'delete_model_document'),
(168, 'Can view Document', 42, 'view_model_document'),
(169, 'Can add Requête BI', 43, 'add_model_query'),
(170, 'Can change Requête BI', 43, 'change_model_query'),
(171, 'Can delete Requête BI', 43, 'delete_model_query'),
(172, 'Can view Requête BI', 43, 'view_model_query'),
(173, 'Can add Adresse', 44, 'add_model_adresse'),
(174, 'Can change Adresse', 44, 'change_model_adresse'),
(175, 'Can delete Adresse', 44, 'delete_model_adresse'),
(176, 'Can view Adresse', 44, 'view_model_adresse'),
(177, 'Can add Commune', 45, 'add_model_commune'),
(178, 'Can change Commune', 45, 'change_model_commune'),
(179, 'Can delete Commune', 45, 'delete_model_commune'),
(180, 'Can view Commune', 45, 'view_model_commune'),
(181, 'Can add Contact', 46, 'add_model_contact'),
(182, 'Can change Contact', 46, 'change_model_contact'),
(183, 'Can delete Contact', 46, 'delete_model_contact'),
(184, 'Can view Contact', 46, 'view_model_contact'),
(185, 'Can add Pays', 47, 'add_model_pays'),
(186, 'Can change Pays', 47, 'change_model_pays'),
(187, 'Can delete Pays', 47, 'delete_model_pays'),
(188, 'Can view Pays', 47, 'view_model_pays'),
(189, 'Can add Province', 48, 'add_model_province'),
(190, 'Can change Province', 48, 'change_model_province'),
(191, 'Can delete Province', 48, 'delete_model_province'),
(192, 'Can view Province', 48, 'view_model_province'),
(193, 'Can add Société', 49, 'add_model_societe'),
(194, 'Can change Société', 49, 'change_model_societe'),
(195, 'Can delete Société', 49, 'delete_model_societe'),
(196, 'Can view Société', 49, 'view_model_societe'),
(197, 'Can add Ville', 50, 'add_model_ville'),
(198, 'Can change Ville', 50, 'change_model_ville'),
(199, 'Can delete Ville', 50, 'delete_model_ville'),
(200, 'Can view Ville', 50, 'view_model_ville'),
(201, 'Can add Type Période', 51, 'add_model_type_periode'),
(202, 'Can change Type Période', 51, 'change_model_type_periode'),
(203, 'Can delete Type Période', 51, 'delete_model_type_periode'),
(204, 'Can view Type Période', 51, 'view_model_type_periode'),
(205, 'Can add District', 52, 'add_model_district'),
(206, 'Can change District', 52, 'change_model_district'),
(207, 'Can delete District', 52, 'delete_model_district'),
(208, 'Can view District', 52, 'view_model_district'),
(209, 'Can add Historique Action', 53, 'add_model_historique_action'),
(210, 'Can change Historique Action', 53, 'change_model_historique_action'),
(211, 'Can delete Historique Action', 53, 'delete_model_historique_action'),
(212, 'Can view Historique Action', 53, 'view_model_historique_action'),
(213, 'Can add Log', 54, 'add_model_log'),
(214, 'Can change Log', 54, 'change_model_log'),
(215, 'Can delete Log', 54, 'delete_model_log'),
(216, 'Can view Log', 54, 'view_model_log');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$260000$79XVVUvjBNSfsvisTxmZSh$uxVMtOOu5fN5CqgvkaIho0j6FnLWOuBmb1LJglapfWc=', '2023-10-23 10:45:38.309864', 1, 'admin', '', '', 'admin@erp.nous', 1, 1, '2018-06-04 13:02:41.356000');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `categorie_tag`
--

DROP TABLE IF EXISTS `categorie_tag`;
CREATE TABLE IF NOT EXISTS `categorie_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(250) NOT NULL,
  `code` varchar(100) DEFAULT NULL,
  `description` varchar(550) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `dossier_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `categorie_tag_auteur_id_642c5041_fk_ErpBackOf` (`auteur_id`),
  KEY `categorie_tag_dossier_id_b3b2451f_fk_dossier_id` (`dossier_id`),
  KEY `categorie_tag_statut_id_46126ef6_fk_ErpBackOf` (`statut_id`),
  KEY `categorie_tag_company_id_967e102d_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `categorie_tag`
--

INSERT INTO `categorie_tag` (`id`, `designation`, `code`, `description`, `etat`, `creation_date`, `update_date`, `auteur_id`, `dossier_id`, `statut_id`, `company_id`) VALUES
(1, 'Comptabilité', 'ACC', 'RAS', NULL, '2022-03-28 02:24:13.278378', '2022-03-28 02:27:36.325192', NULL, 2, NULL, NULL),
(2, 'RH', 'ACC', 'RAS', NULL, '2022-03-28 02:30:01.636460', '2022-03-28 02:30:01.636460', NULL, 2, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `cnf_address`
--

DROP TABLE IF EXISTS `cnf_address`;
CREATE TABLE IF NOT EXISTS `cnf_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `type` int(11) NOT NULL,
  `street` varchar(100) DEFAULT NULL,
  `street2` varchar(100) DEFAULT NULL,
  `zip_code` varchar(100) DEFAULT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `city` int(11) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `township` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `country` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_address_city_8a187c6c` (`city`),
  KEY `cnf_address_province_0776921d` (`province`),
  KEY `cnf_address_township_66f4bb0e` (`township`),
  KEY `cnf_address_created_by_f0f43ab7` (`created_by`),
  KEY `cnf_address_country_f66e12a0` (`country`),
  KEY `cnf_address_status_259f2300` (`status`),
  KEY `cnf_address_updated_by_b559c6a0` (`updated_by`),
  KEY `cnf_address_company_id_8bdd176f` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_city`
--

DROP TABLE IF EXISTS `cnf_city`;
CREATE TABLE IF NOT EXISTS `cnf_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_city_created_by_9ed4a1c1` (`created_by`),
  KEY `cnf_city_province_6ee0cc2b` (`province`),
  KEY `cnf_city_status_f8461345` (`status`),
  KEY `cnf_city_updated_by_342ecb30` (`updated_by`),
  KEY `cnf_city_company_id_797681eb` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_company`
--

DROP TABLE IF EXISTS `cnf_company`;
CREATE TABLE IF NOT EXISTS `cnf_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `picture_icon` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `adress_country` varchar(100) DEFAULT NULL,
  `adress_state` varchar(100) DEFAULT NULL,
  `adress_city` varchar(100) DEFAULT NULL,
  `adress_line1` varchar(100) DEFAULT NULL,
  `adress_line2` varchar(100) DEFAULT NULL,
  `phone_number1` varchar(100) DEFAULT NULL,
  `phone_number2` varchar(100) DEFAULT NULL,
  `nbr_periode_gl` int(11) DEFAULT NULL,
  `nbr_periode_ar` int(11) DEFAULT NULL,
  `nbr_periode_ap` int(11) DEFAULT NULL,
  `nbr_periode_cm` int(11) DEFAULT NULL,
  `nbr_periode_fa` int(11) DEFAULT NULL,
  `nbr_periode_bgt` int(11) DEFAULT NULL,
  `nbr_periode_py` int(11) DEFAULT NULL,
  `period_begin_date` datetime(6) DEFAULT NULL,
  `period_end_date` datetime(6) DEFAULT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `township_id` int(11) DEFAULT NULL,
  `currency_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `province_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `period_type_id` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_company_created_by_5e5fe289` (`created_by`),
  KEY `cnf_company_township_id_badbaa51` (`township_id`),
  KEY `cnf_company_currency_id_9708a600` (`currency_id`),
  KEY `cnf_company_parent_id_9ce6f186` (`parent_id`),
  KEY `cnf_company_country_id_4cb90c44` (`country_id`),
  KEY `cnf_company_province_id_ee0bbef0` (`province_id`),
  KEY `cnf_company_status_971ce15d` (`status`),
  KEY `cnf_company_period_type_id_b629067c` (`period_type_id`),
  KEY `cnf_company_updated_by_714abdd1` (`updated_by`),
  KEY `cnf_company_city_id_3bede75c` (`city_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `cnf_company`
--

INSERT INTO `cnf_company` (`id`, `code`, `name`, `picture_icon`, `type`, `email`, `website`, `adress_country`, `adress_state`, `adress_city`, `adress_line1`, `adress_line2`, `phone_number1`, `phone_number2`, `nbr_periode_gl`, `nbr_periode_ar`, `nbr_periode_ap`, `nbr_periode_cm`, `nbr_periode_fa`, `nbr_periode_bgt`, `nbr_periode_py`, `period_begin_date`, `period_end_date`, `description`, `state`, `created_date`, `updated_date`, `created_by`, `township_id`, `currency_id`, `parent_id`, `country_id`, `province_id`, `status`, `period_type_id`, `updated_by`, `city_id`) VALUES
(1, 'MD', 'Nsandax', '', 'SARL', '', '', '', '', '', '', '', '', '', 12, 12, 12, 12, 12, 12, 12, NULL, NULL, '', NULL, '2023-10-23 12:54:46.576458', '2023-10-23 12:54:46.576458', 7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `cnf_company_autres_adresses`
--

DROP TABLE IF EXISTS `cnf_company_autres_adresses`;
CREATE TABLE IF NOT EXISTS `cnf_company_autres_adresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_societe_id` int(11) NOT NULL,
  `model_adresse_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnf_company_autres_adres_model_societe_id_model_a_5667bd02_uniq` (`model_societe_id`,`model_adresse_id`),
  KEY `cnf_company_autres_adresses_model_societe_id_acd1e00f` (`model_societe_id`),
  KEY `cnf_company_autres_adresses_model_adresse_id_032aa05e` (`model_adresse_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_company_contacts`
--

DROP TABLE IF EXISTS `cnf_company_contacts`;
CREATE TABLE IF NOT EXISTS `cnf_company_contacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_societe_id` int(11) NOT NULL,
  `model_contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnf_company_contacts_model_societe_id_model_c_d6172b76_uniq` (`model_societe_id`,`model_contact_id`),
  KEY `cnf_company_contacts_model_societe_id_51803e7f` (`model_societe_id`),
  KEY `cnf_company_contacts_model_contact_id_154fce23` (`model_contact_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_contact`
--

DROP TABLE IF EXISTS `cnf_contact`;
CREATE TABLE IF NOT EXISTS `cnf_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `company_type` int(11) NOT NULL,
  `nature` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `website` varchar(250) DEFAULT NULL,
  `function` varchar(250) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `street2` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `mobile` varchar(100) DEFAULT NULL,
  `zip_code` varchar(100) DEFAULT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `city` int(11) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `country` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_contact_city_1c657290` (`city`),
  KEY `cnf_contact_province_ae3311a0` (`province`),
  KEY `cnf_contact_created_by_af9bc16b` (`created_by`),
  KEY `cnf_contact_country_76301cd2` (`country`),
  KEY `cnf_contact_status_d23db3ad` (`status`),
  KEY `cnf_contact_updated_by_bdb92612` (`updated_by`),
  KEY `cnf_contact_company_id_ba7ee74d` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_contact_autres_adresses`
--

DROP TABLE IF EXISTS `cnf_contact_autres_adresses`;
CREATE TABLE IF NOT EXISTS `cnf_contact_autres_adresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_contact_id` int(11) NOT NULL,
  `model_adresse_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnf_contact_autres_adres_model_contact_id_model_a_2822df64_uniq` (`model_contact_id`,`model_adresse_id`),
  KEY `cnf_contact_autres_adresses_model_contact_id_fe733d4d` (`model_contact_id`),
  KEY `cnf_contact_autres_adresses_model_adresse_id_2d5f361c` (`model_adresse_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_country`
--

DROP TABLE IF EXISTS `cnf_country`;
CREATE TABLE IF NOT EXISTS `cnf_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_country_created_by_e481b1df` (`created_by`),
  KEY `cnf_country_status_29325f35` (`status`),
  KEY `cnf_country_updated_by_84c66869` (`updated_by`),
  KEY `cnf_country_company_id_a2c2c7b4` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_district`
--

DROP TABLE IF EXISTS `cnf_district`;
CREATE TABLE IF NOT EXISTS `cnf_district` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `province` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_district_created_by_63a92c0b` (`created_by`),
  KEY `cnf_district_province_fbf929cc` (`province`),
  KEY `cnf_district_status_09d97a9f` (`status`),
  KEY `cnf_district_updated_by_f318a118` (`updated_by`),
  KEY `cnf_district_company_id_461d5fe5` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_state`
--

DROP TABLE IF EXISTS `cnf_state`;
CREATE TABLE IF NOT EXISTS `cnf_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `country` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_state_created_by_091cf2fa` (`created_by`),
  KEY `cnf_state_country_3661f474` (`country`),
  KEY `cnf_state_status_23bee0fd` (`status`),
  KEY `cnf_state_updated_by_383f4688` (`updated_by`),
  KEY `cnf_state_company_id_9b55498a` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_township`
--

DROP TABLE IF EXISTS `cnf_township`;
CREATE TABLE IF NOT EXISTS `cnf_township` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_township_created_by_8a94b030` (`created_by`),
  KEY `cnf_township_status_af2dc205` (`status`),
  KEY `cnf_township_updated_by_a960c1c4` (`updated_by`),
  KEY `cnf_township_city_266bb114` (`city`),
  KEY `cnf_township_company_id_8b8ac570` (`company_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cnf_type_period`
--

DROP TABLE IF EXISTS `cnf_type_period`;
CREATE TABLE IF NOT EXISTS `cnf_type_period` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `periodicity` varchar(100) DEFAULT NULL,
  `number_per_fiscal_year` int(11) DEFAULT NULL,
  `description` longtext,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `company` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cnf_type_period_created_by_0850855d` (`created_by`),
  KEY `cnf_type_period_company_fc2f3bf6` (`company`),
  KEY `cnf_type_period_status_9f9988a1` (`status`),
  KEY `cnf_type_period_updated_by_c3cbab7e` (`updated_by`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2022-03-24 16:38:03.798839', '6', 'Module Application', 2, '[{\"changed\": {\"fields\": [\"numero_ordre\"]}}]', 15, 1),
(2, '2022-03-26 18:15:52.252792', '3208', 'Module Archivage / Documents', 3, '', 24, 1),
(3, '2022-03-26 18:16:20.615902', '3559', 'ACTION module_archivage_get_generer_dossier', 3, '', 7, 1),
(4, '2022-03-26 18:16:20.622899', '3558', 'ACTION module_archivage_update_dossier', 3, '', 7, 1),
(5, '2022-03-26 18:16:20.628901', '3557', 'ACTION module_archivage_add_dossier', 3, '', 7, 1),
(6, '2022-03-26 18:16:20.632900', '3556', 'ACTION module_archivage_detail_dossier', 3, '', 7, 1),
(7, '2022-03-26 18:16:20.635906', '3555', 'ACTION module_archivage_list_dossier', 3, '', 7, 1),
(8, '2022-03-27 12:04:15.387275', '3564', 'ACTION module_archivage_get_generer_document', 3, '', 7, 1),
(9, '2022-03-27 12:04:15.394271', '3563', 'ACTION module_archivage_update_document', 3, '', 7, 1),
(10, '2022-03-27 12:04:15.400274', '3562', 'ACTION module_archivage_add_document', 3, '', 7, 1),
(11, '2022-03-27 12:04:15.405270', '3561', 'ACTION module_archivage_detail_document', 3, '', 7, 1),
(12, '2022-03-27 12:04:15.407270', '3560', 'ACTION module_archivage_list_document', 3, '', 7, 1),
(13, '2022-03-27 12:04:51.800800', '3212', 'Module Archivage / Rapport Documents', 3, '', 24, 1),
(14, '2022-03-27 12:04:51.807797', '3211', 'Module Archivage / Documents', 3, '', 24, 1),
(15, '2022-03-28 01:36:32.087720', '3569', 'ACTION module_archivage_get_generer_document', 3, '', 7, 1),
(16, '2022-03-28 01:36:32.096719', '3568', 'ACTION module_archivage_update_document', 3, '', 7, 1),
(17, '2022-03-28 01:36:32.102720', '3567', 'ACTION module_archivage_add_document', 3, '', 7, 1),
(18, '2022-03-28 01:36:32.107720', '3566', 'ACTION module_archivage_detail_document', 3, '', 7, 1),
(19, '2022-03-28 01:36:32.109720', '3565', 'ACTION module_archivage_list_document', 3, '', 7, 1),
(20, '2022-03-28 01:36:55.581213', '3214', 'Module Archivage / Rapport Documents', 3, '', 24, 1),
(21, '2022-03-28 01:36:55.589212', '3213', 'Module Archivage / Documents', 3, '', 24, 1),
(22, '2023-09-28 06:29:07.590280', '1', 'NSANDAX', 2, '[{\"changed\": {\"fields\": [\"Nom\", \"Email\", \"Phone\"]}}]', 19, 1),
(23, '2023-09-29 03:45:13.729165', '7', 'Admin', 2, '[{\"changed\": {\"fields\": [\"Prenom\", \"Nom\", \"Nom complet\", \"User\"]}}]', 21, 1),
(24, '2023-09-29 04:08:52.834130', '7', 'Admin', 2, '[]', 21, 1);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'ErpBackOffice', 'model_actionutilisateur'),
(8, 'ErpBackOffice', 'model_civilite'),
(9, 'ErpBackOffice', 'model_devise'),
(36, 'ErpBackOffice', 'model_employe'),
(10, 'ErpBackOffice', 'model_groupemenu'),
(11, 'ErpBackOffice', 'model_groupepermission'),
(12, 'ErpBackOffice', 'model_groupepermissionutilisateur'),
(13, 'ErpBackOffice', 'model_ligneregle'),
(14, 'ErpBackOffice', 'model_message'),
(15, 'ErpBackOffice', 'model_module'),
(16, 'ErpBackOffice', 'model_moduleovermodel'),
(17, 'ErpBackOffice', 'model_notification'),
(18, 'ErpBackOffice', 'model_operationnalisation_module'),
(19, 'ErpBackOffice', 'model_organisation'),
(20, 'ErpBackOffice', 'model_permission'),
(21, 'ErpBackOffice', 'model_personne'),
(22, 'ErpBackOffice', 'model_place'),
(23, 'ErpBackOffice', 'model_regle'),
(24, 'ErpBackOffice', 'model_sousmodule'),
(25, 'ErpBackOffice', 'model_taux'),
(26, 'ErpBackOffice', 'model_temp_notification'),
(27, 'ErpBackOffice', 'model_typeorganisation'),
(28, 'ErpBackOffice', 'model_usersessions'),
(29, 'ErpBackOffice', 'model_wkf_approbation'),
(30, 'ErpBackOffice', 'model_wkf_condition'),
(31, 'ErpBackOffice', 'model_wkf_etape'),
(32, 'ErpBackOffice', 'model_wkf_historique'),
(33, 'ErpBackOffice', 'model_wkf_stakeholder'),
(34, 'ErpBackOffice', 'model_wkf_transition'),
(35, 'ErpBackOffice', 'model_wkf_workflow'),
(40, 'ModuleArchivage', 'model_categorie_tag'),
(42, 'ModuleArchivage', 'model_document'),
(37, 'ModuleArchivage', 'model_document_archivage'),
(39, 'ModuleArchivage', 'model_document_partage'),
(41, 'ModuleArchivage', 'model_dossier'),
(38, 'ModuleArchivage', 'model_tag'),
(44, 'ModuleConfiguration', 'model_adresse'),
(45, 'ModuleConfiguration', 'model_commune'),
(46, 'ModuleConfiguration', 'model_contact'),
(52, 'ModuleConfiguration', 'model_district'),
(47, 'ModuleConfiguration', 'model_pays'),
(48, 'ModuleConfiguration', 'model_province'),
(43, 'ModuleConfiguration', 'model_query'),
(49, 'ModuleConfiguration', 'model_societe'),
(51, 'ModuleConfiguration', 'model_type_periode'),
(50, 'ModuleConfiguration', 'model_ville'),
(53, 'ModuleSupport', 'model_historique_action'),
(54, 'ModuleSupport', 'model_log'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'sessions', '0001_initial', '2022-04-04 07:56:24.474026'),
(2, 'contenttypes', '0001_initial', '2022-04-04 07:56:24.624028'),
(3, 'contenttypes', '0002_remove_content_type_name', '2022-04-04 07:56:24.767028'),
(4, 'auth', '0001_initial', '2022-04-04 07:56:25.596027'),
(5, 'ErpBackOffice', '0001_initial', '2022-04-04 07:56:39.313028'),
(6, 'ModuleArchivage', '0001_initial', '2022-04-04 07:56:41.669028'),
(7, 'admin', '0001_initial', '2022-04-04 07:56:41.908025'),
(8, 'admin', '0002_logentry_remove_auto_add', '2022-04-04 07:56:41.949029'),
(9, 'admin', '0003_logentry_add_action_flag_choices', '2022-04-04 07:56:42.081028'),
(10, 'auth', '0002_alter_permission_name_max_length', '2022-04-04 07:56:42.196025'),
(11, 'auth', '0003_alter_user_email_max_length', '2022-04-04 07:56:42.290028'),
(12, 'auth', '0004_alter_user_username_opts', '2022-04-04 07:56:42.324030'),
(13, 'auth', '0005_alter_user_last_login_null', '2022-04-04 07:56:42.419028'),
(14, 'auth', '0006_require_contenttypes_0002', '2022-04-04 07:56:42.438029'),
(15, 'auth', '0007_alter_validators_add_error_messages', '2022-04-04 07:56:42.473029'),
(16, 'auth', '0008_alter_user_username_max_length', '2022-04-04 07:56:42.576028'),
(17, 'auth', '0009_alter_user_last_name_max_length', '2022-04-04 07:56:42.662026'),
(18, 'ErpBackOffice', '0002_auto_20220502_1215', '2022-09-25 23:18:12.716402'),
(19, 'ModuleArchivage', '0002_auto_20220502_1159', '2022-09-25 23:18:12.774015'),
(20, 'ModuleArchivage', '0003_auto_20220502_1215', '2022-09-25 23:18:12.805468'),
(21, 'ModuleArchivage', '0004_auto_20220502_1330', '2022-09-25 23:18:12.857915'),
(22, 'ModuleArchivage', '0005_auto_20220506_0636', '2022-09-25 23:18:12.903729'),
(23, 'ModuleArchivage', '0006_auto_20220509_1256', '2022-09-25 23:18:13.042817'),
(24, 'ModuleArchivage', '0007_auto_20220512_1315', '2022-09-25 23:18:13.102494'),
(25, 'ModuleArchivage', '0008_auto_20220512_1318', '2022-09-25 23:18:13.158281'),
(26, 'ModuleArchivage', '0009_auto_20220512_1320', '2022-09-25 23:18:13.190426'),
(27, 'ModuleArchivage', '0010_auto_20220520_1131', '2022-09-25 23:18:13.226676'),
(28, 'ModuleArchivage', '0011_auto_20220520_1310', '2022-09-25 23:18:13.253889'),
(29, 'ModuleArchivage', '0012_auto_20220521_1104', '2022-09-25 23:18:13.286846'),
(30, 'ModuleArchivage', '0013_auto_20220531_1755', '2022-09-25 23:18:13.326999'),
(31, 'ModuleArchivage', '0014_auto_20220925_2317', '2022-09-25 23:18:13.374111'),
(32, 'ModuleConfiguration', '0001_initial', '2022-09-25 23:18:13.688480'),
(33, 'ModuleConfiguration', '0002_auto_20221208_1907', '2023-09-28 05:23:24.703571'),
(34, 'ErpBackOffice', '0003_remove_model_devise_est_virtuelle', '2023-09-28 05:23:24.801230'),
(35, 'ModuleConfiguration', '0003_auto_20230928_0518', '2023-09-28 05:23:29.048856'),
(36, 'ErpBackOffice', '0004_auto_20230928_0518', '2023-09-28 05:23:31.205410'),
(37, 'ModuleArchivage', '0015_auto_20220926_0905', '2023-09-28 05:23:31.327161'),
(38, 'ModuleArchivage', '0016_auto_20220926_0906', '2023-09-28 05:23:31.373926'),
(39, 'ModuleArchivage', '0017_auto_20220926_1044', '2023-09-28 05:23:31.420551'),
(40, 'ModuleArchivage', '0018_auto_20220926_1159', '2023-09-28 05:23:31.467726'),
(41, 'ModuleArchivage', '0019_auto_20220926_1435', '2023-09-28 05:23:31.514035'),
(42, 'ModuleArchivage', '0020_auto_20220926_1534', '2023-09-28 05:23:31.558813'),
(43, 'ModuleArchivage', '0021_auto_20221208_1907', '2023-09-28 05:23:31.602313'),
(44, 'ModuleArchivage', '0022_auto_20221212_0550', '2023-09-28 05:23:31.716072'),
(45, 'ModuleArchivage', '0023_auto_20221213_1715', '2023-09-28 05:23:31.758022'),
(46, 'ModuleArchivage', '0024_alter_model_document_access_token', '2023-09-28 05:23:31.804038'),
(47, 'ModuleArchivage', '0025_alter_model_document_access_token', '2023-09-28 05:23:31.846113'),
(48, 'ModuleArchivage', '0026_auto_20230928_0518', '2023-09-28 05:23:33.187143'),
(49, 'ModuleArchivage', '0027_alter_model_document_access_token', '2023-09-28 05:23:33.244097'),
(50, 'auth', '0010_alter_group_name_max_length', '2023-09-28 05:23:33.398565'),
(51, 'auth', '0011_update_proxy_permissions', '2023-09-28 05:23:33.452538'),
(52, 'auth', '0012_alter_user_first_name_max_length', '2023-09-28 05:23:33.514621'),
(53, 'ErpBackOffice', '0005_auto_20230928_1109', '2023-09-28 11:09:55.873739'),
(54, 'ErpBackOffice', '0006_auto_20230929_0211', '2023-09-29 02:44:32.775106'),
(55, 'ErpBackOffice', '0007_auto_20230929_0243', '2023-09-29 02:44:32.781116'),
(56, 'ErpBackOffice', '0008_auto_20230929_0245', '2023-09-29 02:45:54.291109'),
(57, 'ErpBackOffice', '0007_auto_20230929_0235', '2023-09-29 02:53:01.987370'),
(58, 'ErpBackOffice', '0008_auto_20230929_0240', '2023-09-29 02:53:02.002998'),
(59, 'ErpBackOffice', '0009_delete_model_employe', '2023-09-29 02:53:17.537084'),
(60, 'ErpBackOffice', '0002_initial', '2023-09-29 05:10:51.420511'),
(61, 'ModuleArchivage', '0002_initial', '2023-09-29 05:10:51.440121'),
(62, 'ModuleSupport', '0001_initial', '2023-10-07 16:16:23.951118'),
(63, 'ModuleConfiguration', '0002_auto_20231023_1042', '2023-10-23 10:42:45.129990'),
(64, 'ModuleSupport', '0002_auto_20231023_1042', '2023-10-23 10:42:45.151214'),
(65, 'ModuleConfiguration', '0003_model_adresse_societe', '2023-10-23 12:36:39.464190');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('6itplzrxvrp1ah5dhekfk3nwxp09po6f', 'ZGM2YjZkMmQxNjdlNWIxYjQzNTIzNzJiMmFhYTNjZGFjYjYyODQ5Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NjIyNDRiNTcyZWMwMDFlYzQyYzZhOWI4Y2EyNGFjYWQzY2YzYjU2IiwiTE9HSU5fQ09VTlQiOjF9', '2022-03-07 06:48:38.388456'),
('ker7aiqafb8a2v2i6efk1ovl4mk2b2v9', 'MDNkZWJjN2RhYWM3NWFmNjI5NjQwZWIyMGZhNzMzZWJhNzllNGZjMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NjIyNDRiNTcyZWMwMDFlYzQyYzZhOWI4Y2EyNGFjYWQzY2YzYjU2IiwiTE9HSU5fQ09VTlQiOjJ9', '2022-04-07 16:35:46.825261'),
('kmz1aeopx5ecnmzy2sowz2eh67bifoaz', '.eJxVjLkOwjAQBf_FNbJ8JD5SQoGQIGmgtrzeFQ6gRMpRIf6dREoB7Zt582YhzlMO80hDaJFVTLLd7wYxPalbAT5id-956rtpaIGvCt_oyC890mu_uX-BHMe8vEkbCQpBE4IlKBxptB49eVEKH5WRVIrSWJGcUORc0qaQyYpCRYmQxBI9N8dTHQ7Nrb6yyny-g6Y72A:1qurVC:kLZTQF0tlqpjBj9FVkrnnnDNXMLKii80Q8Eu7tRUrWg', '2023-11-06 10:45:38.313864'),
('qm4psndfd0idz3lnbobgjey2g45xj8fx', 'ZjczNTY5NDc4MWQzMjIxNWNmMTUxZjk3ZjcwNzY5NDFmNWJkN2Q0ODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5NjIyNDRiNTcyZWMwMDFlYzQyYzZhOWI4Y2EyNGFjYWQzY2YzYjU2IiwiTE9HSU5fQ09VTlQiOjN9', '2022-10-09 23:19:59.382846'),
('ug0uabe2ea98n3vczvwlynmr55p5iqvm', '.eJxVjDsLwjAURv9LZgk3SfPqqIMI2i46hyT3YqvSQh-T-N9toYOu3znfebMQ56kJ80hDaJGVTLDd75ZiflK3AnzE7t7z3HfT0Ca-KnyjI7_0SK_95v4Fmjg2y5uUEUliUoTJUiocKbQePXnQ4KM0gjRoYyE7kORcVqYQ2UIho8CUYYme6-OpCof6Vl1ZqT9fg6Q71w:1qrSG9:vk1vJc9_mc-pBKKwN5li8WskEtq_xtPfTwMx-eHEf0w', '2023-10-28 01:12:01.221642'),
('zlzb4kwdru2c8vgquuet2utnfpdc8de8', '.eJxVjLkOwjAQBf_FNbLWR3ykhAIhQdJAbdneFQmgRMpRIf6dREoB7Zt582YhzlMT5pGG0CIrmWC73y3F_KRuBfiI3b3nue-moU18VfhGR37pkV77zf0LNHFsljcpI5LEpAiTpaQdKbQePXkowEdpBBVQGAvZgSTnsjJaZAtaRoEpwxI918dTFQ71rbqyUn--g6I71g:1qliRq:HLsAdGuEv04GBjOYsdCIA1qUx5vhBdg32Q1CymMQw7c', '2023-10-12 05:16:22.294492');

-- --------------------------------------------------------

--
-- Structure de la table `document`
--

DROP TABLE IF EXISTS `document`;
CREATE TABLE IF NOT EXISTS `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(250) NOT NULL,
  `type` int(11) NOT NULL,
  `taille` int(11) DEFAULT NULL,
  `type_mime` int(11) NOT NULL,
  `mime` varchar(250) NOT NULL,
  `res_field` varchar(250) DEFAULT NULL,
  `res_id` int(11) DEFAULT NULL,
  `est_public` tinyint(1) NOT NULL,
  `est_archive` tinyint(1) NOT NULL,
  `est_bloque` tinyint(1) NOT NULL,
  `access_token` varchar(250) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `description` varchar(550) DEFAULT NULL,
  `indexation` varchar(4000) DEFAULT NULL,
  `fichier` varchar(100) NOT NULL,
  `miniature` varchar(100) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `auteur_blocage_id` int(11) DEFAULT NULL,
  `dossier_id` int(11) DEFAULT NULL,
  `res_model_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `document_auteur_id_c7cfa46e_fk_ErpBackOffice_model_personne_id` (`auteur_id`),
  KEY `document_auteur_blocage_id_5b4f16fe_fk_ErpBackOf` (`auteur_blocage_id`),
  KEY `document_dossier_id_75692ce9_fk_dossier_id` (`dossier_id`),
  KEY `document_res_model_id_96784805_fk_django_content_type_id` (`res_model_id`),
  KEY `document_statut_id_387fe1ab_fk_ErpBackOffice_model_wkf_etape_id` (`statut_id`),
  KEY `document_company_id_aa203b11_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `document`
--

INSERT INTO `document` (`id`, `designation`, `type`, `taille`, `type_mime`, `mime`, `res_field`, `res_id`, `est_public`, `est_archive`, `est_bloque`, `access_token`, `url`, `description`, `indexation`, `fichier`, `miniature`, `etat`, `creation_date`, `update_date`, `auteur_id`, `auteur_blocage_id`, `dossier_id`, `res_model_id`, `statut_id`, `company_id`) VALUES
(1, 'Fichier test.py', 1, 250, 2, 'application/pdf', 'fichier', 1, 1, 0, 1, '', '', 'RAS', 'RAS', 'uploads/2022/03/28/640059.png', 'uploads/2022/03/28/accueil_erp.PNG', NULL, '2022-03-28 01:44:13.133272', '2022-03-28 01:44:13.133272', NULL, 7, NULL, 8, NULL, NULL),
(3, 'Fiches social.docx', 1, 250, 3, 'application/pdf', 'fichier', 1, 1, 0, 1, '', '', 'RAS', 'RAS', 'uploads/2022/04/01/Fiche_sociale.docx', '', NULL, '2022-04-01 13:44:16.086485', '2022-04-01 13:44:16.086485', NULL, 7, NULL, 8, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `document_archivage`
--

DROP TABLE IF EXISTS `document_archivage`;
CREATE TABLE IF NOT EXISTS `document_archivage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `document_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `document_archivage_auteur_id_e660ad69_fk_ErpBackOf` (`auteur_id`),
  KEY `document_archivage_document_id_6607a579_fk_document_id` (`document_id`),
  KEY `document_archivage_company_id_087a3dd9_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `document_favoris`
--

DROP TABLE IF EXISTS `document_favoris`;
CREATE TABLE IF NOT EXISTS `document_favoris` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_document_id` int(11) NOT NULL,
  `model_personne_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `document_favoris_model_document_id_model__2a7c2019_uniq` (`model_document_id`,`model_personne_id`),
  KEY `document_favoris_model_personne_id_353670ba_fk_ErpBackOf` (`model_personne_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `document_partage`
--

DROP TABLE IF EXISTS `document_partage`;
CREATE TABLE IF NOT EXISTS `document_partage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(250) NOT NULL,
  `type` int(11) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `date_echeance` datetime(6) DEFAULT NULL,
  `description` varchar(550) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `document_partage_auteur_id_445291ff_fk_ErpBackOf` (`auteur_id`),
  KEY `document_partage_statut_id_ac69bd4e_fk_ErpBackOf` (`statut_id`),
  KEY `document_partage_company_id_f0b5cddc_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `document_partage`
--

INSERT INTO `document_partage` (`id`, `designation`, `type`, `url`, `date_echeance`, `description`, `etat`, `creation_date`, `update_date`, `auteur_id`, `statut_id`, `company_id`) VALUES
(1, 'Test lien partagé', 1, 'http://test.com', '2022-03-28 02:30:00.000000', 'RAS', NULL, '2022-03-28 02:32:05.281282', '2022-03-28 02:32:05.281282', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `document_partage_documents`
--

DROP TABLE IF EXISTS `document_partage_documents`;
CREATE TABLE IF NOT EXISTS `document_partage_documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_document_partage_id` int(11) NOT NULL,
  `model_document_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `document_partage_documen_model_document_partage_i_d55365eb_uniq` (`model_document_partage_id`,`model_document_id`),
  KEY `document_partage_doc_model_document_id_2e6705d6_fk_document_` (`model_document_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `document_partage_documents`
--

INSERT INTO `document_partage_documents` (`id`, `model_document_partage_id`, `model_document_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `document_tags`
--

DROP TABLE IF EXISTS `document_tags`;
CREATE TABLE IF NOT EXISTS `document_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_document_id` int(11) NOT NULL,
  `model_tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `document_tags_model_document_id_model_tag_id_1f1ebac5_uniq` (`model_document_id`,`model_tag_id`),
  KEY `document_tags_model_tag_id_9535f977_fk_tag_id` (`model_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `dossier`
--

DROP TABLE IF EXISTS `dossier`;
CREATE TABLE IF NOT EXISTS `dossier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(250) NOT NULL,
  `sequence` varchar(100) DEFAULT NULL,
  `description` varchar(550) DEFAULT NULL,
  `owner_read` tinyint(1) NOT NULL,
  `est_racine` tinyint(1) NOT NULL,
  `est_archivage` tinyint(1) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dossier_auteur_id_07552c1f_fk_ErpBackOffice_model_personne_id` (`auteur_id`),
  KEY `dossier_parent_id_2899561c_fk_dossier_id` (`parent_id`),
  KEY `dossier_statut_id_a70eb421_fk_ErpBackOffice_model_wkf_etape_id` (`statut_id`),
  KEY `dossier_company_id_bf71da5f_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `dossier`
--

INSERT INTO `dossier` (`id`, `designation`, `sequence`, `description`, `owner_read`, `est_racine`, `est_archivage`, `etat`, `creation_date`, `update_date`, `auteur_id`, `parent_id`, `statut_id`, `company_id`) VALUES
(1, 'Dossier test 1', '1', 'RAS', 1, 1, 1, NULL, '2022-03-28 02:24:20.616336', '2022-03-28 02:24:20.616336', NULL, NULL, NULL, NULL),
(2, 'Dossier test 3', '2', 'RAS', 1, 1, 1, NULL, '2022-03-28 02:25:23.263165', '2022-03-28 02:27:36.289192', NULL, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `dossier_read_groups`
--

DROP TABLE IF EXISTS `dossier_read_groups`;
CREATE TABLE IF NOT EXISTS `dossier_read_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_dossier_id` int(11) NOT NULL,
  `model_groupepermission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dossier_read_groups_model_dossier_id_model_g_0a022a95_uniq` (`model_dossier_id`,`model_groupepermission_id`),
  KEY `dossier_read_groups_model_groupepermissi_a521e772_fk_ErpBackOf` (`model_groupepermission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `dossier_read_groups`
--

INSERT INTO `dossier_read_groups` (`id`, `model_dossier_id`, `model_groupepermission_id`) VALUES
(1, 1, 2),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `dossier_write_groups`
--

DROP TABLE IF EXISTS `dossier_write_groups`;
CREATE TABLE IF NOT EXISTS `dossier_write_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_dossier_id` int(11) NOT NULL,
  `model_groupepermission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dossier_write_groups_model_dossier_id_model_g_e71473af_uniq` (`model_dossier_id`,`model_groupepermission_id`),
  KEY `dossier_write_groups_model_groupepermissi_6b987731_fk_ErpBackOf` (`model_groupepermission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_actionutilisateur`
--

DROP TABLE IF EXISTS `erpbackoffice_model_actionutilisateur`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_actionutilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_action` varchar(200) DEFAULT NULL,
  `ref_action` varchar(200) DEFAULT NULL,
  `description` longtext NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_actionutilisateur_auteur_id_aa959d04` (`auteur_id`),
  KEY `ErpBackOffice_model_actionutilisateur_permission_id_966ab320` (`permission_id`),
  KEY `ErpBackOffice_model_actionutilisateur_statut_id_e80c738f` (`statut_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3658 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_actionutilisateur`
--

INSERT INTO `erpbackoffice_model_actionutilisateur` (`id`, `nom_action`, `ref_action`, `description`, `url`, `etat`, `update_date`, `creation_date`, `auteur_id`, `permission_id`, `statut_id`) VALUES
(10, 'get_lister_utilisateurs', '', '', NULL, NULL, '2021-05-29 17:50:51.898783', '2021-05-29 17:50:51.898783', NULL, 3703, NULL),
(12, 'get_lister_roles', '', '', NULL, NULL, '2021-05-29 18:24:55.682204', '2021-05-29 18:24:55.682204', NULL, 3713, NULL),
(13, 'get_lister_modules', '', '', NULL, NULL, '2021-05-29 18:25:10.096618', '2021-05-29 18:25:10.096618', NULL, 3717, NULL),
(14, 'get_details_module', '', '', NULL, NULL, '2021-05-29 18:25:12.185005', '2021-05-29 18:25:12.185005', NULL, 3717, NULL),
(15, 'get_lister_regle', '', '', NULL, NULL, '2021-06-01 12:49:50.296668', '2021-06-01 12:49:50.296668', NULL, 3734, NULL),
(16, 'get_creer_regle', '', '', NULL, NULL, '2021-06-01 12:49:52.864267', '2021-06-01 12:49:52.864267', NULL, 3735, NULL),
(17, 'get_details_regle', '', '', NULL, NULL, '2021-06-01 13:02:41.116127', '2021-06-01 13:02:41.116127', NULL, 3734, NULL),
(19, 'get_details_utilisateur', '', '', NULL, NULL, '2021-06-02 11:37:37.534651', '2021-06-02 11:37:37.534651', NULL, 3703, NULL),
(364, 'get_creer_wizard_menu', NULL, 'XD', NULL, NULL, '2021-06-04 12:49:58.363065', '2021-06-04 11:57:14.276480', NULL, 3757, NULL),
(365, 'get_creer_sousmodule', '', '', NULL, NULL, '2021-06-04 12:34:39.474635', '2021-06-04 12:34:39.474635', NULL, 3751, NULL),
(366, 'get_lister_sousmodule', '', '', NULL, NULL, '2021-06-04 12:35:45.841130', '2021-06-04 12:35:45.841130', NULL, 3750, NULL),
(368, 'get_details_sousmodule', '', '', NULL, NULL, '2021-06-04 12:41:06.630401', '2021-06-04 12:41:06.630401', NULL, 3750, NULL),
(369, 'get_lister_actionutilisateur', '', '', NULL, NULL, '2021-06-04 12:41:24.913816', '2021-06-04 12:41:24.913816', NULL, 3742, NULL),
(370, 'get_lister_permission', '', '', NULL, NULL, '2021-06-04 12:42:57.391409', '2021-06-04 12:42:57.391409', NULL, 3738, NULL),
(381, 'get_creer_wizard_menu', '', '', NULL, NULL, '2021-06-08 08:34:59.191852', '2021-06-08 08:34:59.191852', NULL, 3751, NULL),
(389, 'get_details_role', '', '', NULL, NULL, '2021-06-08 12:53:10.442663', '2021-06-08 12:53:10.442663', NULL, 3713, NULL),
(390, 'get_attribuer_role', '', '', NULL, NULL, '2021-06-08 12:53:22.829336', '2021-06-08 12:53:22.829336', NULL, 3711, NULL),
(391, 'get_ajouter_droits', '', '', NULL, NULL, '2021-06-08 13:01:10.379102', '2021-06-08 13:01:10.379102', NULL, 3715, NULL),
(392, 'get_creer_role', '', '', NULL, NULL, '2021-06-08 13:03:57.762615', '2021-06-08 13:03:57.762615', NULL, 3714, NULL),
(1380, 'get_creer_permission', '', '', NULL, NULL, '2021-06-12 02:49:12.665391', '2021-06-12 02:49:12.665391', NULL, 3739, NULL),
(1381, 'get_details_permission', '', '', NULL, NULL, '2021-06-12 02:50:20.142853', '2021-06-12 02:50:20.142853', NULL, 3738, NULL),
(1382, 'get_creer_actionutilisateur', '', '', NULL, NULL, '2021-06-12 02:54:15.879184', '2021-06-12 02:54:15.879184', NULL, 3743, NULL),
(1384, 'get_details_actionutilisateur', '', '', NULL, NULL, '2021-06-12 02:54:31.059231', '2021-06-12 02:54:31.059231', NULL, 3742, NULL),
(1399, 'get_lister_groupemenu', '', '', NULL, NULL, '2021-06-13 16:44:04.591876', '2021-06-13 16:44:04.591876', NULL, 3746, NULL),
(1400, 'get_creer_groupemenu', '', '', NULL, NULL, '2021-06-13 16:44:06.587287', '2021-06-13 16:44:06.587287', NULL, 3747, NULL),
(1401, 'get_details_groupemenu', '', '', NULL, NULL, '2021-06-13 16:44:33.318342', '2021-06-13 16:44:33.318342', NULL, 3746, NULL),
(1403, 'get_creer_module', '', '', NULL, NULL, '2021-06-13 17:29:10.232835', '2021-06-13 17:29:10.232835', NULL, 3718, NULL),
(1404, 'get_creer_modele', '', '', NULL, NULL, '2021-06-13 17:29:15.381316', '2021-06-13 17:29:15.381316', NULL, 3718, NULL),
(1424, 'get_lister_workflow', '', '', NULL, NULL, '2021-06-28 12:47:24.229241', '2021-06-28 12:47:24.229241', NULL, 3729, NULL),
(1428, 'get_modifier_permission', '', '', NULL, NULL, '2021-07-19 13:38:42.442322', '2021-07-19 13:38:42.442322', NULL, 3740, NULL),
(1429, 'get_modifier_sousmodule', '', '', NULL, NULL, '2021-07-19 20:47:34.119813', '2021-07-19 20:47:34.119813', NULL, 3752, NULL),
(1439, 'get_modifier_actionutilisateur', '', '', NULL, NULL, '2021-08-10 02:35:10.191095', '2021-08-10 02:35:10.191095', NULL, 3744, NULL),
(3477, 'get_creer_modele_gen', '', '', NULL, NULL, '2021-10-06 01:30:24.384792', '2021-10-06 01:30:24.384792', NULL, 3718, NULL),
(3493, 'get_details_workflow', '', '', NULL, NULL, '2021-10-06 06:59:17.946956', '2021-10-06 06:59:17.946956', NULL, 3729, NULL),
(3502, 'get_retirer_droits', '', '', NULL, NULL, '2021-10-06 09:07:23.491249', '2021-10-06 09:07:23.491249', NULL, 3715, NULL),
(3541, 'get_creer_sous_module_of_module', '', '', NULL, NULL, '2021-12-20 15:48:17.357706', '2021-12-20 15:48:17.357706', NULL, 3718, NULL),
(3552, 'get_creer_utilisateur', '', '', NULL, NULL, '2021-12-21 08:20:13.543645', '2021-12-21 08:20:13.543645', NULL, 3710, NULL),
(3553, 'get_creer_workflow', '', '', NULL, NULL, '2021-12-21 16:09:22.402475', '2021-12-21 16:09:22.402475', NULL, 3730, NULL),
(3554, 'get_modifier_role', '', '', NULL, NULL, '2021-12-22 10:14:11.386203', '2021-12-22 10:14:11.386203', NULL, 3715, NULL),
(3570, 'get_lister_sous_modules_of_module', '', '', NULL, NULL, '2022-03-27 16:28:49.207610', '2022-03-27 16:28:49.207610', NULL, 3717, NULL),
(3571, 'module_archivage_list_document', '', '', NULL, NULL, '2022-03-28 01:40:50.258414', '2022-03-28 01:40:50.258414', NULL, 3779, NULL),
(3572, 'module_archivage_detail_document', '', '', NULL, NULL, '2022-03-28 01:40:50.265411', '2022-03-28 01:40:50.265411', NULL, 3779, NULL),
(3573, 'module_archivage_add_document', '', '', NULL, NULL, '2022-03-28 01:40:50.279413', '2022-03-28 01:40:50.279413', NULL, 3780, NULL),
(3574, 'module_archivage_update_document', '', '', NULL, NULL, '2022-03-28 01:40:50.294414', '2022-03-28 01:40:50.294414', NULL, 3781, NULL),
(3575, 'module_archivage_get_generer_document', '', '', NULL, NULL, '2022-03-28 01:40:50.301413', '2022-03-28 01:40:50.301413', NULL, 3782, NULL),
(3576, 'module_archivage_list_dossier', '', '', NULL, NULL, '2022-03-28 02:10:16.380797', '2022-03-28 02:10:16.380797', NULL, 3784, NULL),
(3577, 'module_archivage_detail_dossier', '', '', NULL, NULL, '2022-03-28 02:10:16.389798', '2022-03-28 02:10:16.389798', NULL, 3784, NULL),
(3578, 'module_archivage_add_dossier', '', '', NULL, NULL, '2022-03-28 02:10:16.409795', '2022-03-28 02:10:16.409795', NULL, 3785, NULL),
(3579, 'module_archivage_update_dossier', '', '', NULL, NULL, '2022-03-28 02:10:16.435800', '2022-03-28 02:10:16.435800', NULL, 3786, NULL),
(3580, 'module_archivage_get_generer_dossier', '', '', NULL, NULL, '2022-03-28 02:10:16.456795', '2022-03-28 02:10:16.456795', NULL, 3787, NULL),
(3581, 'module_archivage_list_categorie_tag', '', '', NULL, NULL, '2022-03-28 02:13:04.339360', '2022-03-28 02:13:04.339360', NULL, 3789, NULL),
(3582, 'module_archivage_detail_categorie_tag', '', '', NULL, NULL, '2022-03-28 02:13:04.347360', '2022-03-28 02:13:04.347360', NULL, 3789, NULL),
(3583, 'module_archivage_add_categorie_tag', '', '', NULL, NULL, '2022-03-28 02:13:04.360358', '2022-03-28 02:13:04.360358', NULL, 3790, NULL),
(3584, 'module_archivage_update_categorie_tag', '', '', NULL, NULL, '2022-03-28 02:13:04.374363', '2022-03-28 02:13:04.374363', NULL, 3791, NULL),
(3585, 'module_archivage_get_generer_categorie_tag', '', '', NULL, NULL, '2022-03-28 02:13:04.382365', '2022-03-28 02:13:04.382365', NULL, 3792, NULL),
(3586, 'module_archivage_list_tag', '', '', NULL, NULL, '2022-03-28 02:17:52.521635', '2022-03-28 02:17:52.521635', NULL, 3794, NULL),
(3587, 'module_archivage_detail_tag', '', '', NULL, NULL, '2022-03-28 02:17:52.526635', '2022-03-28 02:17:52.526635', NULL, 3794, NULL),
(3588, 'module_archivage_add_tag', '', '', NULL, NULL, '2022-03-28 02:17:52.537632', '2022-03-28 02:17:52.537632', NULL, 3795, NULL),
(3589, 'module_archivage_update_tag', '', '', NULL, NULL, '2022-03-28 02:17:52.547632', '2022-03-28 02:17:52.547632', NULL, 3796, NULL),
(3590, 'module_archivage_get_generer_tag', '', '', NULL, NULL, '2022-03-28 02:17:52.552634', '2022-03-28 02:17:52.552634', NULL, 3797, NULL),
(3591, 'module_archivage_list_document_partage', '', '', NULL, NULL, '2022-03-28 02:21:19.813243', '2022-03-28 02:21:19.813243', NULL, 3799, NULL),
(3592, 'module_archivage_detail_document_partage', '', '', NULL, NULL, '2022-03-28 02:21:19.829187', '2022-03-28 02:21:19.830185', NULL, 3799, NULL),
(3593, 'module_archivage_add_document_partage', '', '', NULL, NULL, '2022-03-28 02:21:19.853184', '2022-03-28 02:21:19.853184', NULL, 3800, NULL),
(3594, 'module_archivage_update_document_partage', '', '', NULL, NULL, '2022-03-28 02:21:19.887186', '2022-03-28 02:21:19.887186', NULL, 3801, NULL),
(3595, 'module_archivage_get_generer_document_partage', '', '', NULL, NULL, '2022-03-28 02:21:19.913185', '2022-03-28 02:21:19.913185', NULL, 3802, NULL),
(3598, 'module_support_list_historique_action', '', '', NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3809, NULL),
(3599, 'module_support_detail_historique_action', '', '', NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3809, NULL),
(3600, 'module_support_add_historique_action', '', '', NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3810, NULL),
(3601, 'module_support_update_historique_action', '', '', NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3811, NULL),
(3602, 'module_support_get_generer_historique_action', '', '', NULL, NULL, '2023-10-15 13:39:44.322464', '2023-10-15 13:39:44.322464', 7, 3812, NULL),
(3603, 'module_support_list_log', '', '', NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3814, NULL),
(3604, 'module_support_detail_log', '', '', NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3814, NULL),
(3605, 'module_support_add_log', '', '', NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3815, NULL),
(3606, 'module_support_update_log', '', '', NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3816, NULL),
(3607, 'module_support_get_generer_log', '', '', NULL, NULL, '2023-10-15 13:40:51.890502', '2023-10-15 13:40:51.890502', 7, 3817, NULL),
(3608, 'module_configuration_list_societe', '', '', NULL, NULL, '2023-10-23 12:32:44.522632', '2023-10-23 12:32:44.522632', 7, 3819, NULL),
(3609, 'module_configuration_detail_societe', '', '', NULL, NULL, '2023-10-23 12:32:44.528247', '2023-10-23 12:32:44.528247', 7, 3819, NULL),
(3610, 'module_configuration_add_societe', '', '', NULL, NULL, '2023-10-23 12:32:44.530267', '2023-10-23 12:32:44.530267', 7, 3820, NULL),
(3611, 'module_configuration_update_societe', '', '', NULL, NULL, '2023-10-23 12:32:44.532247', '2023-10-23 12:32:44.532247', 7, 3821, NULL),
(3612, 'module_configuration_get_generer_societe', '', '', NULL, NULL, '2023-10-23 12:32:44.534250', '2023-10-23 12:32:44.534250', 7, 3822, NULL),
(3613, 'module_configuration_list_contact', '', '', NULL, NULL, '2023-10-23 12:39:00.554024', '2023-10-23 12:39:00.554024', 7, 3824, NULL),
(3614, 'module_configuration_detail_contact', '', '', NULL, NULL, '2023-10-23 12:39:00.554024', '2023-10-23 12:39:00.554024', 7, 3824, NULL),
(3615, 'module_configuration_add_contact', '', '', NULL, NULL, '2023-10-23 12:39:00.559283', '2023-10-23 12:39:00.559283', 7, 3825, NULL),
(3616, 'module_configuration_update_contact', '', '', NULL, NULL, '2023-10-23 12:39:00.561284', '2023-10-23 12:39:00.561284', 7, 3826, NULL),
(3617, 'module_configuration_get_generer_contact', '', '', NULL, NULL, '2023-10-23 12:39:00.563288', '2023-10-23 12:39:00.563288', 7, 3827, NULL),
(3618, 'module_configuration_list_adresse', '', '', NULL, NULL, '2023-10-23 12:39:32.228383', '2023-10-23 12:39:32.228383', 7, 3829, NULL),
(3619, 'module_configuration_detail_adresse', '', '', NULL, NULL, '2023-10-23 12:39:32.230449', '2023-10-23 12:39:32.230449', 7, 3829, NULL),
(3620, 'module_configuration_add_adresse', '', '', NULL, NULL, '2023-10-23 12:39:32.234511', '2023-10-23 12:39:32.234511', 7, 3830, NULL),
(3621, 'module_configuration_update_adresse', '', '', NULL, NULL, '2023-10-23 12:39:32.239049', '2023-10-23 12:39:32.239049', 7, 3831, NULL),
(3622, 'module_configuration_get_generer_adresse', '', '', NULL, NULL, '2023-10-23 12:39:32.243115', '2023-10-23 12:39:32.243115', 7, 3832, NULL),
(3623, 'module_configuration_list_pays', '', '', NULL, NULL, '2023-10-23 12:40:34.129013', '2023-10-23 12:40:34.129013', 7, 3834, NULL),
(3624, 'module_configuration_detail_pays', '', '', NULL, NULL, '2023-10-23 12:40:34.130054', '2023-10-23 12:40:34.130054', 7, 3834, NULL),
(3625, 'module_configuration_add_pays', '', '', NULL, NULL, '2023-10-23 12:40:34.132015', '2023-10-23 12:40:34.132015', 7, 3835, NULL),
(3626, 'module_configuration_update_pays', '', '', NULL, NULL, '2023-10-23 12:40:34.135022', '2023-10-23 12:40:34.135022', 7, 3836, NULL),
(3627, 'module_configuration_get_generer_pays', '', '', NULL, NULL, '2023-10-23 12:40:34.136888', '2023-10-23 12:40:34.136888', 7, 3837, NULL),
(3628, 'module_configuration_list_province', '', '', NULL, NULL, '2023-10-23 12:41:06.463847', '2023-10-23 12:41:06.463847', 7, 3839, NULL),
(3629, 'module_configuration_detail_province', '', '', NULL, NULL, '2023-10-23 12:41:06.463847', '2023-10-23 12:41:06.463847', 7, 3839, NULL),
(3630, 'module_configuration_add_province', '', '', NULL, NULL, '2023-10-23 12:41:06.465846', '2023-10-23 12:41:06.465846', 7, 3840, NULL),
(3631, 'module_configuration_update_province', '', '', NULL, NULL, '2023-10-23 12:41:06.467566', '2023-10-23 12:41:06.467566', 7, 3841, NULL),
(3632, 'module_configuration_get_generer_province', '', '', NULL, NULL, '2023-10-23 12:41:06.470678', '2023-10-23 12:41:06.470678', 7, 3842, NULL),
(3633, 'module_configuration_list_ville', '', '', NULL, NULL, '2023-10-23 12:41:45.770623', '2023-10-23 12:41:45.770623', 7, 3844, NULL),
(3634, 'module_configuration_detail_ville', '', '', NULL, NULL, '2023-10-23 12:41:45.771631', '2023-10-23 12:41:45.771631', 7, 3844, NULL),
(3635, 'module_configuration_add_ville', '', '', NULL, NULL, '2023-10-23 12:41:45.775284', '2023-10-23 12:41:45.775284', 7, 3845, NULL),
(3636, 'module_configuration_update_ville', '', '', NULL, NULL, '2023-10-23 12:41:45.776293', '2023-10-23 12:41:45.776293', 7, 3846, NULL),
(3637, 'module_configuration_get_generer_ville', '', '', NULL, NULL, '2023-10-23 12:41:45.778291', '2023-10-23 12:41:45.778291', 7, 3847, NULL),
(3638, 'module_configuration_list_district', '', '', NULL, NULL, '2023-10-23 12:43:42.622737', '2023-10-23 12:43:42.622737', 7, 3849, NULL),
(3639, 'module_configuration_detail_district', '', '', NULL, NULL, '2023-10-23 12:43:42.622737', '2023-10-23 12:43:42.622737', 7, 3849, NULL),
(3640, 'module_configuration_add_district', '', '', NULL, NULL, '2023-10-23 12:43:42.624737', '2023-10-23 12:43:42.624737', 7, 3850, NULL),
(3641, 'module_configuration_update_district', '', '', NULL, NULL, '2023-10-23 12:43:42.625737', '2023-10-23 12:43:42.625737', 7, 3851, NULL),
(3642, 'module_configuration_get_generer_district', '', '', NULL, NULL, '2023-10-23 12:43:42.627803', '2023-10-23 12:43:42.627803', 7, 3852, NULL),
(3643, 'module_configuration_list_commune', '', '', NULL, NULL, '2023-10-23 12:44:38.873714', '2023-10-23 12:44:38.873714', 7, 3854, NULL),
(3644, 'module_configuration_detail_commune', '', '', NULL, NULL, '2023-10-23 12:44:38.875182', '2023-10-23 12:44:38.875182', 7, 3854, NULL),
(3645, 'module_configuration_add_commune', '', '', NULL, NULL, '2023-10-23 12:44:38.879196', '2023-10-23 12:44:38.879196', 7, 3855, NULL),
(3646, 'module_configuration_update_commune', '', '', NULL, NULL, '2023-10-23 12:44:38.881192', '2023-10-23 12:44:38.881192', 7, 3856, NULL),
(3647, 'module_configuration_get_generer_commune', '', '', NULL, NULL, '2023-10-23 12:44:38.884191', '2023-10-23 12:44:38.884191', 7, 3857, NULL),
(3653, 'module_configuration_list_type_periode', '', '', NULL, NULL, '2023-10-23 12:47:51.075306', '2023-10-23 12:47:51.075306', 7, 3864, NULL),
(3654, 'module_configuration_detail_type_periode', '', '', NULL, NULL, '2023-10-23 12:47:51.076317', '2023-10-23 12:47:51.076317', 7, 3864, NULL),
(3655, 'module_configuration_add_type_periode', '', '', NULL, NULL, '2023-10-23 12:47:51.078746', '2023-10-23 12:47:51.078746', 7, 3865, NULL),
(3656, 'module_configuration_update_type_periode', '', '', NULL, NULL, '2023-10-23 12:47:51.081845', '2023-10-23 12:47:51.081845', 7, 3866, NULL),
(3657, 'module_configuration_get_generer_type_periode', '', '', NULL, NULL, '2023-10-23 12:47:51.086062', '2023-10-23 12:47:51.086062', 7, 3867, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_civilite`
--

DROP TABLE IF EXISTS `erpbackoffice_model_civilite`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_civilite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(20) NOT NULL,
  `designation_court` varchar(5) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_civilite_auteur_id_0226f22d` (`auteur_id`),
  KEY `ErpBackOffice_model__statut_id_ce0d439f_fk_ErpBackOf` (`statut_id`),
  KEY `ErpBackOffice_model__company_id_2da0dc37_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_devise`
--

DROP TABLE IF EXISTS `erpbackoffice_model_devise`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_devise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbole_devise` varchar(5) DEFAULT NULL,
  `code_iso` varchar(5) DEFAULT NULL,
  `designation` varchar(200) DEFAULT NULL,
  `est_reference` tinyint(1) NOT NULL,
  `est_active` tinyint(1) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `code_sous_unite` varchar(20) DEFAULT NULL,
  `designation_sous_unite` varchar(200) DEFAULT NULL,
  `est_locale` tinyint(1) NOT NULL,
  `num_decimale` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `sous_unite` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_devise_auteur_id_2b88a169` (`auteur_id`),
  KEY `ErpBackOffice_model_devise_statut_id_567b6268` (`statut_id`),
  KEY `ErpBackOffice_model_devise_company_id_37a3a837_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_groupemenu`
--

DROP TABLE IF EXISTS `erpbackoffice_model_groupemenu`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_groupemenu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) DEFAULT NULL,
  `icon_menu` varchar(150) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `numero_ordre` int(11) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `module_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_groupemenu_auteur_id_55bd7e3e` (`auteur_id`),
  KEY `ErpBackOffice_model_groupemenu_module_id_4519e285` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_groupemenu`
--

INSERT INTO `erpbackoffice_model_groupemenu` (`id`, `designation`, `icon_menu`, `description`, `url`, `numero_ordre`, `creation_date`, `auteur_id`, `module_id`) VALUES
(1, 'Utilisateur', 'user.svg', NULL, NULL, 1, '2020-06-19 14:31:45.730992', NULL, 5),
(2, 'Sécurité', 'tick-inside-circle.svg', NULL, NULL, 2, '2021-06-03 16:21:30.976786', NULL, 5),
(3, 'Génération', 'settings-gears.svg', NULL, NULL, 4, '2021-06-03 16:21:44.964332', NULL, 5),
(4, 'Workflow', 'workflow.svg', NULL, NULL, 5, '2021-06-03 16:21:48.014185', NULL, 5),
(5, 'Configuration', 'setting.svg', NULL, NULL, 6, '2021-06-03 16:23:42.956028', NULL, 5),
(51, 'Layout', 'line-chart-for-business.svg', NULL, NULL, 3, '2021-06-03 16:21:54.465126', NULL, 5),
(52, 'Archivage', 'achats.svg', 'Menu Archivage', NULL, 1, '2022-03-24 16:40:14.188816', NULL, 7),
(53, 'Analyses', 'line-chart-for-business.svg', 'Menu Analyses', NULL, 2, '2022-03-24 16:40:14.199813', NULL, 7),
(54, 'Configurations', 'setting.svg', 'Menu Configurations', NULL, 3, '2022-03-24 16:40:14.204815', NULL, 7),
(55, 'Support', 'achats.svg', 'Groupe Menu Support', NULL, 1, '2023-09-29 05:39:38.447479', 7, 8),
(56, 'Rapports', 'file.svg', 'Groupe Menu Rapports', NULL, 2, '2023-09-29 05:39:38.447479', 7, 8),
(57, 'Business Intelligence', 'line-chart-for-business.svg', 'Groupe Menu Business Intelligence', NULL, 3, '2023-09-29 05:39:38.459421', 7, 8),
(58, 'Configurations', 'setting.svg', 'Groupe Menu Configurations', NULL, 4, '2023-09-29 05:39:38.459421', 7, 8);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_groupepermission`
--

DROP TABLE IF EXISTS `erpbackoffice_model_groupepermission`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_groupepermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(100) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_groupepermission_auteur_id_ba5aed16` (`auteur_id`),
  KEY `ErpBackOffice_model_groupepermission_statut_id_dbfb3cd4` (`statut_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_groupepermission`
--

INSERT INTO `erpbackoffice_model_groupepermission` (`id`, `designation`, `etat`, `update_date`, `creation_date`, `url`, `auteur_id`, `statut_id`) VALUES
(2, 'Administrateur ARPCE', NULL, '2021-05-29 16:14:35.609996', '2020-03-28 13:59:34.350219', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_groupepermissionutilisateur`
--

DROP TABLE IF EXISTS `erpbackoffice_model_groupepermissionutilisateur`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_groupepermissionutilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `groupe_permission_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `utilisateur_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_groupep_auteur_id_b1fb3c41` (`auteur_id`),
  KEY `ErpBackOffice_model_groupep_groupe_permission_id_2496c315` (`groupe_permission_id`),
  KEY `ErpBackOffice_model_groupep_statut_id_d5eace5b` (`statut_id`),
  KEY `ErpBackOffice_model_groupep_utilisateur_id_f1bb30f0` (`utilisateur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_groupepermission_permissions`
--

DROP TABLE IF EXISTS `erpbackoffice_model_groupepermission_permissions`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_groupepermission_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_groupepermission_id` int(11) NOT NULL,
  `model_permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ErpBackOffice_model_grou_model_groupepermission_i_9cc87f8e_uniq` (`model_groupepermission_id`,`model_permission_id`),
  KEY `ErpBackOffice_model_groupep_model_groupepermission_id_a3381349` (`model_groupepermission_id`),
  KEY `ErpBackOffice_model_groupep_model_permission_id_012945be` (`model_permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_ligneregle`
--

DROP TABLE IF EXISTS `erpbackoffice_model_ligneregle`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_ligneregle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sequence` int(11) NOT NULL,
  `type_operation` int(11) NOT NULL,
  `type_condition` int(11) NOT NULL,
  `valeur` varchar(500) DEFAULT NULL,
  `code` varchar(500) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `regle_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model__auteur_id_7e4fdfc9_fk_ErpBackOf` (`auteur_id`),
  KEY `ErpBackOffice_model__regle_id_ab01ec55_fk_ErpBackOf` (`regle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_message`
--

DROP TABLE IF EXISTS `erpbackoffice_model_message`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `objet` varchar(50) DEFAULT NULL,
  `corps` varchar(500) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `expediteur_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_message_auteur_id_49f2810d` (`auteur_id`),
  KEY `ErpBackOffice_model_message_statut_id_91b74f23` (`statut_id`),
  KEY `ErpBackOffice_model_message_expediteur_id_c4dcca45` (`expediteur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_message_destinataire`
--

DROP TABLE IF EXISTS `erpbackoffice_model_message_destinataire`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_message_destinataire` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_message_id` int(11) NOT NULL,
  `model_employe_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ErpBackOffice_model_mess_model_message_id_model_e_c3f76327_uniq` (`model_message_id`,`model_employe_id`),
  KEY `ErpBackOffice_model_message_model_message_id_52f73cf1` (`model_message_id`),
  KEY `ErpBackOffice_model_message_model_employe_id_558b18df` (`model_employe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_module`
--

DROP TABLE IF EXISTS `erpbackoffice_model_module`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_module` varchar(50) DEFAULT NULL,
  `nom_application` varchar(100) DEFAULT NULL,
  `code` varchar(5) DEFAULT NULL,
  `description` longtext,
  `est_installe` tinyint(1) NOT NULL,
  `url_vers` varchar(100) DEFAULT NULL,
  `numero_ordre` int(11) NOT NULL,
  `icon_module` varchar(50) DEFAULT NULL,
  `couleur` varchar(15) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_module_auteur_id_68143df0` (`auteur_id`),
  KEY `ErpBackOffice_model_module_statut_id_fcab785c` (`statut_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_module`
--

INSERT INTO `erpbackoffice_model_module` (`id`, `nom_module`, `nom_application`, `code`, `description`, `est_installe`, `url_vers`, `numero_ordre`, `icon_module`, `couleur`, `url`, `etat`, `update_date`, `creation_date`, `auteur_id`, `statut_id`) VALUES
(5, 'Configuration', 'ModuleConfiguration', 'CONF', 'Module de getsion des configurations de l\'ERP', 1, 'configuration/dashboard', 99, 'configuration', 'bg-darkTeal', NULL, NULL, '2021-12-02 12:04:05.970517', '2021-01-20 17:16:29.726249', NULL, NULL),
(6, 'Application', 'ModuleApplication', 'APPL', 'Module de gestion des modules de l\'ERP', 1, 'application/list', 98, 'Application', 'bg-cobalt', NULL, NULL, '2022-03-24 16:38:03.788844', '2021-01-20 17:16:23.446390', NULL, NULL),
(7, 'Archivage', 'ModuleArchivage', NULL, 'Module de gestion électronique des documents', 1, 'archivage/', 97, 'archivage', 'Vert', NULL, NULL, '2022-03-24 16:40:12.199567', '2022-03-24 16:40:12.199567', NULL, NULL),
(8, 'Support', 'ModuleSupport', NULL, 'Module de gestion du support dans l\'ERP', 1, 'support/', 101, 'ventes', 'Bleu foncé', NULL, NULL, '2023-09-29 05:39:37.169240', '2023-09-29 05:39:37.169240', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_moduleovermodel`
--

DROP TABLE IF EXISTS `erpbackoffice_model_moduleovermodel`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_moduleovermodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_modele` varchar(100) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `model_id_id` int(11) DEFAULT NULL,
  `module_id_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_moduleovermodel_auteur_id_17fbec2d` (`auteur_id`),
  KEY `ErpBackOffice_model_moduleovermodel_model_id_id_66892769` (`model_id_id`),
  KEY `ErpBackOffice_model_moduleovermodel_module_id_id_90e3417b` (`module_id_id`),
  KEY `ErpBackOffice_model_moduleovermodel_statut_id_a4c09ac1` (`statut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_notification`
--

DROP TABLE IF EXISTS `erpbackoffice_model_notification`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(500) DEFAULT NULL,
  `url_piece_concernee` varchar(300) DEFAULT NULL,
  `module_source` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_notification_auteur_id_a6ecf61d` (`auteur_id`),
  KEY `ErpBackOffice_model_notification_statut_id_2da680e0` (`statut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_operationnalisation_module`
--

DROP TABLE IF EXISTS `erpbackoffice_model_operationnalisation_module`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_operationnalisation_module` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(100) DEFAULT NULL,
  `date_debut` datetime(6) NOT NULL,
  `date_fin` datetime(6) NOT NULL,
  `est_active` tinyint(1) NOT NULL,
  `est_cloture` tinyint(1) NOT NULL,
  `observation` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model__auteur_id_f4078799_fk_ErpBackOf` (`auteur_id`),
  KEY `ErpBackOffice_model__module_id_0fbb80ba_fk_ErpBackOf` (`module_id`),
  KEY `ErpBackOffice_model__statut_id_9268574a_fk_ErpBackOf` (`statut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_organisation`
--

DROP TABLE IF EXISTS `erpbackoffice_model_organisation`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_organisation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(150) NOT NULL,
  `slogan` varchar(150) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  `icon` varchar(500) DEFAULT NULL,
  `image_cover` varchar(500) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `boite_postal` varchar(50) DEFAULT NULL,
  `fax` varchar(50) DEFAULT NULL,
  `numero_fiscal` varchar(50) DEFAULT NULL,
  `site_web` varchar(100) DEFAULT NULL,
  `adresse` varchar(100) DEFAULT NULL,
  `nom_application` varchar(50) DEFAULT NULL,
  `est_active` tinyint(1) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `commune_quartier_id` int(11) DEFAULT NULL,
  `devise_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `type_organisation_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_organisation_auteur_id_dadcfc9c` (`auteur_id`),
  KEY `ErpBackOffice_model_organisation_commune_quartier_id_90475249` (`commune_quartier_id`),
  KEY `ErpBackOffice_model_organisation_devise_id_d9b255d2` (`devise_id`),
  KEY `ErpBackOffice_model_organisation_statut_id_3cdea369` (`statut_id`),
  KEY `ErpBackOffice_model_organisation_type_organisation_id_a1231800` (`type_organisation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_organisation`
--

INSERT INTO `erpbackoffice_model_organisation` (`id`, `nom`, `slogan`, `email`, `image`, `icon`, `image_cover`, `phone`, `boite_postal`, `fax`, `numero_fiscal`, `site_web`, `adresse`, `nom_application`, `est_active`, `etat`, `update_date`, `creation_date`, `url`, `auteur_id`, `commune_quartier_id`, `devise_id`, `statut_id`, `type_organisation_id`) VALUES
(1, 'NSANDAX', NULL, 'contact@nsandax.com', 'ErpProject/image/logo_large.png', 'ErpProject/image/logo.png', 'ErpProject/image/background.jpg', '+ 243 81 912 18 38', NULL, NULL, NULL, NULL, '91 bis Boulvard du 30 juin', NULL, 1, NULL, '2023-09-28 06:29:07.588394', '2021-05-29 16:15:01.330172', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_permission`
--

DROP TABLE IF EXISTS `erpbackoffice_model_permission`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) DEFAULT NULL,
  `numero` int(11) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `sous_module_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero` (`numero`),
  KEY `ErpBackOffice_model_permission_auteur_id_04c3b95d` (`auteur_id`),
  KEY `ErpBackOffice_model_permission_sous_module_id_e1255552` (`sous_module_id`),
  KEY `ErpBackOffice_model_permission_statut_id_44c257a2` (`statut_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3868 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_permission`
--

INSERT INTO `erpbackoffice_model_permission` (`id`, `designation`, `numero`, `url`, `etat`, `update_date`, `creation_date`, `auteur_id`, `sous_module_id`, `statut_id`) VALUES
(1333, 'CREER_RAPPORT_CONFIGURATION', 172, NULL, NULL, '2021-05-29 16:15:05.339077', '2020-09-09 14:24:08.664312', NULL, 1, NULL),
(3653, 'LISTER_DASHBOARD', 496, NULL, NULL, '2021-05-29 16:15:05.339077', '2020-09-29 13:35:42.217284', NULL, 1, NULL),
(3703, 'LISTER_UTILISATEUR', 546, NULL, NULL, '2021-05-29 17:46:02.066253', '2021-05-29 17:45:58.197147', NULL, 2, NULL),
(3710, 'CREER_UTILISATEUR', 547, NULL, NULL, '2021-05-29 17:53:24.221067', '2021-05-29 17:52:13.407922', NULL, 2, NULL),
(3711, 'MODIFIER_UTILISATEUR', 548, NULL, NULL, '2021-05-29 17:53:35.767251', '2021-05-29 17:53:35.767251', NULL, 2, NULL),
(3712, 'SUPPRIMER_UTILISATEUR', 549, NULL, NULL, '2021-05-29 17:53:49.204509', '2021-05-29 17:53:49.204509', NULL, 2, NULL),
(3713, 'LISTER_ROLE', 550, NULL, NULL, '2021-05-29 17:54:12.070432', '2021-05-29 17:54:12.070432', NULL, 3, NULL),
(3714, 'CREER_ROLE', 551, NULL, NULL, '2021-05-29 17:54:19.697482', '2021-05-29 17:54:19.697482', NULL, 3, NULL),
(3715, 'MODIFIER_ROLE', 552, NULL, NULL, '2021-05-29 17:54:27.604641', '2021-05-29 17:54:27.604641', NULL, 3, NULL),
(3716, 'SUPPRIMER_ROLE', 553, NULL, NULL, '2021-05-29 17:54:36.157696', '2021-05-29 17:54:36.157696', NULL, 3, NULL),
(3717, 'LISTER_GENERATION_MDT', 554, NULL, NULL, '2021-05-29 17:54:59.151229', '2021-05-29 17:54:59.151229', NULL, 4, NULL),
(3718, 'CREER_GENERATION_MDT', 555, NULL, NULL, '2021-05-29 17:55:14.319997', '2021-05-29 17:55:14.319997', NULL, 4, NULL),
(3719, 'MODIFIER_GENERATION_MDT', 556, NULL, NULL, '2021-05-29 17:55:23.162748', '2021-05-29 17:55:23.162748', NULL, 4, NULL),
(3720, 'SUPPRIMER_GENERATION_MDT', 557, NULL, NULL, '2021-05-29 17:55:36.528862', '2021-05-29 17:55:36.528862', NULL, 4, NULL),
(3721, 'LISTER_GENERATION_TU', 558, NULL, NULL, '2021-05-29 17:56:30.259238', '2021-05-29 17:56:30.259238', NULL, 5, NULL),
(3722, 'CREER_GENERATION_TU', 559, NULL, NULL, '2021-05-29 17:56:54.245629', '2021-05-29 17:56:47.384408', NULL, 5, NULL),
(3723, 'MODIFIER_GENERATION_TU', 560, NULL, NULL, '2021-05-29 17:57:11.725661', '2021-05-29 17:57:11.725661', NULL, 5, NULL),
(3724, 'SUPPIMER_GENERATION_TU', 561, NULL, NULL, '2021-05-29 17:58:09.854339', '2021-05-29 17:58:09.854339', NULL, 5, NULL),
(3725, 'LISTER_GENERATION_TS', 562, NULL, NULL, '2021-05-29 17:58:34.507790', '2021-05-29 17:58:34.507790', NULL, 6, NULL),
(3726, 'CREER_GENERATION_TS', 563, NULL, NULL, '2021-05-29 17:58:43.549009', '2021-05-29 17:58:43.549009', NULL, 6, NULL),
(3727, 'MODIFIER_GENERATION_TS', 564, NULL, NULL, '2021-05-29 17:58:53.746477', '2021-05-29 17:58:53.746477', NULL, 6, NULL),
(3728, 'SUPPRIMER_GENERATION_TS', 565, NULL, NULL, '2021-05-29 17:59:03.406107', '2021-05-29 17:59:03.406107', NULL, 6, NULL),
(3729, 'LISTER_WORKFLOW', 566, NULL, NULL, '2021-05-29 18:00:04.430071', '2021-05-29 18:00:04.430071', NULL, 7, NULL),
(3730, 'CREER_WORKFLOW', 567, NULL, NULL, '2021-05-29 18:00:16.656030', '2021-05-29 18:00:16.656030', NULL, 7, NULL),
(3731, 'MODIFIER_WORKFLOW', 568, NULL, NULL, '2021-05-29 18:00:40.892470', '2021-05-29 18:00:40.892470', NULL, 7, NULL),
(3732, 'SUPPRIMER_WORKFLOW', 569, NULL, NULL, '2021-05-29 18:00:49.685246', '2021-05-29 18:00:49.685246', NULL, 7, NULL),
(3733, 'LISTER_PARAMETRE', 570, NULL, NULL, '2021-05-29 18:01:23.913788', '2021-05-29 18:01:23.913788', NULL, 8, NULL),
(3734, 'LISTER_REGLE', 571, NULL, NULL, '2021-05-29 18:03:49.989953', '2021-05-29 18:03:49.989953', NULL, 3187, NULL),
(3735, 'CREER_REGLE', 572, NULL, NULL, '2021-05-29 18:04:02.624959', '2021-05-29 18:04:02.624959', NULL, 3187, NULL),
(3736, 'MODIFIER_REGLE', 573, NULL, NULL, '2021-05-29 18:04:15.247022', '2021-05-29 18:04:15.247022', NULL, 3187, NULL),
(3737, 'SUPPRIMER_REGLE', 574, NULL, NULL, '2021-05-29 18:04:25.215281', '2021-05-29 18:04:25.215281', NULL, 3187, NULL),
(3738, 'LISTER_PERMISSION', 575, NULL, NULL, '2021-05-29 18:04:47.417327', '2021-05-29 18:04:47.417327', NULL, 3188, NULL),
(3739, 'CREER_PERMISSION', 576, NULL, NULL, '2021-05-29 18:05:11.935576', '2021-05-29 18:05:11.935576', NULL, 3188, NULL),
(3740, 'MODIFIER_PERMISSION', 577, NULL, NULL, '2021-05-29 18:05:27.991204', '2021-05-29 18:05:27.991204', NULL, 3188, NULL),
(3741, 'SUPPRIMER_PERMISSION', 578, NULL, NULL, '2021-05-29 18:05:54.132183', '2021-05-29 18:05:54.132183', NULL, 3188, NULL),
(3742, 'LISTER_ACTION', 579, NULL, NULL, '2021-05-29 18:06:08.947066', '2021-05-29 18:06:08.947066', NULL, 3189, NULL),
(3743, 'CREER_ACTION', 580, NULL, NULL, '2021-05-29 18:06:54.008409', '2021-05-29 18:06:54.008409', NULL, 3189, NULL),
(3744, 'MODIFIER_ACTION', 581, NULL, NULL, '2021-05-29 18:07:42.039028', '2021-05-29 18:07:13.890705', NULL, 3189, NULL),
(3745, 'SUPPRIMER_ACTION', 582, NULL, NULL, '2021-05-29 18:07:31.140297', '2021-05-29 18:07:31.140297', NULL, 3189, NULL),
(3746, 'LISTER_GROUPE_MENU', 583, NULL, NULL, '2021-06-03 15:54:33.466391', '2021-06-03 15:54:33.466391', NULL, 3192, NULL),
(3747, 'CREER_GROUPE_MENU', 584, NULL, NULL, '2021-06-03 15:56:21.327836', '2021-06-03 15:56:21.327836', NULL, 3192, NULL),
(3748, 'MODIFIER_GROUPE_MENU', 585, NULL, NULL, '2021-06-03 15:56:38.048316', '2021-06-03 15:56:38.048316', NULL, 3193, NULL),
(3749, 'SUPPRIMER_GROUPE_MENU', 586, NULL, NULL, '2021-06-03 16:00:35.088270', '2021-06-03 16:00:35.088270', NULL, 3192, NULL),
(3750, 'LISTER_SOUS_MODULE', 587, NULL, NULL, '2021-06-03 16:00:58.160142', '2021-06-03 16:00:58.160142', NULL, 3193, NULL),
(3751, 'CREER_SOUS_MODULE', 588, NULL, NULL, '2021-06-03 16:01:14.317240', '2021-06-03 16:01:14.317240', NULL, 3193, NULL),
(3752, 'MODIFIER_SOUS_MODULE', 589, NULL, NULL, '2021-06-03 16:01:29.464434', '2021-06-03 16:01:29.464434', NULL, 3193, NULL),
(3753, 'SUPPRIMER_SOUS_MODULE', 590, NULL, NULL, '2021-06-03 16:01:48.774422', '2021-06-03 16:01:48.774422', NULL, 3193, NULL),
(3757, 'CREER_WIZARD_MENU', 592, NULL, NULL, '2021-06-04 12:48:21.351047', '2021-06-04 12:48:21.351047', NULL, 3198, NULL),
(3760, 'CREER_WIZARD_MENU2', 594, NULL, NULL, '2021-06-04 13:53:41.694010', '2021-06-04 13:53:41.694010', NULL, NULL, NULL),
(3761, 'ADMIN_DASHBOARD_ARCHIVAGE', 595, NULL, NULL, '2022-03-24 16:40:14.223814', '2022-03-24 16:40:14.223814', NULL, 3199, NULL),
(3762, 'USER_DASHBOARD_ARCHIVAGE', 596, NULL, NULL, '2022-03-24 16:40:14.231815', '2022-03-24 16:40:14.232813', NULL, 3199, NULL),
(3778, 'SUPPRIMER_DOCUMENT', 597, NULL, NULL, '2022-03-28 01:40:50.218412', '2022-03-28 01:40:50.218412', NULL, 3215, NULL),
(3779, 'LISTER_DOCUMENT', 598, NULL, NULL, '2022-03-28 01:40:50.253414', '2022-03-28 01:40:50.253414', NULL, 3215, NULL),
(3780, 'CREER_DOCUMENT', 599, NULL, NULL, '2022-03-28 01:40:50.274411', '2022-03-28 01:40:50.274411', NULL, 3215, NULL),
(3781, 'MODIFIER_DOCUMENT', 600, NULL, NULL, '2022-03-28 01:40:50.287413', '2022-03-28 01:40:50.287413', NULL, 3215, NULL),
(3782, 'ANALYSER_DOCUMENT', 601, NULL, NULL, '2022-03-28 01:40:50.298411', '2022-03-28 01:40:50.298411', NULL, 3216, NULL),
(3783, 'SUPPRIMER_DOSSIER', 602, NULL, NULL, '2022-03-28 02:10:16.359794', '2022-03-28 02:10:16.359794', NULL, 3217, NULL),
(3784, 'LISTER_DOSSIER', 603, NULL, NULL, '2022-03-28 02:10:16.372795', '2022-03-28 02:10:16.372795', NULL, 3217, NULL),
(3785, 'CREER_DOSSIER', 604, NULL, NULL, '2022-03-28 02:10:16.399796', '2022-03-28 02:10:16.399796', NULL, 3217, NULL),
(3786, 'MODIFIER_DOSSIER', 605, NULL, NULL, '2022-03-28 02:10:16.421796', '2022-03-28 02:10:16.421796', NULL, 3217, NULL),
(3787, 'ANALYSER_DOSSIER', 606, NULL, NULL, '2022-03-28 02:10:16.447796', '2022-03-28 02:10:16.447796', NULL, 3217, NULL),
(3788, 'SUPPRIMER_CATEGORIE_TAG', 607, NULL, NULL, '2022-03-28 02:13:04.321363', '2022-03-28 02:13:04.321363', NULL, 3218, NULL),
(3789, 'LISTER_CATEGORIE_TAG', 608, NULL, NULL, '2022-03-28 02:13:04.332362', '2022-03-28 02:13:04.332362', NULL, 3218, NULL),
(3790, 'CREER_CATEGORIE_TAG', 609, NULL, NULL, '2022-03-28 02:13:04.354360', '2022-03-28 02:13:04.355359', NULL, 3218, NULL),
(3791, 'MODIFIER_CATEGORIE_TAG', 610, NULL, NULL, '2022-03-28 02:13:04.367360', '2022-03-28 02:13:04.367360', NULL, 3218, NULL),
(3792, 'ANALYSER_CATEGORIE_TAG', 611, NULL, NULL, '2022-03-28 02:13:04.379364', '2022-03-28 02:13:04.379364', NULL, 3218, NULL),
(3793, 'SUPPRIMER_TAG', 612, NULL, NULL, '2022-03-28 02:17:52.507635', '2022-03-28 02:17:52.507635', NULL, 3219, NULL),
(3794, 'LISTER_TAG', 613, NULL, NULL, '2022-03-28 02:17:52.515632', '2022-03-28 02:17:52.515632', NULL, 3219, NULL),
(3795, 'CREER_TAG', 614, NULL, NULL, '2022-03-28 02:17:52.531633', '2022-03-28 02:17:52.531633', NULL, 3219, NULL),
(3796, 'MODIFIER_TAG', 615, NULL, NULL, '2022-03-28 02:17:52.543632', '2022-03-28 02:17:52.543632', NULL, 3219, NULL),
(3797, 'ANALYSER_TAG', 616, NULL, NULL, '2022-03-28 02:17:52.551634', '2022-03-28 02:17:52.551634', NULL, 3219, NULL),
(3798, 'SUPPRIMER_DOCUMENT_PARTAGE', 617, NULL, NULL, '2022-03-28 02:21:19.771187', '2022-03-28 02:21:19.771187', NULL, 3220, NULL),
(3799, 'LISTER_DOCUMENT_PARTAGE', 618, NULL, NULL, '2022-03-28 02:21:19.790184', '2022-03-28 02:21:19.790184', NULL, 3220, NULL),
(3800, 'CREER_DOCUMENT_PARTAGE', 619, NULL, NULL, '2022-03-28 02:21:19.844188', '2022-03-28 02:21:19.844188', NULL, 3220, NULL),
(3801, 'MODIFIER_DOCUMENT_PARTAGE', 620, NULL, NULL, '2022-03-28 02:21:19.870187', '2022-03-28 02:21:19.870187', NULL, 3220, NULL),
(3802, 'ANALYSER_DOCUMENT_PARTAGE', 621, NULL, NULL, '2022-03-28 02:21:19.900185', '2022-03-28 02:21:19.900185', NULL, 3220, NULL),
(3803, 'ADMIN_DASHBOARD_SUPPORT', 622, NULL, NULL, '2023-09-29 05:39:38.463592', '2023-09-29 05:39:38.463592', 7, 3221, NULL),
(3804, 'USER_DASHBOARD_SUPPORT', 623, NULL, NULL, '2023-09-29 05:39:38.477576', '2023-09-29 05:39:38.477576', 7, 3221, NULL),
(3808, 'SUPPRIMER_HISTORIQUE_ACTION', 624, NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3223, NULL),
(3809, 'LISTER_HISTORIQUE_ACTION', 625, NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3223, NULL),
(3810, 'CREER_HISTORIQUE_ACTION', 626, NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3223, NULL),
(3811, 'MODIFIER_HISTORIQUE_ACTION', 627, NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3223, NULL),
(3812, 'ANALYSER_HISTORIQUE_ACTION', 628, NULL, NULL, '2023-10-15 13:39:44.306871', '2023-10-15 13:39:44.306871', 7, 3223, NULL),
(3813, 'SUPPRIMER_LOG', 629, NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3224, NULL),
(3814, 'LISTER_LOG', 630, NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3224, NULL),
(3815, 'CREER_LOG', 631, NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3224, NULL),
(3816, 'MODIFIER_LOG', 632, NULL, NULL, '2023-10-15 13:40:51.878382', '2023-10-15 13:40:51.878382', 7, 3224, NULL),
(3817, 'ANALYSER_LOG', 633, NULL, NULL, '2023-10-15 13:40:51.889393', '2023-10-15 13:40:51.889393', 7, 3224, NULL),
(3818, 'SUPPRIMER_SOCIETE', 634, NULL, NULL, '2023-10-23 12:32:44.511592', '2023-10-23 12:32:44.511592', 7, 3225, NULL),
(3819, 'LISTER_SOCIETE', 635, NULL, NULL, '2023-10-23 12:32:44.520631', '2023-10-23 12:32:44.520631', 7, 3225, NULL),
(3820, 'CREER_SOCIETE', 636, NULL, NULL, '2023-10-23 12:32:44.529247', '2023-10-23 12:32:44.529247', 7, 3225, NULL),
(3821, 'MODIFIER_SOCIETE', 637, NULL, NULL, '2023-10-23 12:32:44.532247', '2023-10-23 12:32:44.532247', 7, 3225, NULL),
(3822, 'ANALYSER_SOCIETE', 638, NULL, NULL, '2023-10-23 12:32:44.533247', '2023-10-23 12:32:44.533247', 7, 3225, NULL),
(3823, 'SUPPRIMER_CONTACT', 639, NULL, NULL, '2023-10-23 12:39:00.547015', '2023-10-23 12:39:00.547015', 7, 3226, NULL),
(3824, 'LISTER_CONTACT', 640, NULL, NULL, '2023-10-23 12:39:00.553022', '2023-10-23 12:39:00.553022', 7, 3226, NULL),
(3825, 'CREER_CONTACT', 641, NULL, NULL, '2023-10-23 12:39:00.558285', '2023-10-23 12:39:00.558285', 7, 3226, NULL),
(3826, 'MODIFIER_CONTACT', 642, NULL, NULL, '2023-10-23 12:39:00.560280', '2023-10-23 12:39:00.560280', 7, 3226, NULL),
(3827, 'ANALYSER_CONTACT', 643, NULL, NULL, '2023-10-23 12:39:00.562281', '2023-10-23 12:39:00.562281', 7, 3226, NULL),
(3828, 'SUPPRIMER_ADRESSE', 644, NULL, NULL, '2023-10-23 12:39:32.217290', '2023-10-23 12:39:32.217290', 7, 3227, NULL),
(3829, 'LISTER_ADRESSE', 645, NULL, NULL, '2023-10-23 12:39:32.227288', '2023-10-23 12:39:32.227288', 7, 3227, NULL),
(3830, 'CREER_ADRESSE', 646, NULL, NULL, '2023-10-23 12:39:32.233501', '2023-10-23 12:39:32.233501', 7, 3227, NULL),
(3831, 'MODIFIER_ADRESSE', 647, NULL, NULL, '2023-10-23 12:39:32.237509', '2023-10-23 12:39:32.237509', 7, 3227, NULL),
(3832, 'ANALYSER_ADRESSE', 648, NULL, NULL, '2023-10-23 12:39:32.242116', '2023-10-23 12:39:32.242116', 7, 3227, NULL),
(3833, 'SUPPRIMER_PAYS', 649, NULL, NULL, '2023-10-23 12:40:34.121751', '2023-10-23 12:40:34.121751', 7, 3228, NULL),
(3834, 'LISTER_PAYS', 650, NULL, NULL, '2023-10-23 12:40:34.128012', '2023-10-23 12:40:34.128012', 7, 3228, NULL),
(3835, 'CREER_PAYS', 651, NULL, NULL, '2023-10-23 12:40:34.131103', '2023-10-23 12:40:34.131103', 7, 3228, NULL),
(3836, 'MODIFIER_PAYS', 652, NULL, NULL, '2023-10-23 12:40:34.134037', '2023-10-23 12:40:34.134037', 7, 3228, NULL),
(3837, 'ANALYSER_PAYS', 653, NULL, NULL, '2023-10-23 12:40:34.135878', '2023-10-23 12:40:34.135878', 7, 3228, NULL),
(3838, 'SUPPRIMER_PROVINCE', 654, NULL, NULL, '2023-10-23 12:41:06.457140', '2023-10-23 12:41:06.457140', 7, 3229, NULL),
(3839, 'LISTER_PROVINCE', 655, NULL, NULL, '2023-10-23 12:41:06.462849', '2023-10-23 12:41:06.462849', 7, 3229, NULL),
(3840, 'CREER_PROVINCE', 656, NULL, NULL, '2023-10-23 12:41:06.465846', '2023-10-23 12:41:06.465846', 7, 3229, NULL),
(3841, 'MODIFIER_PROVINCE', 657, NULL, NULL, '2023-10-23 12:41:06.467566', '2023-10-23 12:41:06.467566', 7, 3229, NULL),
(3842, 'ANALYSER_PROVINCE', 658, NULL, NULL, '2023-10-23 12:41:06.469669', '2023-10-23 12:41:06.469669', 7, 3229, NULL),
(3843, 'SUPPRIMER_VILLE', 659, NULL, NULL, '2023-10-23 12:41:45.761618', '2023-10-23 12:41:45.761618', 7, 3230, NULL),
(3844, 'LISTER_VILLE', 660, NULL, NULL, '2023-10-23 12:41:45.769619', '2023-10-23 12:41:45.769619', 7, 3230, NULL),
(3845, 'CREER_VILLE', 661, NULL, NULL, '2023-10-23 12:41:45.774401', '2023-10-23 12:41:45.774401', 7, 3230, NULL),
(3846, 'MODIFIER_VILLE', 662, NULL, NULL, '2023-10-23 12:41:45.776293', '2023-10-23 12:41:45.776293', 7, 3230, NULL),
(3847, 'ANALYSER_VILLE', 663, NULL, NULL, '2023-10-23 12:41:45.778291', '2023-10-23 12:41:45.778291', 7, 3230, NULL),
(3848, 'SUPPRIMER_DISTRICT', 664, NULL, NULL, '2023-10-23 12:43:42.617622', '2023-10-23 12:43:42.617622', 7, 3231, NULL),
(3849, 'LISTER_DISTRICT', 665, NULL, NULL, '2023-10-23 12:43:42.621732', '2023-10-23 12:43:42.621732', 7, 3231, NULL),
(3850, 'CREER_DISTRICT', 666, NULL, NULL, '2023-10-23 12:43:42.623839', '2023-10-23 12:43:42.623839', 7, 3231, NULL),
(3851, 'MODIFIER_DISTRICT', 667, NULL, NULL, '2023-10-23 12:43:42.625737', '2023-10-23 12:43:42.625737', 7, 3231, NULL),
(3852, 'ANALYSER_DISTRICT', 668, NULL, NULL, '2023-10-23 12:43:42.626737', '2023-10-23 12:43:42.626737', 7, 3231, NULL),
(3853, 'SUPPRIMER_COMMUNE', 669, NULL, NULL, '2023-10-23 12:44:38.862713', '2023-10-23 12:44:38.862713', 7, 3232, NULL),
(3854, 'LISTER_COMMUNE', 670, NULL, NULL, '2023-10-23 12:44:38.872726', '2023-10-23 12:44:38.872726', 7, 3232, NULL),
(3855, 'CREER_COMMUNE', 671, NULL, NULL, '2023-10-23 12:44:38.878195', '2023-10-23 12:44:38.878195', 7, 3232, NULL),
(3856, 'MODIFIER_COMMUNE', 672, NULL, NULL, '2023-10-23 12:44:38.881192', '2023-10-23 12:44:38.881192', 7, 3232, NULL),
(3857, 'ANALYSER_COMMUNE', 673, NULL, NULL, '2023-10-23 12:44:38.883192', '2023-10-23 12:44:38.883192', 7, 3232, NULL),
(3863, 'SUPPRIMER_TYPE_PERIODE', 674, NULL, NULL, '2023-10-23 12:47:51.068947', '2023-10-23 12:47:51.068947', 7, 3234, NULL),
(3864, 'LISTER_TYPE_PERIODE', 675, NULL, NULL, '2023-10-23 12:47:51.074402', '2023-10-23 12:47:51.074402', 7, 3234, NULL),
(3865, 'CREER_TYPE_PERIODE', 676, NULL, NULL, '2023-10-23 12:47:51.078746', '2023-10-23 12:47:51.078746', 7, 3234, NULL),
(3866, 'MODIFIER_TYPE_PERIODE', 677, NULL, NULL, '2023-10-23 12:47:51.080927', '2023-10-23 12:47:51.080927', 7, 3234, NULL),
(3867, 'ANALYSER_TYPE_PERIODE', 678, NULL, NULL, '2023-10-23 12:47:51.086062', '2023-10-23 12:47:51.086062', 7, 3234, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_personne`
--

DROP TABLE IF EXISTS `erpbackoffice_model_personne`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_personne` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prenom` varchar(250) DEFAULT NULL,
  `nom` varchar(250) DEFAULT NULL,
  `nom_complet` varchar(400) DEFAULT NULL,
  `image` varchar(700) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `adresse` varchar(500) DEFAULT NULL,
  `est_actif` tinyint(1) NOT NULL,
  `creation_date` datetime(6) DEFAULT NULL,
  `est_particulier` tinyint(1) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `commune_quartier_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `ErpBackOffice_model_personne_auteur_id_056eb8d3` (`auteur_id`),
  KEY `ErpBackOffice_model_personne_commune_quartier_id_fde7bd31` (`commune_quartier_id`),
  KEY `ErpBackOffice_model__company_id_a37cf772_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_personne`
--

INSERT INTO `erpbackoffice_model_personne` (`id`, `prenom`, `nom`, `nom_complet`, `image`, `email`, `phone`, `adresse`, `est_actif`, `creation_date`, `est_particulier`, `auteur_id`, `commune_quartier_id`, `company_id`, `update_date`, `user_id`) VALUES
(7, 'Admin', 'Admin', 'Admin', NULL, 'admin@erp.cd', NULL, NULL, 1, '2019-02-14 14:33:44.158602', 1, NULL, NULL, NULL, '2023-09-29 04:08:52.818500', 1);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_place`
--

DROP TABLE IF EXISTS `erpbackoffice_model_place`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) DEFAULT NULL,
  `code_telephone` varchar(5) DEFAULT NULL,
  `place_type` int(11) NOT NULL,
  `code_pays` varchar(3) DEFAULT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_place_auteur_id_00319a42` (`auteur_id`),
  KEY `ErpBackOffice_model_place_parent_id_7c0f1a3c` (`parent_id`),
  KEY `ErpBackOffice_model_place_company_id_59fe0cb4_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_regle`
--

DROP TABLE IF EXISTS `erpbackoffice_model_regle`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_regle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(100) DEFAULT NULL,
  `filtre` varchar(250) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `groupe_permission_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_regle_auteur_id_f927114c` (`auteur_id`),
  KEY `ErpBackOffice_model_regle_groupe_permission_id_2ddc54b5` (`groupe_permission_id`),
  KEY `ErpBackOffice_model_regle_statut_id_6fe46559` (`statut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_regle_permissions`
--

DROP TABLE IF EXISTS `erpbackoffice_model_regle_permissions`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_regle_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_regle_id` int(11) NOT NULL,
  `model_permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ErpBackOffice_model_regl_model_regle_id_model_per_fd322cc3_uniq` (`model_regle_id`,`model_permission_id`),
  KEY `ErpBackOffice_model__model_permission_id_ebc2c8aa_fk_ErpBackOf` (`model_permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_sousmodule`
--

DROP TABLE IF EXISTS `erpbackoffice_model_sousmodule`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_sousmodule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_sous_module` varchar(50) DEFAULT NULL,
  `description` longtext,
  `groupe` varchar(50) DEFAULT NULL,
  `icon_menu` varchar(150) DEFAULT NULL,
  `url_vers` varchar(100) DEFAULT NULL,
  `numero_ordre` int(11) NOT NULL,
  `est_model` tinyint(1) NOT NULL,
  `est_dashboard` tinyint(1) NOT NULL,
  `est_actif` tinyint(1) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `groupe_menu_id` int(11) DEFAULT NULL,
  `model_principal_id` int(11) DEFAULT NULL,
  `module_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_sousmodule_auteur_id_40e0dfcc` (`auteur_id`),
  KEY `ErpBackOffice_model_sousmodule_groupe_menu_id_505f9858` (`groupe_menu_id`),
  KEY `ErpBackOffice_model_sousmodule_model_principal_id_dd4d191b` (`model_principal_id`),
  KEY `ErpBackOffice_model_sousmodule_module_id_c3a04ed1` (`module_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3235 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_sousmodule`
--

INSERT INTO `erpbackoffice_model_sousmodule` (`id`, `nom_sous_module`, `description`, `groupe`, `icon_menu`, `url_vers`, `numero_ordre`, `est_model`, `est_dashboard`, `est_actif`, `update_date`, `url`, `creation_date`, `auteur_id`, `groupe_menu_id`, `model_principal_id`, `module_id`) VALUES
(1, 'Tableau de bord', '', NULL, 'dashboard.svg', 'module_configuration_dashboard', 0, 0, 1, 1, '2021-05-29 17:00:53.280868', NULL, '2020-09-09 14:14:28.868103', NULL, NULL, NULL, 5),
(2, 'Utilisateur', '', NULL, 'user.svg', 'module_configuration_list_utilisateurs', 1, 0, 0, 1, '2021-05-29 17:01:15.437269', NULL, '2020-09-07 19:42:28.725441', NULL, 1, NULL, 5),
(3, 'Rôle', '', NULL, 'tick-inside-circle.svg', 'module_configuration_list_roles', 1, 1, 0, 1, '2021-05-29 17:01:33.349661', NULL, '2020-09-07 19:42:28.734439', NULL, 2, NULL, 5),
(4, 'Générer Modèle, Dao et Templates dans un Module', '', NULL, NULL, 'module_configuration_list_modules', 1, 0, 0, 1, '2021-05-29 17:02:51.848483', NULL, '2020-09-07 19:42:28.740436', NULL, 3, NULL, 5),
(5, 'Générer les Tests Unitaires', '', NULL, NULL, 'module_configuration_generate_test', 2, 0, 0, 1, '2021-05-29 17:02:56.535652', NULL, '2020-09-07 19:42:28.747447', NULL, 3, NULL, 5),
(6, 'Générer les Tests Selenium', '', NULL, NULL, 'module_configuration_generate_selenium', 3, 0, 0, 1, '2021-05-29 16:15:22.026738', NULL, '2020-09-07 19:42:28.753408', NULL, 3, NULL, 5),
(7, 'Workflow', '', NULL, NULL, 'module_configuration_list_workflow', 1, 1, 0, 1, '2021-05-29 16:15:22.026738', NULL, '2020-09-07 19:42:28.759405', NULL, 4, NULL, 5),
(8, 'Paramètres généraux', '', NULL, 'setting.svg', 'module_configuration_configuration', 1, 0, 0, 0, '2021-05-29 17:05:32.121827', NULL, '2020-09-07 19:42:28.764402', NULL, NULL, NULL, 5),
(3187, 'Règle', '', NULL, NULL, 'module_configuration_list_regle', 3, 0, 0, 1, '2021-05-29 16:47:55.964042', NULL, '2021-05-29 16:47:36.745791', NULL, 2, NULL, 5),
(3188, 'Permission', '', NULL, NULL, 'module_Configuration_list_permission', 4, 0, 0, 1, '2021-05-29 18:02:48.283912', NULL, '2021-06-03 12:19:02.833665', NULL, 2, NULL, 5),
(3189, 'Actions', '', NULL, NULL, 'module_Configuration_list_actionutilisateur', 5, 0, 0, 1, '2021-05-29 18:03:15.195887', NULL, '2021-06-03 12:19:13.700944', NULL, 2, NULL, 5),
(3190, 'Générer Dao et Templates par Modèle', '', NULL, NULL, 'module_configuration_add_dao_template', 4, 0, 0, 1, '2021-05-29 18:24:07.957858', NULL, '2021-06-03 14:52:10.662933', NULL, 3, NULL, 5),
(3191, 'Générer Squelette d\'un Module avec ses fonctions', '', NULL, NULL, 'module_configuration_generate_framework', 5, 0, 0, 0, '2021-05-29 18:24:53.990838', NULL, '2021-05-29 18:24:53.990838', NULL, 3, NULL, 5),
(3192, 'Groupe Menu', '', NULL, NULL, 'module_Configuration_list_groupemenu', 1, 0, 0, 1, '2021-06-03 15:53:21.050340', NULL, '2021-06-03 15:53:21.050340', NULL, 51, NULL, 5),
(3193, 'Menu', '', NULL, NULL, 'module_Configuration_list_sousmodule', 2, 1, 0, 1, '2021-06-03 15:53:57.008313', NULL, '2021-06-03 16:15:28.082405', NULL, 51, NULL, 5),
(3198, 'Wizard Menu', '', '', '', 'module_Configuration_add_wizard_menu', 3, 0, 0, 1, '2021-06-04 12:48:21.343371', NULL, '2021-06-04 12:48:21.343371', NULL, 51, NULL, 5),
(3199, 'Tableau de Bord', 'Tableau de Bord', '', 'dashboard.svg', 'module_archivage_index', 0, 0, 1, 1, '2022-03-24 16:40:14.210815', NULL, '2022-03-24 16:40:14.210815', NULL, NULL, NULL, 7),
(3215, 'Documents', 'Menu Document', '', '', 'module_archivage_list_document', 1, 1, 0, 1, '2022-03-28 01:40:50.164412', NULL, '2022-03-28 01:40:50.164412', NULL, 52, 42, 7),
(3216, 'Rapport Documents', '', '', '', 'module_archivage_get_generer_document', 21, 1, 0, 1, '2022-03-28 01:40:50.243411', NULL, '2022-03-28 01:40:50.243411', NULL, 53, 42, 7),
(3217, 'Dossiers', 'Menu dossier', '', '', 'module_archivage_list_dossier', 2, 1, 0, 1, '2022-03-28 02:10:16.285797', NULL, '2022-03-28 02:10:16.285797', NULL, 54, 41, 7),
(3218, 'Catégories étiquette', 'Menu catégories étiquettes', '', '', 'module_archivage_list_categorie_tag', 3, 1, 0, 1, '2022-03-28 02:13:04.267361', NULL, '2022-03-28 02:13:04.267361', NULL, 54, 40, 7),
(3219, 'Étiquettes', 'Menu Étiquettes', '', '', 'module_archivage_list_tag', 4, 1, 0, 1, '2022-03-28 02:17:52.465635', NULL, '2022-03-28 02:17:52.465635', NULL, 54, 38, 7),
(3220, 'Liens partagés', 'Menu Liens partagés', '', '', 'module_archivage_list_document_partage', 5, 1, 0, 1, '2022-03-28 02:21:19.711187', NULL, '2022-03-28 02:21:19.711187', NULL, 54, 39, 7),
(3221, 'Tableau de Bord', 'Tableau de Bord', '', 'dashboard.svg', 'module_support_index', 0, 0, 1, 1, '2023-09-29 05:39:38.463592', NULL, '2023-09-29 05:39:38.463592', NULL, NULL, NULL, 8),
(3223, 'Historiques Actions', 'Menu Historiques Actions', '', '', 'module_support_list_historique_action', 1, 1, 0, 1, '2023-10-15 13:39:44.288189', NULL, '2023-10-15 13:39:44.288189', 7, 55, 53, 8),
(3224, 'Logs', 'Menu Logs', '', '', 'module_support_list_log', 2, 1, 0, 1, '2023-10-15 13:40:51.857647', NULL, '2023-10-15 13:40:51.857647', 7, 55, 54, 8),
(3225, 'Sociétés', 'Menu Sociétés', '', '', 'module_configuration_list_societe', 60, 1, 0, 1, '2023-10-23 12:32:44.350901', NULL, '2023-10-23 12:32:44.350901', 7, 5, 49, 5),
(3226, 'Contacts', 'Menu Contacts', '', '', 'module_configuration_list_contact', 61, 1, 0, 1, '2023-10-23 12:39:00.454026', NULL, '2023-10-23 12:39:00.454026', 7, 5, 46, 5),
(3227, 'Adresses', 'Menu Adresses', '', '', 'module_configuration_list_adresse', 62, 1, 0, 1, '2023-10-23 12:39:32.099825', NULL, '2023-10-23 12:39:32.099825', 7, 5, 44, 5),
(3228, 'Pays', 'Menu Pays', '', '', 'module_configuration_list_pays', 63, 1, 0, 1, '2023-10-23 12:40:34.076868', NULL, '2023-10-23 12:40:34.076868', 7, 5, 47, 5),
(3229, 'Provinces', 'Menu Provinces', '', '', 'module_configuration_list_province', 64, 1, 0, 1, '2023-10-23 12:41:06.392220', NULL, '2023-10-23 12:41:06.392220', 7, 5, 48, 5),
(3230, 'Villes', 'Menu Villes', '', '', 'module_configuration_list_ville', 65, 1, 0, 1, '2023-10-23 12:41:45.699860', NULL, '2023-10-23 12:41:45.699860', 7, 5, 50, 5),
(3231, 'Districts', 'Menu Districts', '', '', 'module_configuration_list_district', 66, 1, 0, 1, '2023-10-23 12:43:42.564353', NULL, '2023-10-23 12:43:42.564353', 7, 5, 52, 5),
(3232, 'Communes', 'Menu Communes', '', '', 'module_configuration_list_commune', 67, 1, 0, 1, '2023-10-23 12:44:38.798873', NULL, '2023-10-23 12:44:38.798873', 7, 5, 45, 5),
(3234, 'Types Période', 'Menu Types Période', '', '', 'module_configuration_list_type_periode', 68, 1, 0, 1, '2023-10-23 12:47:50.747185', NULL, '2023-10-23 12:47:50.747185', 7, 5, 51, 5);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_taux`
--

DROP TABLE IF EXISTS `erpbackoffice_model_taux`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_taux` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `montant` double NOT NULL,
  `est_courant` tinyint(1) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `devise_arrive_id` int(11) DEFAULT NULL,
  `devise_depart_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_taux_auteur_id_b6cb4619` (`auteur_id`),
  KEY `ErpBackOffice_model_taux_devise_arrive_id_8efb0c68` (`devise_arrive_id`),
  KEY `ErpBackOffice_model_taux_devise_depart_id_6d75a281` (`devise_depart_id`),
  KEY `ErpBackOffice_model_taux_statut_id_ebaa4149` (`statut_id`),
  KEY `ErpBackOffice_model_taux_company_id_7eabb638_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_temp_notification`
--

DROP TABLE IF EXISTS `erpbackoffice_model_temp_notification`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_temp_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_action` varchar(50) DEFAULT NULL,
  `lien_action` varchar(300) DEFAULT NULL,
  `source_identifiant` int(11) DEFAULT NULL,
  `est_lu` tinyint(1) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `notification_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_temp_notification_auteur_id_15998ec3` (`auteur_id`),
  KEY `ErpBackOffice_model_temp_notification_notification_id_e9e496e7` (`notification_id`),
  KEY `ErpBackOffice_model_temp_notification_statut_id_a8adcf11` (`statut_id`),
  KEY `ErpBackOffice_model_temp_notification_user_id_37ee5265` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_typeorganisation`
--

DROP TABLE IF EXISTS `erpbackoffice_model_typeorganisation`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_typeorganisation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) NOT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_typeorganisation_auteur_id_00c9dcca` (`auteur_id`),
  KEY `ErpBackOffice_model_typeorganisation_statut_id_9d7e1ec9` (`statut_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_usersessions`
--

DROP TABLE IF EXISTS `erpbackoffice_model_usersessions`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_usersessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_key` varchar(100) DEFAULT NULL,
  `login_date` datetime(6) DEFAULT NULL,
  `logout_date` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `session_id` varchar(40) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_usersessions_session_id_d4c7de02` (`session_id`),
  KEY `ErpBackOffice_model_usersessions_user_id_90d28d06` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_usersessions`
--

INSERT INTO `erpbackoffice_model_usersessions` (`id`, `session_key`, `login_date`, `logout_date`, `is_active`, `session_id`, `user_id`) VALUES
(1, '6itplzrxvrp1ah5dhekfk3nwxp09po6f', '2022-02-21 06:48:38.372833', NULL, 1, '6itplzrxvrp1ah5dhekfk3nwxp09po6f', 1),
(2, 'ker7aiqafb8a2v2i6efk1ovl4mk2b2v9', '2022-03-24 16:35:46.802262', NULL, 1, 'ker7aiqafb8a2v2i6efk1ovl4mk2b2v9', 1),
(3, 'qm4psndfd0idz3lnbobgjey2g45xj8fx', '2022-09-25 23:19:59.365568', NULL, 1, 'qm4psndfd0idz3lnbobgjey2g45xj8fx', 1),
(4, 'zlzb4kwdru2c8vgquuet2utnfpdc8de8', '2023-09-28 05:16:22.294492', NULL, 1, 'zlzb4kwdru2c8vgquuet2utnfpdc8de8', 1),
(5, 'ug0uabe2ea98n3vczvwlynmr55p5iqvm', '2023-10-14 01:12:01.205536', NULL, 1, 'ug0uabe2ea98n3vczvwlynmr55p5iqvm', 1),
(6, 'kmz1aeopx5ecnmzy2sowz2eh67bifoaz', '2023-10-23 10:45:38.303866', NULL, 1, 'kmz1aeopx5ecnmzy2sowz2eh67bifoaz', 1);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_approbation`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_approbation`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_approbation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(500) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `transition_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_wkf_approbation_auteur_id_19581e40` (`auteur_id`),
  KEY `ErpBackOffice_model_wkf_approbation_transition_id_d61f7932` (`transition_id`),
  KEY `ErpBackOffice_model__company_id_d314bff0_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_condition`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_condition`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_condition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_wkf_condition_auteur_id_c1aaecd5` (`auteur_id`),
  KEY `ErpBackOffice_model__company_id_a39ab650_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `erpbackoffice_model_wkf_condition`
--

INSERT INTO `erpbackoffice_model_wkf_condition` (`id`, `designation`, `update_date`, `creation_date`, `auteur_id`, `company_id`) VALUES
(1, 'Approval', '2021-05-29 16:15:39.337676', '2021-05-29 16:15:39.006417', NULL, NULL),
(2, 'Upload', '2021-05-29 16:15:39.337676', '2021-05-29 16:15:39.006417', NULL, NULL),
(3, 'Link', '2021-05-29 16:15:39.337676', '2021-05-29 16:15:39.006417', NULL, NULL),
(5, 'Responsible', '2021-05-29 16:15:39.337676', '2021-05-29 16:15:39.006417', NULL, NULL),
(8, 'LinkParam', '2021-05-29 16:15:39.337676', '2021-05-29 16:15:39.006417', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_etape`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_etape`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_etape` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(50) NOT NULL,
  `label` varchar(50) DEFAULT NULL,
  `est_initiale` tinyint(1) NOT NULL,
  `est_succes` tinyint(1) NOT NULL,
  `est_echec` tinyint(1) NOT NULL,
  `num_ordre` int(11) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `workflow_id` int(11) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_wkf_etape_auteur_id_65814ea7` (`auteur_id`),
  KEY `ErpBackOffice_model_wkf_etape_workflow_id_d5668427` (`workflow_id`),
  KEY `ErpBackOffice_model__company_id_90d9a733_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_historique`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_historique`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_historique` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `document_id` int(10) UNSIGNED DEFAULT NULL,
  `notes` varchar(500) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `etape_id` int(11) DEFAULT NULL,
  `employe_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_wkf_historique_auteur_id_9aeb7a95` (`auteur_id`),
  KEY `ErpBackOffice_model_wkf_historique_content_type_id_7e38a621` (`content_type_id`),
  KEY `ErpBackOffice_model_wkf_historique_etape_id_93db80ab` (`etape_id`),
  KEY `ErpBackOffice_model_wkf_historique_employe_id_bda3702a` (`employe_id`),
  KEY `ErpBackOffice_model__company_id_6a0f5482_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_stakeholder`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_stakeholder`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_stakeholder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document_id` int(10) UNSIGNED DEFAULT NULL,
  `est_delegation` tinyint(1) NOT NULL,
  `comments` varchar(500) DEFAULT NULL,
  `url_detail` varchar(100) DEFAULT NULL,
  `module_source` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `transition_id` int(11) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model__auteur_id_5e3556aa_fk_ErpBackOf` (`auteur_id`),
  KEY `ErpBackOffice_model__content_type_id_89d5e165_fk_django_co` (`content_type_id`),
  KEY `ErpBackOffice_model__transition_id_7be546c8_fk_ErpBackOf` (`transition_id`),
  KEY `ErpBackOffice_model__company_id_3b5dc574_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_stakeholder_carbon_copies`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_stakeholder_carbon_copies`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_stakeholder_carbon_copies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_wkf_stakeholder_id` int(11) NOT NULL,
  `model_employe_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ErpBackOffice_model_wkf__model_wkf_stakeholder_id_a244769f_uniq` (`model_wkf_stakeholder_id`,`model_employe_id`),
  KEY `ErpBackOffice_model__model_employe_id_fc492d58_fk_ErpBackOf` (`model_employe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_stakeholder_employes`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_stakeholder_employes`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_stakeholder_employes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_wkf_stakeholder_id` int(11) NOT NULL,
  `model_employe_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ErpBackOffice_model_wkf__model_wkf_stakeholder_id_9a566b59_uniq` (`model_wkf_stakeholder_id`,`model_employe_id`),
  KEY `ErpBackOffice_model__model_employe_id_788fd45e_fk_ErpBackOf` (`model_employe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_transition`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_transition`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_transition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(250) DEFAULT NULL,
  `operateur` int(11) NOT NULL,
  `traitement` varchar(250) DEFAULT NULL,
  `est_decisive` tinyint(1) NOT NULL,
  `est_configurable` tinyint(1) NOT NULL,
  `est_delegable` tinyint(1) NOT NULL,
  `est_filtrable` tinyint(1) NOT NULL,
  `est_generate_doc` tinyint(1) NOT NULL,
  `filtre` varchar(50) DEFAULT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `condition_id` int(11) DEFAULT NULL,
  `etape_destination_id` int(11) NOT NULL,
  `etape_source_id` int(11) NOT NULL,
  `groupe_permission_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ErpBackOffice_model_wkf_transition_auteur_id_226e2bf8` (`auteur_id`),
  KEY `ErpBackOffice_model_wkf_transition_condition_id_d477ef0b` (`condition_id`),
  KEY `ErpBackOffice_model_wkf_transition_etape_destination_id_18f56e36` (`etape_destination_id`),
  KEY `ErpBackOffice_model_wkf_transition_etape_source_id_2a45b641` (`etape_source_id`),
  KEY `ErpBackOffice_model_wkf_transition_groupe_permission_id_225abfa5` (`groupe_permission_id`),
  KEY `ErpBackOffice_model__company_id_a902fb71_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `erpbackoffice_model_wkf_workflow`
--

DROP TABLE IF EXISTS `erpbackoffice_model_wkf_workflow`;
CREATE TABLE IF NOT EXISTS `erpbackoffice_model_wkf_workflow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_document` varchar(30) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_document` (`type_document`),
  KEY `ErpBackOffice_model_wkf_workflow_auteur_id_2dd4a8f3` (`auteur_id`),
  KEY `ErpBackOffice_model_wkf_workflow_content_type_id_9c815a15` (`content_type_id`),
  KEY `ErpBackOffice_model__company_id_0b94b16c_fk_cnf_compa` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `query`
--

DROP TABLE IF EXISTS `query`;
CREATE TABLE IF NOT EXISTS `query` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` varchar(100) NOT NULL,
  `query` longtext,
  `description` longtext,
  `visibilite` int(11) NOT NULL,
  `type_view` varchar(100) NOT NULL,
  `designation` varchar(250) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `champs_afficher` longtext,
  `chart_type` varchar(250) DEFAULT NULL,
  `chart_view` varchar(250) DEFAULT NULL,
  `est_regroupe` tinyint(1) NOT NULL,
  `legend_dataset` varchar(250) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `regr_count` int(11) NOT NULL,
  `title_card` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `query_auteur_id_8330e231` (`auteur_id`),
  KEY `query_role_id_ebc43a11` (`role_id`),
  KEY `query_statut_id_41b93ec0` (`statut_id`),
  KEY `query_model_id_c350b999` (`model_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `sup_action_story`
--

DROP TABLE IF EXISTS `sup_action_story`;
CREATE TABLE IF NOT EXISTS `sup_action_story` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `Before_value` varchar(1024) DEFAULT NULL,
  `After_value` varchar(1024) DEFAULT NULL,
  `model` varchar(1024) NOT NULL,
  `autor` varchar(1024) NOT NULL,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `sup_logs`
--

DROP TABLE IF EXISTS `sup_logs`;
CREATE TABLE IF NOT EXISTS `sup_logs` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `error` varchar(1024) NOT NULL,
  `model` varchar(1024) NOT NULL,
  `autor` varchar(1024) NOT NULL,
  `state` varchar(50) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `tag`
--

DROP TABLE IF EXISTS `tag`;
CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `designation` varchar(250) NOT NULL,
  `code` varchar(100) DEFAULT NULL,
  `couleur` varchar(100) DEFAULT NULL,
  `description` varchar(550) DEFAULT NULL,
  `etat` varchar(50) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `auteur_id` int(11) DEFAULT NULL,
  `categorie_id` int(11) DEFAULT NULL,
  `statut_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tag_auteur_id_46f5f19d_fk_ErpBackOffice_model_personne_id` (`auteur_id`),
  KEY `tag_categorie_id_347dd64a_fk_categorie_tag_id` (`categorie_id`),
  KEY `tag_statut_id_19d7bb63_fk_ErpBackOffice_model_wkf_etape_id` (`statut_id`),
  KEY `tag_company_id_34aab3e0_fk_cnf_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `tag`
--

INSERT INTO `tag` (`id`, `designation`, `code`, `couleur`, `description`, `etat`, `creation_date`, `update_date`, `auteur_id`, `categorie_id`, `statut_id`, `company_id`) VALUES
(1, 'Facturation', 'FAC', 'Rouge', 'RAS', NULL, '2022-03-28 02:23:49.127823', '2022-03-28 02:24:13.288377', NULL, 1, NULL, NULL),
(2, 'Social', 'SOC', 'Bleu', 'RAS', NULL, '2022-03-28 02:29:57.499403', '2022-03-28 02:30:01.650461', NULL, 2, NULL, NULL);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `erpbackoffice_model_personne`
--
ALTER TABLE `erpbackoffice_model_personne`
  ADD CONSTRAINT `ErpBackOffice_model_personne_user_id_aed4c0fe_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
