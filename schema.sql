CREATE DATABASE  IF NOT EXISTS `dbinformationmanagement` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbinformationmanagement`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: dbinformationmanagement
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appliances`
--

DROP TABLE IF EXISTS `appliances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appliances` (
  `appliance_id` int NOT NULL AUTO_INCREMENT,
  `appliance_name` varchar(200) NOT NULL,
  `appliance_type` varchar(100) DEFAULT NULL,
  `appliance_brand` varchar(100) DEFAULT NULL,
  `appliance_weight` float DEFAULT NULL,
  `appliance_voltage` int DEFAULT NULL,
  `appliance_price` float DEFAULT NULL,
  `appliance_quantity` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`appliance_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `category_summary`
--

DROP TABLE IF EXISTS `category_summary`;
/*!50001 DROP VIEW IF EXISTS `category_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `category_summary` AS SELECT 
 1 AS `category`,
 1 AS `count`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `furniture`
--

DROP TABLE IF EXISTS `furniture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `furniture` (
  `furniture_id` int NOT NULL AUTO_INCREMENT,
  `furniture_name` varchar(200) NOT NULL,
  `furniture_type` varchar(100) DEFAULT NULL,
  `furniture_weight` float DEFAULT NULL,
  `furniture_price` float DEFAULT NULL,
  `furniture_quantity` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`furniture_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shoes`
--

DROP TABLE IF EXISTS `shoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shoes` (
  `shoes_id` int NOT NULL AUTO_INCREMENT,
  `shoes_name` varchar(200) NOT NULL,
  `shoes_brand` varchar(100) DEFAULT NULL,
  `shoes_size` int DEFAULT NULL,
  `shoes_gender` varchar(50) DEFAULT NULL,
  `shoes_color` varchar(50) DEFAULT NULL,
  `shoes_price` float DEFAULT NULL,
  `shoes_quantity` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`shoes_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stationery`
--

DROP TABLE IF EXISTS `stationery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stationery` (
  `stationery_id` int NOT NULL AUTO_INCREMENT,
  `stationery_name` varchar(200) NOT NULL,
  `stationery_brand` varchar(100) DEFAULT NULL,
  `stationery_type` varchar(100) DEFAULT NULL,
  `stationery_quantity` int DEFAULT NULL,
  `stationery_price` float DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`stationery_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `user_items_bought` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'dbinformationmanagement'
--

--
-- Dumping routines for database 'dbinformationmanagement'
--

--
-- Final view structure for view `category_summary`
--

/*!50001 DROP VIEW IF EXISTS `category_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `category_summary` AS select 'Furniture' AS `category`,count(0) AS `count` from `furniture` union all select 'Shoes' AS `Shoes`,count(0) AS `COUNT(*)` from `shoes` union all select 'Appliances' AS `Appliances`,count(0) AS `COUNT(*)` from `appliances` union all select 'Stationery' AS `Stationery`,count(0) AS `COUNT(*)` from `stationery` order by `count` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-24  4:28:38

--# Stored procedures --
with app.app_context():
    try:
        db.create_all()

        # Check if InsertFurniture procedure exists before creating it
        result = db.session.execute(text("SHOW PROCEDURE STATUS WHERE Db = 'dbinformationmanagement' AND Name = 'InsertFurniture'"))
        procedure_exists = result.rowcount > 0

        if not procedure_exists:
            # Stored procedure: InsertFurniture
            db.session.execute(text('''
                CREATE PROCEDURE InsertFurniture(
                    IN furniture_name VARCHAR(200),
                    IN furniture_type VARCHAR(100),
                    IN furniture_weight FLOAT,
                    IN furniture_price FLOAT
                )
                BEGIN
                    INSERT INTO Furniture (furniture_name, furniture_type, furniture_weight, furniture_price)
                    VALUES (furniture_name, furniture_type, furniture_weight, furniture_price);
                END;
            '''))
            db.session.commit()

            

    except Exception as e:
        print(f"Error creating stored procedures: {e}")

        # Stored procedure: UpdateFurniturePrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateFurniturePrice(
                IN p_furniture_id INT,
                IN p_new_price FLOAT
            )
            BEGIN
                UPDATE Furniture
                SET furniture_price = p_new_price
                WHERE furniture_id = p_furniture_id;
            END;
        '''))

        # Stored procedure: DeleteFurnitureById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteFurnitureById(
                IN p_furniture_id INT
            )
            BEGIN
                DELETE FROM Furniture
                WHERE furniture_id = p_furniture_id;
            END;
        '''))

        # Stored procedure: InsertShoes
        db.session.execute(text('''
            CREATE PROCEDURE InsertShoes(
                IN shoes_name VARCHAR(200),
                IN shoes_brand VARCHAR(100),
                IN shoes_size INT,
                IN shoes_gender VARCHAR(50),
                IN shoes_color VARCHAR(50),
                IN shoes_price FLOAT
            )
            BEGIN
                INSERT INTO Shoes (shoes_name, shoes_brand, shoes_size, shoes_gender, shoes_color, shoes_price)
                VALUES (shoes_name, shoes_brand, shoes_size, shoes_gender, shoes_color, shoes_price);
            END;
        '''))

        # Stored procedure: UpdateShoesPrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateShoesPrice(
                IN shoes_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Shoes
                SET shoes_price = new_price
                WHERE shoes_id = shoes_id;
            END;
        '''))

        # Stored procedure: DeleteShoesById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteShoesById(
                IN shoes_id INT
            )
            BEGIN
                DELETE FROM Shoes
                WHERE shoes_id = shoes_id;
            END;
        '''))

        # Stored procedure: InsertAppliance
        db.session.execute(text('''
            CREATE PROCEDURE InsertAppliance(
                IN appliance_name VARCHAR(200),
                IN appliance_type VARCHAR(100),
                IN appliance_brand VARCHAR(100),
                IN appliance_weight FLOAT,
                IN appliance_voltage INT,
                IN appliance_price FLOAT
            )
            BEGIN
                INSERT INTO Appliances (appliance_name, appliance_type, appliance_brand, appliance_weight, appliance_voltage, appliance_price)
                VALUES (appliance_name, appliance_type, appliance_brand, appliance_weight, appliance_voltage, appliance_price);
            END;
        '''))

        # Stored procedure: UpdateAppliancePrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateAppliancePrice(
                IN appliance_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Appliances
                SET appliance_price = new_price
                WHERE appliance_id = appliance_id;
            END;
        '''))

        # Stored procedure: DeleteApplianceById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteApplianceById(
                IN appliance_id INT
            )
            BEGIN
                DELETE FROM Appliances
                WHERE appliance_id = appliance_id;
            END;
        '''))

        # Stored procedure: InsertStationery
        db.session.execute(text('''
            CREATE PROCEDURE InsertStationery(
                IN stationery_name VARCHAR(200),
                IN stationery_brand VARCHAR(100),
                IN stationery_type VARCHAR(100),
                IN stationery_quantity INT,
                IN stationery_price FLOAT
            )
            BEGIN
                INSERT INTO Stationery (stationery_name, stationery_brand, stationery_type, stationery_quantity, stationery_price)
                VALUES (stationery_name, stationery_brand, stationery_type, stationery_quantity, stationery_price);
            END;
        '''))

        # Stored procedure: UpdateStationeryPrice
        db.session.execute(text('''
            CREATE PROCEDURE UpdateStationeryPrice(
                IN stationery_id INT,
                IN new_price FLOAT
            )
            BEGIN
                UPDATE Stationery
                SET stationery_price = new_price
                WHERE stationery_id = stationery_id;
            END;
        '''))

        # Stored procedure: DeleteStationeryById
        db.session.execute(text('''
            CREATE PROCEDURE DeleteStationeryById(
                IN stationery_id INT
            )
            BEGIN
                DELETE FROM Stationery
                WHERE stationery_id = stationery_id;
            END;
        '''))

        db.session.commit()

    except Exception as e:
        print(f"Error creating stored procedure: {e}")

    # TRIGGERS
-- Furniture Insert Trigger
DELIMITER //
 
CREATE TRIGGER furniture_insert_trigger AFTER INSERT ON Furniture
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Furniture (furniture_id, action, item_name, item_type)
    VALUES (NEW.furniture_id, 'INSERT', NEW.furniture_name, NEW.furniture_type);
END;
//
 
-- Furniture Update Trigger
DELIMITER //
 
CREATE TRIGGER furniture_update_trigger AFTER UPDATE ON Furniture
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Furniture (furniture_id, action, item_name, item_type)
    VALUES (NEW.furniture_id, 'UPDATE', NEW.furniture_name, NEW.furniture_type);
END;
//
 
-- Furniture Delete Trigger
DELIMITER //
 
CREATE TRIGGER furniture_delete_trigger AFTER DELETE ON Furniture
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Furniture (furniture_id, action, item_name, item_type)
    VALUES (OLD.furniture_id, 'DELETE', OLD.furniture_name, OLD.furniture_type);
END;
//
 
-- Shoes Insert Trigger
DELIMITER //
 
CREATE TRIGGER shoes_insert_trigger AFTER INSERT ON Shoes
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Shoes (shoes_id, action, item_name, item_brand, item_size, item_gender, item_color, item_price)
    VALUES (NEW.shoes_id, 'INSERT', NEW.shoes_name, NEW.shoes_brand, NEW.shoes_size, NEW.shoes_gender, NEW.shoes_color, NEW.shoes_price);
END;
//
 
-- Shoes Update Trigger
DELIMITER //
 
CREATE TRIGGER shoes_update_trigger AFTER UPDATE ON Shoes
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Shoes (shoes_id, action, item_name, item_brand, item_size, item_gender, item_color, item_price)
    VALUES (NEW.shoes_id, 'UPDATE', NEW.shoes_name, NEW.shoes_brand, NEW.shoes_size, NEW.shoes_gender, NEW.shoes_color, NEW.shoes_price);
END;
//
 
-- Shoes Delete Trigger
DELIMITER //
 
CREATE TRIGGER shoes_delete_trigger AFTER DELETE ON Shoes
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Shoes (shoes_id, action, item_name, item_brand, item_size, item_gender, item_color, item_price)
    VALUES (OLD.shoes_id, 'DELETE', OLD.shoes_name, OLD.shoes_brand, OLD.shoes_size, OLD.shoes_gender, OLD.shoes_color, OLD.shoes_price);
END;
//
 
-- Appliances Insert Trigger
DELIMITER //
 
CREATE TRIGGER appliances_insert_trigger AFTER INSERT ON Appliances
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Appliances (appliance_id, action, item_name, item_type, item_brand, item_weight, item_voltage, item_price)
    VALUES (NEW.appliance_id, 'INSERT', NEW.appliance_name, NEW.appliance_type, NEW.appliance_brand, NEW.appliance_weight, NEW.appliance_voltage, NEW.appliance_price);
END;
//
 
-- Appliances Update Trigger
DELIMITER //
 
CREATE TRIGGER appliances_update_trigger AFTER UPDATE ON Appliances
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Appliances (appliance_id, action, item_name, item_type, item_brand, item_weight, item_voltage, item_price)
    VALUES (NEW.appliance_id, 'UPDATE', NEW.appliance_name, NEW.appliance_type, NEW.appliance_brand, NEW.appliance_weight, NEW.appliance_voltage, NEW.appliance_price);
END;
//
 
-- Appliances Delete Trigger
DELIMITER //
 
CREATE TRIGGER appliances_delete_trigger AFTER DELETE ON Appliances
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Appliances (appliance_id, action, item_name, item_type, item_brand, item_weight, item_voltage, item_price)
    VALUES (OLD.appliance_id, 'DELETE', OLD.appliance_name, OLD.appliance_type, OLD.appliance_brand, OLD.appliance_weight, OLD.appliance_voltage, OLD.appliance_price);
END;
//
 
-- Stationery Insert Trigger
DELIMITER //
 
CREATE TRIGGER stationery_insert_trigger AFTER INSERT ON Stationery
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Stationery (stationery_id, action, item_name, item_type, item_brand, item_quantity, item_price)
    VALUES (NEW.stationery_id, 'INSERT', NEW.stationery_name, NEW.stationery_type, NEW.stationery_brand, NEW.stationery_quantity, NEW.stationery_price);
END;
//
 
-- Stationery Update Trigger
DELIMITER //
 
CREATE TRIGGER stationery_update_trigger AFTER UPDATE ON Stationery
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Stationery (stationery_id, action, item_name, item_type, item_brand, item_quantity, item_price)
    VALUES (NEW.stationery_id, 'UPDATE', NEW.stationery_name, NEW.stationery_type, NEW.stationery_brand, NEW.stationery_quantity,  NEW.stationery_price);
END;
//
 
-- Stationery Delete Trigger
DELIMITER //
 
CREATE TRIGGER stationery_delete_trigger AFTER UPDATE ON Stationery
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Stationery (stationery_id, action, item_name, item_type, item_brand, item_quantity, item_price)
    VALUES (NEW.stationery_id, 'DELETE', NEW.stationery_name, NEW.stationery_type, NEW.stationery_brand, NEW.stationery_quantity,  NEW.stationery_price);
END;
//
        
