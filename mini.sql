-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: mini
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booked`
--

DROP TABLE IF EXISTS `booked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booked` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `hid` int(11) NOT NULL,
  `noHrs` int(11) NOT NULL,
  `finalAmount` decimal(5,2) NOT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT '2038-01-18 22:00:00',
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`bid`),
  KEY `cid` (`cid`),
  KEY `hid` (`hid`),
  CONSTRAINT `booked_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer` (`cid`),
  CONSTRAINT `booked_ibfk_2` FOREIGN KEY (`hid`) REFERENCES `helper` (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booked`
--

LOCK TABLES `booked` WRITE;
/*!40000 ALTER TABLE `booked` DISABLE KEYS */;
INSERT INTO `booked` VALUES (1,1,1,1,0.00,'2017-10-19 08:00:00','2038-01-18 22:00:00',1),(2,1,1,3,399.00,'2017-10-21 04:00:00','2038-01-18 22:00:00',1),(3,1,1,2,0.00,'2017-10-21 04:00:00','2038-01-18 22:00:00',0),(4,1,1,3,0.00,'2017-10-21 07:00:00','2038-01-18 22:00:00',0),(5,1,1,2,299.00,'2017-10-09 03:00:00','2017-10-09 05:00:00',0),(6,1,1,1,199.00,'2017-10-11 02:00:00','2017-10-11 03:00:00',0),(18,1,2,1,199.00,'2017-10-11 02:30:00','2017-10-11 03:30:00',0),(19,1,2,1,199.00,'2017-10-09 03:30:00','2017-10-09 04:30:00',0),(20,1,2,1,199.00,'2017-10-22 03:00:00','2017-10-22 04:00:00',0);
/*!40000 ALTER TABLE `booked` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booked2`
--

DROP TABLE IF EXISTS `booked2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booked2` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `hid` int(11) NOT NULL,
  `noHrs` int(11) NOT NULL,
  `finalAmount` decimal(5,2) NOT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT '2038-01-18 22:00:00',
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`bid`),
  KEY `cid` (`cid`),
  KEY `hid` (`hid`),
  CONSTRAINT `booked2_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer` (`cid`),
  CONSTRAINT `booked2_ibfk_2` FOREIGN KEY (`hid`) REFERENCES `helper` (`hid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booked2`
--

LOCK TABLES `booked2` WRITE;
/*!40000 ALTER TABLE `booked2` DISABLE KEYS */;
/*!40000 ALTER TABLE `booked2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cleaning`
--

DROP TABLE IF EXISTS `cleaning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cleaning` (
  `clid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `noShirt` int(11) NOT NULL DEFAULT '0',
  `noPant` int(11) NOT NULL DEFAULT '0',
  `nowoolen` int(11) NOT NULL DEFAULT '0',
  `noItem` int(11) NOT NULL DEFAULT '0',
  `finalAmount` int(11) NOT NULL DEFAULT '0',
  `serviceDate` datetime DEFAULT NULL,
  PRIMARY KEY (`clid`),
  KEY `cid` (`cid`),
  CONSTRAINT `cleaning_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `customer` (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cleaning`
--

LOCK TABLES `cleaning` WRITE;
/*!40000 ALTER TABLE `cleaning` DISABLE KEYS */;
INSERT INTO `cleaning` VALUES (1,1,2,2,3,1,140,'2017-10-09 00:26:10'),(2,1,1,0,1,1,80,'2017-10-09 01:25:27'),(3,1,1,0,1,1,80,'2017-10-09 01:26:27'),(4,1,1,1,2,2,160,'2017-10-09 01:27:25'),(5,1,1,1,2,2,160,'2017-10-09 01:28:26'),(6,1,1,1,2,2,160,'2017-10-09 01:30:57'),(7,1,1,1,2,2,160,'2017-10-09 01:31:30'),(8,1,1,1,2,2,160,'2017-10-09 01:38:23'),(9,1,1,1,2,2,160,'2017-10-09 01:39:26'),(10,1,1,1,2,2,160,'2017-10-09 01:39:56'),(11,1,1,1,2,2,160,'2017-10-09 01:40:28'),(12,1,1,1,2,2,160,'2017-10-09 01:41:02'),(13,1,1,1,0,1,65,'2017-10-09 11:02:01');
/*!40000 ALTER TABLE `cleaning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `mobile` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `adress` varchar(255) NOT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `mail` (`mail`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'atharva','7030447477','gomekaratharva@gmail.com','pune'),(2,'rasika','9764298692','rasika.gohokar89@gmail.com','pune');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `helper`
--

DROP TABLE IF EXISTS `helper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `helper` (
  `hid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) NOT NULL,
  `sid` int(11) NOT NULL,
  PRIMARY KEY (`hid`),
  KEY `sid` (`sid`),
  CONSTRAINT `helper_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `service` (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `helper`
--

LOCK TABLES `helper` WRITE;
/*!40000 ALTER TABLE `helper` DISABLE KEYS */;
INSERT INTO `helper` VALUES (1,'ramesh',NULL,'9988776655',1),(2,'suresh',NULL,'9876543210',1),(3,'dinesh',NULL,'9871234756',2),(4,'mangesh',NULL,'7709821652',2);
/*!40000 ALTER TABLE `helper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(255) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,'electrician'),(2,'plumber');
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-10 23:08:48
