from whois import whois
import os
# lấy các thông tin tên miền từ whois và nối các thông tin và 1 biến chuổi
def domain_information(domain):
    domain_infomations = whois(domain)
    keys = ["domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date",
            "expiration_date", "name_servers", "status", "emails", "dnssec", "name", "org", "address",
            "city", "state", "registrant_postal_code", "country"]
    update_domain_infomation = ""
    for key in keys:
        update_domain_infomation += str(f"{domain_infomations[key]}, ")
    if domain.split(".")[1] in "net":
        return update_domain_infomation+"net"
    else:
        return update_domain_infomation+"com"
    
# phân loại tên miền thông qua phân loại thủ công từ người dùng để gán nhãn sau đó tự động lưu
def save_file(path, domain):
    desicion_train = ""
    while True:
        ask = input("bạn hãy cho tôi biết tên miền này nên dùng hay không vậy ạ: ")
        # phân loại không nên dùng
        if ask.lower() in ["không nên dùng", "không nên sử dụng", "đừng dùng", "đừng dùng nó", "không nên dùng nó", "không", "không dùng"]:
            desicion_train = "không nên dùng"
            break
        # phân loại nên dùng
        elif ask.lower() in ["dùng nó", "hãy dùng nó", "dùng nó đi", "hãy sữ dụng nó", "sử dụng nó", "nên", "nên dùng"]:
            desicion_train = "nên sử dụng"
            break
        # xử lý ngoại lệ
        else:
            os.system("cls")
            print("vui lòng nhập phân loại của bạn 'nên dùng' hay 'không' hoặc nói rõ hơn, hãy đào tạo lại nhé")
            continue
    # lưu thông tin tên miền đã được gán nhãn vào tệp
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{domain_information(domain=domain)} - {desicion_train}\n")
            return "đã lưu đào tạo"
    except Exception as e:
        return f"mã lỗi: {e}"