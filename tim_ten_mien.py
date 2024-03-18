from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from doan_ten_mien_hoc_may import DomainPredict
import os

# thiết lập trình duyệt
def browser_custom():
    option = Options()
    option.add_argument("--log-level=3")
    option.add_argument("--headless")
    browser = webdriver.Chrome(options=option)
    os.system("cls")
    return browser

# tìm tên miền với 20 lần lặp
def finding_domain():
    browser = browser_custom()
    domains, uptimes = [], []
    for i in range(20):
        try:
            browser.get("https://emailfake.com/fake_email_generator")
            email = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email_ch_text"]'))).text
            domain = email.split("@")[1]

            uptime_text = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkdomainset"]'))).text
            uptime = uptime_text.split()[4]

            domains.append(domain)
            uptimes.append(uptime)

            print(f"{i} - {domain} - {uptime} days")
        except Exception as e:
            print(f"mã lỗi: {e}")
            browser.quit()
            return domains, uptimes
    browser.quit()
    return domains, uptimes

# dự đoán tên miền
def domain_predict_tool(path_train, domain):
    domain_predict = DomainPredict()
    return domain_predict.predict(path=path_train, domain=domain)

# kiểm tra tên miền có tồn tại trong nhật ký hay không
def log():
    if os.path.exists("log.txt") == False:
        with open("log.txt", "w"): pass
    with open("log.txt", "r") as f:
        return f.read().splitlines()
    
# phân loại tên miền và lưu kết quả dự đoán vào tệp
def domain_desicion(path_domain, path_train):
    domains, uptimes = finding_domain()
    with open(path_domain, "a", encoding="utf-8") as f:
        for i in range(len(domains)):
            domain = domains[i]
            uptime = uptimes[i]
            if int(uptime) < 4 and domain.split(".")[1] in ["net", "com"] and domain not in log():
                try:
                    f.write(f"{domain} - {domain_predict_tool(path_train=path_train, domain=domain)}\n")
                    with open("log.txt", "a") as f:
                        f.write(f"{domain}\n")
                except Exception as e:
                    print(f"mã lỗi: {e}")
                    f.write(f"{domain}\n")
    return "saved"

# quản lý chạy
def run_manager(path_domain, path_train):
    while True:
        try:
            os.system("cls")
            domain_desicion(path_domain=path_domain, path_train=path_train)
        except Exception as e:
            os.system("cls")
            print(f"mã lỗi: {e}")
            continue
