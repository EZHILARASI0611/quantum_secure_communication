import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------------------
# LOAD RESULTS
# -----------------------------------------

data = pd.read_csv("results.csv")

print("\n======================================")
print("       QUANTUM SECURITY GRAPHS")
print("======================================")

print("\nResults loaded successfully!")
print("\nNumber of experiments:", len(data))


# -----------------------------------------
# GRAPH 1: QBER VS EVE
# -----------------------------------------

plt.figure(figsize=(8, 5))

for noise in sorted(data["Noise_Rate_Percent"].unique()):

    subset = data[data["Noise_Rate_Percent"] == noise]

    plt.plot(
        subset["Eve_Rate_Percent"],
        subset["QBER_Percent"],
        marker="o",
        label=f"Noise {noise:.0f}%"
    )

plt.xlabel("Eve Interception Rate (%)")
plt.ylabel("QBER (%)")
plt.title("QBER vs Eve Interception Rate")
plt.legend()
plt.grid(True)

plt.savefig("qber_vs_eve.png", dpi=300, bbox_inches="tight")

plt.close()

print("\nCreated: qber_vs_eve.png")


# -----------------------------------------
# GRAPH 2: QBER VS NOISE
# -----------------------------------------

plt.figure(figsize=(8, 5))

for eve in sorted(data["Eve_Rate_Percent"].unique()):

    subset = data[data["Eve_Rate_Percent"] == eve]

    plt.plot(
        subset["Noise_Rate_Percent"],
        subset["QBER_Percent"],
        marker="o",
        label=f"Eve {eve:.0f}%"
    )

plt.xlabel("Channel Noise (%)")
plt.ylabel("QBER (%)")
plt.title("QBER vs Channel Noise")
plt.legend()
plt.grid(True)

plt.savefig("qber_vs_noise.png", dpi=300, bbox_inches="tight")

plt.close()

print("Created: qber_vs_noise.png")


# -----------------------------------------
# GRAPH 3: KEY LENGTH VS EVE
# -----------------------------------------

plt.figure(figsize=(8, 5))

for noise in sorted(data["Noise_Rate_Percent"].unique()):

    subset = data[data["Noise_Rate_Percent"] == noise]

    plt.plot(
        subset["Eve_Rate_Percent"],
        subset["Key_Length"],
        marker="o",
        label=f"Noise {noise:.0f}%"
    )

plt.xlabel("Eve Interception Rate (%)")
plt.ylabel("Final Key Length")
plt.title("Final Key Length vs Eve Interception")
plt.legend()
plt.grid(True)

plt.savefig(
    "key_length_vs_eve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: key_length_vs_eve.png")


# -----------------------------------------
# GRAPH 4: EXECUTION TIME
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    range(1, len(data) + 1),
    data["Execution_Time"],
    marker="o"
)

plt.xlabel("Experiment Number")
plt.ylabel("Execution Time (seconds)")
plt.title("Experiment Execution Time")
plt.grid(True)

plt.savefig(
    "execution_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Created: execution_time.png")


# -----------------------------------------
# FINISHED
# -----------------------------------------

print("\n======================================")
print("       ALL GRAPHS CREATED")
print("======================================")

print("\nYour graph files are:")

print("1. qber_vs_eve.png")
print("2. qber_vs_noise.png")
print("3. key_length_vs_eve.png")
print("4. execution_time.png")

print("\nDone!")