import sys
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget


def readDataMot(filename='angles.csv', columns_of_interest=None):
    if columns_of_interest is None:
        columns_of_interest = ['time', 'right knee', 'left knee', 'right hip', 'left hip',
                               'right shank', 'left shank', 'right thigh', 'left thigh']

    data = defaultdict(list)
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for _ in range(10):
            next(csv_reader)
        headers = next(csv_reader)
        headers_list = headers[0].split('\t')
        col_indices = {col: headers_list.index(col) for col in columns_of_interest if col in headers_list}

        for row in csv_reader:
            for col, index in col_indices.items():
                try:
                    row_data = row[0].split('\t')
                    value = float(row_data[index])
                    data[col].append(value)
                except (ValueError, IndexError):
                    continue

    return data


class PlotTab(QWidget):
    def __init__(self, patients_data, non_patients_data, column_en, column_vn):
        super().__init__()
        layout = QVBoxLayout(self)

        figure, ax = plt.subplots(figsize=(8, 6))
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        ax.plot(non_patients_data['time'], non_patients_data[column_en], label='Người có hoạt động')
        ax.plot(patients_data['time'], patients_data[column_en], label='Người không hoạt động')
        ax.set_xlabel('Thời gian')
        ax.set_ylabel(f'{column_vn}')
        ax.set_title(f'So sánh {column_vn}: Người bệnh vs Người khỏe')
        ax.legend()
        ax.grid(True)

        canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("So sánh dữ liệu")
        self.setGeometry(100, 100, 1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.plot_data()

    def plot_data(self):
        patients_data = readDataMot('./output/adhdStudy_Sports2D/adhdStudy_Sports2D_angles_person00.mot')
        non_patients_data = readDataMot('./output/adhdStudy_Sports2D/adhdStudy_Sports2D_angles_person01.mot')

        columns_of_interest = ['right knee', 'left knee', 'right hip', 'left hip',
                               'right shank', 'left shank', 'right thigh', 'left thigh']
        columns_of_interestVN = ['đầu gối phải', 'đầu gối trái', 'hông phải', 'hông trái', 'cẳng chân phải',
                                 'cẳng chân trái', 'đùi phải', 'đùi trái']

        # Tạo từ điển ánh xạ
        column_mapping = dict(zip(columns_of_interest, columns_of_interestVN))

        for column_en, column_vn in column_mapping.items():
            tab = PlotTab(patients_data, non_patients_data, column_en, column_vn)
            self.tab_widget.addTab(tab, column_vn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
