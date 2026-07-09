-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 17, 2026 at 10:34 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `delivery_share`
--

-- --------------------------------------------------------

--
-- Table structure for table `ds_admin`
--

CREATE TABLE `ds_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_admin`
--

INSERT INTO `ds_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ds_bill`
--

CREATE TABLE `ds_bill` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `amount` bigint(20) NOT NULL,
  `lat` varchar(20) NOT NULL,
  `lon` varchar(20) NOT NULL,
  `dp_id` varchar(20) NOT NULL,
  `pay_st` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `deliver_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_bill`
--

INSERT INTO `ds_bill` (`id`, `uname`, `amount`, `lat`, `lon`, `dp_id`, `pay_st`, `rdate`, `deliver_st`) VALUES
(1, 'surya', 300, '10.806328440476824', ' 78.70914459228516', '', 0, '17-04-2026', 0),
(2, 'surya', 300, '10.806328440476824', ' 78.70914459228516', 'D001', 0, '17-04-2026', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ds_cart`
--

CREATE TABLE `ds_cart` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `food_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `category` varchar(30) NOT NULL,
  `qty` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_cart`
--

INSERT INTO `ds_cart` (`id`, `uname`, `food_id`, `status`, `rdate`, `price`, `category`, `qty`, `amount`, `bill_id`) VALUES
(1, 'surya', 1, 1, '17-04-2026', 150, 'Biriyani', 2, 300, 2),
(2, 'surya', 1, 1, '17-04-2026', 150, 'Biriyani', 2, 300, 2);

-- --------------------------------------------------------

--
-- Table structure for table `ds_category`
--

CREATE TABLE `ds_category` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_category`
--

INSERT INTO `ds_category` (`id`, `category`) VALUES
(1, 'Biriyani'),
(2, 'Meals'),
(3, 'Fast Food'),
(4, 'Snacks');

-- --------------------------------------------------------

--
-- Table structure for table `ds_contact`
--

CREATE TABLE `ds_contact` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_contact`
--

INSERT INTO `ds_contact` (`id`, `name`, `email`, `subject`, `message`, `dtime`) VALUES
(1, 'Vijay', 'vijay@gmail.com', 'delivery', 'delivery and food details', '2025-04-30 06:48:30');

-- --------------------------------------------------------

--
-- Table structure for table `ds_deliver_person`
--

CREATE TABLE `ds_deliver_person` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_deliver_person`
--

INSERT INTO `ds_deliver_person` (`id`, `name`, `mobile`, `email`, `latitude`, `longitude`, `uname`, `pass`) VALUES
(1, 'Deepan', 8956745896, 'deepan@gmail.com', '10.821011683986189', ' 78.70099869427095', 'D001', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `ds_feedback`
--

CREATE TABLE `ds_feedback` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `feedback` text NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_feedback`
--

INSERT INTO `ds_feedback` (`id`, `uname`, `feedback`, `dtime`) VALUES
(1, 'Raj', 'good', '2025-04-30 06:39:47'),
(2, 'Raj', 'test', '2026-04-16 10:15:35');

-- --------------------------------------------------------

--
-- Table structure for table `ds_food`
--

CREATE TABLE `ds_food` (
  `id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL,
  `food` varchar(50) NOT NULL,
  `price` double NOT NULL,
  `food_img` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_food`
--

INSERT INTO `ds_food` (`id`, `category`, `food`, `price`, `food_img`) VALUES
(1, 'Biriyani', 'Chicken Biriyani', 150, 'F1chibri.jpg'),
(2, 'Biriyani', 'Mutton Biryani', 250, 'F2Mutton-Biryani.jpg'),
(3, 'Meals', 'Full Meals', 150, 'F3meals.jpg'),
(4, 'Fast Food', 'French Fries', 40, 'F4ffrice.jpg'),
(5, 'Fast Food', 'Burger', 50, 'F5burger.jpeg'),
(6, 'Fast Food', 'Sanwich', 45, 'F6sanw.jpg'),
(7, 'Snacks', 'Samosa', 20, 'F7sams.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `ds_user`
--

CREATE TABLE `ds_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `location` varchar(30) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_user`
--

INSERT INTO `ds_user` (`id`, `name`, `location`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`) VALUES
(1, 'Raj', 'GG Nagar', 'Chennai', 9633852455, 'raj@gmail.com', 'raj', '123456', '03-02-2025'),
(2, 'Surya', 'Trichy', 'Trichy', 8956237415, 'surya@gmail.com', 'surya', '1234', '16-04-2026');
