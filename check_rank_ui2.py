import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
                             QVBoxLayout, QWidget, QLineEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Thiết lập trình điều khiển (Chrome driver)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=chrome_options)

# Hàm tìm kiếm từ khóa và kiểm tra thứ hạng của domain
def check_keyword_rank(driver, domain, keyword):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword)
    search_box.submit()
    time.sleep(2)  # Đợi trang kết quả tải xong
    
    results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    for index, result in enumerate(results[:50], start=1):  # Kiểm tra 50 kết quả đầu tiên
        try:
            link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if domain in link:
                return index
        except Exception:
            continue
    return None

# Lớp thực thi công việc tìm kiếm trong luồng riêng
class RankCheckerThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, domain, keywords):
        super().__init__()
        self.domain = domain
        self.keywords = keywords

    def run(self):
        try:
            driver = setup_driver()
            results = []
            for keyword in self.keywords:
                self.progress_signal.emit(f"Tìm kiếm từ khóa: {keyword}")
                rank = check_keyword_rank(driver, self.domain, keyword)
                if rank:
                    results.append(f"Từ khóa '{keyword}' tìm thấy ở vị trí: {rank}")
                else:
                    results.append(f"Từ khóa '{keyword}' không tìm thấy trong top 50")
            driver.quit()
            self.finished_signal.emit("\n".join(results))
        except Exception as e:
            self.error_signal.emit(str(e))

# Lớp giao diện PyQt5
class RankCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.rank_thread = None
    
    def init_ui(self):
        self.setWindowTitle("Rank Checker")
        self.setGeometry(100, 100, 700, 500)
        
        layout = QVBoxLayout()

        self.domain_input = QLineEdit(self)
        self.domain_input.setPlaceholderText("Nhập domain (vd: example.com)")
        layout.addWidget(self.domain_input)

        self.keyword_input = QTextEdit(self)
        self.keyword_input.setPlaceholderText("Nhập từ khóa (mỗi từ khóa trên một dòng)")
        layout.addWidget(self.keyword_input)

        self.progress_label = QLabel("Tiến trình:", self)
        layout.addWidget(self.progress_label)

        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.check_button = QPushButton("Kiểm tra thứ hạng", self)
        self.check_button.clicked.connect(self.run_check)
        layout.addWidget(self.check_button)

        self.export_button = QPushButton("Xuất kết quả ra file", self)
        self.export_button.clicked.connect(self.export_results)
        layout.addWidget(self.export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_check(self):
        domain = self.domain_input.text().strip()
        keywords = self.keyword_input.toPlainText().strip().split('\n')
        
        if not domain or not keywords:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập domain và từ khóa!")
            return

        self.result_display.clear()
        self.progress_label.setText("Đang tìm kiếm...")

        self.rank_thread = RankCheckerThread(domain, keywords)
        self.rank_thread.progress_signal.connect(self.update_progress)
        self.rank_thread.finished_signal.connect(self.display_results)
        self.rank_thread.error_signal.connect(self.display_error)
        self.rank_thread.start()

    def update_progress(self, message):
        self.progress_label.setText(message)

    def display_results(self, results):
        self.result_display.setText(results)
        self.progress_label.setText("Hoàn thành!")

    def display_error(self, error_message):
        QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {error_message}")
        self.progress_label.setText("Lỗi xảy ra trong quá trình tìm kiếm.")

    def export_results(self):
        results = self.result_display.toPlainText()
        if not results:
            QMessageBox.warning(self, "Lỗi", "Không có kết quả để xuất!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu file", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(results)
            QMessageBox.information(self, "Thành công", "Xuất file thành công!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RankCheckerApp()
    window.show()
    sys.exit(app.exec_())
