from flask import Flask, jsonify, send_from_directory, request

import os
import mysql.connector

from secure_communication import (
    run_bb84,
    run_mlkem,
    derive_hybrid_key,
    encrypt_message,
    decrypt_message
)

from bb84 import (
    generate_bits,
    generate_bases,
    encode_bits,
    measure_states,
    sift_key,
    calculate_qber
)

from attack import eve_intercept
from noise import apply_bit_flip_noise


app = Flask(__name__)


# ============================================================
# MYSQL DATABASE CONNECTION
# ============================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="qsc_database"
)

cursor = db.cursor()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "system": "Quantum-Safe Secure Communication System",
        "status": "running",
        "message": "Flask backend is working"
    })


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    frontend_folder = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "frontend"
    )

    return send_from_directory(
        frontend_folder,
        "index.html"
    )


# ============================================================
# SECURITY TEST API
# ============================================================

@app.route("/api/security-test")
def security_test():

    alice_key, bob_key, qber = run_bb84(
        number_of_bits=256
    )

    qber_threshold = 0.11

    if qber >= qber_threshold:

        return jsonify({
            "status": "REJECTED",
            "qber": round(qber * 100, 2),
            "message": "QBER is too high. Communication rejected."
        })

    pqc_secret = run_mlkem()

    hybrid_key = derive_hybrid_key(
        alice_key,
        pqc_secret
    )

    message = (
        "Hello Bob! "
        "This message is protected using "
        "BB84 and post-quantum cryptography."
    )

    encrypted_message = encrypt_message(
        message,
        hybrid_key
    )

    decrypted_message = decrypt_message(
        encrypted_message,
        hybrid_key
    )

    if message == decrypted_message:

        communication_status = "SECURE"

    else:

        communication_status = "NOT SECURE"


    return jsonify({

        "status": communication_status,

        "bb84": {

            "qubits": 256,

            "sifted_key_length":
                len(alice_key),

            "qber_percent":
                round(qber * 100, 2),

            "security_threshold_percent":
                11
        },

        "pqc": {

            "algorithm":
                "ML-KEM-768",

            "status":
                "SUCCESS",

            "shared_secret_length":
                len(pqc_secret)
        },

        "encryption": {

            "algorithm":
                "AES-GCM",

            "status":
                "SUCCESS"
        },

        "verification": {

            "original_message":
                message,

            "decrypted_message":
                decrypted_message,

            "message_match":
                message == decrypted_message
        }
    })


# ============================================================
# QUANTUM CHANNEL EXPERIMENT API
# ============================================================

@app.route("/api/experiment", methods=["GET"])
def experiment():

    try:

        # ----------------------------------------------------
        # GET VALUES FROM DASHBOARD
        # ----------------------------------------------------

        eve_rate = float(
            request.args.get(
                "eve",
                0
            )
        )

        noise_rate = float(
            request.args.get(
                "noise",
                0
            )
        )


        # ----------------------------------------------------
        # CONVERT PERCENTAGE TO DECIMAL
        # ----------------------------------------------------

        eve_rate = eve_rate / 100

        noise_rate = noise_rate / 100


        # ----------------------------------------------------
        # NUMBER OF QUBITS
        # ----------------------------------------------------

        number_of_bits = 256


        # ----------------------------------------------------
        # ALICE GENERATES RANDOM BITS
        # ----------------------------------------------------

        alice_bits = generate_bits(
            number_of_bits
        )


        # ----------------------------------------------------
        # ALICE GENERATES BASES
        # ----------------------------------------------------

        alice_bases = generate_bases(
            number_of_bits
        )


        # ----------------------------------------------------
        # ENCODE QUANTUM STATES
        # ----------------------------------------------------

        quantum_states = encode_bits(
            alice_bits,
            alice_bases
        )


        # ----------------------------------------------------
        # EVE ATTACK
        # ----------------------------------------------------

        eve_attack = eve_rate > 0

        quantum_states, intercepted_count = eve_intercept(
            quantum_states,
            eve_attack,
            eve_rate
        )


        # ----------------------------------------------------
        # CHANNEL NOISE
        # ----------------------------------------------------

        quantum_states, noise_errors = apply_bit_flip_noise(
            quantum_states,
            noise_rate
        )


        # ----------------------------------------------------
        # BOB GENERATES BASES
        # ----------------------------------------------------

        bob_bases = generate_bases(
            number_of_bits
        )


        # ----------------------------------------------------
        # BOB MEASURES STATES
        # ----------------------------------------------------

        bob_bits = measure_states(
            quantum_states,
            bob_bases
        )


        # ----------------------------------------------------
        # SIFT KEY
        # ----------------------------------------------------

        alice_key, bob_key = sift_key(
            alice_bits,
            alice_bases,
            bob_bits,
            bob_bases
        )


        # ----------------------------------------------------
        # CALCULATE QBER
        # ----------------------------------------------------

        qber = calculate_qber(
            alice_key,
            bob_key
        )


        # ----------------------------------------------------
        # SECURITY CHECK
        # ----------------------------------------------------

        if qber < 0.11:

            security_status = "SECURE"

        else:

            security_status = "REJECTED"


        # ----------------------------------------------------
        # SAVE RESULT TO MYSQL
        # ----------------------------------------------------

        insert_query = """
        INSERT INTO experiments
        (
            qubits,
            eve_rate,
            noise_rate,
            eve_intercepted,
            noise_errors,
            qber,
            key_length,
            security_status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """


        values = (

            number_of_bits,

            eve_rate * 100,

            noise_rate * 100,

            intercepted_count,

            noise_errors,

            qber * 100,

            len(alice_key),

            security_status

        )


        cursor.execute(
            insert_query,
            values
        )


        db.commit()


        # ----------------------------------------------------
        # RETURN RESULT TO DASHBOARD
        # ----------------------------------------------------

        return jsonify({

            "experiment": {

                "qubits":
                    number_of_bits,

                "eve_rate_percent":
                    round(
                        eve_rate * 100,
                        2
                    ),

                "noise_rate_percent":
                    round(
                        noise_rate * 100,
                        2
                    )
            },


            "results": {

                "qber_percent":
                    round(
                        qber * 100,
                        2
                    ),

                "key_length":
                    len(alice_key),

                "eve_intercepted":
                    intercepted_count,

                "noise_errors":
                    noise_errors
            },


            "security": {

                "threshold_percent":
                    11,

                "status":
                    security_status
            },


            "database": {

                "status":
                    "SAVED"

            }

        })


    except Exception as error:

        print("\nDATABASE / EXPERIMENT ERROR:")
        print(error)


        return jsonify({

            "status":
                "ERROR",

            "message":
                str(error)

        }), 500

# ============================================================
# GET SAVED EXPERIMENTS
# ============================================================

@app.route("/api/experiments", methods=["GET"])
def get_experiments():

    try:

        cursor.execute("""
            SELECT
                id,
                qubits,
                eve_rate,
                noise_rate,
                eve_intercepted,
                noise_errors,
                qber,
                key_length,
                security_status,
                created_at
            FROM experiments
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        experiments = []

        for row in rows:

            experiments.append({

                "id": row[0],

                "qubits": row[1],

                "eve_rate_percent": float(row[2]),

                "noise_rate_percent": float(row[3]),

                "eve_intercepted": row[4],

                "noise_errors": row[5],

                "qber_percent": float(row[6]),

                "key_length": row[7],

                "security_status": row[8],

                "created_at": str(row[9])

            })


        return jsonify({

            "status": "SUCCESS",

            "count": len(experiments),

            "experiments": experiments

        })


    except Exception as error:

        print("\nDATABASE READ ERROR:")
        print(error)

        return jsonify({

            "status": "ERROR",

            "message": str(error)

        }), 500
# ============================================================
# RUN FLASK SERVER
# ============================================================

if __name__ == "__main__":

    print("\n======================================")
    print(" QUANTUM-SAFE COMMUNICATION SERVER")
    print("======================================")


    print("\nStarting Flask server...")


    print("\nDashboard:")
    print(
        "http://127.0.0.1:5000/dashboard"
    )


    print("\nSecurity API:")
    print(
        "http://127.0.0.1:5000/api/security-test"
    )


    print("\nExperiment API:")
    print(
        "http://127.0.0.1:5000/api/experiment?eve=50&noise=5"
    )


    print("\nMySQL Database:")
    print(
        "qsc_database"
    )


    app.run(
        debug=True
    )