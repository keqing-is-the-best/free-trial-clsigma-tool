import os
# hiển thị các lựa chọn chạy công cụ
def options():
    print("chọn các tùy chọn sau:")
    print("1. tìm tên miền")
    print("2. đào tạo công cụ này")
    print("3. tải xuống các gói cần thiết")
    print("\ndự đoán với công nghệ AI cơ bản:")
    print("4. đoán tên miền (máy học)")
    print("5. đoán các tên miền từ tệp đã đoán trước đó (máy học)")
    print("\ndự đoán với công nghệ AI tiên tiến nhất:")
    print("6. đoán tên miền (học sâu)")
    print("7. đoán các tên miền từ tệp đã đoán trước đó (học sâu)")

# hàm chứa các mô đun tìm tên miền
def finding_domain():
    from module.tim_ten_mien import run_manager
    run_manager(path_train="ten_mien_dao_tao.txt", path_domain="ten_mien_da_tim.txt")

# hàm chứa các mô đun dự đoán tên miền
def predict_domain_hoc_may():
    from module.doan_ten_mien_hoc_may import DomainPredict
    while True:
        try:
            domain_ = input("nhập tên miền của bạn để tôi đoán: ").lower().strip()
            print(DomainPredict().predict(path="ten_mien_dao_tao.txt", domain=domain_))
        except Exception as e:
            print(f"error code: {e}")
            continue

# hàm chứa các mô đun đoán tên miền trong file đã nhận
def file_predict_hoc_may():
    from module.du_doan_lai_tep_hoc_may import file_domains_predict
    domains_result = file_domains_predict(path_domain="ten_mien_da_tim.txt", path_train="ten_mien_dao_tao.txt")
    for domain in domains_result:
        print(domain)
    input("\nnhấn enter để đóng")

def predict_domain_hoc_sau():
    from module.doan_ten_mien_hoc_sau import DLPredict
    model, vectorizer = DLPredict().neural_netwwork("ten_mien_dao_tao.txt")
    os.system("cls")
    while True:
        try:
            user_input = input("nhập tên miền: ").strip().lower()
            predict = DLPredict().predict(model=model, vectorizer=vectorizer, domain=user_input)
            os.system("cls")
            if float(predict[0][0]) > 0.5:
                print(f"nên dùng {round(float(predict[0][0])*100.0, 2)}%")
            else:
                print(f"đừng dùng {round(float(predict[0][0])*100.0, 2)}%")
        except:
            os.system("cls")
            print("vui lòng nhập đúng tên miền!")
            continue

def file_predict_hoc_sau():
    from module.doan_lai_tep_hoc_sau import predict_model
    domain_pre = predict_model(path_domain="ten_mien_da_tim.txt", path_train="ten_mien_dao_tao.txt")
    os.system("cls")
    for result in domain_pre:
        print(result)
    input("\nnhấn enter để đóng")

# hàm chứa các mô đun để đào tạo công cụ
def training():
    while True:
        get_domain = input("nhập tên miền cần đào tạo: ").lower().strip()
        # kiểm tra ngoại lệ đầu vào
        if "." not in get_domain:
            os.system("cls")
            print("vui lòng nhập đúng tên miền đi ạ")
            continue
        try:
            from module.dao_tao import save_file
            print(save_file(path="ten_mien_dao_tao.txt", domain=get_domain))
            input("nhập enter để tiếp tục đào tạo")
            os.system("cls")
        except Exception as e:
            os.system("cls")
            print(f"error code: {e}")
            continue

def install_package():
    from module.tai_goi_can_thiet import install
    print(install())

# in ra các tiêu đề trước khi chạy vòng lặp bắt ngoại lệ
options()
# vòng lặp bắt ngoại lệ khi người dùng chọn
while True:
    try:
        user_input = input("\nnhập vào lựa chọn của bạn: ").strip()
        if int(user_input) == 1:
            os.system("cls")
            finding_domain()
        elif int(user_input) == 2:
            os.system("cls")
            training()
        elif int(user_input) == 3:
            os.system("cls")
            install_package()
        elif int(user_input) == 4:
            os.system("cls")
            predict_domain_hoc_may()
        elif int(user_input) == 5:
            os.system("cls")
            file_predict_hoc_may()
        elif int(user_input) == 6:
            os.system("cls")
            predict_domain_hoc_sau()
        elif int(user_input) == 7:
            os.system("cls")
            file_predict_hoc_sau()
        else:
            os.system("cls")
            print("vui lòng nhập lựa chọn của bạn tương ứng số thứ tự phía trên")
            options()
            continue
    except:
        os.system("cls")
        print("vui lòng nhập lựa chọn của bạn tương ứng số thứ tự phía trên")
        options()
        continue
