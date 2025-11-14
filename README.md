

DevSecOps Hands-On Lab – SAST & Security Gate

[GitHub Workflow Status](https://github.com/Expert632/SAST_TEST4)

## Overview

This repository demonstrates a **hands-on DevSecOps lab** designed to teach and 

showcase **Static Application Security Testing (SAST)** and **security gating** using 

**GitHub Actions** and **Python scripts**.

The lab simulates real-world DevSecOps practices, from **code validation** to **vulnerability 

detection** and **security enforcement**, providing a clear, reproducible workflow for 

educational purposes and professional portfolios.

---

## Lab Workflow Steps

1. Repository Creation

   * Initialize a new GitHub repository to host all lab files and workflows.

2. Validation

   * Ensure repository structure is correct and ready for code integration.

3. Safe Application

   * `safe_app.py`: Python file without vulnerabilities for baseline testing.

4. Vulnerable Application (Non-Critical)

   * `vulnerable_app.py`: Python file without critical vulnerabilities, used for testing syntax and 

basic SAST scans.

5. Pipeline 01 – Syntax Verification

   * Validates Python syntax on every commit or push.
   * Generates a **TXT report** with syntax check results.

6. Interpretation Script for Syntax

   * `interpret_report.py`: Parses the syntax report to highlight errors (if any).

7. Pipeline 02 – SAST Scan

   * Scans the Python code using **Semgrep** for potential vulnerabilities.
   * Generates **TXT and JSON reports**.
   * Initial scan shows **no critical vulnerabilities**.

8. Critical Vulnerability Testing

   * `vulnerable_critical.py`: Adds one **critical vulnerability** for testing SAST detection.

9. Interpretation Scripts for SAST Reports

   * `interpret_sast_report.py`: Interprets TXT and JSON reports.
   * `interpret_sast_txt_critical.py`: Specifically highlights critical vulnerabilities.

10. Pipeline 03 – Security Gate

    * Uses `security_gate.py` to enforce security rules.
    * If **at least one critical vulnerability** is detected, the pipeline fails (**Red**).
    * If no critical vulnerabilities are found, the pipeline passes (**Green**).

11. Final Result

    * Pipeline 03 displays **Red** due to the detected critical vulnerability, demonstrating 

**security enforcement** in CI/CD.

---

## Repository Structure

```
.github/
  workflows/
    pipeline-01-syntax.yml
    pipeline-02-sast.yml
    pipeline-03-security-gate.yml
scripts/
  interpret_report.py
  interpret_sast_report.py
  interpret_sast_txt_critical.py
  security_gate.py
src/
  safe_app.py
  vulnerable_app.py
  vulnerable_critical.py
sast-reports/
  semgrep-report.json
README.md
```

---

## Key Skills Demonstrated

-DevSecOps Practices: CI/CD integration with GitHub Actions pipelines.
-SAST Scanning: Detecting vulnerabilities in Python code using Semgrep.
-Report Interpretation: Parsing TXT and JSON reports for actionable insights.
-Security Gate Enforcement: Automatic pipeline fail when critical vulnerabilities exist.
-Hands-On Automation: Python scripting to automate detection and reporting.

---

## Getting Started

1. Clone the Repository

```bash
git clone https://github.com/YourUsername/DevSecOps-SAST-Lab.git
cd DevSecOps-SAST-Lab
```

2. Run Python Scripts for Report Interpretation

```bash
python scripts/interpret_sast_report.py
python scripts/interpret_sast_txt_critical.py
```

3. Observe Pipelines

Pipeline 01:** Syntax verification
Pipeline 02:** SAST scanning (detects critical and non-critical vulnerabilities)
Pipeline 03:** Security gate enforcement

4. Check Reports

* Reports are stored in `sast-reports/` as **TXT** and **JSON** for review.

---

## Which demonstrates this practical lab 

* Demonstrates **real DevSecOps workflow** in a hands-on environment.
* Shows ability to **detect, interpret, and enforce security policies** automatically.
* Provides **reproducible and clear examples** for education or portfolio purposes.
* Highlights **automation skills using Python and GitHub Actions**, key for modern 

DevSecOps roles.

---

## Technologies Used

-GitHub Actions** – CI/CD pipelines
-Python 3** – Scripting and report interpretation
-Semgrep** – SAST scanning
-JSON & TXT Reports** – Automated reporting of vulnerabilities

---

## Author

MACHANE  Salim – DevSecOps Enthusiast

 LinkedIn: https://www.linkedin.com/in/salim-machane-b8640a1a7/
 GitHub: https://github.com/Expert632

---

## Hashtags for Visibility

```
#DevSecOps #SAST #GitHubActions #CyberSecurity #Python #Automation #CI_CD 

#PortfolioProject
```

