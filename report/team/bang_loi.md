# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Cách làm khi nhóm chỉ có một người (khai báo minh bạch)

Nhóm NhomKhongTen chỉ có một thành viên (Nguyễn Công Tĩnh) và đã được người ra đề đồng ý cho làm một mình. Không có người thứ hai để gắn nhãn, nên hai bộ nhãn được tạo bằng **hai lượt gắn tách nhau, theo hai cách đọc khác nhau, có hỗ trợ của trợ lý AI (Claude)**; Nguyễn Công Tĩnh rà soát và chịu trách nhiệm về nhãn cuối:

- **Lượt 1** (vai người gắn nhãn 1): đọc từng ca, gắn theo bảng định nghĩa năm loại PAIR trong đề bài.
- **Lượt 2** (vai người gắn nhãn 2): gắn lại từ đầu, không nhìn lượt 1, bằng cây câu hỏi theo thứ tự: (1) đầu vào/thao tác của khách có sai không → Do người dùng; (2) trợ lý có làm được việc này không, kể cả khi cố → nếu không: Giới hạn hệ thống; (3) có ai nhận ra cái sai trước khi kiểm tra mẫu không → nếu không: Ngầm; (4) có vi phạm thiết kế/chính sách không → Hệ thống; (5) đúng thiết kế nhưng khách thấy sai → Ngữ cảnh.

Hai lượt được so sau khi đã gắn xong; không sửa bộ nhãn nào sau khi so (RULES.md).

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Lượt 1 (định nghĩa PAIR) · Người gắn nhãn 2: Lượt 2 (cây câu hỏi) — gắn tách nhau, không đối chiếu trong lúc gắn.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 20 / 20 = 100% (≥ 80%, không cần viết lại định nghĩa).

Phân bố nhãn thống nhất: Do người dùng 4 ca (1, 6, 9, 14) · Hệ thống 5 ca (2, 7, 8, 15, 20) · Ngữ cảnh 4 ca (3, 10, 16, 18) · Giới hạn hệ thống 4 ca (4, 11, 13, 19) · Ngầm 3 ca (5, 12, 17).

**Hạn chế:** hai lượt cùng do một người (có AI hỗ trợ) thực hiện nên mức độc lập thấp hơn hai người thật; đồng thuận 100% có thể cao hơn thực tế. Cách giảm: lượt 2 dùng cây câu hỏi khác lượt 1, và các ca dễ lẫn bên dưới đã ghi quy tắc phân biệt.

## Quy tắc phân biệt cho các ca không trùng

Không có ca không trùng (20/20). Các ca dễ lẫn nhất khi gắn, kèm quy tắc đã dùng:

- **Ca 6, 9 là Do người dùng, không phải Hệ thống:** gốc lỗi là khách chọn sai mục / nhập sai mã; việc trợ lý không gợi ý là chỗ cần cải thiện, ghi ở cột khắc phục, không đổi nhãn.
- **Ca 13 là Giới hạn hệ thống:** yêu cầu ngoài phạm vi thì là giới hạn, kể cả khi trợ lý xử lý giới hạn đó kém (trả lời chung chung).
- **Ca 8, 15 là Hệ thống, không phải Ngầm:** cái sai đã lộ ra (trích dẫn nhìn thấy được, nhân viên bắt được); Ngầm chỉ dùng khi không ai nhận ra cho tới khi kiểm tra mẫu.
- **Ca 18 là Ngữ cảnh:** số tiền đúng chính sách (30.000 đ × 50% = 15.000 đ), chỉ giả định "khách hiểu cách tính" không khớp.
- **Ca 12 là Ngầm:** kết quả vẫn đúng nhưng chi phí token gấp 3 lần suốt 3 tuần không ai thấy; "sai" có thể là sai về chi phí.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò có quyền quyết định.

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed` (reason = ma_khong_hop_le, trace_id); cảnh báo khi > 2% số yêu cầu/ngày, xem báo cáo hằng ngày | Nhận diện định dạng mã đơn sàn TMĐT và tra sang mã vận đơn; không tra được thì hướng dẫn kèm ảnh vị trí mã vận đơn, không dừng im | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin nhắn "đã hoàn" (`refund_message_sent`) không có `refund_ledger_write` với ket_qua = ok cùng trace_id; ngưỡng 0 ca, có 1 ca là báo động | Chỉ báo "đã hoàn" khi sổ cái trả ok; lỗi 503 sau 3 lần thì báo khách "đang xử lý" và `handoff_to_staff`; thêm khoá chống trùng (idempotency_key) cho ca 20 | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Tỉ lệ `ticket_reopened` với reason = so_tien mà `audit_sample_checked` thấy số tiền đúng, tính theo tuần; ngưỡng > 0,5% số yêu cầu | Mẫu tin nhắn luôn ghi cách tính (ví dụ: phí 30.000 đ × 50% = 15.000 đ) và điều khoản áp dụng | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` với reason = thieu_du_lieu, đếm theo loại yêu cầu mỗi tuần; quoc_te chỉ thành công 27,3% trong đợt chạy thử | Giữ cách chuyển nhân viên kèm tóm tắt; đưa quoc_te ra khỏi pilot (1,88× [simulated]); trợ lý nói rõ "không xử lý được" ngay lần đầu, không chạy lại | PM trợ lý hoàn phí |
| 17 | Ngầm | Kiểm tra mẫu 100 đơn/tuần (`audit_sample_checked`) so số tiền hoàn với bảng giá hiện hành; ngưỡng 1% đơn lệch thì điều tra trong 24 giờ | Xoá bộ nhớ đệm khi có bảng giá mới; ghi phiên bản bảng giá vào trace của mỗi lần chạy; truy hoàn/bù 212 đơn lệch | Kế toán trưởng |
