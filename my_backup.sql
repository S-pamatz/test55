-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: our_users1
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `affiliate`
--

DROP TABLE IF EXISTS `affiliate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `affiliate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_file` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password_hash` varchar(102) DEFAULT NULL,
  `firstname` varchar(200) DEFAULT NULL,
  `lastname` varchar(200) DEFAULT NULL,
  `is_admin` tinyint DEFAULT NULL,
  `areaofinterest` varchar(200) DEFAULT NULL,
  `wsuCampus` varchar(200) DEFAULT NULL,
  `department` varchar(200) DEFAULT NULL,
  `membership` varchar(200) DEFAULT NULL,
  `sponsor` varchar(200) DEFAULT NULL,
  `partners` varchar(200) DEFAULT NULL,
  `university` varchar(200) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `is_ban` tinyint DEFAULT NULL,
  `is_validated` tinyint(1) DEFAULT '0',
  `wsu_faculty` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliate`
--

LOCK TABLES `affiliate` WRITE;
/*!40000 ALTER TABLE `affiliate` DISABLE KEYS */;
INSERT INTO `affiliate` VALUES (1,'Default_pic.png',NULL,'pbkdf2:sha256:260000$0AuECtTVrgWn7YiY$76bfe3bf545a40bf2bd7658f834ecc0a05ff0f3742ce77f3c471ce933c9b7e62','Brian','Joo',1,NULL,'WSU Spokane',NULL,'Yes',NULL,NULL,NULL,'1',NULL,1,NULL),(7,'Default_pic.png','brianjoo500@gmail.com','pbkdf2:sha256:260000$ZFh3tpNXmmWQ4vvp$28cb398456bf382f19afae8b38b2f4605d3419fc7bb04d4accd1409697fab46b','Brian','Joo',0,NULL,'WSU Spokane',NULL,'Please Select an Option Below',NULL,NULL,NULL,'1',1,0,NULL),(8,'Default_pic.png','5@gmail.com','pbkdf2:sha256:260000$m6MC3dEFCkiEcz4Y$e40b2a0a59a07e76a577505468f142499e3a48cf2bcf44d294b09b09393c7565','Brian','Joo',0,NULL,'WSU Tri-Cities','SBS','Please Select an Option Below','Ecol','PNNL','WSU','1',1,1,NULL),(9,'Default_pic.png','8@gmail.com','pbkdf2:sha256:260000$GXxG9zgd6fu8MXFb$63d668ea0118e04ab9e774800dc89252a5d1fa7060bd8a18656365b41f0fc102','Brian','Joo',0,NULL,'WSU Spokane',NULL,'Yes',NULL,NULL,NULL,'1',1,1,NULL),(11,'Default_pic.png','t1@gmail.com','pbkdf2:sha256:260000$GuTxQFEM3UhuAq6b$a498e31a16bdb37ceff69e1643d759e964b3aaa798d6de7a8727e05f1ed740da','dr','pepper',1,NULL,'WSU Pullman','Chem','Yes, I am a member','USDA','PNNL','UW','1',NULL,1,NULL),(12,'Default_pic.png','de@gmail.com','pbkdf2:sha256:260000$iryUe9R4tDwqw8mU$97de3883f7388523f4a0ad5bc17a8c10919ec023d7a80c3c02477e588d53b6d5','demo','demo',0,NULL,'WSU Tri-Cities','Chem','Yes, I am a member','Ecol','PNNL','WSU','hello.com',0,1,NULL),(13,'e61833904ec63db9.png','l@gmail.com','pbkdf2:sha256:260000$SeLMof2KZEiTth1p$e0b2ea0aa09cffb60d4c3c330cdeee006d40520dc608d3dd9075cb0e8e3dea37','test','harold',0,NULL,'WSU Pullman','Bio','Yes',NULL,NULL,'WSU','1@gmail.com',0,1,NULL),(40,'Default_pic.png',NULL,'pbkdf2:sha256:260000$BT6b8EZ4MwX7h9F0$448fb11aa5af24b2e33505bcd3222485b08909b8d54761a7d6f9da8068d633da','Brian','Joo',0,NULL,'WSU Spokane','Anthropology','Yes',NULL,NULL,NULL,'1',0,1,NULL),(78,'119bccbff980bb5e.png','brian.joo@wsu.edu','pbkdf2:sha256:260000$a4kpWliCbnGUcjvh$fa4bd0afd17ad2d79c83d743a71c4d0b7119d1da32f28ceb5f263fe08eab1977','GO','COUGS',0,NULL,'WSU Spokane','CS','No, I am not a member','Ecol','PNNL','OS','h121221',0,1,NULL);
/*!40000 ALTER TABLE `affiliate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliate_subcategories`
--

DROP TABLE IF EXISTS `affiliate_subcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `affiliate_subcategories` (
  `affiliate_id` int NOT NULL,
  `subcategory_id` int NOT NULL,
  PRIMARY KEY (`affiliate_id`,`subcategory_id`),
  KEY `subcategory_id` (`subcategory_id`),
  CONSTRAINT `affiliate_subcategories_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`),
  CONSTRAINT `affiliate_subcategories_ibfk_2` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliate_subcategories`
--

LOCK TABLES `affiliate_subcategories` WRITE;
/*!40000 ALTER TABLE `affiliate_subcategories` DISABLE KEYS */;
/*!40000 ALTER TABLE `affiliate_subcategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `air`
--

DROP TABLE IF EXISTS `air`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `air` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `air`
--

LOCK TABLES `air` WRITE;
/*!40000 ALTER TABLE `air` DISABLE KEYS */;
INSERT INTO `air` VALUES (1,'Carbon Cycling'),(2,'Air quality'),(3,'Evaporation'),(4,'Flux measurement'),(5,'Modeling'),(6,'Climate');
/*!40000 ALTER TABLE `air` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `biginterest`
--

DROP TABLE IF EXISTS `biginterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `biginterest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `affiliate_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  CONSTRAINT `biginterest_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `biginterest`
--

LOCK TABLES `biginterest` WRITE;
/*!40000 ALTER TABLE `biginterest` DISABLE KEYS */;
INSERT INTO `biginterest` VALUES (9,'Interest1',NULL),(10,'Interest1',NULL),(26,'Interest1',11),(27,'Interest1',11),(28,'Interest1',78),(29,'Interest2',78),(30,'Interest1',78),(31,'Air',78),(32,'Water',78);
/*!40000 ALTER TABLE `biginterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Bio'),(2,'Chem'),(3,'CS'),(4,'Eng'),(5,'EE');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edu`
--

DROP TABLE IF EXISTS `edu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `affiliate_id` int DEFAULT NULL,
  `education_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  KEY `education_id` (`education_id`),
  CONSTRAINT `edu_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`),
  CONSTRAINT `edu_ibfk_2` FOREIGN KEY (`education_id`) REFERENCES `education` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edu`
--

LOCK TABLES `edu` WRITE;
/*!40000 ALTER TABLE `edu` DISABLE KEYS */;
INSERT INTO `edu` VALUES (1,13,1),(2,11,2),(3,11,3),(5,11,5);
/*!40000 ALTER TABLE `edu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `education`
--

DROP TABLE IF EXISTS `education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `education` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `college` varchar(255) DEFAULT NULL,
  `year` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `education`
--

LOCK TABLES `education` WRITE;
/*!40000 ALTER TABLE `education` DISABLE KEYS */;
INSERT INTO `education` VALUES (1,'Water','Ph.D.','1231',NULL),(2,'CSCS','M.S.','12312312123',NULL),(3,'cs','Ph.D.','wsu','2011'),(5,'1','Ph.D.','1','2007');
/*!40000 ALTER TABLE `education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exp`
--

DROP TABLE IF EXISTS `exp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `affiliate_id` int DEFAULT NULL,
  `experience_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  KEY `experience_id` (`experience_id`),
  CONSTRAINT `exp_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`),
  CONSTRAINT `exp_ibfk_2` FOREIGN KEY (`experience_id`) REFERENCES `experience` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exp`
--

LOCK TABLES `exp` WRITE;
/*!40000 ALTER TABLE `exp` DISABLE KEYS */;
INSERT INTO `exp` VALUES (1,13,1),(2,11,2);
/*!40000 ALTER TABLE `exp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experience`
--

DROP TABLE IF EXISTS `experience`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experience` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `date_from` varchar(120) DEFAULT NULL,
  `date_to` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experience`
--

LOCK TABLES `experience` WRITE;
/*!40000 ALTER TABLE `experience` DISABLE KEYS */;
INSERT INTO `experience` VALUES (1,'professor','1','2023-10-01','2023-10-01'),(2,'Prof','wsy','2023-07-01','2023-04-01');
/*!40000 ALTER TABLE `experience` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest_subcategory_association`
--

DROP TABLE IF EXISTS `interest_subcategory_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interest_subcategory_association` (
  `interest_id` int DEFAULT NULL,
  `subcategory_id` int DEFAULT NULL,
  KEY `interest_id` (`interest_id`),
  KEY `subcategory_id` (`subcategory_id`),
  CONSTRAINT `interest_subcategory_association_ibfk_1` FOREIGN KEY (`interest_id`) REFERENCES `interesttest2` (`id`),
  CONSTRAINT `interest_subcategory_association_ibfk_2` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest_subcategory_association`
--

LOCK TABLES `interest_subcategory_association` WRITE;
/*!40000 ALTER TABLE `interest_subcategory_association` DISABLE KEYS */;
INSERT INTO `interest_subcategory_association` VALUES (1,31),(1,32),(1,33),(1,32),(1,32),(1,32),(1,31),(1,32);
/*!40000 ALTER TABLE `interest_subcategory_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interestform`
--

DROP TABLE IF EXISTS `interestform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interestform` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interestform`
--

LOCK TABLES `interestform` WRITE;
/*!40000 ALTER TABLE `interestform` DISABLE KEYS */;
INSERT INTO `interestform` VALUES (1,'Interest1'),(2,'Interest2'),(3,'Interest3'),(4,'Air'),(5,'Water'),(6,'Land');
/*!40000 ALTER TABLE `interestform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interests`
--

DROP TABLE IF EXISTS `interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `affiliate_id` int DEFAULT NULL,
  `intresttest_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  KEY `intresttest_id` (`intresttest_id`),
  CONSTRAINT `interests_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`),
  CONSTRAINT `interests_ibfk_2` FOREIGN KEY (`intresttest_id`) REFERENCES `intrest_test` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interests`
--

LOCK TABLES `interests` WRITE;
/*!40000 ALTER TABLE `interests` DISABLE KEYS */;
/*!40000 ALTER TABLE `interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interests_multiple`
--

DROP TABLE IF EXISTS `interests_multiple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interests_multiple` (
  `intresttest_id` int DEFAULT NULL,
  `subcategory_id` int DEFAULT NULL,
  KEY `intresttest_id` (`intresttest_id`),
  KEY `subcategory_id` (`subcategory_id`),
  CONSTRAINT `interests_multiple_ibfk_2` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interests_multiple`
--

LOCK TABLES `interests_multiple` WRITE;
/*!40000 ALTER TABLE `interests_multiple` DISABLE KEYS */;
/*!40000 ALTER TABLE `interests_multiple` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interesttest2`
--

DROP TABLE IF EXISTS `interesttest2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interesttest2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `subcategory_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `subcategory_id` (`subcategory_id`),
  CONSTRAINT `interesttest2_ibfk_1` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interesttest2`
--

LOCK TABLES `interesttest2` WRITE;
/*!40000 ALTER TABLE `interesttest2` DISABLE KEYS */;
INSERT INTO `interesttest2` VALUES (1,'Air',31),(10,'fuck',31),(11,'fuck2',36),(15,'test2',NULL);
/*!40000 ALTER TABLE `interesttest2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `intrest_test`
--

DROP TABLE IF EXISTS `intrest_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intrest_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `subcategory_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `subcategory_id` (`subcategory_id`),
  CONSTRAINT `intrest_test_ibfk_1` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intrest_test`
--

LOCK TABLES `intrest_test` WRITE;
/*!40000 ALTER TABLE `intrest_test` DISABLE KEYS */;
/*!40000 ALTER TABLE `intrest_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partners`
--

DROP TABLE IF EXISTS `partners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partners`
--

LOCK TABLES `partners` WRITE;
/*!40000 ALTER TABLE `partners` DISABLE KEYS */;
INSERT INTO `partners` VALUES (1,'PNNL'),(2,'MYSQL');
/*!40000 ALTER TABLE `partners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(400) DEFAULT NULL,
  `url` varchar(400) DEFAULT NULL,
  `authorss` varchar(120) DEFAULT NULL,
  `publisher` varchar(120) DEFAULT NULL,
  `year` varchar(120) DEFAULT NULL,
  `partners` varchar(200) DEFAULT NULL,
  `sponsor` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (8,'123123','12312312','12312',NULL,'Present','PNNL','NASA'),(9,'123','12312','Jan boll',NULL,'2019','MYSQL','NASA');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publications`
--

DROP TABLE IF EXISTS `publications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `authors` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `journal` varchar(100) DEFAULT NULL,
  `volume` int DEFAULT NULL,
  `issue` int DEFAULT NULL,
  `publication_year` int DEFAULT NULL,
  `page_range` varchar(20) DEFAULT NULL,
  `affiliate_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  CONSTRAINT `publications_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publications`
--

LOCK TABLES `publications` WRITE;
/*!40000 ALTER TABLE `publications` DISABLE KEYS */;
INSERT INTO `publications` VALUES (3,'21321312','123123','12321',123213,1231,12312,'123123',7),(10,'brian ','Streamflow–concentration relationships of surface water in the Choapa basin: historical analysis and projections under climate change',NULL,NULL,NULL,NULL,NULL,NULL),(11,'brian ','Análisis y síntesis de buenas prácticas en la educación socioambiental interdisciplinaria en Estados Unidos',NULL,NULL,NULL,NULL,NULL,NULL),(12,'brian ','VAN EEN LUSTRUM EN EEN LUSTHOF',NULL,NULL,NULL,NULL,NULL,NULL),(13,'brian ','Streamflow–concentration relationships of surface water in the Choapa basin: historical analysis and projections under climate change',NULL,NULL,NULL,NULL,NULL,NULL),(14,'brian ','Análisis y síntesis de buenas prácticas en la educación socioambiental interdisciplinaria en Estados Unidos',NULL,NULL,NULL,NULL,NULL,NULL),(15,'brian ','VAN EEN LUSTRUM EN EEN LUSTHOF',NULL,NULL,NULL,NULL,NULL,NULL),(33,'Brian Joo','Water utility engagement in wildfire mitigation in watersheds in the western United States.',NULL,NULL,NULL,NULL,NULL,13),(34,'testPUB','testPUB','testPUB',123123213,12321,123123,'12312',13),(35,'Brian Joo','Streamflow–concentration relationships of surface water in the Choapa basin: historical analysis and projections under climate change',NULL,NULL,NULL,NULL,NULL,NULL),(107,'Vanessa Hernandez, J. Arumí, J. Boll, Denisse J. Duhalde, S. MacDonell, R. Oyarzún','Streamflow–concentration relationships of surface water in the Choapa basin: historical analysis and projections under climate change','10.1080/02626667.2023.2212167',NULL,NULL,2025,NULL,78),(119,'Vanessa Hernandez, J. Arumí, J. Boll, Denisse J. Duhalde, S. MacDonell, R. Oyarzún','Streamflow–concentration relationships of surface water in the Choapa basin: historical analysis and projections under climate change','10.1080/02626667.2023.2212167',NULL,NULL,2023,NULL,11),(120,'Jan Boll, Timothy E. Link, Mary V. Santelmann, Robert Heinse, Barbara A. Cosens','Análisis y síntesis de buenas prácticas en la educación socioambiental interdisciplinaria en Estados Unidos','10.22201/CEIICH.24485705E.2016.10.57755',NULL,NULL,2016,NULL,11),(121,'Jan Maarten Boll','VAN EEN LUSTRUM EN EEN LUSTHOF','10.1163/2543-1749-90000353',NULL,NULL,2013,NULL,11);
/*!40000 ALTER TABLE `publications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smallinterest`
--

DROP TABLE IF EXISTS `smallinterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smallinterest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `affiliate_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  CONSTRAINT `smallinterest_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smallinterest`
--

LOCK TABLES `smallinterest` WRITE;
/*!40000 ALTER TABLE `smallinterest` DISABLE KEYS */;
INSERT INTO `smallinterest` VALUES (8,'small1',NULL),(9,'small2',78),(10,'small2',78),(11,'small1',78),(12,'small1',78),(13,'small1',78),(14,'small2',78),(15,'small2',78),(16,'small1',78),(17,'small2',78),(18,'small3',78),(19,'small1',78),(20,'small1',78),(21,'small2',78),(22,'small1',78),(23,'small1',78),(24,'small2',78),(25,'small1',78),(26,'small2',78),(27,'small2',78),(28,'small3',78),(29,'small3',78),(32,'small2',11),(33,'small2',11),(34,'small1',11),(35,'small1',11),(36,'small1',11),(37,'small2',11),(38,'small3',11),(39,'small1',11),(40,'small1',11),(41,'small1',11),(42,'small1',11),(43,'small1',11),(44,'Carbon Cycling',78);
/*!40000 ALTER TABLE `smallinterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smallinterestform`
--

DROP TABLE IF EXISTS `smallinterestform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smallinterestform` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smallinterestform`
--

LOCK TABLES `smallinterestform` WRITE;
/*!40000 ALTER TABLE `smallinterestform` DISABLE KEYS */;
INSERT INTO `smallinterestform` VALUES (1,'small1'),(2,'small2'),(3,'small3'),(4,'small11_1'),(5,'Carbon Cycling'),(6,'Air quality'),(7,'Evaporation'),(8,'Flux measurement'),(9,'Modeling'),(10,'Drinking'),(11,'Ground'),(12,'Surface'),(13,'Deforestation'),(14,'Wildfire'),(15,'Land Use Change');
/*!40000 ALTER TABLE `smallinterestform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsor`
--

DROP TABLE IF EXISTS `sponsor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsor`
--

LOCK TABLES `sponsor` WRITE;
/*!40000 ALTER TABLE `sponsor` DISABLE KEYS */;
INSERT INTO `sponsor` VALUES (1,'Ecol'),(2,'NASA'),(3,'USDA'),(4,'USAID'),(5,'NSF');
/*!40000 ALTER TABLE `sponsor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (31,'water1'),(32,'water2'),(33,'water3'),(34,'air1'),(35,'air2'),(36,'air3'),(37,'land1'),(38,'land2'),(39,'land3');
/*!40000 ALTER TABLE `subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subinterest`
--

DROP TABLE IF EXISTS `subinterest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subinterest` (
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subinterest`
--

LOCK TABLES `subinterest` WRITE;
/*!40000 ALTER TABLE `subinterest` DISABLE KEYS */;
/*!40000 ALTER TABLE `subinterest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `universities__colleges`
--

DROP TABLE IF EXISTS `universities__colleges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `universities__colleges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `universities__colleges`
--

LOCK TABLES `universities__colleges` WRITE;
/*!40000 ALTER TABLE `universities__colleges` DISABLE KEYS */;
INSERT INTO `universities__colleges` VALUES (1,'WSU'),(2,'OS'),(3,'UW'),(4,'UI'),(5,'Univ NM');
/*!40000 ALTER TABLE `universities__colleges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `universities_colleges`
--

DROP TABLE IF EXISTS `universities_colleges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `universities_colleges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `universities_colleges`
--

LOCK TABLES `universities_colleges` WRITE;
/*!40000 ALTER TABLE `universities_colleges` DISABLE KEYS */;
INSERT INTO `universities_colleges` VALUES (1,'WSU'),(2,'OS'),(3,'UW'),(4,'UI'),(5,'Univ NM');
/*!40000 ALTER TABLE `universities_colleges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_subinterests`
--

DROP TABLE IF EXISTS `user_subinterests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_subinterests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `affiliate_id` int DEFAULT NULL,
  `subinterest_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `affiliate_id` (`affiliate_id`),
  KEY `subinterest_id` (`subinterest_id`),
  CONSTRAINT `user_subinterests_ibfk_1` FOREIGN KEY (`affiliate_id`) REFERENCES `affiliate` (`id`),
  CONSTRAINT `user_subinterests_ibfk_2` FOREIGN KEY (`subinterest_id`) REFERENCES `subinterest` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_subinterests`
--

LOCK TABLES `user_subinterests` WRITE;
/*!40000 ALTER TABLE `user_subinterests` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_subinterests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `water`
--

DROP TABLE IF EXISTS `water`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `water` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `water`
--

LOCK TABLES `water` WRITE;
/*!40000 ALTER TABLE `water` DISABLE KEYS */;
INSERT INTO `water` VALUES (1,'Drinking'),(2,'Ground'),(3,'Surface'),(4,'Supply');
/*!40000 ALTER TABLE `water` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works`
--

DROP TABLE IF EXISTS `works`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `works` (
  `affiliate_id` tinyint DEFAULT NULL,
  `project_id` tinyint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works`
--

LOCK TABLES `works` WRITE;
/*!40000 ALTER TABLE `works` DISABLE KEYS */;
INSERT INTO `works` VALUES (13,0),(13,0),(11,0),(78,8),(11,9);
/*!40000 ALTER TABLE `works` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works_departments`
--

DROP TABLE IF EXISTS `works_departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `works_departments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `affiliate_id` int DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works_departments`
--

LOCK TABLES `works_departments` WRITE;
/*!40000 ALTER TABLE `works_departments` DISABLE KEYS */;
INSERT INTO `works_departments` VALUES (8,12,2),(9,37,2),(10,47,4),(12,48,1),(13,41,1),(14,49,3),(15,50,1),(16,51,1),(17,52,3),(18,53,3),(19,54,3),(20,55,5),(21,56,3),(22,57,3),(23,58,5),(24,59,5),(25,60,5),(26,61,5),(27,62,3),(28,63,3),(29,64,5),(30,65,1),(31,66,4),(35,70,3),(36,71,2),(39,74,1),(44,78,3),(45,11,2),(46,13,1);
/*!40000 ALTER TABLE `works_departments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-05 19:14:02
