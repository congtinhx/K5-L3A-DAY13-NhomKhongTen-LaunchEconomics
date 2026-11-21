# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: NhomKhongTen
- Lớp: L3A
- Thành viên: Nguyễn Công Tĩnh (làm một mình, kiêm cả bốn vai, đã được người ra đề đồng ý) — xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Dựng hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN để hội đồng Gate 2a quyết định có mở pilot hay không, trả lời bốn câu: có đáng chạy không, nhân viên có dùng không, khi hỏng thì sao, pilot thiết kế thế nào để ra quyết định. Mọi con số do `src/lab13.py` tính trên hai file CSV giả lập; số từ cột `_simulated` ghi nhãn `simulated`; nhiệm vụ sau dùng lại số của nhiệm vụ trước (A3 → phạm vi pilot, B → luật dừng và rủi ro, D → điều kiện của đề xuất).

## 3. Giải pháp

- **A · Chi phí** ([bang_chi_phi.md](bang_chi_phi.md)): viết ba hàm A1 (qua 1,20 · 1,25 · 1,25), hàm `mo_hinh` cộng token + tool của **mọi** lần chạy và phút xem lại / làm lại, chia cho số việc **thành công**; tách theo `loai` (A3) kèm tỉ lệ ok theo từng lần thử; cộng chi phí cố định 40 triệu đ/tháng cho phạm vi (A4).
- **B · Độ nhạy** ([bang_chi_phi.md](bang_chi_phi.md)): 9 kịch bản đổi một yếu tố, một cặp, giới hạn 1/2/3 lần chạy tính chi phí cả hệ thống, kịch bản xem lại 100% có tính điểm hoà vốn.
- **C · Lỗi** ([bang_loi.md](bang_loi.md)): hai lượt gắn nhãn 20 ca tách nhau theo hai cách đọc khác nhau (có AI hỗ trợ, khai báo rõ), so nhãn, bảng khắc phục 5 ca đủ năm loại PAIR.
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính năm câu D1 trước, rồi chọn chia theo nhân viên 20 + 20, nới mde lên 6 điểm; tính tỉ lệ mở lại hiện tại trước khi đặt luật an toàn; 4 luật dừng đủ NẾU – TRONG – THÌ – KHÔNG THÌ.
- **E · Chỉ số và hồ sơ** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): tính thử ba chỉ số, đề xuất thêm một chỉ số dùng và một chỉ số an toàn, 10 event có trace_id, 4 dòng rủi ro kinh tế, hồ sơ một trang bảy mục.

## 4. Kết quả

- Chi phí mỗi việc thành công **4.472 đ** [simulated], gấp 16,3× hoá đơn token chia số yêu cầu (274,7 đ); làm lại chiếm 51,8%, xem lại 40,7% [simulated].
- Theo loại: noi_dia 0,22×, hang_nang 0,69×, quoc_te **1,88×**, doi_tac 0,85× của 12.000 đ [simulated]; quoc_te chạy lại không giúp (lần 3 chỉ đúng 2,2%).
- Phạm vi noi_dia + hang_nang cộng cố định: 4.599 đ = 0,38× [simulated]; xem lại 100%: 0,98–1,03× [simulated].
- Ba yếu tố nhạy nhất: làm lại · xem lại · lương. Giới hạn 2 lần chạy rẻ nhất cho công ty (6.901.220 đ [simulated]).
- Pilot: theo nhân viên, 859/nhóm, DE 6,96, ≥ 299 yêu cầu/người; power 0,64 nếu tác động thật 5 điểm.
- Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%.
- **Đề xuất cuối: Go có điều kiện** cho pilot noi_dia + hang_nang, bốn điều kiện có người phụ trách và ngày kiểm tra.
- Duyệt chéo: nhóm một người không được ghép cặp hội đồng; `phieu_cham.md` là phiếu tự chấm theo thang hội đồng (30/30, tự chấm), ghi rõ không phải kết quả hội đồng thật.

## 5. Khó khăn và cách xử lý

- **Làm một mình** nên không có hai người gắn nhãn độc lập ở nhiệm vụ C và không có nhóm để duyệt chéo. Xử lý: gắn hai lượt tách nhau theo hai cách đọc khác nhau, không sửa nhãn sau khi so; khai báo hạn chế trong `bang_loi.md`; phiếu chấm ghi rõ là tự chấm, không bịa kết quả hội đồng.
- **Máy không cài được `statsmodels`/`scipy`** (pip báo `No matching distribution found for statsmodels` vì không có mạng). Xử lý: tính cỡ mẫu bằng `statistics.NormalDist` theo công thức trong `docs/du_lieu_va_cong_thuc.md`; power tính theo Cohen's h giống `NormalIndPower`, code tự dùng `statsmodels` nếu có. Kết quả khớp đáp án: 1.251 · 3.103 · 1.000 · 300 · 299, power 0,64.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`. Nhóm một người: Nguyễn Công Tĩnh làm toàn bộ (code, kiểm số, gắn nhãn, giữ hồ sơ), có dùng trợ lý AI (Claude) và đã khai báo trong báo cáo cá nhân.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại và làm lại là số giả lập; chi phí thật chỉ biết sau tuần 1 pilot khi có event `staff_review_decision`, `staff_rework_completed`.
- Mde 6 điểm: có 36% khả năng bỏ sót tác động thật 5 điểm; nếu kết quả không có ý nghĩa thống kê thì không kết luận "không có tác động".
- ICC 0,02 là giả định; nên ước lượng lại từ tỉ lệ thành công theo staff_id khi có dữ liệu pilot.
- Hai bộ nhãn C không độc lập bằng hai người thật; nên mời một người ngoài gắn lại để kiểm tra.

## 8. Tài liệu tham khảo

- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, arXiv:2504.13359.
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure".
- Tài liệu statsmodels, `statsmodels.stats.power.NormalIndPower`.
- Tài liệu của lab: `docs/du_lieu_va_cong_thuc.md`, `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`, `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`.
