# models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from whois import whois

class DomainPredict():
    # lấy thông tin tên miền đầu vào
    def domain_information(self, domain):
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
        
    # đọc tệp và lưu chúng ra thành 2 loại X và y (dữ liệu và nhãn)
    def read_file(self, path):
        X_train, y_train = [], []
        with open(path, "r", encoding="utf-8") as file:
            data = file.read().splitlines()
            for info in data:
                X_train.append(info.split(" - ")[0])
                y_train.append(info.split(" - ")[1])
        return [X_train], y_train
    
    # hàm dự đoán
    def predict(self, path, domain):
        domain_info = self.domain_information(domain=domain)
        X_train, y_train = self.read_file(path=path)
        # khởi tạo 1 phương thức bag of word
        bow_transformer = CountVectorizer()
        # mã hóa dữ liệu đào tạo bằng bag of word
        X_train = bow_transformer.fit_transform(X_train[0]).toarray()
        # tất cả các mô hình phân loại
        desicion_tree = DecisionTreeClassifier()
        random_forest = RandomForestClassifier()
        bayes_model = GaussianNB()
        svm_model = SVC(probability=True)
        knn_model = KNeighborsClassifier(n_neighbors=3)
        # sử dụng mô hình bỏ phiếu để kết hợp tất cả mô hình trên lại
        voting_model = VotingClassifier(estimators=[("desicion tree", desicion_tree),
                                                    ("random forest", random_forest),
                                                    ("svm", svm_model),
                                                    ("knn", knn_model),
                                                    ("bayes", bayes_model)], voting="soft")
        # đào tạo mô hình
        voting_model.fit(X_train, y_train)
        # mã hóa đầu vào và dự đoán
        X_test = bow_transformer.transform([domain_info]).toarray()
        predict = voting_model.predict(X_test)
        # lưu lại kết quả dự đoán vào hàm
        return predict[0]