-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: Information_Database
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Address`
--

DROP TABLE IF EXISTS `Address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Address` (
  `AddressID` int NOT NULL AUTO_INCREMENT,
  `Street` varchar(100) DEFAULT NULL,
  `City` varchar(50) DEFAULT NULL,
  `State` varchar(50) DEFAULT NULL,
  `Zipcode` int DEFAULT NULL,
  `Country` varchar(50) DEFAULT NULL,
  `PersonID` int DEFAULT NULL,
  PRIMARY KEY (`AddressID`),
  KEY `PersonID` (`PersonID`),
  CONSTRAINT `Address_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Address`
--

LOCK TABLES `Address` WRITE;
/*!40000 ALTER TABLE `Address` DISABLE KEYS */;
INSERT INTO `Address` VALUES (1,'123 Maple St','Springfield','IL',62704,'USA',1),(2,'456 Oak Ave','Rivertown','CA',90210,'USA',2);
/*!40000 ALTER TABLE `Address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Businesses`
--

DROP TABLE IF EXISTS `Businesses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Businesses` (
  `BusinessID` int NOT NULL AUTO_INCREMENT,
  `BusinessName` varchar(100) NOT NULL,
  `BusinessType` enum('Physical','Online') DEFAULT NULL,
  PRIMARY KEY (`BusinessID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Businesses`
--

LOCK TABLES `Businesses` WRITE;
/*!40000 ALTER TABLE `Businesses` DISABLE KEYS */;
INSERT INTO `Businesses` VALUES (1,'John\'s Bakery','Physical'),(2,'Jane\'s Blog','Online');
/*!40000 ALTER TABLE `Businesses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Online`
--

DROP TABLE IF EXISTS `Online`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Online` (
  `BusinessID` int NOT NULL,
  `Website` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`BusinessID`),
  CONSTRAINT `Online_ibfk_1` FOREIGN KEY (`BusinessID`) REFERENCES `Businesses` (`BusinessID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Online`
--

LOCK TABLES `Online` WRITE;
/*!40000 ALTER TABLE `Online` DISABLE KEYS */;
INSERT INTO `Online` VALUES (2,'www.janesblog.com');
/*!40000 ALTER TABLE `Online` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Person`
--

DROP TABLE IF EXISTS `Person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Person` (
  `PersonID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  PRIMARY KEY (`PersonID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Person`
--

LOCK TABLES `Person` WRITE;
/*!40000 ALTER TABLE `Person` DISABLE KEYS */;
INSERT INTO `Person` VALUES (1,'John','Doe','john.doe@email.com','1990-01-01'),(2,'Jane','Smith','jane.smith@email.com','1985-06-12');
/*!40000 ALTER TABLE `Person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PersonBusiness`
--

DROP TABLE IF EXISTS `PersonBusiness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PersonBusiness` (
  `PersonID` int NOT NULL,
  `BusinessID` int NOT NULL,
  `AssociationDate` date DEFAULT NULL,
  PRIMARY KEY (`PersonID`,`BusinessID`),
  KEY `BusinessID` (`BusinessID`),
  CONSTRAINT `PersonBusiness_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE CASCADE,
  CONSTRAINT `PersonBusiness_ibfk_2` FOREIGN KEY (`BusinessID`) REFERENCES `Businesses` (`BusinessID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PersonBusiness`
--

LOCK TABLES `PersonBusiness` WRITE;
/*!40000 ALTER TABLE `PersonBusiness` DISABLE KEYS */;
INSERT INTO `PersonBusiness` VALUES (1,1,'2022-06-15'),(2,2,'2023-07-10');
/*!40000 ALTER TABLE `PersonBusiness` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PhoneNumbers`
--

DROP TABLE IF EXISTS `PhoneNumbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PhoneNumbers` (
  `PhoneNumberID` int NOT NULL AUTO_INCREMENT,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  `PersonID` int DEFAULT NULL,
  PRIMARY KEY (`PhoneNumberID`),
  KEY `PersonID` (`PersonID`),
  CONSTRAINT `PhoneNumbers_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PhoneNumbers`
--

LOCK TABLES `PhoneNumbers` WRITE;
/*!40000 ALTER TABLE `PhoneNumbers` DISABLE KEYS */;
INSERT INTO `PhoneNumbers` VALUES (1,'555-1234',1),(2,'555-5678',2);
/*!40000 ALTER TABLE `PhoneNumbers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Physical`
--

DROP TABLE IF EXISTS `Physical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Physical` (
  `BusinessID` int NOT NULL,
  `AddressID` int DEFAULT NULL,
  PRIMARY KEY (`BusinessID`),
  KEY `AddressID` (`AddressID`),
  CONSTRAINT `Physical_ibfk_1` FOREIGN KEY (`BusinessID`) REFERENCES `Businesses` (`BusinessID`) ON DELETE CASCADE,
  CONSTRAINT `Physical_ibfk_2` FOREIGN KEY (`AddressID`) REFERENCES `Address` (`AddressID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Physical`
--

LOCK TABLES `Physical` WRITE;
/*!40000 ALTER TABLE `Physical` DISABLE KEYS */;
INSERT INTO `Physical` VALUES (1,1);
/*!40000 ALTER TABLE `Physical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vehicle`
--

DROP TABLE IF EXISTS `Vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vehicle` (
  `VehicleID` int NOT NULL AUTO_INCREMENT,
  `Make` varchar(50) DEFAULT NULL,
  `Model` varchar(50) DEFAULT NULL,
  `Year` int DEFAULT NULL,
  `VIN_Number` varchar(17) DEFAULT NULL,
  `LicensePlate` varchar(10) DEFAULT NULL,
  `PersonID` int DEFAULT NULL,
  PRIMARY KEY (`VehicleID`),
  UNIQUE KEY `VIN_Number` (`VIN_Number`),
  UNIQUE KEY `LicensePlate` (`LicensePlate`),
  KEY `PersonID` (`PersonID`),
  CONSTRAINT `Vehicle_ibfk_1` FOREIGN KEY (`PersonID`) REFERENCES `Person` (`PersonID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehicle`
--

LOCK TABLES `Vehicle` WRITE;
/*!40000 ALTER TABLE `Vehicle` DISABLE KEYS */;
INSERT INTO `Vehicle` VALUES (1,'Toyota','Corolla',2015,'1HGBH41JXMN109186','ABC1234',1),(2,'Ford','F-150',2018,'1FTFW1EF3JFB23456','XYZ5678',2);
/*!40000 ALTER TABLE `Vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-09 17:16:25
