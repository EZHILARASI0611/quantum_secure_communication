# Quantum-Safe Secure Communication System Using BB84 and Post-Quantum Cryptography

## 📌 Project Overview

The **Quantum-Safe Secure Communication System** is a final-year project that demonstrates how quantum key distribution and post-quantum cryptography can be combined to improve secure communication.

The project combines:

* **BB84 Quantum Key Distribution (QKD)**
* **Eavesdropping detection using QBER**
* **Channel noise simulation**
* **Qiskit-based BB84 quantum circuit demonstration**
* **ML-KEM-768 Post-Quantum Cryptography**
* **AES-GCM encryption**
* **Hybrid key derivation**
* **Flask web backend**
* **Interactive web dashboard**
* **MySQL experiment database**
* **Experiment history and result analysis**

The system is implemented as a working software prototype and is designed for educational and experimental purposes.

---

## 🎯 Objectives

The main objectives of this project are:

1. To implement the BB84 quantum key distribution protocol.
2. To simulate eavesdropping using an intercept-resend attack.
3. To simulate noise in the communication channel.
4. To calculate the Quantum Bit Error Rate (QBER).
5. To determine whether a generated key should be accepted or rejected.
6. To demonstrate BB84 using Qiskit quantum circuits.
7. To implement ML-KEM-768 for post-quantum key exchange.
8. To use AES-GCM for secure message encryption.
9. To combine BB84 and post-quantum cryptography into a hybrid security approach.
10. To provide a web dashboard for security experiments.
11. To store experiment results using MySQL.

---

## 🏗️ System Architecture

```text
                 ┌───────────────┐
                 │     Alice     │
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │ BB84 Key        │
                │ Generation      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Eve Attack      │
                │ Simulation      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Channel Noise   │
                │ Simulation      │
                └────────┬────────┘
                         │
                         ▼
                 ┌──────────────┐
                 │     Bob      │
                 └──────┬───────┘
                        │
                        ▼
                ┌─────────────────┐
                │ QBER Calculation│
                └────────┬────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ QBER < 11%? │
                  └──────┬──────┘
                         │
                ┌────────┴────────┐
                │                 │
              YES                NO
                │                 │
                ▼                 ▼
           ┌─────────┐       ┌─────────┐
           │ ACCEPT  │       │ REJECT  │
           └────┬────┘       └─────────┘
                │
                ▼
        ┌──────────────────┐
        │ ML-KEM-768       │
        │ Key Exchange     │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Hybrid Key       │
        │ Derivation       │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ AES-GCM          │
        │ Encryption       │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Secure Message   │
        └──────────────────┘

                 │
                 ▼
        ┌──────────────────┐
        │ Flask Dashboard  │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ MySQL Database   │
        └──────────────────┘
```

---

## 🔐 How the System Works

### 1. BB84 Key Generation

Alice generates random bits and randomly selects quantum bases.

The bits are encoded into BB84 states:

* `|0⟩`
* `|1⟩`
* `|+⟩`
* `|-⟩`

Bob independently selects measurement bases.

After measurement, Alice and Bob compare their bases and keep only the matching positions. This produces the **sifted key**.

---

### 2. Eve Attack Simulation

The system can simulate an eavesdropper called **Eve**.

Eve uses an intercept-resend attack:

```text
Alice → Eve → Bob
```

Eve intercepts selected quantum states, measures them, and sends replacement states to Bob.

This can introduce errors into the key.

---

### 3. Channel Noise

The system also simulates communication-channel noise.

Noise can change the transmitted quantum state and introduce errors even when Eve is not present.

---

### 4. QBER Calculation

The **Quantum Bit Error Rate (QBER)** is calculated by comparing Alice's and Bob's sifted keys.

```text
QBER = Number of mismatched bits
       ─────────────────────────────
          Total sifted bits
```

The project uses an **11% security threshold** for the prototype.

```text
QBER < 11%  → ACCEPTED / SECURE

QBER ≥ 11%  → REJECTED
```

---

### 5. Post-Quantum Cryptography

The project uses **ML-KEM-768** as the post-quantum key exchange component.

ML-KEM is used to demonstrate protection against future attacks from sufficiently capable quantum computers.

---

### 6. Hybrid Key

The BB84-derived key material and ML-KEM shared secret are combined using a cryptographic key derivation process.

The resulting key is used for symmetric encryption.

---

### 7. AES-GCM Encryption

The project uses **AES-GCM** for authenticated encryption.

It provides:

* Confidentiality
* Integrity
* Authentication

The system encrypts a message and then decrypts it to verify that the original message is recovered correctly.

---

## 🌐 Web Dashboard

The Flask web application provides an interactive dashboard for running security experiments.

The dashboard supports:

* Security testing
* Eve interception control
* Channel noise control
* QBER visualization
* Security status
* Final key length
* Eve interception statistics
* Noise statistics
* Saved experiment history

---

## 🗄️ MySQL Database

Experiment results are stored in a MySQL database.

The `experiments` table stores information such as:

| Field           | Description                  |
| --------------- | ---------------------------- |
| ID              | Experiment identifier        |
| Qubits          | Number of simulated qubits   |
| Eve Rate        | Eve interception percentage  |
| Noise Rate      | Channel noise percentage     |
| Eve Intercepted | Number of intercepted states |
| Noise Errors    | Number of noise errors       |
| QBER            | Quantum Bit Error Rate       |
| Key Length      | Final sifted key length      |
| Security Status | SECURE or REJECTED           |
| Created At      | Experiment timestamp         |

---

## 📊 Sample Experimental Results

Example results from the project:

|  Eve | Noise |   QBER | Status   |
| ---: | ----: | -----: | -------- |
|   0% |    0% |     0% | SECURE   |
|  25% |    0% |  4.84% | SECURE   |
|  50% |    0% | 10.48% | SECURE   |
|  75% |    0% | 17.29% | REJECTED |
| 100% |    0% | 27.20% | REJECTED |
|   0% |   20% | 21.43% | REJECTED |

These results illustrate that increasing eavesdropping or channel noise can increase QBER, and the prototype rejects keys when QBER reaches or exceeds the configured 11% threshold.

Because the simulation uses random values, individual experimental results may vary between runs.

---

## 🧪 Technologies Used

### Programming

* Python

### Quantum Computing

* Qiskit
* Qiskit Aer

### Post-Quantum Cryptography

* ML-KEM-768
* liboqs

### Encryption

* AES-GCM
* SHA-256 based key derivation

### Backend

* Flask

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Database

* MySQL

### Data Analysis

* NumPy
* Pandas
* Matplotlib

---

## 📁 Project Structure

```text
quantum_secure_communication/
│
├── backend/
│   ├── app.py
│   ├── bb84.py
│   ├── attack.py
│   ├── noise.py
│   ├── experiments.py
│   ├── graphs.py
│   ├── qiskit_bb84.py
│   ├── pqc.py
│   ├── encryption.py
│   ├── secure_communication.py
│   └── test_secure_communication.py
│
├── frontend/
│   └── index.html
│
├── results.csv
├── qber_vs_eve.png
├── qber_vs_noise.png
├── key_length_vs_eve.png
├── execution_time.png
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project

```bash
cd quantum_secure_communication
```

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Create the database:

```sql
CREATE DATABASE qsc_database;
```

Create the experiments table:

```sql
CREATE TABLE experiments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    qubits INT NOT NULL,
    eve_rate DECIMAL(5,2) NOT NULL,
    noise_rate DECIMAL(5,2) NOT NULL,
    eve_intercepted INT NOT NULL,
    noise_errors INT NOT NULL,
    qber DECIMAL(6,2) NOT NULL,
    key_length INT NOT NULL,
    security_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Configure the MySQL password

The Flask application reads the MySQL password from the environment variable:

```text
MYSQL_PASSWORD
```

Windows PowerShell example:

```powershell
$env:MYSQL_PASSWORD="YOUR_MYSQL_PASSWORD"
```

Do not commit your actual password to GitHub.

### 6. Start the Flask application

```powershell
python backend\app.py
```

Open the dashboard:

```text
http://127.0.0.1:5000/dashboard
```

---

## 🧪 Running Individual Components

### BB84 simulation

```powershell
python backend\bb84.py
```

### Qiskit BB84 demonstration

```powershell
python backend\qiskit_bb84.py
```

### PQC test

```powershell
python backend\pqc.py
```

### Encryption test

```powershell
python backend\encryption.py
```

### Hybrid secure communication

```powershell
python backend\secure_communication.py
```

### Reproducibility tests

```powershell
python backend\test_secure_communication.py
```

---

## ⚠️ Project Scope

This project is a **software prototype and educational demonstration** of quantum-safe secure communication.

The BB84 communication used by the web application is simulated in software. The project also includes a separate Qiskit-based BB84 quantum-circuit demonstration.

It does not represent communication over a physical quantum network or real quantum hardware.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Integration with real quantum hardware
* Real-time quantum network communication
* Advanced QBER analysis
* More post-quantum algorithms
* User authentication
* Role-based dashboard access
* Secure cloud deployment
* Enhanced database analytics
* Automated security reports
* Hardware-based quantum key distribution

---

## 👩‍💻 Project Purpose

This project demonstrates the integration of **quantum key distribution, post-quantum cryptography, and classical authenticated encryption** in a single experimental security system.

It is intended for academic learning, experimentation, and demonstration of quantum-safe communication concepts.
