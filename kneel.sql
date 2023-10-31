CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);
CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);
CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);
CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metalId` INTEGER NOT NULL,
    `sizeId` INTEGER NOT NULL,
    `styleId` INTEGER NOT NULL,
    `timestamp` DATETIME NOT NULL,
    FOREIGN KEY(`metalId`) REFERENCES `Metals`(`id`),
    FOREIGN KEY(`styleId`) REFERENCES `Styles`(`id`),
    FOREIGN KEY(`sizeId`) REFERENCES `Sizes`(`id`)
);

INSERT INTO `Metals` VALUES (null, 'Gold', 500.00);
INSERT INTO `Metals` VALUES (null, 'Silver', 250.00);
INSERT INTO `Metals` VALUES (null, 'Platinum', 1000.00);

INSERT INTO `Sizes` VALUES (null, '0.5 carets', 300.00);
INSERT INTO `Sizes` VALUES (null, '1 carets', 600.00);
INSERT INTO `Sizes` VALUES (null, '2 carets', 1200.00);

INSERT INTO `Styles` VALUES (null, 'Vintage', 800.00);
INSERT INTO `Styles` VALUES (null, 'Modern', 750.00);
INSERT INTO `Styles` VALUES (null, 'Classic', 700.00);

INSERT INTO `Orders` (`id`, `metalId`, `sizeId`, `styleId`, `timestamp`) VALUES (null, 1, 2, 3, '2023-10-30 12:00:00');
