# Phiếu chấm hội đồng Gate 2a

Nhóm số n chấm nhóm số n + 1; nhóm cuối chấm nhóm 1. Chấm theo bằng chứng trong hồ sơ, không theo cách trình bày: một đề xuất No-go có lý do bằng số được điểm cao hơn một đề xuất Go bỏ qua con số bất lợi.

> **Ghi chú minh bạch.** Nhóm NhomKhongTen chỉ có một thành viên (Nguyễn Công Tĩnh), làm một mình với sự đồng ý của người ra đề, nên không được ghép cặp duyệt chéo với nhóm n + 1 và không có hồ sơ nhóm khác để chấm. Để không bịa kết quả duyệt chéo (RULES.md), phiếu dưới đây là **tự chấm hồ sơ của chính nhóm theo đúng thang hội đồng**, dùng để soát lỗi trước khi nộp. Nếu giảng viên/coach phân một nhóm để chấm chéo, phiếu sẽ được điền lại bằng kết quả thật trong một commit mới.

- Nhóm chấm (hội đồng): NhomKhongTen (tự chấm, thay cho duyệt chéo)
- Nhóm được chấm: NhomKhongTen (`report/team/ho_so_launch_v0.md`)

| Tiêu chí | 0 điểm | 5 điểm | 10 điểm | Điểm | Lý do (có số) |
| --- | --- | --- | --- | ---: | --- |
| Đề xuất khớp bằng chứng | Mâu thuẫn với số của chính nhóm | Khớp nhưng bỏ qua một con số bất lợi | Khớp, nêu cả con số bất lợi và cách xử lý | 10 | Go có điều kiện khớp chi phí phạm vi 0,38× [simulated]; nêu ra con số bất lợi: power 0,64 ở 5 điểm, xem lại 100% là 0,98–1,03× [simulated], hang_nang mở lại 8,23%, quoc_te 1,88×; mỗi cái có cách xử lý và người phụ trách |
| Số giả lập và phạm vi | Không nhãn; phạm vi "mọi yêu cầu" | Có nhãn hoặc có thu hẹp phạm vi | Nhãn ở mọi số giả lập; phạm vi thu hẹp có lý do bằng số | 10 | Mọi số từ cột `_simulated` có nhãn [simulated]; phạm vi thu hẹp về noi_dia + hang_nang với lý do 0,22× / 0,69× so với quoc_te 1,88× (thành công 27,3%, lần 3 chỉ đúng 2,2%) và doi_tac 0,85× |
| Pilot ra được quyết định | Không đối chứng hoặc thiếu cỡ mẫu | Đủ cỡ mẫu, luật dừng chung chung | Tách được tác động, đủ mẫu, luật dừng có ngưỡng, thời hạn, người có quyền dừng | 10 | Đối chứng cùng thời gian, ngẫu nhiên theo nhân viên, 20 cụm/nhóm; 859/nhóm với ≥ 299 yêu cầu/người cho mde 6 điểm (đánh đổi đã ghi); luật dừng có ngưỡng (2 điểm/6%, 8.000 đ, 40%), thời hạn (3 ngày, 2 tuần, 1 tuần), người dừng (Giám đốc vận hành) |
| **Tổng** | | | | **30 / 30** | Tự chấm, có thể cao hơn điểm hội đồng thật |

**Quyết định của hội đồng:** Go có điều kiện

**Lý do:** Chi phí trong phạm vi 0,38× nhân viên tự làm [simulated] và kế hoạch tách được tác động, nhưng mde phải nới lên 6 điểm (power 0,64 ở 5 điểm) và xem lại 100% xoá gần hết khoản tiết kiệm (0,98–1,03× [simulated]), nên chỉ duyệt khi bốn điều kiện trong hồ sơ được kiểm tra đúng hạn.

**Một câu hỏi cho đội trình:** Mở lại 7 ngày của hang_nang là 8,23% trong đợt chạy thử, cao hơn trần 6% của cả phạm vi; nếu nhóm đối chứng hang_nang cũng cao như vậy, luật an toàn hiện tại có bắt được trợ lý làm hang_nang tệ hơn không?

**Câu trả lời của đội trình (ghi lại tại buổi):** Tự trả lời (không có buổi duyệt chéo): luật an toàn so với đối chứng (+2 điểm) nên vẫn bắt được nếu trợ lý làm tệ hơn; ngoài ra hồ sơ yêu cầu theo dõi riêng hang_nang so với đối chứng cùng loại, và luật chi phí cho phép PM thu hẹp về chỉ noi_dia. Điểm yếu còn lại: số yêu cầu hang_nang nhỏ (158/982 ≈ 16% phạm vi) nên so sánh riêng loại này có power thấp.
