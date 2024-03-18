from module.doan_ten_mien_hoc_may import DomainPredict
import os

# in ra thanh tải
def task_bar(char, loading_name, clear_screen):
    print(loading_name, end="", flush=True)
    print(char, end="", flush=True)
    if clear_screen == True:
        try:
            os.system("cls")
        except:
            os.system("clear")

# tách các phân loại ra để chỉ lấy tên miền
def file_domain_geted(path):
    bag_lines = []
    with open(path, "r", encoding="utf-8") as file:
        data = file.read().splitlines()
    for lines in data:
        bag_lines.append(lines.split(" - ")[0])
    return bag_lines

# dự đoán tất cả tên miền trong tệp
def file_domains_predict(path_domain, path_train):
    bag_result = []
    domains = file_domain_geted(path_domain)
    domain_predict = DomainPredict()
    task_bar(char="", loading_name="đang dự đoán..", clear_screen="")
    for domain in domains:
        task_bar(".", loading_name="", clear_screen="")
        try:
            domain_pre = domain_predict.predict(path=path_train, domain=domain)
        except:
            pass
        bag_result.append(f"{domain} - {domain_pre}")
    task_bar(char="", loading_name="", clear_screen=True)
    return bag_result