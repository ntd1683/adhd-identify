import os
import adhd_cal
import logging
from Sports2D import Sports2D

logging.basicConfig(format='%(message)s', level=logging.WARNING)


def main_menu():
    while True:
        print("\nMenu:")
        print("1. Phân tích video từ file TOML")
        print("2. Phân tích file CSV ADHD")
        print("3. Kết thúc")

        choice = input("Chọn một tùy chọn (1-3): ")

        if choice == '1':
            name_file_toml = input("Nhập tên file TOML: ")

            if not name_file_toml.endswith('.toml'):
                logging.warning(f"File TOML {name_file_toml} không hợp lệ.")
            else:
                if os.path.exists(name_file_toml):
                    Sports2D.detect_pose(name_file_toml)
                    Sports2D.compute_angles(name_file_toml)
                else:
                    logging.warning("File TOML không tồn tại.")

        elif choice == '2':
            name_file_csv = input("Nhập tên file CSV: ")

            if not name_file_csv.endswith('_angles.csv'):
                logging.warning(f"File CSV {name_file_csv} không hợp lệ.")
            else:
                if os.path.exists(name_file_csv):
                    results = adhd_cal.adhd_cal(name_file_csv)
                    if results:
                        print("ADHD detected!")
                    else:
                        print("ADHD not detected!")
                else:
                    logging.warning("File CSV không tồn tại.")
        elif choice == '3':
            print("Kết thúc chương trình. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == '__main__':
    print("HELLO WORLD !!!")
    main_menu()
