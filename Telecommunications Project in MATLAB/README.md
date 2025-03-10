# Constellation Design for Simultaneous Wireless Information and Power Transfer (SWIPT)

---

This is a project that was created by me for the course **Communication Systems II** in the 6th semester of my studies. This project is about Simultaneous Wireless Information and Power Transfer. We were given the 2 papers that I have uploaded and the assignments were:

- Fig. 2 in [R1] represents the PAPR behavior versus 𝑑𝑚𝑖𝑛 of 16-Circular QAM compared with known modulation schemes, namely 16-PAM, 16-PSK, and 16-QAM. Provide theoretical analysis about PAPR versus 𝑑𝑚𝑖𝑛 for all the above constellations and verify the results in Fig. 2 through simulation.
- Fig. 3 in [R1] illustrates SEP versus normalized harvested energy of the modulation schemes for fixed SNR. Furthermore, Fig. 4 in [R1] illustrates SEP versus SNR for fixed normalized energy harvesting. Verify these results through both theoretical analysis and simulation results. Include in your analysis, one of the state-of-the-art constellation schemes for SWIPT presented in [R2].

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Installation](#installation)
- [Methodology](#methodology)
- [Simulation Results](#simulation-results)
- [References](#references)
- [Future Work](#future-work)
- [Contact](#contact)

---

## Project Overview
This project focuses on **Simultaneous Wireless Information and Power Transfer (SWIPT)** and investigates the performance of **16-Circular QAM (16-CQAM)** compared to conventional modulation schemes such as **16-PAM, 16-PSK, and 16-QAM**. 

The project is based on two research papers:
- **[R1]** provides theoretical and simulation results regarding the Peak-to-Average Power Ratio (PAPR) and Symbol Error Probability (SEP) of different modulation schemes.
- **[R2]** presents state-of-the-art constellation schemes for SWIPT.

Our goal is to analyze, verify, and simulate key results from these papers.

---

## Objectives
1. **Analyze and verify** the **PAPR vs. minimum Euclidean distance** (𝑑𝑚𝑖𝑛) for 16-CQAM and compare it with:
   - 16-PAM
   - 16-PSK
   - 16-QAM

2. **Reproduce and validate** the results from **Fig. 2 in [R1]** using MATLAB simulations.

3. **Analyze and simulate** the **Symbol Error Probability (SEP)**:
   - **Fig. 4 in [R1]**: SEP vs. SNR for fixed normalized harvested energy.

4. **Extend the analysis** by incorporating one of the **constellation schemes from [R2]** into our comparisons.

---

## Installation
### Prerequisites:
Ensure you have **MATLAB** installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/geotsad/SWIPT-Constellation-Design.git
   cd SWIPT-Constellation-Design
2. **Open MATLAB** and navigate to the project directory.
3. Run the simulation files:
   - ''plot_CQAM_N4.mlx'' → Simulates 16-CQAM with N=4.
   - plot_CQAM_N8.mlx → Simulates 16-CQAM with N=8.
   - telecommunications.mlx → Main file for running SWIPT simulations.
