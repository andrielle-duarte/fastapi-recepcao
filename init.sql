CREATE DATABASE IF NOT EXISTS recepcao;

CREATE USER IF NOT EXISTS 'recepcao_user'@'%' IDENTIFIED BY 's3nh4d3t3st3';

GRANT ALL PRIVILEGES ON recepcao.* TO 'recepcao_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

USE recepcao;

CREATE TABLE IF NOT EXISTS recepcionista (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  senha VARCHAR(100) NOT NULL,
  admin TINYINT(1) DEFAULT 0,
  PRIMARY KEY (id),
  KEY ix_recepcionista_id (id),
  KEY ix_recepcionista_nome (nome)
);

CREATE TABLE IF NOT EXISTS visitantes (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(100) NOT NULL,
  documento VARCHAR(20) NOT NULL,
  motivo_visita VARCHAR(255) NOT NULL,
  data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
  data_saida DATETIME DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS visitas (
  id INT NOT NULL AUTO_INCREMENT,
  visitante_id INT DEFAULT NULL,
  motivo_visita VARCHAR(255) NOT NULL,
  data_entrada DATETIME DEFAULT NULL,
  data_saida DATETIME DEFAULT NULL,
  PRIMARY KEY (id),
  KEY visitante_id (visitante_id),
  KEY ix_visitas_id (id),
  CONSTRAINT visitas_ibfk_1 FOREIGN KEY (visitante_id) REFERENCES visitantes (id)
);

CREATE DATABASE IF NOT EXISTS keycloak;

GRANT ALL PRIVILEGES ON keycloak.* TO 'andrielle'@'%' IDENTIFIED BY '123456789';
FLUSH PRIVILEGES;
