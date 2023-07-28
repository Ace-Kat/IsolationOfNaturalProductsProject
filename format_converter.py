import csv
import pandas as pd
from openpyxl import Workbook


def read_csv_long_form(file_path):
    long_form_platemap = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            long_form_platemap.append(row)
    return long_form_platemap


def write_csv_long_form(file_path, long_form_platemap):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(long_form_platemap)


def long_to_square(long_form_platemap):
    square_form_platemap = list(map(list, zip(*long_form_platemap)))
    return square_form_platemap


def square_to_long(square_form_platemap):
    long_form_platemap = list(map(list, zip(*square_form_platemap)))
    return long_form_platemap


def convert_96_to_384(square_form_96well):
    # Assuming square_form_96well is a 12x8 list representing a 96-well platemap
    square_form_384well = []
    for row_idx in range(0, 12, 3):
        for col_idx in range(0, 8, 2):
            quadrant = [row[col_idx:col_idx + 2] for row in square_form_96well[row_idx:row_idx + 3]]
            square_form_384well.append(quadrant)
    return square_form_384well


def convert_384_to_96(square_form_384well, quadrant=1):
    # Assuming square_form_384well is a 16x24 list representing a 384-well platemap
    if quadrant not in [1, 2, 3, 4]:
        raise ValueError("Invalid quadrant. Quadrant must be 1, 2, 3, or 4.")

    row_start = (quadrant - 1) // 2 * 6
    col_start = (quadrant - 1) % 2 * 12
    square_form_96well = [row[col_start:col_start + 12] for row in square_form_384well[row_start:row_start + 6]]
    return square_form_96well


# Assuming you have a CSV file with the long-form platemap data
file_path = '/Users/venkatasivaramisetty/PycharmProjects/IsolationOfNaturalProductsProject/20230524_TargetMol27+HF014_consolidatedTransferMap.csv'
long_form_platemap = read_csv_long_form(file_path)

# Convert long-form to square-form
square_form_platemap = long_to_square(long_form_platemap)

# Convert square-form to 96-well and 384-well
square_form_96well = square_form_platemap
square_form_384well = convert_96_to_384(square_form_96well)
square_form_96well_from_384 = convert_384_to_96(square_form_384well, quadrant=1)

# Writing the outputs to CSV files
write_csv_long_form('long_form_platemap.csv', long_form_platemap)

df_square = pd.DataFrame(square_form_platemap)
df_square.to_csv('square_form_platemap.csv', index=False, header=False)

df_96well = pd.DataFrame(square_form_96well)
df_96well.to_csv('96_well_platemap.csv', index=False, header=False)

df_384well = pd.DataFrame(square_form_384well)
df_384well.to_csv('384_well_platemap.csv', index=False, header=False)

df_96well_from_384 = pd.DataFrame(square_form_96well_from_384)
df_96well_from_384.to_csv('96_well_platemap_from_384.csv', index=False, header=False)
