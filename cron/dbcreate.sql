-- phpMyAdmin SQL Dump
-- version 4.2.8.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 17, 2014 at 09:45 AM
-- Server version: 5.5.39
-- PHP Version: 5.4.32

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `data.sgul.ac.uk`
--
CREATE DATABASE IF NOT EXISTS `data.sgul.ac.uk` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `data.sgul.ac.uk`;

-- --------------------------------------------------------

--
-- Table structure for table `coursemodules`
--
-- Creation: Sep 17, 2014 at 09:44 AM
--

DROP TABLE IF EXISTS `coursemodules`;
CREATE TABLE IF NOT EXISTS `coursemodules` (
  `modulecode` varchar(20) COLLATE utf8_bin NOT NULL,
  `fullname` varchar(100) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `datacatalogue`
--
-- Creation: Sep 17, 2014 at 09:44 AM
--

DROP TABLE IF EXISTS `datacatalogue`;
CREATE TABLE IF NOT EXISTS `datacatalogue` (
  `humanurl` varchar(100) COLLATE utf8_bin NOT NULL,
  `csv` varchar(100) COLLATE utf8_bin NOT NULL,
  `json` varchar(100) COLLATE utf8_bin NOT NULL,
  `rdfdump` varchar(100) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--
-- Creation: Sep 17, 2014 at 09:44 AM
--

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE IF NOT EXISTS `jobs` (
  `reference` varchar(20) COLLATE utf8_bin NOT NULL,
  `closing_date` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `interview_date` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `salary` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `title` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `topic` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `type` varchar(40) COLLATE utf8_bin DEFAULT NULL,
  `url` varchar(100) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `library`
--
-- Creation: Sep 17, 2014 at 09:44 AM
--

DROP TABLE IF EXISTS `library`;
CREATE TABLE IF NOT EXISTS `library` (
  `library_id` varchar(20) COLLATE utf8_bin NOT NULL,
  `author` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `date` varchar(15) COLLATE utf8_bin DEFAULT NULL,
  `isbn` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `oclc` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `publisher` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `subject` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `title` varchar(100) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `publications`
--
-- Creation: Sep 17, 2014 at 09:44 AM
--

DROP TABLE IF EXISTS `publications`;
CREATE TABLE IF NOT EXISTS `publications` (
  `puburl` varchar(20) COLLATE utf8_bin NOT NULL,
  `authorslist` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `title` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `doi` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `year` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  `repository` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `abstract` blob
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coursemodules`
--
ALTER TABLE `coursemodules`
 ADD PRIMARY KEY (`modulecode`);

--
-- Indexes for table `datacatalogue`
--
ALTER TABLE `datacatalogue`
 ADD PRIMARY KEY (`humanurl`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
 ADD PRIMARY KEY (`reference`);

--
-- Indexes for table `library`
--
ALTER TABLE `library`
 ADD PRIMARY KEY (`library_id`);

--
-- Indexes for table `publications`
--
ALTER TABLE `publications`
 ADD PRIMARY KEY (`puburl`);
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;