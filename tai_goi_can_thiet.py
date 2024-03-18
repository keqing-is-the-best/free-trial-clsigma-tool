def install():
    import os
    os.system("pip install selenium webdriver-manager python-whois keras tensorflow scikit-learn numpy")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print(ChromeDriverManager().install())
    except:
        return "đã có lỗi khi tải chrome driver"
    