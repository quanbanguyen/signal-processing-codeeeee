# Mô phỏng đầu-cuối giao thoa kế vô tuyến UHF 4 phần tử quan sát bức xạ Mặt Trời ở 610 MHz

**End-to-End Simulation of a Four-Element UHF Radio Interferometer for Solar Radio Observation at 610 MHz**

Đồ án tốt nghiệp — Trường Điện – Điện tử, Đại học Bách Khoa Hà Nội (HUST)

| | |
|---|---|
| **Tác giả** | Nguyễn Bá Quân |
| **MSSV** | 20224350 |
| **Email** | quan.nb224350@sis.hust.edu.vn |
| **Báo cáo LaTeX** | [`baocaodatn/datn/`](baocaodatn/datn/) (biên dịch bằng XeLaTeX, xem README riêng trong thư mục) |

---

## 1. Giới thiệu

Đồ án xây dựng một pipeline mô phỏng đầu-cuối cho một **giao thoa kế vô tuyến (radio interferometer) gồm 4 anten Yagi-Uda hoạt động ở tần số 610 MHz**, dùng để quan sát bức xạ vô tuyến bùng phát từ Mặt Trời (solar radio burst). Pipeline gồm hai nhánh chính, ghép lại thành một chuỗi mô phỏng thống nhất:

1. **Thiết kế & mô phỏng anten**: dựng mô hình anten Yagi-Uda 610 MHz (kiểu "U-frame", 14 dây dẫn: 4 reflector + folded dipole + 6 director) bằng **NEC-2** thông qua **4NEC2**, kiểm chứng chéo bằng **CST Studio Suite**, sau đó trích xuất giản đồ bức xạ (primary beam) làm đầu vào cho mô phỏng tín hiệu.
2. **Mô phỏng chuỗi tín hiệu giao thoa kế**: dùng dữ liệu flux Mặt Trời thực tế (trạm **SWS Learmonth – RSTN**, 610 MHz) làm nguồn tín hiệu, mô phỏng điện áp thu trên từng anten (nhiễu Johnson, suy hao Friis), tương quan chéo (correlator) giữa các cặp anten, tính toán độ phủ u-v, dựng ảnh dirty image/PSF, và cuối cùng đối chiếu với dữ liệu đo thực địa tại **Hòa Lạc**.

Ngoài ra có một công cụ web phụ trợ (`radio_simulation.html`) để trực quan hóa giản đồ bức xạ anten.

## 2. Kiến trúc pipeline tổng thể

```
 NEC-2 / 4NEC2 (yagi_610_Uframe.nec)
          │  mô phỏng anten Yagi-Uda 610 MHz
          ▼
   4nec2-out/ ──► trích xuất giản đồ bức xạ (primary beam)
          │
          ▼
 primary_beam.py  (class PrimaryBeam, nạp từ .npz)
          │
          ▼                     raw_signal_from_sws/ (SWS Learmonth RSTN)
          │                              │ sws_to_csv.py
          │                              ▼
          │                     file_excel_du_lieu/ (flux Mặt Trời .csv theo ngày)
          │                              │
          ▼                              ▼
        the_newest_heart_of_project.ipynb   (notebook trung tâm — toàn bộ pipeline)
   ┌─────────────────────────────────────────────────────────┐
   │ nạp dữ liệu SWS → vật lý hệ thống (Friis) → bố trí mảng   │
   │ anten → sinh điện áp per-antenna (nhiễu Johnson)          │
   │ → lượng tử hóa 16-bit (IQ) → correlator → u-v coverage    │
   │ → dirty image / PSF → so sánh với đo thực địa Hòa Lạc     │
   └─────────────────────────────────────────────────────────┘
          │
          ▼
   IQ_data_for signal_processing/   Cell_I_Data/   export_thesis_figures.py
   (dữ liệu IQ 16-bit cho xử lý       (kết quả sweep      (hình cho báo cáo)
    tín hiệu / FPGA)                   bố trí mảng)
```

## 3. Cấu trúc thư mục

| Thư mục | Vai trò |
|---|---|
| `baocaodatn/datn/` | **Báo cáo LaTeX chính thức** của đồ án (`main.tex`, `chapters/`, `figures/`, `main.pdf`) |
| `DATN-REFERENCE/` | Tài liệu tham khảo: báo cáo giao thoa kế, mã nguồn tham khảo dự án DLITE (GNU Radio), tài liệu thuật toán tái tạo ảnh |
| `toolmophong_APSYNSIM_trengithub/` | Repo con (APSYNSIM) — công cụ mô phỏng giao thoa kế mã nguồn mở, dùng tham khảo/đối chiếu |
| `4nec2-out/` | Output thô từ mô phỏng NEC-2 cho anten Yagi 2 phần tử ở nhiều khoảng cách |
| `baocaomophonganten4nec2/` | Báo cáo mô phỏng anten bằng 4NEC2, dữ liệu primary beam, script parse output NEC |
| `file_trichxuat_primary beam_cua_anten/` | Phiên bản trước của notebook chính, primary beam đã trích xuất, các file `.nec` anten 2 phần tử |
| `raw_signal_from_sws/` | Dữ liệu thô `.txt` từ trạm SWS Learmonth (RSTN) theo ngày |
| `file_excel_du_lieu/` | Dữ liệu flux Mặt Trời dạng `.csv` (đã chuyển đổi từ `.txt` gốc) |
| `IQ_data_for signal_processing/` | Dữ liệu IQ đã lượng tử hóa (16-bit, fc = 610 MHz, 4 anten) xuất cho xử lý tín hiệu/FPGA |
| `Cell_I_Data/` | Dữ liệu sweep bố trí mảng anten (Case 2), hình cho báo cáo |
| `avg_power_thu_từ project_a_long/` | Ảnh kết quả công suất thu giao thoa 610 MHz theo từng ngày |
| `file_trichxuat_primary beam_cua_anten/`, `Cell_I_Data/` | Xem ở trên |
| `tong hop file note và bao cao/` | Ghi chú, chương thảo luận, sơ đồ flowchart các cell notebook |
| `project ngoai doi/` | Tài liệu tham khảo từ nhóm khác (báo cáo Yagi-Uda, ảnh anten thực tế) |

> Các thư mục dữ liệu lớn (`.npz`, `.pkl`, `Cell_H_Data/`, `Cell_I_Data/`, `.ipynb_checkpoints/`) không được Git theo dõi — xem [`.gitignore`](.gitignore).

## 4. Notebook trung tâm — `the_newest_heart_of_project.ipynb`

Đây là notebook chứa **toàn bộ pipeline mô phỏng tín hiệu/giao thoa kế**, gồm các cell chính theo trình tự:

1. Cấu hình chung → nạp dữ liệu SWS (ban ngày) → nạp primary beam thật từ 4NEC2
2. Vật lý hệ thống (phương trình Friis) → bố trí mảng anten
3. Sinh chuỗi điện áp per-antenna (mô hình nhiễu Johnson) → lượng tử hóa 16-bit, xuất hex
4. Trực quan hóa (Plotly) → correlator → tính u-v coverage (ENU → XYZ → uvw)
5. Dựng dirty image, PSF cho nhiều kịch bản bố trí mảng (1D, cross 4-anten, tam giác kiểu DLITE)
6. Case 2: mảng mở rộng 2D, forward model đĩa Mặt Trời → xuất hình cho báo cáo → sweep hình học mảng
7. Đối chiếu kết quả mô phỏng với dữ liệu đo thực tế tại Hòa Lạc (20/03/2025)

Do file `.ipynb` khá lớn (~13 MB), các file `nb_cell_index.txt`, `nb_array_search.txt`, `nb_search_out.txt`, `cell_13.txt`…`cell_18.txt` ở thư mục gốc là **bản trích xuất nội dung từng cell** để tra cứu nhanh mà không cần mở notebook.

## 5. Script Python chính (thư mục gốc)

| File | Chức năng |
|---|---|
| `interfsim.py` | Engine giao thoa kế lõi (mảng East-North 2D): mô phỏng điện áp per-antenna có nhiễu Johnson, mô hình thuận van Cittert–Zernike sinh visibility từ sky model (theo Thompson–Moran–Swenson) |
| `primary_beam.py` | Nạp giản đồ bức xạ trích từ 4NEC2 (`.npz`), cung cấp class `PrimaryBeam` dùng làm primary beam trong pipeline |
| `sws_to_csv.py` | Chuyển dữ liệu thô trạm RSTN Learmonth (`.txt`) sang `.csv`, tách phần dữ liệu ban ngày |
| `simulate-iq-signal-from-sws.py` | Đọc dữ liệu flux Mặt Trời từ CSV, mô phỏng tín hiệu IQ |
| `transfer-data.py` | Chuyển đổi file `.txt` sang `.csv` (tiện ích đơn giản) |
| `export_thesis_figures.py` | Xuất từng hình riêng lẻ (`.png`) cho báo cáo, từ dữ liệu Case 2 |
| `make_figure_4_1.py` | Sinh sơ đồ khối pipeline (Hình 4.1 trong báo cáo) — kết quả: `figure_4_1_pipeline.png` |
| `import numpy as np, json.py` | Chuyển primary beam (`UFRAME_primary_beam_610MHz.npz`) sang JSON cho công cụ web `radio_simulation.html` |

## 6. Công cụ web phụ trợ — `radio_simulation.html`

Trang **"Mô phỏng Giao thoa Vô tuyến Thiên văn"** — công cụ tĩnh chạy trong trình duyệt, dùng để trực quan hóa giản đồ bức xạ (primary beam) đã trích xuất từ 4NEC2 (đọc dữ liệu JSON sinh bởi script ở mục 5).

## 7. Nguồn dữ liệu thực tế

- **Flux Mặt Trời**: trạm giám sát **SWS Learmonth (RSTN — Radio Solar Telescope Network)**, tần số 610 MHz.
- **Dữ liệu đối chiếu thực địa**: đo đạc tại **Hòa Lạc**, dùng để kiểm chứng kết quả mô phỏng (xem cell cuối của notebook trung tâm).

## 8. Công cụ & môi trường

- **Python** — thư viện chính: `numpy`, `scipy` (`interpolate`, `ndimage`, `special`), `matplotlib`, `plotly`, `dataclasses`, `concurrent.futures`.
- **NEC-2 / 4NEC2** — mô phỏng anten Yagi-Uda (file `.nec`, output `.out.txt`).
- **CST Studio Suite** — kiểm chứng chéo kết quả mô phỏng anten (xem hướng dẫn trong [`HuongDan_Yagi_4NEC2_CST.md`](HuongDan_Yagi_4NEC2_CST.md)).
- **Jupyter Notebook** — môi trường chạy pipeline chính.
- **LaTeX (XeLaTeX)** — biên soạn báo cáo đồ án trong `baocaodatn/datn/`.

## 9. Hướng dẫn tái lập nhanh

1. Mô phỏng/parse anten: chạy mô hình `yagi_610_Uframe (1).nec` trong 4NEC2 → output vào `4nec2-out/`, đối chiếu hướng dẫn trong `HuongDan_Yagi_4NEC2_CST.md`.
2. Chuẩn bị dữ liệu Mặt Trời: `python sws_to_csv.py` để chuyển dữ liệu thô trong `raw_signal_from_sws/` sang `file_excel_du_lieu/`.
3. Mở `the_newest_heart_of_project.ipynb` và chạy tuần tự các cell — đây là bước chạy toàn bộ pipeline mô phỏng giao thoa kế.
4. Xuất hình cho báo cáo: `python export_thesis_figures.py` / `python make_figure_4_1.py`.
5. Biên dịch báo cáo: xem hướng dẫn trong `baocaodatn/datn/README.md`.

## 10. Tài liệu tham khảo trong repo

- `DATN-REFERENCE/` — báo cáo giao thoa kế tham khảo, mã nguồn dự án DLITE, tài liệu thuật toán tái tạo ảnh.
- `toolmophong_APSYNSIM_trengithub/` — công cụ mô phỏng giao thoa kế mã nguồn mở APSYNSIM (dùng đối chiếu).
- `project ngoai doi/` — tài liệu tham khảo từ nhóm khác về anten Yagi-Uda.
