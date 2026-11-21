# Báo cáo cá nhân — NguyenCongTinh-2A202603373

## 1. Thông tin thành viên

- Họ tên: Nguyễn Công Tĩnh
- MSSV: 2A202603373
- Email: tinh22102004@gmail.com
- Vai trong nhóm: làm một mình nên kiêm cả bốn vai — người viết code, người kiểm số, người gắn nhãn 1, người gắn nhãn 2 kiêm giữ hồ sơ.

## 2. Phần việc phụ trách

Toàn bộ năm nhiệm vụ A–E và các file nộp: `src/lab13.py`, sáu file hồ sơ trong `report/team/`, `group_report.md`, `TEAM.md`.

## 3. Đóng góp cụ thể

- A: viết ba hàm A1 và `mo_hinh`; tính A2, A3 (kèm tỉ lệ ok theo lần thử), A4 chi phí cố định.
- B: chạy 9 kịch bản độ nhạy, kịch bản cặp, B3 chi phí cả hệ thống, B4 xem lại 100% và điểm hoà vốn.
- C: hai lượt gắn nhãn 20 ca, bảng khắc phục 5 ca.
- D: năm câu D1, chọn cách chia theo nhân viên 20 + 20 với mde 6 điểm, viết `pilot_plan.yaml` với 4 luật dừng.
- E: ba chỉ số, 10 event, 4 dòng rủi ro, hồ sơ launch v0 với đề xuất Go có điều kiện.

## 4. Bằng chứng

- `cd src && python3 lab13.py` in `Ba phép thử đáp án biết trước: ĐẠT` và các bảng A–E.
- Số chính: 4.472 đ/việc [simulated]; 16,3×; A3 0,22× / 0,69× / 1,88× / 0,85× [simulated]; B1 +51,8% làm lại; D1 1.251 · 3.103 · 1.000 · 300 · 299; E1 82,83% · 27,12% · 4,25%.
- Kiểm tay: 4.373.585 ÷ 978 = 4.472 đ; câu D1e: 20m ≥ 859 × (0,98 + 0,02m) → m ≥ 298,5 → 299.
- `report/team/pilot_plan.yaml` đọc được bằng `yaml.safe_load`, không còn dấu `?` ngoài chú thích.

## 5. Công cụ AI đã dùng

- **Claude (Anthropic)**: đọc đề, gợi ý và viết code `src/lab13.py`, soạn nháp các file hồ sơ, hỗ trợ hai lượt gắn nhãn nhiệm vụ C (đã khai báo trong `bang_loi.md`).
- Cách tự kiểm tra: chạy `python3 lab13.py` và đối chiếu từng số với bảng tự đối chiếu trong `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md` (lệch dưới 2%); tính tay hai số ở mục 4; chạy `yaml.safe_load`, `grep -v '^ *#' pilot_plan.yaml | grep '?'` và lệnh grep kiểm tra từ cấm theo checklist SUBMISSION.
- Mọi con số trong hồ sơ do `src/lab13.py` tính ra hoặc tính tay có ghi cách tính; không có số nào do AI tự đặt ra.

## 6. Tự đánh giá

- Phần A, B, D1, E1 khớp đáp án; hiểu được vì sao tử số tính mọi lần chạy còn mẫu số chỉ đếm việc thành công, vì sao số cụm (không phải tổng yêu cầu) quyết định cỡ mẫu hiệu dụng (< c ÷ ICC).
- Điểm yếu: làm một mình nên nhiệm vụ C không có hai người gắn nhãn độc lập thật và không có buổi duyệt chéo thật; đã ghi rõ hạn chế trong hồ sơ.
