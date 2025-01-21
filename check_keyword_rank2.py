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
    max_pages = 5  # số trang sẽ tìm kiếm trên google (top 50)
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
    "màn hình crv",
    "màn hình android crv",
    "so sánh màn hình bravigo và oled",
    "so sánh màn hình bravigo và gotech",
    "mặt dưỡng màn hình android",
    "có nên thay màn hình zin xe cx5 hay không",
    "màn hình android ford transit",
    "màn hình android cho crv",
    "màn hình android ô tô Chevrolet Colorado 2021",
    "màn hình android honda city",
    "màn hình android cho wuling huangwang",
    "màn hình android cho xe Skoda Kodiaq",
    "màn hình android nghe nhạc hay nhất",
    "màn hình android cho honda city",
    "màn hình android đáng mua 2024",
    "màn hình zin xpander",
    "màn hình android ô tô 13 inch",
    "màn hình cho xe hyundai creta",
    "màn hình xe i10 chính hãng",
    "màn hình android cho xe fortuner",
    "màn hình android mercerdes",
    "màn hình cx5",
    "màn hình android KIA Sonet",
    "màn hình android toyota vios",
    "màn hình android ghế sau ô tô",
    "màn hình android xe accent",
    "màn hình cho xe creta",
    "màn hình android vinfast lux sa2.0",
    "màn hình android cho mazda cx5",
    "màn hình android xe Hyundai Creta",
    "màn hình crv 2022",
    "màn hình android ô tô ford everest",
    "màn hình android cho xe vios",
    "màn hình android 7 inch",
    "màn hình android cho xe sorento",
    "màn hình android cho cx5",
    "màn hình android ô tô 7 inch",
    "màn hình android 13 inch",
    "màn hình android cerato",
    "màn hình mazda cx5 2023",
    "màn hình android xe tải",
    "màn hình xe i10",
    "so sánh màn hình bravigo và zestech",
    "màn hình xe tải",
    "màn hình android 10 inch",
    "màn hình android elantra",
    "màn hình toyota wigo",
    "màn hình android cho xe ford ranger",
    "màn hình android cho xe camry",
    "màn hình mazda 3",
    "màn hình android cho xe hilux",
    "màn hình kia morning",
    "màn hình android xe civic",
    "màn hình android innova",
    "màn hình android cho xpander",
    "màn hình android xe Brio",
    "màn hình android ô tô mazda",
    "màn hình android ô tô 12 inch",
    "màn hình android xe toyota cross",
    "màn hình android mazda",
    "màn hình ô tô 12.3 inch",
    "màn hình android cho xe altis",
    "màn hình innova",
    "màn hình android cho xe hrv",
    "màn hình android 9 inch",
    "màn hình cho vinfast fadil",
    "màn hình android ô tô"
]  # Thêm các từ khóa cần kiểm tra

    for keyword in keywords:
        rank, link = check_keyword_rank(driver, keyword)
        print(f"Từ khóa: {keyword}")
        print(f"Thứ hạng: {rank}")
        print(f"Link: {link}\n")
    
    driver.quit()

if __name__ == "__main__":
    main()
