-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2024 at 01:27 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prayagedu`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis_settings_inputs`
--

CREATE TABLE `analysis_settings_inputs` (
  `AnalysisInputID` int(11) NOT NULL,
  `AnalysisType` varchar(100) NOT NULL,
  `AnalysisInput` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`AnalysisInput`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `analysis_settings_inputs`
--

INSERT INTO `analysis_settings_inputs` (`AnalysisInputID`, `AnalysisType`, `AnalysisInput`) VALUES
(3, 'TimeWise', '{\"Timestamp\": \"2024-05-03 21:53:43\"}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis_settings_inputs`
--
ALTER TABLE `analysis_settings_inputs`
  ADD PRIMARY KEY (`AnalysisInputID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis_settings_inputs`
--
ALTER TABLE `analysis_settings_inputs`
  MODIFY `AnalysisInputID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
