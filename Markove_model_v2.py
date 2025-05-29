import pandas as pd
from collections import defaultdict
from combinations import getCombinations
from Matrix import Matrix
from indices import getIndices

# Global dictionaries
sections_dict = defaultdict(int)
failure_rate = {}
repair_rate = {}
delay_time = defaultdict(float)
output1, output2, output3 = {}, {}, {}

# Read and extract relevant data from the CSV using pandas
def read_csv_data(filename):
    df = pd.read_csv(f"{filename}.csv", header=None)
    return df.iloc[1:, 3:7]  # Skip header row and select columns 3-6

# Update section occurrence count
def get_section_data(df):
    for section in df.iloc[:, 0]:
        sections_dict[section] += 1
    return validate_sections(sections_dict, id=1)

# Extract delay times per section
def compute_delay_times(df):
    for section, delay in zip(df.iloc[:, 0], df.iloc[:, 2]):
        delay_time[section] += float(delay)
    return delay_time

# Compute failure rate per section
def compute_failure_rates(years):
    for name, count in sections_dict.items():
        failure_rate[name] = count / years
    return validate_sections(failure_rate, id=2)

# Compute repair rate per section
def compute_repair_rates():
    for section, delay in delay_time.items():
        repair_rate[section] = round((8760 * sections_dict[section]) / delay, 3)
    return validate_sections(repair_rate, id=3)

# Ensure all section combinations are present in the data
def validate_sections(source_dict, id):
    combos = getCombinations(num_sections)
    for combo in combos:
        source_dict.setdefault(combo, 0)

        if id == 1:
            output1[combo] = source_dict[combo]
        elif id == 2:
            output2[combo] = source_dict[combo]
        elif id == 3:
            output3[combo] = source_dict[combo]

# Flatten result matrix to list of probabilities
def extract_probabilities(result_matrix):
    return [row[0] for row in result_matrix]

# === Main execution block ===
if __name__ == '__main__':
    filename = input("Enter the filename without extension: ").strip()
    years = int(input("Enter number of years: "))
    num_sections = int(input("Enter number of sections of the feeder: "))

    csv_df = read_csv_data(filename)

    get_section_data(csv_df)
    compute_delay_times(csv_df)
    compute_failure_rates(years)
    compute_repair_rates()

    print("\nSections:", output1)
    print("Failure Rates:", output2)
    print("Repair Rates:", output3)

    f_rates = list(output2.values())
    r_rates = list(output3.values())

    matrix_model = Matrix(f_rates, r_rates, num_sections)

    print("\nTransition Matrix:")
    for row in matrix_model.create_matrix():
        print(row)

    probabilities = extract_probabilities(matrix_model.matrix_calling())
    print("\nProbabilities:", probabilities)

    print("\nIndices:")
    print(getIndices(probabilities, output2, output3, num_sections))
