CREATE TABLE IF NOT EXISTS `cargo` (
  `idCargo` tinyint(3) NOT NULL AUTO_INCREMENT,
  `nombreCargo` varchar(100) NOT NULL,
  `estado` tinyint(3) UNSIGNED NOT NULL DEFAULT '1',
  PRIMARY KEY (`idCargo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `categoria` (
  `idCategoria` tinyint(3) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombreCategoria` varchar(60) NOT NULL,
  `estado` tinyint(3) UNSIGNED NOT NULL DEFAULT '1',
  PRIMARY KEY (`idCategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `curso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `creditos` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `detallepedido` (
  `idPedido` int(10) UNSIGNED NOT NULL,
  `idProducto` int(10) UNSIGNED NOT NULL,
  `cantidad` tinyint(3) UNSIGNED NOT NULL,
  `CostoDetalle` decimal(9,2) NOT NULL,
  PRIMARY KEY (`idPedido`,`idProducto`),
  KEY `idProducto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `empleado` (
  `idEmpleado` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombreEmpleado` varchar(100) NOT NULL,
  `correoEmpleado` varchar(100) NOT NULL,
  `passwordEmpleado` blob NOT NULL,
  `encuestasRealizadas` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `estado` tinyint(3) UNSIGNED NOT NULL DEFAULT '1',
  `idCargo` tinyint(3) UNSIGNED NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  KEY `idCargo` (`idCargo`)
) ENGINE=InnoDB DEFAULT  CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `pedido` (
  `idPedido` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `estado` varchar(15) NOT NULL,
  `costoTotal` decimal(9,2) NOT NULL,
  `idEmpleado` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `idEmpleado` (`idEmpleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `producto` (
  `idProducto` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombreProducto` varchar(100) NOT NULL,
  `precio` decimal(9,2) NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `estado` tinyint(3) UNSIGNED NOT NULL DEFAULT '1',
  `idCategoria` tinyint(3) UNSIGNED NOT NULL,
  PRIMARY KEY (`idProducto`),
  KEY `idCategoria` (`idCategoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `detallepedido`
  ADD CONSTRAINT `detallepedido_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`),
  ADD CONSTRAINT `detallepedido_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`);


ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`idCargo`) REFERENCES `cargo` (`idCargo`);

ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idEmpleado`) REFERENCES `empleado` (`idEmpleado`);

ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`);