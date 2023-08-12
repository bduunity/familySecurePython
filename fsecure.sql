-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 12, 2023 at 04:02 AM
-- Server version: 8.0.33-0ubuntu0.22.04.4
-- PHP Version: 8.1.2-1ubuntu2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fsecure`
--

-- --------------------------------------------------------

--
-- Table structure for table `childs`
--

CREATE TABLE `childs` (
  `id` int NOT NULL,
  `deviceImei` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_german2_ci NOT NULL,
  `parent_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `childs`
--

INSERT INTO `childs` (`id`, `deviceImei`, `parent_id`, `name`) VALUES
(17, 'dsa', 4, 'Child');

-- --------------------------------------------------------

--
-- Table structure for table `confirm_child`
--

CREATE TABLE `confirm_child` (
  `id` int NOT NULL,
  `deviceImei` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL,
  `code` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `confirm_child`
--

INSERT INTO `confirm_child` (`id`, `deviceImei`, `code`) VALUES
(14, 'ieD1691822447', 632062),
(15, 'Yp71691823887', 970873),
(16, 'N8K1691824224', 527971);

-- --------------------------------------------------------

--
-- Table structure for table `confirm_email`
--

CREATE TABLE `confirm_email` (
  `id` int NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL,
  `code` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `confirm_email`
--

INSERT INTO `confirm_email` (`id`, `email`, `code`) VALUES
(4, 'dsa@dsa.dsa', 10032);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL,
  `token` varchar(50) COLLATE utf8mb4_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_german2_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `token`) VALUES
(3, 'asd@asd.asd', 'asdasd', '8ea7076289'),
(4, 'qwe@qwe.qwe', 'qweqwe', '49b29d82ff');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `childs`
--
ALTER TABLE `childs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `confirm_child`
--
ALTER TABLE `confirm_child`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `confirm_email`
--
ALTER TABLE `confirm_email`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `childs`
--
ALTER TABLE `childs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `confirm_child`
--
ALTER TABLE `confirm_child`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `confirm_email`
--
ALTER TABLE `confirm_email`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
