import subprocess
import pandas as pd
import os

# Define the values for T
T_values = [10, 100, 500, 1000, 2000, 2500]

# Initialize a list to hold the results
results = []

# Directory to store output files (optional)
output_dir = "output_files"
os.makedirs(output_dir, exist_ok=True)

# Run the simulation for each T value and collect the results
for T in T_values:
    total_wait_time = 0
    total_service_time = 0
    total_runs = 10
    
    for i in range(total_runs):  # Run each T value 10 times
        command = f"python main.py {T} 1 1 9 5 12"
        try:
            # Execute the command and capture the output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            
            # Parse the output assuming it is in the format "accepted rejected curr_time avg_wait_time avg_service_time"
            parts = output.split()
            if len(parts) == 5:
                accepted, rejected, curr_time, avg_wait_time, avg_service_time = parts
                avg_wait_time = float(avg_wait_time)
                total_wait_time += avg_wait_time
                avg_service_time = float(avg_service_time)
                total_service_time += avg_service_time
            else:
                print(f"Unexpected output format: {output}")
        
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e.output}")
            avg_wait_time = 0
        
    # Calculate average wait time for this T
    if total_runs > 0:
        average_wait_time = total_wait_time / total_runs
        average_service_time = total_service_time / total_runs
    else:
        average_wait_time = 0
        average_service_time = 0
    
    # Store the result in the list
    results.append({
        "T": T,
        "Average Wait Time": average_wait_time + average_service_time,
        "Wait Time": total_wait_time + total_service_time
    })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
excel_file = "average_wait_times.xlsx"
df.to_excel(excel_file, index=False)

print(f"Results have been saved to {excel_file}")
