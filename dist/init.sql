CREATE USER 'kelinci'@'localhost' IDENTIFIED BY 'ujiKlinis@2021';
GRANT ALL PRIVILEGES ON * . * TO 'kelinci'@'localhost';
FLUSH PRIVILEGES;
DROP DATABASE IF EXISTS `kelinci`;
CREATE DATABASE `kelinci`;

use `kelinci`;

DROP TABLE IF EXISTS `kirim_whatsapp` ;
CREATE TABLE `kirim_whatsapp` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tujuan` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `otp` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `uuid` varchar(50)  NOT NULL,
  `waktu_started` datetime NOT NULL,
  `waktu_expired` datetime DEFAULT NULL,
  `inserted` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ;

INSERT INTO kirim_whatsapp VALUES(
    NULL,
    '6285655443271',
    '123123',
    NOW()+INTERVAL 4 HOUR,
    NOW()+INTERVAL 1 DAY,
    NOW()
);

DROP TABLE IF EXISTS `kirim_whatsapp_riwayat` ;
CREATE TABLE `kirim_whatsapp_riwayat` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tujuan` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `otp` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `uuid` varchar(50)  NOT NULL,
  `waktu_started` datetime NOT NULL,
  `waktu_expired` datetime DEFAULT NULL,
  `response` text COLLATE latin1_general_ci NOT NULL,
  `inserted` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ;


-- PROCEDURES
use kelinci;
SET character_set_client  = utf8;
SET character_set_results = utf8;
SET collation_connection  = utf8_general_ci;

DELIMITER //

DROP EVENT IF EXISTS `event_per_5_menit`//
CREATE EVENT `event_per_5_menit` ON SCHEDULE EVERY 5 MINUTE DO
BEGIN
    DECLARE _now DATETIME DEFAULT NULL;
    DECLARE _1menitlalu DATETIME DEFAULT NULL;
    DECLARE _10menitlalu DATETIME DEFAULT NULL;
    DECLARE _24jamlalu DATETIME DEFAULT NULL;

    SET _now = NOW();
    SET _1menitlalu = SUBDATE(_now, INTERVAL 1 MINUTE);
    SET _10menitlalu = SUBDATE(_now, INTERVAL 10 MINUTE);
    SET _24jamlalu = SUBDATE(_now, INTERVAL 24 HOUR);

    # hapus kirim_whatsapp
    INSERT INTO kirim_whatsapp_riwayat
        SELECT
            NULL,
            tujuan
            otp
            uuid,
            waktu_started
            waktu_expired
            CONCAT('** event expired ** ',response),
            NOW()
        FROM
            kirim_whatsapp
    WHERE waktu_expired<=_1menitlalu;
    DELETE FROM kirim_whatsapp WHERE waktu_expired<=_1menitlalu;

END//

DROP EVENT IF EXISTS `event_per_1_menit`//
CREATE EVENT `event_per_1_menit` ON SCHEDULE EVERY 1 MINUTE DO
BEGIN
    DECLARE _now DATETIME DEFAULT NULL;
    DECLARE _1menitlalu DATETIME DEFAULT NULL;
    DECLARE _10menitlalu DATETIME DEFAULT NULL;
    DECLARE _24jamlalu DATETIME DEFAULT NULL;

    SET _now = NOW();
    SET _1menitlalu = SUBDATE(_now, INTERVAL 1 MINUTE);
    SET _10menitlalu = SUBDATE(_now, INTERVAL 10 MINUTE);
    SET _24jamlalu = SUBDATE(_now, INTERVAL 24 HOUR);

END//
DELIMITER ;
