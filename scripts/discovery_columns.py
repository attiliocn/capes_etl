#!/usr/bin/env python3

import csv
import os
import yaml

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
                    csv_header_split = csv_header.split(dialect.delimiter)
                    detected_columns.extend(csv_header_split)
    return detected_columns 

def main():
    columns = discover_columns()
    unique_columns = list(set(columns))
    default_mapping = {col:col for col in unique_columns}
    print(default_mapping)

    print(os.getcwd())

    with open('config/default_mapping.yaml', mode='w') as f:
        yaml.dump(default_mapping, f)

if __name__ == '__main__':
    main()