# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot.

Nhóm: NhomKhongTen (1 thành viên: Nguyễn Công Tĩnh) · Lớp: L3A · Phạm vi đề xuất: chỉ `noi_dia` + `hang_nang`

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | 4.472 đ toàn mẫu, gấp 16,3× hoá đơn token chia số yêu cầu (274,7 đ); trong phạm vi 3.414 đ, cộng cố định 4.599 đ [simulated] ([bang_chi_phi.md](bang_chi_phi.md) A2, A4) | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1. Làm lại ±51,8% · 2. Xem lại ±40,7% · 3. Lương +23,1%; giá token chỉ ±5,6% [simulated] (B1, B2) | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Phạm vi: 0,38× của 12.000 đ (đã cộng cố định), cả hệ thống toàn mẫu 0,49×; **bất lợi:** quoc_te 1,88× (loại), xem lại 100% thì 0,98–1,03× [simulated] (A3, B4) | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Chính trong đợt chạy thử 82,83% (994/1.200) · Bỏ qua gợi ý 27,12% (48/177) · Mở lại 7 ngày 4,25% (51/1.200), phạm vi 3,97%, **hang_nang 8,23%**; 10 event có trace_id ([chi_so.md](chi_so.md)) | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca, đồng thuận 20/20 = 100% (hai lượt gắn tách nhau, có AI hỗ trợ, nhóm 1 người); 5 cách khắc phục đủ năm loại; lỗi nặng nhất: ca 7 báo "đã hoàn" khi sổ cái lỗi, ca 20 hoàn trùng ([bang_loi.md](bang_loi.md)) | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia theo nhân viên 20 + 20, ngẫu nhiên, mde 6 điểm, 859/nhóm, DE 6,96, ≥ 299 yêu cầu/người; **bất lợi:** power chỉ 0,64 nếu tác động thật 5 điểm; 4 luật dừng; quyết định 2027-01-05 ([pilot_plan.yaml](pilot_plan.yaml)) | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Làm lại gấp đôi → 6.787 đ (+51,8%); xem lại 100% kéo dài → 11.743–12.415 đ (0,98–1,03×); khối lượng còn nửa → +2.370 đ/việc [simulated] ([chi_so.md](chi_so.md) E2) | Giả lập | PM trợ lý hoàn phí |

**Đề xuất:** Go có điều kiện — mở pilot cho `noi_dia` + `hang_nang`, không mở cho `quoc_te`, `doi_tac`. Điều kiện (mỗi điều kiện có người phụ trách và ngày kiểm tra; ngày bắt đầu dự kiến 2026-11-30):

- Sửa luồng ghi sổ cái: chỉ báo "đã hoàn" khi sổ cái trả ok, thêm khoá chống trùng (ca 7, 20), đối soát mỗi giờ ngưỡng 0 ca — Kỹ sư trưởng agent, kiểm tra 2026-11-27.
- Ký chấp nhận đánh đổi mức chênh 6 điểm (power 0,64 nếu tác động thật chỉ 5 điểm) và chốt seed bốc thăm 20261130 — Giám đốc vận hành LogiX-VN, kiểm tra 2026-11-28.
- Bật đủ 10 event có trace_id; thay phút xem lại / làm lại simulated bằng phút đo thật và tính lại chi phí sau tuần 1 — PM trợ lý hoàn phí, kiểm tra 2026-12-07.
- Có kế hoạch giảm xem lại theo bậc (xem lại 100% là 0,98–1,03× [simulated], hoà vốn khi ≤ 5,1 / 4,8 phút) và theo dõi riêng mở lại của hang_nang (8,23% trong đợt chạy thử) so với đối chứng — Trưởng nhóm CSKH, kiểm tra 2026-12-14.

Không đạt điều kiện nào thì chuyển thành No-go và quay lại Gate 2a sau khi sửa.

**Đề xuất cuối: Go có điều kiện** cho pilot `noi_dia` + `hang_nang` (chi phí 0,38× [simulated], chia theo nhân viên 20 + 20, quyết định ngày 2027-01-05).
