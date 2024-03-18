import os
from doan_ten_mien_hoc_sau import DLPredict

# tách các phân loại ra để chỉ lấy tên miền
def file_domain_geted(path):
    bag_lines = []
    with open(path, "r", encoding="utf-8") as file:
        data = file.read().splitlines()
    for lines in data:
        bag_lines.append(lines.split(" - ")[0])
    return bag_lines

# dự đoán tất cả tên miền trong tệp
def predict_model(path_train, path_domain):
    bag_result = []
    domains = file_domain_geted(path_domain)
    model, vectorizer = DLPredict().neural_netwwork(path_train=path_train)
    for domain in domains:
        try:
            domain_pre = DLPredict().predict(model=model, vectorizer=vectorizer, domain=domain)
            if float(domain_pre[0][0]) > 0.5:
                domain_pre = f"nên dùng {round(float(domain_pre[0][0])*100.0, 2)}%"
            else:
                domain_pre = f"đừng dùng {round(float(domain_pre[0][0])*100.0, 2)}%"
        except:
            pass
        bag_result.append(f"{domain} - {domain_pre}")
    return bag_result
