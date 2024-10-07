import os
import adhd_cal
import logging
from Sports2D import Sports2D

logging.basicConfig(format='%(message)s', level=logging.WARNING)


def main_menu():
    while True:
        print("\nMenu:")
        print("1. Phân tích video từ file TOML")
        print("2. Phân tích file angle ADHD")
        print("3. Kết thúc")

        choice = input("Chọn một tùy chọn (1-3): ")

        if choice == '1':
            name_file_toml = input("Nhập tên file TOML: ")

            if not name_file_toml.endswith('.toml'):
                logging.warning(f"File TOML {name_file_toml} không hợp lệ.")
            else:
                if os.path.exists(name_file_toml):
                    Sports2D.process(name_file_toml)
                else:
                    logging.warning("File TOML không tồn tại.")

        elif choice == '2':
            print("VD Tên file : ./input/angles.mot")
            name_file_csv = input("Nhập tên file phân tích: ")

            if name_file_csv[0] == "\"" and name_file_csv[-1] == "\"":
                name_file_csv = name_file_csv[1:-1]

            print("Name file csv: ", name_file_csv)

            if os.path.exists(name_file_csv):
                results = adhd_cal.adhd_cal(name_file_csv)
                if results:
                    print("Determine if the leg moves!")
                else:
                    print("Determine if the leg does not move!")
            else:
                logging.warning("File không tồn tại.")

        elif choice == '3':
            print("Kết thúc chương trình. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == '__main__':
    print("HELLO WORLD !!!")
    main_menu()
