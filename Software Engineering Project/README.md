# [Project Name/Topic] - Software Engineering II

## Table of Contents
* [Project Overview](#project-overview)
* [Deliverable 1: Agile Development & MVP](#deliverable-1-agile-development--mvp)
* [Deliverable 2: CI/CD & Automated Testing](#deliverable-2-cicd--automated-testing)
* [Deliverable 3: Software Quality & Security Analysis](#deliverable-3-software-quality--security-analysis)
* [Technologies Used](#technologies-used)
* [Installation & Setup](#installation--setup)

## Project Overview
This repository contains the full-stack source code, automated pipelines, and quality assurance reports for **SociActive**. The project was developed as part of the "Software Engineering II" course at the Electrical and Computer Engineering (ECE) department of AUTH. 

The primary focus of this project is not just on writing code, but on applying modern **DevOps practices, Agile methodologies, and strict Software Quality standards (ISO 25010)** throughout the software development lifecycle.

## Deliverable 1: Agile Development & MVP
The first phase focused on project management and the initial scaffolding of the web application:
* **Agile/Scrum Methodology:** Managed the project lifecycle using Agile principles, defining roles, and tracking progress via sprints.
* **Full-Stack Implementation:** Developed the initial Minimum Viable Product (MVP) using **React** for the frontend and **Node.js/Express** for the backend.
* **Version Control:** Established a robust branching strategy using Git and GitHub.

## Deliverable 2: CI/CD & Automated Testing
The second phase transitioned the project into a continuous integration environment:
* **CI/CD Pipelines:** Configured **GitHub Actions** to automate the build, testing, and deployment processes, ensuring code stability upon every commit.
* **Backend Testing:** Implemented comprehensive unit and integration tests for the Node.js APIs.
* **Frontend Testing:** Developed component-level and UI tests for the React frontend to ensure a seamless user experience.

## Deliverable 3: Software Quality & Security Analysis
The final phase focused on rigorous quality assurance and vulnerability mitigation:
* **Static Code Analysis & SAST:** Performed Static Application Security Testing and maintainability checks to identify code smells and vulnerabilities early.
* **Dynamic Analysis & DAST:** Executed Dynamic Application Security Testing to evaluate the application's runtime security posture.
* **Performance Testing:** Conducted load and spike testing to evaluate system reliability under heavy traffic.
* **Quality Assessment:** Evaluated the final software product against the **ISO 25010** software quality model (Maintainability, Security, Performance Efficiency, etc.).

## Technologies Used
* **Frontend:** React.js, JavaScript 
* **Backend:** Node.js, Express.js
* **DevOps & CI/CD:** Git, GitHub Actions
* **Testing:** Cypress
* **Static/Dynamic Analysis:** Cyclopt Companion

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/geotsad/Academic-Projects.git](https://github.com/geotsad/Academic-Projects.git)

2. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   npm install
   npm start

3. Open a new terminal, navigate to the frontend directory, and start the React app:
   ```bash
   cd frontend
   npm install
   npm start
