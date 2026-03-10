import subprocess
import sys

print("\nStarting experiment pipeline...\n")

# Step 1: Run text generation
print("Step 1: Running generation script...")
subprocess.run([sys.executable, "src/run_generation.py"], check=True)

# Step 2: Run Detoxify scoring
print("\nStep 2: Running Detoxify scoring...")
subprocess.run([sys.executable, "src/score_detoxify.py"], check=True)

print("\nPipeline complete.")
print("Check the outputs folder for results.")