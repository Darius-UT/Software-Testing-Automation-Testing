# Software Testing - Project 3: Automation Testing (Level 2)

Dự án kiểm thử tự động hóa cho website [LambdaTest eCommerce](https://ecommerce-playground.lambdatest.io/) sử dụng **Python** và **Selenium WebDriver** theo mô hình **Data-Driven Testing**.

## 📋 Mục lục
1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt môi trường](#2-cài-đặt-môi-trường)
3. [Cấu trúc dự án](#3-cấu-trúc-dự-án)
4. [Quy ước Code (Convention)](#4-quy-ước-code-convention)
5. [Cách chạy Test](#5-cách-chạy-test)

---

## 1. Yêu cầu hệ thống
* **Python**: Phiên bản 3.12.
* **Trình duyệt**: Google Chrome (Phiên bản mới nhất).
* **Editor**: Visual Studio Code (Khuyên dùng).

---

## 2. Cài đặt môi trường

Mỗi thành viên khi clone code về cần thực hiện các bước sau **một lần duy nhất** để thiết lập môi trường chạy code giống nhau:

### Bước 1: Tạo môi trường ảo (Virtual Environment)
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
python -m venv venv
````

### Bước 2: Kích hoạt môi trường ảo

* **Windows (Command Prompt/PowerShell):**
    ```bash
    .\venv\Scripts\activate
    ```
* **macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```

*(Sau khi kích hoạt, bạn sẽ thấy chữ `(venv)` hiện ở đầu dòng lệnh terminal)*

### Bước 3: Cài đặt thư viện

Chạy lệnh sau để cài tất cả thư viện cần thiết (Selenium, v.v.):

```bash
pip install -r requirements.txt
```

Trong trường hợp Terminal hiển thị thông báo: *[notice] A new release of pip is available: 24.2 -> 25.3*. Hãy chạy lệnh cài đặt theo yêu cầu: 
```bash
python.exe -m pip install --upgrade pip
```


### Bước 4: Cài đặt WebDriver

1. Kiểm tra phiên bản Chrome trên máy bạn: `Settings` -\> `About Chrome` (Rất có thể là: 142.0.7444.176).
2. Tải **ChromeDriver** tương ứng với phiên bản Chrome tại: [Link Download Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
3. Giải nén file `chromedriver.exe` và copy vào thư mục `Drivers/` trong dự án.

---

## 3\. Cấu trúc dự án

```text
SOFTWARE-TESTING-PROJECT-03/
│
├── Drivers/                  # Chứa file chromedriver.exe (Local only - Không commit lên Git)
│
├── Data/                     # Chứa các file CSV dữ liệu test (Data-Driven)
│   ├── update_cart_data.csv
│   ├── login_data.csv
│   └── ...
│
├── TestScripts/              # Chứa mã nguồn kiểm thử (1 file .py = 1 Feature)
│   ├── test_feature_09_cart_manage.py
│   ├── test_feature_01_login.py
│   └── ...
│
├── .gitignore                # File cấu hình bỏ qua rác của Git
├── requirements.txt          # Danh sách thư viện Python cần cài
├── run_all_tests.py          # File chạy toàn bộ test case (Runner)
└── README.md                 # Hướng dẫn dự án (File này)
```

---

## 4\. Quy ước Code (Convention)

Để code đồng bộ, dễ đọc và tránh xung đột khi merge, toàn bộ nhóm tuân thủ quy tắc sau:

### Đặt tên (Naming)

* **File Python:** `snake_case` (chữ thường cách nhau dấu gạch dưới).
* Ví dụ: `test_feature_01_login.py`, `common_functions.py`
* **Class:** `PascalCase` (Chữ cái đầu mỗi từ viết hoa).
* Ví dụ: `TestLoginFeature`, `TestCartManage`
* **Hàm/Biến:** `snake_case`.
* Ví dụ: `test_login_success`, `user_email`, `btn_login`

### Quy tắc Data-Driven (Level 2)

1. **File CSV:** Đặt trong thư mục `Data/`.
2. **Dấu phân cách:** Sử dụng dấu phẩy `,` (Comma) làm delimiter chuẩn. Chú ý Region setting của máy tính.
3. **Tổ chức Test Script:**
      * Mỗi Feature tương ứng 1 file Python riêng biệt trong `TestScripts/`.
      * Sử dụng `setUpClass` để mở trình duyệt 1 lần cho cả class (Tối ưu hiệu suất).
      * Sử dụng `tearDownClass` để đóng trình duyệt.

### Format Code

* Khuyên dùng extension **Python** của Microsoft và bật chế độ **Format On Save** trên VS Code.

---

## 5\. Cách chạy Test

Đảm bảo bạn đã kích hoạt môi trường ảo `(venv)` trước khi chạy.

### Cách 1: Chạy một Feature cụ thể

Chạy lệnh python trỏ đến file script bạn muốn test:

```bash
python TestScripts/test_feature_09_cart_manage.py
```

### Cách 2: Chạy toàn bộ dự án

(Yêu cầu đã tạo file `run_all_tests.py` gom các test suite lại)

```bash
python run_all_tests.py
```

### Cách 3: Debug lỗi

Nếu test fail, hãy kiểm tra log lỗi trên Terminal:

  * `AssertionError`: Dữ liệu thực tế trên web khác dữ liệu mong đợi trong CSV.
  * `NoSuchElementException`: Không tìm thấy phần tử (sai XPath hoặc web chưa load xong).
  * `StaleElementReferenceException`: Phần tử bị cũ do trang web reload (cần tìm lại phần tử).

<!-- end list -->


### Cách 4: Thoát `(venv)`

Để thoát giao diện terminal của venv, dùng lệnh:
```bash
deactivate
```