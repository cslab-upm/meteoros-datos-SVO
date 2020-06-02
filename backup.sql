-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: meteorosdb
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `datos_meteoros`
--

DROP TABLE IF EXISTS `datos_meteoros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datos_meteoros` (
  `ID` varchar(50) NOT NULL,
  `DATE` varchar(50) NOT NULL,
  `STATION` varchar(50) NOT NULL,
  `DURATION` int(11) NOT NULL,
  `DAY` varchar(50) NOT NULL,
  `TYPE` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_meteoros`
--

LOCK TABLES `datos_meteoros` WRITE;
/*!40000 ALTER TABLE `datos_meteoros` DISABLE KEYS */;
INSERT INTO `datos_meteoros` (`ID`, `DATE`, `STATION`, `DURATION`, `DAY`, `TYPE`) VALUES ('fuenlabrada_2020-05-20-02211192','2020/05/20-02:21:11.92','fuenlabrada',2977,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-04224389','2020/05/20-04:22:43.89','fuenlabrada',1138,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-05125283','2020/05/20-05:12:52.83','fuenlabrada',633,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-05182980','2020/05/20-05:18:29.80','fuenlabrada',1800,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-06202607','2020/05/20-06:20:26.07','fuenlabrada',2534,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-06490160','2020/05/20-06:49:01.60','fuenlabrada',5875,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-07061389','2020/05/20-07:06:13.89','fuenlabrada',223,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-07373819','2020/05/20-07:37:38.19','fuenlabrada',836,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-07401326','2020/05/20-07:40:13.26','fuenlabrada',1156,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-07552745','2020/05/20-07:55:27.45','fuenlabrada',2287,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-08173736','2020/05/20-08:17:37.36','fuenlabrada',750,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-08250160','2020/05/20-08:25:01.60','fuenlabrada',534,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-08323029','2020/05/20-08:32:30.29','fuenlabrada',1560,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-09425854','2020/05/20-09:42:58.54','fuenlabrada',1154,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-09435582','2020/05/20-09:43:55.82','fuenlabrada',1516,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-10141651','2020/05/20-10:14:16.51','fuenlabrada',2025,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-10154248','2020/05/20-10:15:42.48','fuenlabrada',1542,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-11152203','2020/05/20-11:15:22.03','fuenlabrada',432,'2020-05-20','overdense'),('fuenlabrada_2020-05-20-22131970','2020/05/20-22:13:19.70','fuenlabrada',2450,'2020-05-20','overdense');
/*!40000 ALTER TABLE `datos_meteoros` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-02 22:17:02
