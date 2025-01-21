from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class RankCheckerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.domain_input = TextInput(hint_text='Nhập domain (vd: example.com)', multiline=False)
        self.layout.add_widget(self.domain_input)

        self.keyword_input = TextInput(hint_text='Nhập từ khóa', multiline=True)
        self.layout.add_widget(self.keyword_input)

        self.check_button = Button(text='Kiểm tra thứ hạng')
        self.check_button.bind(on_press=self.run_check)
        self.layout.add_widget(self.check_button)

        self.result_label = Label(text='Kết quả sẽ hiển thị ở đây')
        self.layout.add_widget(self.result_label)

        return self.layout

    def run_check(self, instance):
        domain = self.domain_input.text.strip()
        keywords = self.keyword_input.text.strip().split('\n')
        
        if not domain or not keywords:
            self.result_label.text = 'Vui lòng nhập domain và từ khóa!'
            return
        
        results = []
        driver = self.setup_driver()
        for keyword in keywords:
            rank = self.check_keyword_rank(driver, domain, keyword)
            if rank:
                results.append(f"Từ khóa '{keyword}' tìm thấy ở vị trí: {rank}")
            else:
                results.append(f"Từ khóa '{keyword}' không tìm thấy trong top 50")
        driver.quit()
        self.result_label.text = "\n".join(results)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(options=chrome_options)

    def check_keyword_rank(self, driver, domain, keyword):
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.submit()
        time.sleep(2)
        results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
        for index, result in enumerate(results[:50], start=1):
            try:
                link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if domain in link:
                    return index
            except Exception:
                continue
        return None

if __name__ == '__main__':
    RankCheckerApp().run()
