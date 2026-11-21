# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

Số tính bằng `src/lab13.py` (hàm `nhiem_vu_e`) trên 1.200 yêu cầu của đợt chạy thử. Ba chỉ số E1 tính từ các cột không có đuôi `_simulated` (đo từ dữ liệu chạy thử); số lấy từ bảng độ nhạy ghi nhãn `simulated`.

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | **82,83%** (994/1.200); trong phạm vi noi_dia + hang_nang 92,26% (906/982) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | **27,12%** (48/177: sua 41, bo 7) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | **4,25%** (51/1.200); trong phạm vi 3,97% (39/982) |
| Dùng | Nhóm tự đề xuất: **Tỉ lệ nhân viên nhóm can thiệp thật sự dùng trợ lý** | Số yêu cầu trong phạm vi của nhóm can thiệp có event `agent_suggestion_shown` mà nhân viên mở và gửi (`staff_review_decision` hoặc gửi thẳng), chia tổng số yêu cầu trong phạm vi của nhóm can thiệp; theo tuần, theo staff_id | Không cần tính |
| An toàn | Nhóm tự đề xuất: **Tỉ lệ đơn hoàn sai tiền qua kiểm tra mẫu** (bắt lỗi ngầm như ca 5, 17) cùng **số ca hoàn trùng** (ca 20) | Số đơn trong mẫu 100 đơn/tuần có `so_tien_da_hoan` khác `so_tien_dung` (event `audit_sample_checked`), chia 100; số mã đơn có từ 2 `refund_ledger_write` ket_qua = ok | Không cần tính |

Cách viết đúng: "chỉ số chính **trong đợt chạy thử là 82,83%**". Không viết "trợ lý đã nâng chỉ số từ 0,70 lên 0,83": đợt chạy thử không có nhóm đối chứng, và mẫu gồm cả các loại sẽ bị loại khỏi pilot.

## Danh sách event

Mười event, mỗi event có `trace_id` để nối với trace của agent (`logix_runs.csv`).

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, depot, loai, so_tien, arm (tro_ly/doi_chung), staff_id, trace_id | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | request_id, attempt, tokens_in, tokens_out, tool_calls, status, phien_ban_bang_gia, trace_id | Sau mỗi lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, can_xem_lai (0/1), trace_id | Khi gợi ý hiện cho nhân viên |
| `staff_review_decision` | Nhân viên | staff_id, quyet_dinh (giu/sua/bo), phut_xem_lai (đo thật), trace_id | Khi bấm gửi / sửa / bỏ |
| `staff_rework_completed` | Nhân viên | staff_id, phut_lam_lai (đo thật), ly_do, trace_id | Khi làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, ma_don, so_tien, ket_qua (ok/loi), ma_loi, trace_id | Khi ghi sổ hoàn tiền |
| `handoff_to_staff` | Agent | reason (thieu_du_lieu/ngoai_pham_vi/het_lan_chay/…), tom_tat, trace_id | Khi chuyển cho nhân viên |
| `ticket_closed` | Hệ thống ticket | closed_at, created_at, kenh_thong_bao, trace_id | Khi đóng yêu cầu |
| `ticket_reopened` | Khách / hệ thống ticket | reopened_at, reason (so_tien/chua_nhan/khac), trace_id | Khi khách mở lại |
| `audit_sample_checked` | Kế toán | ma_don, so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id | Hằng tuần, mẫu 100 đơn |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, event dùng để tính.

- Chính: `ticket_closed` (closed_at − created_at ≤ 24 giờ) và không có `ticket_reopened` trong 7 ngày, mẫu số là `refund_request_created` → đo được.
- Dùng (bỏ qua gợi ý): `staff_review_decision` với quyet_dinh ∈ {sua, bo} chia số `staff_review_decision` → đo được.
- An toàn (lỗi lọt đến khách): `ticket_reopened` trong 7 ngày chia `refund_request_created` → đo được.
- Dùng tự đề xuất: `agent_suggestion_shown` + `staff_review_decision` theo staff_id, mẫu số `refund_request_created` có arm = tro_ly → đo được.
- An toàn tự đề xuất: `audit_sample_checked` (lệch tiền) và `refund_ledger_write` (đếm ok trùng ma_don) → đo được.
- Chi phí mỗi việc thành công (luật dừng chi phí): `agent_run_completed` (token, tool), `staff_review_decision.phut_xem_lai` và `staff_rework_completed.phut_lam_lai` (thay cho hai cột simulated) → đo được, hết phụ thuộc số giả lập sau tuần 1.

## E2 · Rủi ro kinh tế

Số lấy từ bảng độ nhạy trong `bang_chi_phi.md`.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, từ 4.472 đ lên 6.787 đ mỗi việc thành công [simulated] | Tỉ lệ lam_lai theo tuần > 7% trong phạm vi (đợt chạy thử: 4,9%, 48/982), từ `staff_rework_completed` | Thu hẹp về noi_dia; rà 20 trace làm lại gần nhất tìm nguyên nhân gốc; không mở thêm hang_nang | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ = 0,98× (làm lại 9 phút) hoặc 12.415 đ = 1,03× (làm lại 15,3 phút như dữ liệu) [simulated]; xem lại gấp đôi đã +40,7% [simulated] | % yêu cầu được xem lại còn > 50% cuối bước 0.25, hoặc phut_xem_lai trung bình > 5 phút (hoà vốn 5,1 / 4,8 phút [simulated]) | Giảm xem lại theo bậc (100% → 50% → 20%) khi tỉ lệ sua + bo < 15%; giữ xem lại 100% cho hang_nang lâu hơn | Trưởng nhóm CSKH |
| Lương nhân viên tăng | +23,1%, lên 5.506 đ mỗi việc khi lương tăng 25% [simulated] | Đơn giá phút nhân viên trong kỳ điều chỉnh lương | Cập nhật `luong_phut` trong mô hình, tính lại ngưỡng 8.000 đ của luật dừng | PM trợ lý hoàn phí |
| Khối lượng thấp hơn dự kiến | Cố định 40 triệu đ/tháng: +1.185 đ/việc ở 45.000 yêu cầu/tháng, +2.370 đ/việc nếu còn một nửa (5.784 đ = 0,48×) [simulated] | Số việc thành công theo tuần < 50% kế hoạch | Không mở rộng pilot; đàm phán lại phần cố định theo khối lượng | Giám đốc vận hành LogiX-VN |
