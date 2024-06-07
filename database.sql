CREATE DATABASE backtesting;
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON backtesting.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;