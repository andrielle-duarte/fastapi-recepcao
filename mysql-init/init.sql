CREATE DATABASE IF NOT EXISTS recepcao;

CREATE USER IF NOT EXISTS 'recepcao_user'@'%' IDENTIFIED BY 's3nh4d3t3st3';
  
GRANT ALL ON recepcao.* TO 'recepcao_user'@'%' WITH GRANT OPTION;

USE recepcao;

CREATE TABLE IF NOT EXISTS `recepcionista` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ix_recepcionista_id` (`id`),
  KEY `ix_recepcionista_nome` (`nome`)
);
 
CREATE TABLE IF NOT EXISTS `visitantes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `motivo_visita` varchar(255) NOT NULL,
  `data_entrada` datetime DEFAULT (now()),
  `data_saida` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
);
 
 
CREATE TABLE IF NOT EXISTS `visitas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `visitante_id` int DEFAULT NULL,
  `motivo_visita` varchar(255) NOT NULL,
  `data_entrada` datetime DEFAULT NULL,
  `data_saida` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `visitante_id` (`visitante_id`),
  KEY `ix_visitas_id` (`id`),
  CONSTRAINT `visitas_ibfk_1` FOREIGN KEY (`visitante_id`) REFERENCES `visitantes` (`id`)
);