#!/usr/bin/env python3

import csv
import os
from collections import Counter

RAW_DATA_DIR = 'data/raw'

def discover_columns():
    detected_columns = []
    with os.scandir(RAW_DATA_DIR) as dir:
        for file in dir:
            if file.name.endswith('.csv'):
                # print(file.path)
                with open(file.path, mode='rb') as f:
                    csv_header = f.readline().strip()
                    csv_header = csv_header.decode('utf-8')
                    dialect = csv.Sniffer().sniff(csv_header, delimiters=[",",";","\t","|"])
                    # print("Detected delimiter:", dialect.delimiter)
                    csv_header_split = csv_header.split(dialect.delimiter)
                    detected_columns.extend(csv_header_split)
    return detected_columns 

def main():
    columns = discover_columns()
    for col, count in Counter(columns).items():
        print(f'{col}: {count}')

if __name__ == '__main__':
    main()