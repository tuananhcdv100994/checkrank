from bs4 import BeautifulSoup
import requests

def check_keyword_rank(keyword, domain="bravigo.vn", max_pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    google_url = "https://www.google.com/search?q={}&start={}"

    rank = "Không tìm thấy"
    link = "#"

    for page in range(max_pages):
        start = page * 10
        response = requests.get(google_url.format(keyword, start), headers=headers)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="tF2Cxc")
        
        for index, result in enumerate(results, start=1 + page * 10):
            try:
                result_link = result.find("a")["href"]
                if domain in result_link:
                    rank = f"Top {index}"
                    link = result_link
                    return rank, link
            except:
                continue

    return rank, link

def main():
    keywords = [
        "Màn hình android ô tô", "Top 5 màn hình Android ô tô", "Màn hình Android ô tô nào tốt nhất",
        "Màn hình Android ô tô chất lượng nhất", "Màn hình Android ô tô bền nhất",
        "Màn hình Android ô tô nghe nhạc hay nhất", "So sánh Bravigo và zestech",
        "Màn hình Android cho xe CRV", "Màn hình Android ô tô số 1 hiện nay",
        "Màn hình android có công nghệ Adas", "Màn hình liền camera ô tô"
    ]

    for keyword in keywords:
        rank, link = check_keyword_rank(keyword)
        print(f"Từ khóa: {keyword}")
        print(f"Thứ hạng: {rank}")
        print(f"Link: {link}\n")

if __name__ == "__main__":
    main()
