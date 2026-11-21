"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; statsmodels là tuỳ chọn, chỉ dùng để đối chiếu power ở D1)
Không cần khoá API. Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.

Thực hiện: Nguyễn Công Tĩnh (làm một mình, kiêm cả bốn vai).
Mọi con số tính từ hai cột *_simulated được in kèm nhãn [simulated].
"""
import math
from statistics import NormalDist

import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
CO_DINH_THANG = 40_000_000   # chi phí cố định của trợ lý, đồng mỗi tháng
YEU_CAU_THANG = 45_000       # khoảng 45.000 yêu cầu hoàn phí mỗi tháng
PHAM_VI = ['noi_dia', 'hang_nang']   # phạm vi pilot chọn sau A3
SIM = '[simulated]'


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng.
    Lần chạy thứ i xảy ra khi i-1 lần trước đều sai: tổng (1-p)^(i-1), i=1..k = (1-(1-p)^k)/p."""
    if k is None:
        return 1 / p
    return (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    if k is None:
        return 1.0
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy.
    = số lần chạy kỳ vọng / xác suất thành công; với mọi k đều bằng 1/p (k triệt tiêu)."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')
    print(f'  so_lan_chay_ky_vong(0.8, 2)               = {so_lan_chay_ky_vong(0.8, 2):.2f}')
    print(f'  so_lan_chay_ky_vong(0.8)                  = {so_lan_chay_ky_vong(0.8):.2f}')
    print(f'  he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) = {he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc, so_yc.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi (lần lỗi vẫn tốn tiền).
    - xem_lai, lam_lai: số phút (cột *_simulated) × luong_phut. Đây là số GIẢ LẬP, ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong' (mẫu số chỉ đếm việc thành công).
    - max_lan_chay: bỏ lần chạy có attempt > giới hạn; yêu cầu có so_lan_chay > giới hạn coi là
      chuyen_nhan_vien, phút xem lại và làm lại của yêu cầu đó bằng 0.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(token=tien_token.sum(), tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong,
                thanh_cong=thanh_cong, cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
                so_yc=len(reqs))


def tieu_de(chu):
    print('\n' + '=' * 78 + f'\n{chu}\n' + '=' * 78)


# ---------- Nhiệm vụ A ----------
def nhiem_vu_a(runs, reqs):
    tieu_de('A2 · Mô hình chi phí từ trace (1.200 yêu cầu)')
    kq = mo_hinh(runs, reqs)
    nhan = dict(token='đo từ trace', tool='đo từ trace', chay_lai='đo từ trace',
                xem_lai=SIM, lam_lai=SIM, tong='có phần simulated', thanh_cong='',
                cps=SIM, hoa_don_moi_yc='đo từ trace', so_yc='')
    for ten, gia_tri in kq.items():
        print(f'{ten:16s} {gia_tri:>14,.1f}  {nhan[ten]}')
    print(f'  Số lần gọi tool: {runs.tool_calls.sum():,}; phút xem lại: {reqs.phut_xem_lai_simulated.sum():,} '
          f'{SIM}; phút làm lại: {reqs.phut_lam_lai_simulated.sum():,} {SIM}')
    print(f'  Chi phí mỗi việc thành công / hoá đơn mỗi yêu cầu = {kq["cps"] / kq["hoa_don_moi_yc"]:.1f} lần {SIM}')
    for ten in ['token', 'tool', 'xem_lai', 'lam_lai']:
        print(f'  Tỉ trọng {ten:8s}: {kq[ten] / kq["tong"] * 100:5.1f}%')
    print(f'  Giờ nhân viên (xem lại + làm lại): {(kq["xem_lai"] + kq["lam_lai"]) / kq["tong"] * 100:.1f}% {SIM}')
    khong_tc = kq['so_yc'] - kq['thanh_cong']
    he_thong = (kq['tong'] + khong_tc * BASELINE) / kq['so_yc']
    print(f'  Chi phí cả hệ thống mỗi yêu cầu (cộng 12.000 đ × {khong_tc} ca không thành công): '
          f'{he_thong:,.0f} đ = {he_thong / BASELINE:.2f}× {SIM}')

    tieu_de('A3 · Tách theo loại yêu cầu')
    print(f'{"loai":10s} {"so_yc":>6s} {"ti_le_tc":>9s} {"chay/yc":>8s} {"cps":>9s} {"so 12k":>7s}')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        r = reqs[reqs.loai == loai]
        k = mo_hinh(runs, r)
        print(f'{loai:10s} {len(r):6d} {k["thanh_cong"] / len(r) * 100:8.1f}% {r.so_lan_chay.mean():8.2f} '
              f'{k["cps"]:9,.0f} {k["cps"] / BASELINE:6.2f}×  {SIM}')
    print('\n  Tỉ lệ status == ok theo lần thử (attempt):')
    bang = (runs.merge(reqs[['request_id', 'loai']])
            .assign(ok=lambda d: (d.status == 'ok').astype(float))
            .pivot_table(index='loai', columns='attempt', values='ok', aggfunc=['mean', 'count']))
    print((bang['mean'] * 100).round(1).to_string())
    print('  Số lần chạy ở mỗi attempt:')
    print(bang['count'].to_string())

    tieu_de('A4 · Chi phí cố định, phạm vi noi_dia + hang_nang')
    pv = reqs[reqs.loai.isin(PHAM_VI)]
    k = mo_hinh(runs, pv)
    print(f'  Phạm vi: {len(pv)} yêu cầu, {k["thanh_cong"]} việc thành công, tổng {k["tong"]:,.0f} đ, '
          f'cps {k["cps"]:,.0f} đ {SIM}')
    for ten, he_so in [('45.000 yc/tháng', 1.0), ('một nửa khối lượng', 0.5)]:
        tc_thang = YEU_CAU_THANG * he_so * k['thanh_cong'] / len(reqs)
        co_dinh = CO_DINH_THANG / tc_thang
        tong_viec = k['cps'] + co_dinh
        print(f'  {ten:20s}: {tc_thang:,.0f} việc TC/tháng · cố định {co_dinh:,.0f} đ/việc · '
              f'cps + cố định {tong_viec:,.0f} đ = {tong_viec / BASELINE:.2f}× {SIM}')
    return kq


# ---------- Nhiệm vụ B ----------
def nhiem_vu_b(runs, reqs):
    tieu_de('B1 · Đổi từng yếu tố')
    kich_ban = {
        'Giá token gấp đôi': dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa': dict(gia_vao=13, gia_ra=65),
        'Xem lại gấp đôi': dict(he_so_xem_lai=2),
        'Xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Làm lại gấp đôi': dict(he_so_lam_lai=2),
        'Làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương tăng 25%': dict(luong_phut=2500),
        'Tối đa 2 lần chạy': dict(max_lan_chay=2),
        'Chỉ 1 lần chạy': dict(max_lan_chay=1),
    }
    goc = mo_hinh(runs, reqs)['cps']
    print(f'{"Gốc (A2)":25s} {goc:8,.0f}          {SIM}')
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'{ten:25s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%  {SIM}')

    tieu_de('B2 · Đổi một cặp: giá token gấp đôi + xem lại gấp đôi')
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    rieng = (mo_hinh(runs, reqs, gia_vao=52, gia_ra=260)['cps'] - goc) + \
            (mo_hinh(runs, reqs, he_so_xem_lai=2)['cps'] - goc)
    print(f'  Cặp: {cap:,.0f} đ ({(cap / goc - 1) * 100:+.1f}%); tổng hai tác động riêng: '
          f'{(rieng / goc) * 100:+.1f}% {SIM}')

    tieu_de('B3 · Giới hạn chạy lại: chi phí cả hệ thống cho 1.200 yêu cầu')
    for gh in [1, 2, 3]:
        k = mo_hinh(runs, reqs, max_lan_chay=gh)
        khong_tc = k['so_yc'] - k['thanh_cong']
        he_thong = k['tong'] + khong_tc * BASELINE
        print(f'  {gh} lần: trợ lý {k["tong"]:>11,.0f} đ · không TC {khong_tc:4d} · '
              f'cả hệ thống {he_thong:>11,.0f} đ · cps {k["cps"]:,.0f} đ {SIM}')

    tieu_de('B4 · Xem lại 100% trong phạm vi noi_dia + hang_nang')
    pv = reqs[reqs.loai.isin(PHAM_VI)]
    r_pv = runs[runs.request_id.isin(pv.request_id)]
    co_ok = r_pv[r_pv.status == 'ok'].request_id.nunique()
    so_lam_lai = int((pv.ket_qua == 'lam_lai').sum())
    tc = int((pv.ket_qua == 'thanh_cong').sum())
    may = (r_pv.tokens_in / 1000 * GIA_VAO + r_pv.tokens_out / 1000 * GIA_RA + r_pv.tool_calls * GIA_TOOL).sum()
    tb_lam_lai = reqs.loc[reqs.ket_qua == 'lam_lai', 'phut_lam_lai_simulated']
    print(f'  {len(pv)} yêu cầu; {co_ok} có ít nhất một lần chạy ok; {so_lam_lai} ca lam_lai; {tc} việc TC')
    print(f'  Token + tool của mọi lần chạy trong phạm vi: {may:,.0f} đ')
    print(f'  Phút làm lại trung bình mỗi ca lam_lai (toàn mẫu): {tb_lam_lai.mean():.1f}, '
          f'trung vị {tb_lam_lai.median():.1f} {SIM}')
    for phut_lam_lai in [9, round(tb_lam_lai.mean(), 1)]:
        tong = co_ok * 5 * LUONG_PHUT + so_lam_lai * phut_lam_lai * LUONG_PHUT + may
        cps = tong / tc
        # hoà vốn: thời gian xem lại x sao cho cps = 12.000
        x = (BASELINE * tc - may - so_lam_lai * phut_lam_lai * LUONG_PHUT) / (co_ok * LUONG_PHUT)
        print(f'  Làm lại {phut_lam_lai} phút/ca: tổng {tong:,.0f} đ → {cps:,.0f} đ/việc = '
              f'{cps / BASELINE:.2f}× {SIM}; hoà vốn khi xem lại ≤ {x:.1f} phút')
        print(f'    Tiền xem lại chiếm {co_ok * 5 * LUONG_PHUT / tong * 100:.0f}% tổng')


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức trong docs/du_lieu_va_cong_thuc.md)."""
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc=0.02):
    return 1 + (m - 1) * icc


def power_hai_ti_le(p1, p2, n, alpha=0.05):
    """Power khi mỗi nhóm có n mẫu hiệu dụng (effect size Cohen h, giống statsmodels NormalIndPower)."""
    try:
        from statsmodels.stats.proportion import proportion_effectsize
        from statsmodels.stats.power import NormalIndPower
        return NormalIndPower().power(effect_size=abs(proportion_effectsize(p2, p1)), nobs1=n,
                                      alpha=alpha, ratio=1.0)
    except ImportError:
        h = abs(2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1)))
        z = NormalDist().inv_cdf(1 - alpha / 2)
        nd = NormalDist()
        return nd.cdf(h * math.sqrt(n / 2) - z) + nd.cdf(-h * math.sqrt(n / 2) - z)


def nhiem_vu_d(reqs, icc=0.02):
    tieu_de('D1 · Cỡ mẫu (baseline 0,70; +5 điểm; alpha 0,05; power 0,8; ICC 0,02)')
    n5 = co_mau(0.70, 0.75)
    n6 = co_mau(0.70, 0.76)
    print(f'  a) Chia theo yêu cầu: {n5:,} yêu cầu mỗi nhóm')
    de75 = he_so_thiet_ke(75, icc)
    n_b = math.ceil(n5 * de75)
    print(f'  b) Theo nhân viên, m=75: DE = {de75:.2f}; n = {n_b:,.0f} mỗi nhóm → '
          f'{math.ceil(n_b / 75)} người mỗi nhóm, tổng {2 * math.ceil(n_b / 75)} > 40 → KHÔNG đủ người')
    print(f'  c) 20 nhân viên mỗi nhóm: cỡ mẫu hiệu dụng tối đa < c/ICC = {20 / icc:,.0f} < {n5:,} → KHÔNG đạt')
    print(f'  d) 6 depot mỗi nhóm: cỡ mẫu hiệu dụng tối đa < {6 / icc:,.0f}')
    # e) 20m / (1 + (m-1) icc) >= n6  →  m >= n6 (1 - icc) / (20 - n6 icc)
    m_min = math.ceil(n6 * (1 - icc) / (20 - n6 * icc))
    print(f'  e) Mức chênh 6 điểm cần {n6} mỗi nhóm; 20 người mỗi nhóm → m ≥ {m_min} yêu cầu mỗi người '
          f'(DE = {he_so_thiet_ke(m_min, icc):.2f}; n hiệu dụng = {20 * m_min / he_so_thiet_ke(m_min, icc):.0f})')
    print(f'     Power nếu tác động thật chỉ 5 điểm với n hiệu dụng {n6}: {power_hai_ti_le(0.70, 0.75, n6):.2f}')
    print(f'     Tổng yêu cầu pilot: 40 × {m_min} = {40 * m_min:,} '
          f'(~{40 * m_min / 1500:.1f} ngày khối lượng toàn công ty)')

    tieu_de('D3 · Tỉ lệ mo_lai_trong_7_ngay hiện tại (trước khi đặt luật an toàn)')
    print(f'  Toàn mẫu: {reqs.mo_lai_trong_7_ngay.mean() * 100:.2f}% ({reqs.mo_lai_trong_7_ngay.sum()}/{len(reqs)})')
    pv = reqs[reqs.loai.isin(PHAM_VI)]
    print(f'  Phạm vi noi_dia + hang_nang: {pv.mo_lai_trong_7_ngay.mean() * 100:.2f}% '
          f'({pv.mo_lai_trong_7_ngay.sum()}/{len(pv)})')
    for loai, g in reqs.groupby('loai'):
        print(f'    {loai:10s}: {g.mo_lai_trong_7_ngay.mean() * 100:5.2f}%')
    print(f'  Tỉ lệ lam_lai trong phạm vi: {(pv.ket_qua == "lam_lai").mean() * 100:.1f}% '
          f'({(pv.ket_qua == "lam_lai").sum()}/{len(pv)})')


# ---------- Nhiệm vụ E1 · Chỉ số ----------
def nhiem_vu_e(reqs):
    tieu_de('E1 · Ba chỉ số tính thử trên 1.200 yêu cầu')
    chinh = (reqs.dong_trong_24h == 1) & (reqs.mo_lai_trong_7_ngay == 0)
    xem = reqs[reqs.duoc_xem_lai == 1]
    bo_qua = xem.quyet_dinh_xem_lai.isin(['sua', 'bo'])
    an_toan = reqs.mo_lai_trong_7_ngay == 1
    print(f'  Chính  : {chinh.mean() * 100:.2f}% ({chinh.sum()}/{len(reqs)})')
    print(f'  Dùng   : {bo_qua.mean() * 100:.2f}% ({bo_qua.sum()}/{len(xem)}) '
          f'[sua {(xem.quyet_dinh_xem_lai == "sua").sum()}, bo {(xem.quyet_dinh_xem_lai == "bo").sum()}]')
    print(f'  An toàn: {an_toan.mean() * 100:.2f}% ({an_toan.sum()}/{len(reqs)})')
    pv = reqs[reqs.loai.isin(PHAM_VI)]
    c2 = ((pv.dong_trong_24h == 1) & (pv.mo_lai_trong_7_ngay == 0))
    print(f'  Trong phạm vi noi_dia + hang_nang: chính {c2.mean() * 100:.2f}% ({c2.sum()}/{len(pv)}); '
          f'tỉ lệ được xem lại {pv.duoc_xem_lai.mean() * 100:.1f}%')
    print(f'  Tỉ lệ được xem lại toàn mẫu: {reqs.duoc_xem_lai.mean() * 100:.1f}% ({reqs.duoc_xem_lai.sum()}/{len(reqs)})')


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    nhiem_vu_a(runs, reqs)       # TODO CP1 · A2, A3, A4
    nhiem_vu_b(runs, reqs)       # TODO CP2 · B1–B4
    nhiem_vu_d(reqs)             # TODO CP4 · D1 và tỉ lệ mở lại hiện tại
    nhiem_vu_e(reqs)             # CP5 · tính thử ba chỉ số
