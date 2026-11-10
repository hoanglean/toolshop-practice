# Buổi 1 và Sprint 1: kết quả, giải thích và cách nộp

Đối chiếu phiếu thực hành 10 trang; kiểm tra lại ngày 08/11/2026.

Repo: https://github.com/hoanglean/toolshop-practice

## Kết quả chạy thực tế

Chạy tại thư mục gốc repo với Python 3.12.10, Playwright và Chromium, trên PROD:

| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/buoi1 -v` | 13 passed trong 46.88 giây: 9 test POM và 4 test mẫu |
| `python -m pytest -m smoke -v` | 4 passed, 44 deselected trong 23.96 giây |

`deselected` nghĩa là không thuộc bộ smoke được chọn, không phải lỗi.

Trong phiên kiểm tra, đã chỉ định `PLAYWRIGHT_BROWSERS_PATH` tới bộ Chromium có sẵn trên máy. Không cần cài lại trình duyệt; thay đổi này chỉ áp dụng cho tiến trình kiểm tra.

## Đã làm những gì

| Bài | Nội dung |
|---|---|
| B1.0 | Đếm được 11 dòng chứa `product-name`: 2 dòng chú thích và 9 dòng code. Nếu đổi thuộc tính này, 4 test mẫu cần sửa 9 dòng code. |
| B1.1 | HomePage khai báo locator tìm kiếm, nhập từ khóa và bấm tìm; test kiểm tra có kết quả, tiêu đề và tên sản phẩm chứa `pliers`. |
| B1.2 | Tìm `zzz-no-such-tool`, kiểm tra thông báo không có kết quả và danh sách 0 sản phẩm. |
| B1.3 | ProductPage khai báo tên, đơn giá, số lượng, nút thêm giỏ. Chỉ nhập số lượng khi khác 1; thêm 3 Claw Hammer và kiểm tra toast, badge 3. |
| B1.4 | Dùng đúng Combination Pliers theo phiếu. Đọc đơn giá trước khi thêm 2 sản phẩm, kiểm tra số lượng, thành tiền và tổng giỏ bằng `pytest.approx`. |
| B1.5 | LoginPage hỗ trợ nhập và gửi form; kiểm tra đăng nhập bằng email không tồn tại, URL đăng nhập, cùng hai lỗi bắt buộc khi để trống. |
| B1.6 | Dùng chuỗi HomePage → ProductPage → CartPage, kiểm tra tên sản phẩm trong giỏ trước khi tiếp tục mua sắm, rồi kiểm tra lưới sản phẩm ở trang chủ. |
| B1.7 | Tham số hóa giá tăng/giảm, chờ `sorting_completed`, đọc giá và so với `sorted()`. |
| B1.8 | Đếm lại được 2 dòng locator `product-name`: một trong HomePage và một trong ProductPage; không có trong test POM hoặc smoke. |

B1.6 dùng tên sản phẩm thực tế `Claw Hammer` thay cho ví dụ `Hammer` trong phiếu. HomePage so khớp nguyên tên để tránh bấm nhầm sản phẩm khác có chữ Hammer.

Hành động thêm giỏ chờ phản hồi POST của giỏ trước khi trả về, để chuỗi gọi `go_to_cart()` không chuyển trang quá sớm. Đây là đồng bộ thao tác, không phải assertion trong Page Object.

Nếu chỉ CSS class của website đổi mà `data-test` vẫn giữ nguyên, các locator hiện tại không cần sửa. Nếu chính thuộc tính `product-name` đổi tên, số dòng cần sửa giảm từ 9 xuống 2 nhờ POM.

## Bốn test smoke của Sprint 1

File `tests/ui/test_smoke.py` chứa đúng bốn test, đều dùng Page Object:

1. Tìm `pliers`: có kết quả và mọi tên sản phẩm chứa từ khóa.
2. Thêm 3 `Claw Hammer`: có thông báo thành công và badge giỏ bằng 3.
3. Đăng nhập bằng email không tồn tại: báo `Invalid email or password`, vẫn ở URL đăng nhập.
4. Gửi form Liên hệ trống: báo `Subject is required` và `Message is required`.

ContactPage có thêm hai locator lỗi tương ứng. Nhãn smoke được tập trung ở bộ nghiệm thu này. Hai test mẫu trước đó ở B1.1 và B2.1 vẫn tồn tại, chỉ bỏ nhãn smoke để `pytest -m smoke` chọn đúng bốn test yêu cầu. B2.1 vẫn chạy được bằng đường dẫn hoặc nhãn api.

Khung `conftest.py`, `pytest.ini`, `requirements.txt`, `.gitignore`, `.env.example` và `pages/` đã có trong repo tạo từ template. Tệp `.env` chứa cấu hình cá nhân không đưa vào commit.

## Tự kiểm tra B1.0, B1.8 và ba quy tắc

Chạy trong PowerShell tại thư mục gốc repo:

```powershell
# B1.0: 11 kết quả, gồm 2 dòng chú thích và 9 dòng code.
(Select-String -Path tests\buoi1\test_b1_spaghetti.py -Pattern 'product-name').Count

# B1.8: 2 dòng trong pages, không có trong test POM hay smoke.
Select-String -Path pages\*.py,tests\buoi1\test_b1_pom.py,tests\ui\test_smoke.py -Pattern 'product-name'

# Ba nhóm kiểm tra dưới đây phải không in ra kết quả.
Select-String -Path tests\buoi1\test_b1_pom.py,tests\ui\test_smoke.py -Pattern 'get_by_|locator\('
Select-String -Path pages\*.py -Pattern 'expect\(|assert '
Get-ChildItem tests,pages -Recurse -Filter *.py | Select-String -Pattern 'sleep|wait_for_timeout'
```

Không sửa file test mẫu `test_b1_spaghetti.py`. Ngoại lệ locator trong file mẫu dùng để so sánh với POM; khi quét locator, chọn file POM và smoke như trên.

## Cách nộp và nghiệm thu ngày 11/11

Phiếu yêu cầu nghiệm thu bằng repo công khai, Pull Request và kết quả chạy test. Phiếu không ghi một cổng nộp link cụ thể; xem thêm thông báo của lớp nếu có.

1. Xác nhận đây là repo đồ án của nhóm và đã thêm đủ thành viên.
2. Kiểm tra bảo vệ nhánh `main`: thay đổi qua Pull Request, tối thiểu 1 approval.
3. Tạo nhánh riêng cho phần Sprint 1, commit đúng các file liên quan và đẩy nhánh lên GitHub.
4. Mở PR #1 vào `main`; ghi phần thay đổi và hai kết quả kiểm tra trong bảng đầu tài liệu này.
5. Một thành viên khác đọc code, review và approve; sau đó merge PR.
6. Khi nghiệm thu, mở repo nhóm và chạy `python -m pytest -m smoke`: phải có 4 passed.

Hiện đã sửa code và chạy test trên máy. Chưa đẩy các thay đổi này lên GitHub, chưa kiểm tra đủ thành viên/quy tắc bảo vệ main, và chưa có người khác review hay merge PR. Không xem các mục đó là đã hoàn tất chỉ vì test xanh.
