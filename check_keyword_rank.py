from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    # Cấu hình Chrome để mở ở chế độ ẩn danh
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")  # Chạy ở chế độ không hiển thị (tùy chọn)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_keyword_rank(driver, keyword, domain="bravigo.vn"):
    # Mở Google và tìm kiếm từ khóa
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Đợi kết quả tải

    # Kiểm tra thứ hạng của domain trong kết quả tìm kiếm
    rank = "Không tìm thấy"
    link = "#"
    max_pages = 5  # Giới hạn số trang tìm kiếm (top 30)
    current_page = 1

    while current_page <= max_pages:
        results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

        for index, result in enumerate(results, start=(current_page - 1) * 10 + 1):
            try:
                link_element = result.find_element(By.TAG_NAME, "a")
                result_link = link_element.get_attribute("href")
                if domain in result_link:
                    rank = f"Top {index}"
                    link = result_link
                    return rank, link
            except:
                continue

        # Tự động nhấp vào nút "Next" để chuyển sang trang tiếp theo
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(2)  # Đợi tải trang
            current_page += 1
        except:
            # Nếu không tìm thấy nút "Next" thì dừng
            break

    return rank, link

def main():
    driver = setup_driver()
    keywords = [
        "Màn hình android ô tô", "Top 5 màn hình Android ô tô", "Màn hình Android ô tô nào tốt nhất",
        "Màn hình Android ô tô chất lượng nhất", "Màn hình Android ô tô bền nhất",
        "Màn hình Android ô tô nghe nhạc hay nhất", "So sánh Bravigo và zestech",
        "Màn hình Android cho xe CRV", "Màn hình Android ô tô số 1 hiện nay",
        "Màn hình android có công nghệ Adas", "Màn hình liền camera ô tô",
    ]  # Thêm các từ khóa cần kiểm tra

    for keyword in keywords:
        rank, link = check_keyword_rank(driver, keyword)
        print(f"Từ khóa: {keyword}")
        print(f"Thứ hạng: {rank}")
        print(f"Link: {link}\n")
    
    driver.quit()

if __name__ == "__main__":
    main()
