from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import keras
from whois import whois
import os

class DLPredict:
    def __init__(self):
        pass
    
    # truy xuất thông tin của tên miền
    def domain_information(self, domain):
        domain_infomations = whois(domain)
        keys = ["domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date",
                "expiration_date", "name_servers", "status", "emails", "dnssec", "name", "org", "address",
                "city", "state", "registrant_postal_code", "country"]
        update_domain_infomation = ""
        for key in keys:
            update_domain_infomation += str(f"{domain_infomations[key]}, ")
        if domain.split(".")[1] in "net":
            return [update_domain_infomation+"net"]
        else:
            return [update_domain_infomation+"com"]
    
    # xử lý dữ liệu train của các tên miền
    def process_data_train(self, path_train):
        # mở tệp
        with open(path_train, "r", encoding="utf8") as file:
            data = file.read().splitlines()
        # tách X và y
        bag_x = []
        bag_y = []
        for dt in data:
            bag_x.append(dt.split(" - ")[0])
            bag_y.append(dt.split(" - ")[1])
        # vector hóa dữ liệu
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(bag_x).toarray()
        # chuyển chuổi sang số cho nhãn
        y = []
        for labels in bag_y:
            if labels in "nên sử dụng":
                y.append(1)
            else:
                y.append(0)
        y = np.array(y)
        return X, y, vectorizer
    
    # tạo 1 mô hình mạng thần kinh nhân tạo và train sẳn nó
    def neural_netwwork(self, path_train):
        # xử lý dữ liệu đào tạo
        X, y, vectorizer = self.process_data_train(path_train=path_train)
        neural = int(len(X)/6)
        if neural < 1:
            neural = 1
        model = keras.Sequential([
            keras.layers.Dense(units=neural, input_shape=(X.shape[1],)),
            keras.layers.Dense(units=neural, activation="tanh"),
            keras.layers.Dense(units=neural, activation="relu"),
            keras.layers.Dense(units=neural, activation="sigmoid"),
            keras.layers.Dense(units=1, activation="sigmoid")
        ])
        # các thiết lập cho mô hình
        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=['accuracy']
        )
        # training
        model.fit(X, y, epochs=neural)
        return model, vectorizer
    
    # bắt đầu đoán
    def predict(self, domain, vectorizer, model):
        return model.predict(vectorizer.transform(self.domain_information(domain)).toarray())