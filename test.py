import logging


def is_stable(data, tolerance=0.8):
    total_values = len(data)
    unchanged_count = sum(1 for i in range(1, total_values) if data[i] == data[i-1])

    # Tỷ lệ các giá trị không thay đổi
    unchanged_ratio = unchanged_count / (total_values - 1)

    # Kiểm tra nếu tỷ lệ không thay đổi cao hơn ngưỡng
    return unchanged_ratio >= tolerance

# Ví dụ sử dụng
data_volatile = [97.03058, 97.62004, 99.50334, 102.3161, 104.89, 104.0297, 96.77159, 86.77371, 85.47666, 92.62504, 96.50419, 96.90294, 99.67976, 103.5329, 104.9066, 103.5201]
data_non_volatile = [-180, -180, -180, -180, -180, -180, -180, -180, -180, -117.589, -151.223, -180, -180, -180, -180, -180]

logging.info(is_stable(data_volatile))  # Kết quả: False (không ổn định)
logging.info(is_stable(data_non_volatile))  # Kết quả: True (ổn định)
