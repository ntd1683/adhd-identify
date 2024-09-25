import logging
import math
import os
import csv
from collections import defaultdict

from openvino.runtime.opset13 import result


def is_stable(data, tolerance=0.8):
    """Kiểm tra xem một dãy số có ổn định không dựa trên tỷ lệ các giá trị không thay đổi."""
    unchanged_count = sum(1 for i in range(1, len(data)) if data[i] == data[i - 1])
    unchanged_ratio = unchanged_count / (len(data) - 1)
    return unchanged_ratio >= tolerance


def csv_min_max_cal(filename='angles.csv', threshold=10, columns_of_interest=None):
    """Tính toán giá trị min và max cho các cột quan tâm trong file CSV."""
    if columns_of_interest is None:
        # add time column
        # columns_of_interest = ['time', 'right knee', 'left knee', 'right hip', 'left hip',
        #                        'right shank', 'left shank', 'right thigh', 'left thigh']
        columns_of_interest = ['right knee', 'left knee', 'right hip', 'left hip',
                               'right shank', 'left shank', 'right thigh', 'left thigh']

    data = defaultdict(list)
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for _ in range(10):  # Bỏ qua 10 dòng đầu tiên (metadata)
            next(csv_reader)
        headers = next(csv_reader)  # Tên cột từ dòng thứ 11
        headers_list = headers[0].split('\t')
        col_indices = {col: headers_list.index(col) for col in columns_of_interest if col in headers_list}
        print("Col indices: ", col_indices)

        count_time = 0
        for row in csv_reader:
            for col, index in col_indices.items():
                try:
                    row_data = row[0].split('\t')
                    value = float(row_data[index])
                    data[col].append(value)
                    count_time = count_time + 1
                except (ValueError, IndexError):
                    continue  # Bỏ qua các giá trị không hợp lệ

    results = {}
    stable_columns_count = 0
    count_part = {}
    print("Count time: ", count_time)
    print("Columns of interest: ", data['time'])
    for col in columns_of_interest:
        if data[col]:
            if is_stable(data[col]):
                stable_columns_count += 1
            else:
                results[col] = {'min': min(data[col]), 'max': max(data[col])}
                print("Column: ", col, "Length : ", len(data[col]))
                num_parts = 10
                part_size = math.ceil(len(data[col]) / num_parts)
                for part_num in range(num_parts):
                    # Tính chỉ số bắt đầu và kết thúc của từng phần
                    start_index = part_num * part_size
                    end_index = min(start_index + part_size, len(data[col]))
                    chunk = data[col][start_index:end_index]

                    if len(chunk) > 0:
                        results[f"{col}_part_{part_num + 1}"] = {'min': min(chunk), 'max': max(chunk)}

                        if max(chunk) - min(chunk) > threshold:
                            count_part[f"{col}"] = count_part.get(f"{col}", 0) + 1

    print("Results : ", results)
    print("Count part: ", count_part)
    result_count = 0
    for col in count_part:
        if count_part[col] >= 7:
            result_count = result_count + 1

    return -1 if stable_columns_count >= 4 else result_count


def adhd_cal(filename='angles.csv', count=5, threshold=10):
    """Kiểm tra xem có dấu hiệu của ADHD dựa trên sự chênh lệch giữa giá trị min và max."""
    if not os.path.exists(filename):
        logging.warning(f" File {filename} not found.")
        return False

    result_count = csv_min_max_cal(filename, threshold)
    if result_count == -1:
        logging.warning(" Data no changes, this data is not for human consumption, please review the data.")
        return False

    return result_count >= count
