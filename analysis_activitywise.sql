-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2024 at 01:26 PM
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
-- Table structure for table `analysis_activitywise`
--

CREATE TABLE `analysis_activitywise` (
  `ActivitywiseID` int(11) NOT NULL,
  `UserID` int(10) NOT NULL,
  `ActivityName` varchar(100) NOT NULL,
  `PreferredActivityTime` varchar(100) NOT NULL,
  `EntryDateTime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `UpdatedDateTime` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `analysis_activitywise`
--

INSERT INTO `analysis_activitywise` (`ActivitywiseID`, `UserID`, `ActivityName`, `PreferredActivityTime`, `EntryDateTime`, `UpdatedDateTime`) VALUES
(2, 2, 'NoticeBord', '21', '2024-06-14 09:22:38', NULL),
(3, 2, 'NoticeBord', '21', '2024-06-14 09:55:19', NULL),
(4, 487, 'NoticeBord', '18', '2024-06-14 10:03:21', NULL),
(5, 487, 'EditStudentProfile', '13', '2024-06-14 10:03:21', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis_activitywise`
--
ALTER TABLE `analysis_activitywise`
  ADD PRIMARY KEY (`ActivitywiseID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis_activitywise`
--
ALTER TABLE `analysis_activitywise`
  MODIFY `ActivitywiseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
