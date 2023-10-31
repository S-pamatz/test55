-- MySQL dump 10.16  Distrib 10.1.48-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.48-MariaDB-0+deb9u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `affiliate`
--

DROP TABLE IF EXISTS `Affiliate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Affiliate` (
  `id`  int(11) NOT NULL AUTO_INCREMENT,
  `image_file` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password_hash` varchar(102) DEFAULT NULL,
  `firstname` varchar(200) DEFAULT NULL,
  `lastname` varchar(200) DEFAULT NULL,
  `is_admin` tinyint(4) DEFAULT NULL,
  `areaofinterest` varchar(200) DEFAULT NULL,
  `wsuCampus` varchar(200) DEFAULT NULL,
  `department` varchar(200) DEFAULT NULL,
  `membership` varchar(200) DEFAULT NULL,
  'university'varchar(200) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliate`
--

LOCK TABLES `Affiliate` WRITE;
/*!40000 ALTER TABLE `affiliate` DISABLE KEYS */;
INSERT INTO `Affiliate` VALUES (1,'0c950a3167ccbefe.jpg','limchangthe@yahoo.com','pbkdf2:sha256:260000$QNhRuAlAFB3kQok2$06c86fde8c90ad4bf66224c486b17f25c829983487923ac2240b09f5a910198b','James','Lim',1,'','WSU Pullman','Art','www.howtobeagentleman.com'),(2,'Default_pic.png','brianjoo@gmail.com','pbkdf2:sha256:260000$2rtqZ2MK19nW7pvV$39d26d369a76095ff1b7f3f0728c9a2bca03c4481308ed4e3b821da46d1b2d24','Brian','Joo',0,'None','WSU Pullman','Criminal Justice and Criminology','www.loveyourpuppies.com'),(3,'20846a612d71d60c.jpg','b.kandaswamy@wsu.edu','pbkdf2:sha256:260000$yMDhE9wB6YcX8GEO$d602b5887e87b89544e69f1db9e73ebe165b13dc4ae316a63a1a97dd502e9365','Subu','Kandaswamy',1,'Artificial Intelligence','WSU Pullman','Digital Technology and Culture','ce.wsu.edu/faculty/boll/');
/*!40000 ALTER TABLE `affiliate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus`
--

DROP TABLE IF EXISTS `campus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campus` (
  `id` tinyint(4) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus`
--

LOCK TABLES `campus` WRITE;
/*!40000 ALTER TABLE `campus` DISABLE KEYS */;
INSERT INTO `campus` VALUES (1,'Washington State University(WSU)'),(2,'Ohio State University(OS)'),(3,'University of Washington(UW)');
/*!40000 ALTER TABLE `campus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `id`  int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest`
--

DROP TABLE IF EXISTS `Interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Interest` (
  `id`  int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest`
--

LOCK TABLES `interest` WRITE;
/*!40000 ALTER TABLE `interest` DISABLE KEYS */;
INSERT INTO `interest` VALUES (1,'Carbon Cycling'),(2,'Air quality'),(3,'Evaporation'),(4,'Flux measurement'),(5,'Modeling'),(6,'Drinking'),(7,'Ground'),(8,'Surface'),(9,'Demand'),(10,'Quality'),(11,'Hydrology'),(12,'Economics'),(13,'Policy'),(14,'Resource management'),(15,'Lakes'),(16,'Stream Ecology'),(17,'Eutrophication'),(18,'Ocean'),(19,'Erosion'),(20,'Deforestation'),(21,'Wildfire'),(22,'Land Use Change'),(23,'Management'),(24,'Climate'),(25,'Agriculture'),(26,'Geo Science'),(27,'Human beings'),(28,'Animals'),(29,'Well being'),(30,'Sociology'),(31,'Anthropology'),(32,'Governance'),(33,'Migration'),(34,'Demography'),(35,'Philosophy'),(36,'Communities'),(37,'Political Science'),(38,'Alternative fuel'),(39,'Solar'),(40,'Grid'),(41,'Wind'),(42,'Renewable'),(43,'Supply'),(44,'Soil Health'),(45,'Other'),(46,'Artificial Intelligence');
/*!40000 ALTER TABLE `interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` tinyint(4) DEFAULT NULL,
  `name` varchar(4) DEFAULT NULL,
  `url` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'Sour','www.howtobeagentleman.com');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works`
--

DROP TABLE IF EXISTS `works`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `works` (
  `affiliate_id` tinyint(4) DEFAULT NULL,
  `project_id` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works`
--

LOCK TABLES `works` WRITE;
/*!40000 ALTER TABLE `works` DISABLE KEYS */;
INSERT INTO `works` VALUES (2,1);
/*!40000 ALTER TABLE `works` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

CREATE TABLE intrest_test (
  
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  subcategory_id INT,
  FOREIGN KEY (subcategory_id) REFERENCES subcategory(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE subcategory (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE works_departments (
    id SERIAL PRIMARY KEY,
    affiliate_id INTEGER REFERENCES affiliate(id),
    department_id INTEGER REFERENCES department(id)
);



DROP TABLE IF EXISTS `Universities_Colleges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Universities_Colleges` (
  `id`  int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `Universities__Colleges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Universities__Colleges` (
  `id`  int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
