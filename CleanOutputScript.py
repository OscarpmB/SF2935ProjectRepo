import re
import csv
# -------------------------------------------
# Code from chatgpt that reads the output.txt 
# file generated from `ModelSelection.ipynb`
# and converts interesting values to a csv 
# file. 
# Regex is used to extract the necessary parts
# this strings are then written to the csv 
# that can be opened in google sheets to enble
# a more digestable overview of the results
#
# GridsearchCV from sklearn could have been used instead,
# That have made the grid search much easier to conduct.
# However, `keras.wrapper` module could not be loaded,
# And thus we chose to implement it ourselves.
# -------------------------------------------

# Input and output file paths
input_file = 'output.txt'  # Replace with your input file path
output_csv = 'output_results.csv'

# Initialize lists to store extracted data
results = []

# Regex patterns to match epochs, batch size, learning rate, mean accuracy, and variance
pattern_params = re.compile(r"epochs:\s*(\d+),\s*batch_size:\s*(\d+),\s*learning_rate:\s*([\d.]+)")
pattern_mean_accuracy = re.compile(r"mean accuracy over kfold:\s*([\d.]+)")
pattern_variance = re.compile(r"Variance\s+over kfold:\s*([\d.]+)")

# Read the file and parse content
with open(input_file, 'r') as file:
    content = file.read()
    
    # Split content by each block of hyperparameters (use dashed lines as delimiter)
    blocks = content.split('--------------------------')
    
    # Iterate through each block to extract parameters and metrics
    for block in blocks:
        params_match = pattern_params.search(block)
        mean_accuracy_match = pattern_mean_accuracy.search(block)
        variance_match = pattern_variance.search(block)
        
        # Check if all required matches are found
        if params_match and mean_accuracy_match and variance_match:
            # Extract values
            epochs = int(params_match.group(1))
            batch_size = int(params_match.group(2))
            learning_rate = float(params_match.group(3))
            mean_accuracy = float(mean_accuracy_match.group(1))
            variance = float(variance_match.group(1))
            
            # Append results as a tuple
            results.append((epochs, batch_size, learning_rate, mean_accuracy, variance))

# Write results to a CSV file
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["epochs", "batch_size", "learning_rate", "mean_accuracy", "variance"])
    # Write each row of results
    writer.writerows(results)

print("Extraction and CSV writing complete.")
