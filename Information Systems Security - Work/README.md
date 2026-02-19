# Web Application Security & Vulnerability Remediation (Passman)

## Table of contents
* [Project Overview](#project-overview)
* [Identified Vulnerabilities](#identified-vulnerabilities)
* [Implemented Solutions](#implemented-solutions)
* [Technologies Used](#technologies-used)
* [Installation & Setup](#installation--setup)

## Project Overview
[cite_start]This project focuses on the security assessment and fortification of a deliberately vulnerable password manager web application, named "Passman"[cite: 74, 76]. [cite_start]It was developed as part of the Information Systems Security course (2025-2026) at the Electrical and Computer Engineering department of AUTH[cite: 1, 2, 3].

The goal of this project is to apply both offensive and defensive security techniques by:
* [cite_start]Identifying critical web vulnerabilities within the PHP source code and MySQL database[cite: 6, 75, 78].
* [cite_start]Exploiting these vulnerabilities (Proof of Concept) to demonstrate the risks, such as authentication bypass and session hijacking[cite: 83, 97, 142].
* [cite_start]Redesigning the application's architecture following "Security by Design" principles to remediate all identified flaws[cite: 84, 434].

## Identified Vulnerabilities
During the vulnerability assessment phase, the following critical issues were discovered and exploited:
* **SQL Injection (SQLi):** The login mechanism (login.php) constructed database queries using direct string concatenation, allowing authentication bypass using payloads like `xxx' OR 1=1; [cite_start]-- `[cite: 90, 92, 93, 101].
* [cite_start]**Stored Cross-Site Scripting (XSS):** The notes/announcements feature (notes.php) displayed user input without sanitization, enabling the injection of malicious JavaScript to steal user Session IDs (Cookie Hijacking)[cite: 133, 137, 140, 162].
* [cite_start]**Cleartext Storage of Sensitive Information:** User login credentials and third-party website passwords were saved in the database without any cryptographic protection, violating data confidentiality[cite: 201, 203, 209].
* [cite_start]**Unencrypted Network Traffic:** The application transmitted sensitive data (credentials) over HTTP, allowing interception via network sniffing tools like Wireshark[cite: 239, 241, 244].

## Implemented Solutions
To secure the application against the aforementioned threats, the following defensive mechanisms were implemented:
* [cite_start]**Prepared Statements:** Eliminated SQLi vulnerabilities by replacing dynamic queries with parameterized prepared statements (`bind_param`) in both login and registration processes[cite: 300, 301, 304].
* [cite_start]**Password Hashing & Salting:** Replaced cleartext password storage with cryptographic hashing (SHA-256) combined with unique user salts, ensuring strong credential protection[cite: 273, 275, 276].
* **Symmetric Data Encryption:** Implemented AES-256-GCM encryption using PHP's OpenSSL library to securely store and retrieve third-party website passwords. [cite_start]The encryption key is derived dynamically using PBKDF2 during user login[cite: 315, 319, 322].
* [cite_start]**Output Encoding:** Mitigated Stored XSS attacks by sanitizing all database outputs rendered in the browser using the `htmlspecialchars` function[cite: 364, 367, 368].
* [cite_start]**Transport Layer Security (TLS):** Enforced HTTPS (TLSv1.3) communication to encrypt network traffic and prevent credential interception (Man-in-the-Middle attacks)[cite: 386, 389].

## Technologies Used
* [cite_start]**Backend:** PHP [cite: 6]
* [cite_start]**Database:** MySQL [cite: 6]
* [cite_start]**Environment:** XAMPP (Apache Web Server) 
* [cite_start]**Security Testing Tools:** Wireshark (Network Traffic Analysis), HeidiSQL (Database Management) [cite: 17, 83, 244]

## Installation & Setup
1. Clone the repository to your local machine:
   ```bash
   git clone [https://github.com/geotsad/Academic-Projects.git](https://github.com/geotsad/Academic-Projects.git)
