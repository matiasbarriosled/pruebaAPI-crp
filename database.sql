CREATE DATABASE CryptoDB;
GO

USE CryptoDB;
GO

-- Tabla para la información básica de la criptomoneda
CREATE TABLE Criptomonedas (
    CriptoID INT PRIMARY KEY IDENTITY,
    Nombre NVARCHAR(100) NOT NULL,
    Simbolo NVARCHAR(10) NOT NULL,
    Descripcion NVARCHAR(255) NULL
);

-- Tabla para almacenar el historial de precios
CREATE TABLE HistorialPrecios (
    PrecioID INT PRIMARY KEY IDENTITY,
    CriptoID INT,
    Fecha DATETIME NOT NULL,
    Precio DECIMAL(18, 8) NOT NULL,
    Volumen DECIMAL(18, 8) NULL,
    MarketCap DECIMAL(18, 8) NULL,
    FOREIGN KEY (CriptoID) REFERENCES Criptomonedas(CriptoID)
);
