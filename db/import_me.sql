-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 24, 2022 at 02:38 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pbl`
--

-- --------------------------------------------------------

--
-- Table structure for table `bill_details`
--

CREATE TABLE `bill_details` (
  `bill_id` varchar(30) NOT NULL,
  `items` int(11) NOT NULL,
  `bill_price` int(11) NOT NULL,
  `bill_profit` int(11) NOT NULL,
  `bill_date` date NOT NULL,
  `c_name` varchar(70) NOT NULL,
  `c_email` varchar(70) DEFAULT NULL,
  `discount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bill_details`
--

INSERT INTO `bill_details` (`bill_id`, `items`, `bill_price`, `bill_profit`, `bill_date`, `c_name`, `c_email`, `discount`) VALUES
('jW9euejT', 1, 10, 3, '2022-06-20', 'praveen', NULL, 0),
('NSxBn1gY', 3, 45, 16, '2022-06-22', 'simran', 'simran2296@gmail.com', 0),
('ya1JE097', 9, 648, 199, '2022-06-21', 'vinayak', 'vinayaknigam3373@gmail.com', 10),
('054DAuRF', 17, 480, 170, '2022-06-21', 'rahul', 'rahulshinde959@gmail.com', 5),
('Y1lb7G8x', 23, 660, 245, '2022-06-17', 'anya forger', 'anyaforger@gmail.com', 0),
('8qJgtJfW', 17, 480, 156, '2022-06-19', 'meena', 'menu5900@gmail.com', 0),
('kumNpiAz', 21, 920, 305, '2022-06-22', 'riya desai', 'rdesai.2003@gmail.com', 0),
('sSKFxU4A', 28, 810, 275, '2022-06-22', 'pranav deshpande', 'pranavdspde.99@gmail.com', 0),
('GjH6qrHx', 19, 850, 319, '2022-06-21', 'ishan raskar', 'ishanraskar84@gmail.com', 0),
('tKDol2Kv', 28, 800, 271, '2022-06-22', 'naruto uzumaki', 'hokage.konoha@gmail.com', 0),
('wd3latvf', 14, 325, 122, '2022-06-18', 'neel salunke', 'neelsalunke230@gmail.com', 0),
('lw1jOTLm', 16, 430, 156, '2022-06-22', 'dhruv sinha', 'dhruvsinha478@gmail.com', 0),
('oLO3EtQT', 16, 578, 164, '2022-06-22', 'sakshi joshi', 'sakshijoshi200@gmail.com', 15),
('9Rh1dxxG', 20, 580, 190, '2022-06-19', 'ichigo kurosaki', 'shinigami.ichigo@gmail.com', 5),
('PtBrKxSe', 23, 1095, 403, '2022-06-22', 'sania nanajkar', 'sanianananjkar220@gmail.com', 0),
('weFvWzxF', 47, 950, 331, '2022-06-23', 'jethalal gada', 'jalebi.fafda@gmail.com', 0),
('Pjf0K5Pi', 28, 950, 312, '2022-06-23', 'pushkar ubhe', 'ubhe.pushkar744@gmail.com', 0);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `pname` varchar(70) NOT NULL,
  `barcode` varchar(70) NOT NULL,
  `mrp` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `profit` int(11) NOT NULL,
  `sold` int(11) NOT NULL,
  `date_added` date NOT NULL,
  `pid` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`pname`, `barcode`, `mrp`, `cost`, `quantity`, `profit`, `sold`, `date_added`, `pid`) VALUES
('sprite', '9780201379624', 35, 20, 233, 15, 17, '2022-06-05', 'spt'),
('pepsi', '3450201120002', 40, 25, 241, 15, 11, '2022-06-05', 'psi'),
('mountaindew', '3450201123454', 60, 40, 233, 20, 17, '2022-06-05', 'mdw'),
('mirinda', '9780201379679', 25, 15, 244, 10, 7, '2022-06-05', 'mrd'),
('cocacola', '1230201123454', 90, 55, 247, 35, 8, '2022-06-05', 'ccl'),
('balaji masala chips', '8906010500030', 10, 7, 130, 3, 128, '2022-06-22', 'bmc'),
('pond powder', '9780201345674', 90, 55, 243, 35, 7, '2022-06-05', 'igf'),
('coconut hair oil', '9780201343007', 40, 25, 240, 15, 11, '2022-06-05', 'cho'),
('Cadbury', '9780201345001', 40, 27, 217, 13, 35, '2022-06-05', 'cdb'),
('kitkat', '9780201320008', 40, 25, 234, 15, 21, '2022-06-05', 'kia'),
('milkyway', '9780201330007', 35, 20, 237, 15, 18, '2022-06-05', 'mwy'),
('tiktak', '9780201340006', 10, 7, 241, 3, 9, '2022-06-05', 'tkt'),
('nivia', '9780201344004', 150, 95, 245, 55, 6, '2022-06-05', 'nva'),
('dermicool', '9780201342000', 110, 85, 246, 25, 4, '2022-06-05', 'dcl'),
('trimax', '9780201347005', 40, 25, 219, 15, 31, '2022-06-05', 'trm');

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `bill_id` varchar(30) NOT NULL,
  `pname` varchar(70) NOT NULL,
  `quantity` int(11) NOT NULL,
  `profit_pp` int(11) NOT NULL,
  `barcode` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`bill_id`, `pname`, `quantity`, `profit_pp`, `barcode`) VALUES
('jW9euejT', 'balaji masala chips', 1, 3, '8906010500030'),
('NSxBn1gY', 'mirinda', 1, 10, '9780201379679'),
('NSxBn1gY', 'balaji masala chips', 2, 6, '8906010500030'),
('ya1JE097', 'cocacola', 5, 130, '1230201123454'),
('ya1JE097', 'coconut hair oil', 1, 11, '9780201343007'),
('ya1JE097', 'Cadbury', 2, 18, '9780201345001'),
('ya1JE097', 'nivia', 1, 40, '9780201344004'),
('054DAuRF', 'balaji masala chips', 5, 13, '8906010500030'),
('054DAuRF', 'milkyway', 5, 66, '9780201330007'),
('054DAuRF', 'pepsi', 2, 26, '3450201120002'),
('054DAuRF', 'kitkat', 5, 65, '9780201320008'),
('Y1lb7G8x', 'sprite', 2, 30, '9780201379624'),
('Y1lb7G8x', 'balaji masala chips', 10, 30, '8906010500030'),
('Y1lb7G8x', 'pond powder', 1, 35, '9780201345674'),
('Y1lb7G8x', 'kitkat', 10, 150, '9780201320008'),
('8qJgtJfW', 'balaji masala chips', 10, 30, '8906010500030'),
('8qJgtJfW', 'Cadbury', 2, 26, '9780201345001'),
('8qJgtJfW', 'mountaindew', 5, 100, '3450201123454'),
('kumNpiAz', 'pond powder', 1, 35, '9780201345674'),
('kumNpiAz', 'coconut hair oil', 1, 15, '9780201343007'),
('kumNpiAz', 'Cadbury', 10, 130, '9780201345001'),
('kumNpiAz', 'nivia', 1, 55, '9780201344004'),
('kumNpiAz', 'dermicool', 1, 25, '9780201342000'),
('kumNpiAz', 'kitkat', 2, 30, '9780201320008'),
('kumNpiAz', 'balaji masala chips', 5, 15, '8906010500030'),
('sSKFxU4A', 'balaji masala chips', 10, 30, '8906010500030'),
('sSKFxU4A', 'mountaindew', 5, 100, '3450201123454'),
('sSKFxU4A', 'pond powder', 1, 35, '9780201345674'),
('sSKFxU4A', 'Cadbury', 5, 65, '9780201345001'),
('sSKFxU4A', 'milkyway', 2, 30, '9780201330007'),
('sSKFxU4A', 'tiktak', 5, 15, '9780201340006'),
('GjH6qrHx', 'sprite', 2, 30, '9780201379624'),
('GjH6qrHx', 'mirinda', 2, 20, '9780201379679'),
('GjH6qrHx', 'trimax', 10, 150, '9780201347005'),
('GjH6qrHx', 'nivia', 2, 110, '9780201344004'),
('GjH6qrHx', 'balaji masala chips', 3, 9, '8906010500030'),
('tKDol2Kv', 'balaji masala chips', 15, 45, '8906010500030'),
('tKDol2Kv', 'pepsi', 2, 30, '3450201120002'),
('tKDol2Kv', 'pond powder', 1, 35, '9780201345674'),
('tKDol2Kv', 'Cadbury', 2, 26, '9780201345001'),
('tKDol2Kv', 'milkyway', 2, 30, '9780201330007'),
('tKDol2Kv', 'dermicool', 1, 25, '9780201342000'),
('tKDol2Kv', 'trimax', 4, 60, '9780201347005'),
('tKDol2Kv', 'mountaindew', 1, 20, '3450201123454'),
('wd3latvf', 'balaji masala chips', 5, 15, '8906010500030'),
('wd3latvf', 'sprite', 5, 75, '9780201379624'),
('wd3latvf', 'Cadbury', 2, 26, '9780201345001'),
('wd3latvf', 'tiktak', 2, 6, '9780201340006'),
('lw1jOTLm', 'balaji masala chips', 5, 15, '8906010500030'),
('lw1jOTLm', 'coconut hair oil', 1, 15, '9780201343007'),
('lw1jOTLm', 'pepsi', 3, 45, '3450201120002'),
('lw1jOTLm', 'tiktak', 2, 6, '9780201340006'),
('lw1jOTLm', 'trimax', 5, 75, '9780201347005'),
('oLO3EtQT', 'sprite', 2, 20, '9780201379624'),
('oLO3EtQT', 'cocacola', 1, 22, '1230201123454'),
('oLO3EtQT', 'balaji masala chips', 2, 3, '8906010500030'),
('oLO3EtQT', 'milkyway', 2, 20, '9780201330007'),
('oLO3EtQT', 'coconut hair oil', 5, 45, '9780201343007'),
('oLO3EtQT', 'mirinda', 2, 13, '9780201379679'),
('oLO3EtQT', 'pond powder', 2, 43, '9780201345674'),
('9Rh1dxxG', 'balaji masala chips', 10, 25, '8906010500030'),
('9Rh1dxxG', 'mirinda', 2, 18, '9780201379679'),
('9Rh1dxxG', 'sprite', 2, 27, '9780201379624'),
('9Rh1dxxG', 'pepsi', 2, 26, '3450201120002'),
('9Rh1dxxG', 'mountaindew', 2, 34, '3450201123454'),
('9Rh1dxxG', 'kitkat', 1, 13, '9780201320008'),
('9Rh1dxxG', 'nivia', 1, 48, '9780201344004'),
('PtBrKxSe', 'pond powder', 1, 35, '9780201345674'),
('PtBrKxSe', 'coconut hair oil', 3, 45, '9780201343007'),
('PtBrKxSe', 'nivia', 1, 55, '9780201344004'),
('PtBrKxSe', 'trimax', 2, 30, '9780201347005'),
('PtBrKxSe', 'Cadbury', 6, 78, '9780201345001'),
('PtBrKxSe', 'mountaindew', 2, 40, '3450201123454'),
('PtBrKxSe', 'kitkat', 3, 45, '9780201320008'),
('PtBrKxSe', 'milkyway', 5, 75, '9780201330007'),
('weFvWzxF', 'balaji masala chips', 35, 105, '8906010500030'),
('weFvWzxF', 'mountaindew', 2, 40, '3450201123454'),
('weFvWzxF', 'cocacola', 2, 70, '1230201123454'),
('weFvWzxF', 'sprite', 2, 30, '9780201379624'),
('weFvWzxF', 'Cadbury', 2, 26, '9780201345001'),
('weFvWzxF', 'milkyway', 2, 30, '9780201330007'),
('weFvWzxF', 'pepsi', 2, 30, '3450201120002'),
('Pjf0K5Pi', 'sprite', 2, 30, '9780201379624'),
('Pjf0K5Pi', 'balaji masala chips', 10, 30, '8906010500030'),
('Pjf0K5Pi', 'dermicool', 2, 50, '9780201342000'),
('Pjf0K5Pi', 'trimax', 10, 150, '9780201347005'),
('Pjf0K5Pi', 'Cadbury', 4, 52, '9780201345001');

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE `stats` (
  `pname` varchar(70) NOT NULL,
  `sold` int(11) NOT NULL,
  `net_revenue` int(11) NOT NULL,
  `net_profit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stats`
--

INSERT INTO `stats` (`pname`, `sold`, `net_revenue`, `net_profit`) VALUES
('balaji masala chips', 128, 1269, 373),
('mirinda', 7, 164, 59),
('cocacola', 8, 661, 221),
('coconut hair oil', 11, 406, 131),
('Cadbury', 35, 1392, 447),
('nivia', 6, 877, 307),
('milkyway', 18, 610, 250),
('pepsi', 11, 432, 157),
('kitkat', 21, 828, 303),
('sprite', 17, 580, 240),
('pond powder', 7, 603, 218),
('mountaindew', 17, 1014, 334),
('dermicool', 4, 440, 100),
('tiktak', 9, 90, 27),
('trimax', 31, 1240, 465);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
