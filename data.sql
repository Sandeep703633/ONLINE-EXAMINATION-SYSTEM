-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: e_xam
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (8,'Sandeepbandikatla1@gmail.com','Bsandeep@27');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `c_exam`
--

DROP TABLE IF EXISTS `c_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `c_exam` (
  `subject_code` varchar(255) NOT NULL,
  `exam_name` varchar(255) NOT NULL,
  `exam_date` date NOT NULL,
  `time_limit` time DEFAULT NULL,
  `total_marks` int NOT NULL DEFAULT '0',
  UNIQUE KEY `idx_subject_code` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `c_exam`
--

LOCK TABLES `c_exam` WRITE;
/*!40000 ALTER TABLE `c_exam` DISABLE KEYS */;
INSERT INTO `c_exam` VALUES ('1','python','2023-06-17','04:45:00',10),('123','C','2023-06-20','22:27:00',5);
/*!40000 ALTER TABLE `c_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_results`
--

DROP TABLE IF EXISTS `exam_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_results` (
  `subject_code` varchar(255) NOT NULL,
  `total_score` int NOT NULL,
  `INCORRECT` int DEFAULT NULL,
  `attempted_by` int DEFAULT NULL,
  KEY `subject_code` (`subject_code`),
  KEY `attempted_by_index` (`attempted_by`) USING BTREE,
  CONSTRAINT `exam_results_ibfk_1` FOREIGN KEY (`subject_code`) REFERENCES `c_exam` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_results`
--

LOCK TABLES `exam_results` WRITE;
/*!40000 ALTER TABLE `exam_results` DISABLE KEYS */;
INSERT INTO `exam_results` VALUES ('1',10,NULL,NULL),('123',5,NULL,8),('123',5,NULL,12),('123',5,NULL,11),('123',5,NULL,10),('123',5,NULL,10),('123',5,NULL,13);
/*!40000 ALTER TABLE `exam_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `start_exam`
--

DROP TABLE IF EXISTS `start_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `start_exam` (
  `id` int NOT NULL AUTO_INCREMENT,
  `body` varchar(255) NOT NULL,
  `option_1` varchar(255) NOT NULL,
  `option_2` varchar(255) NOT NULL,
  `option_3` varchar(255) NOT NULL,
  `option_4` varchar(255) NOT NULL,
  `correct_option` varchar(225) DEFAULT NULL,
  `sub_id` varchar(255) DEFAULT NULL,
  `marks` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `start_exam_ibfk_1` (`sub_id`),
  CONSTRAINT `start_exam_ibfk_1` FOREIGN KEY (`sub_id`) REFERENCES `c_exam` (`subject_code`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `start_exam`
--

LOCK TABLES `start_exam` WRITE;
/*!40000 ALTER TABLE `start_exam` DISABLE KEYS */;
INSERT INTO `start_exam` VALUES (13,' What is the output for −\r\n\r\n\'Tutorials Point\' [100:200]?','Index error.',' \' \'','\'Tutorials Point\'','Syntax error','option2','1',10),(15,'What is output for following code −','[1j,4,5]','1','2','typeerror','option4','1',2),(16,'s = 0\r\nfor d in range(0, 5, 0.1):\r\n… s += d\r\n… print(s)','non','Typeerror ','runtime','opt 2 & 3','option4','1',2),(17,'operators in c?','+','-','**','all options','option4','123',5);
/*!40000 ALTER TABLE `start_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (8,'bandikatlasandeep6@gmail.com','123'),(9,'sandeep@gmail.com','123'),(10,'Sandeepbandikatla@gmail.com','123'),(11,'eswarsir@gmail.com','123'),(12,'san@gmail.com','123'),(13,'hi@gmail.com','123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-21 13:14:16
