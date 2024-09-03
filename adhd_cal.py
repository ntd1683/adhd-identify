import logging
import os
import csv
from collections import defaultdict


def is_stable(data, tolerance=0.8):
    """Kiểm tra xem một dãy số có ổn định không dựa trên tỷ lệ các giá trị không thay đổi."""
    unchanged_count = sum(1 for i in range(1, len(data)) if data[i] == data[i - 1])
    unchanged_ratio = unchanged_count / (len(data) - 1)
    return unchanged_ratio >= tolerance


def csv_min_max_cal(filename='angles.csv', columns_of_interest=None):
    """Tính toán giá trị min và max cho các cột quan tâm trong file CSV."""
    if columns_of_interest is None:
        columns_of_interest = ['Right knee', 'Left knee', 'Right hip', 'Left hip',
                               'Right shank', 'Left shank', 'Right thigh', 'Left thigh']

    data = defaultdict(list)
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for _ in range(2):  # Bỏ qua hai dòng đầu tiên (metadata)
            next(csv_reader)
        headers = next(csv_reader)  # Tên cột từ dòng thứ 3
        col_indices = {col: headers.index(col) for col in columns_of_interest if col in headers}
        next(csv_reader)  # Bỏ qua dòng thứ 4

        for row in csv_reader:
            for col, index in col_indices.items():
                try:
                    value = float(row[index])
                    data[col].append(value)
                except (ValueError, IndexError):
                    continue  # Bỏ qua các giá trị không hợp lệ

    results = {}
    stable_columns_count = 0
    for col in columns_of_interest:
        if data[col]:
            if is_stable(data[col]):
                stable_columns_count += 1
            else:
                results[col] = {'min': min(data[col]), 'max': max(data[col])}

    return -1 if stable_columns_count >= 2 else results


def adhd_cal(filename='angles.csv', threshold=10):
    """Kiểm tra xem có dấu hiệu của ADHD dựa trên sự chênh lệch giữa giá trị min và max."""
    if not os.path.exists(filename):
        logging.warning(f" File {filename} not found.")
        return False

    results = csv_min_max_cal(filename)
    if results == -1:
        logging.warning(" Data no changes, this data is not for human consumption, please review the data.")
        return False

    detection_count = sum(1 for col, values in results.items() if values['max'] - values['min'] > threshold)
    return detection_count >= 3
