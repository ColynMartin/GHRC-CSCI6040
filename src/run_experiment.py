import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

print("\nStarting experiment pipeline...\n")

config_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("configs", "base.yaml")

# Step 1: Run text generation
print("Step 1: Running generation script...")
subprocess.run([sys.executable, "src/run_generation.py", config_path], check=True)

# Step 2: Run Detoxify scoring
print("\nStep 2: Running Detoxify scoring...")
subprocess.run([sys.executable, "src/score_detoxify.py"], check=True)

print("\nPipeline complete.")
print("Check the outputs folder for results.")