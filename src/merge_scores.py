#----------------------------------------------------------------------
# Merge the scores from the different models into a single file
# This is a simple script that reads the scores from the different models and merges them into a single file.
# The scores are stored in the outputs folder and are named test_generations_{model_name}.csv
# The final results file is saved as outputs/final_results.csv
#_----------------------------------------------------------------------

import pandas as pd

df = pd.read_csv("outputs/test_generations_detoxify.csv")
df.to_csv("outputs/final_results.csv", index=False)

print("Saved final results file")