# Thư Mục Kiểm Thử & Đánh Giá — `eval/`
**Dự án:** VLearn AI Tutor (LearnLoop) · Phục vụ Mốc CP3, CP4 và Tiêu chí Đánh giá R4 (Rubric Hackathon AI20k)

---

## 1. Mục Đích & Chuẩn Mực Đánh Giá
Thư mục `eval/` chứa toàn bộ dữ liệu kiểm thử thực nghiệm của nhóm nhằm chứng minh tính triệt tiêu lỗi kiến trúc và đối soát trực diện A/B giữa **Hệ thống cũ (Baseline)** và **LearnLoop Tutor mới**:
- **Bộ Golden Set $\ge 20$ test cases** được trích xuất từ 13.494 lượt chatlog thật (`data/vlearn-pack/chatlog/tutor_turns.csv`).
- **Báo cáo kết quả đo lường tự động** đối chiếu trực tiếp với Quality Bar đã cam kết.
- **Script kiểm thử tự động** chạy trực tiếp qua live HTTP API để bất kỳ giám khảo hay người ngoài nhóm nào cũng có thể kiểm chứng lại kết quả độc lập.

---

## 2. Cấu Trúc Thư Mục Chuẩn Hóa

```
eval/
├── README.md                                                # Tài liệu mô tả cấu trúc, taxonomy và hướng dẫn chạy test
├── golden_set_20_cases.json                                 # Bộ 20 Test Cases chuẩn hóa (JSON format, phủ đủ 4 lớp chỗ khó)
├── Bao_cao_kiem_chung_toan_bo_20_test_cases_tu_dong.xlsx     # Bảng Master đối soát A/B 20 test cases, đo lường %, độ dài, độ trễ
└── run_full_evaluation_suite.py                             # Script Python tự động thực thi trọn bộ test suite qua API và xuất Excel
```

*(Ghi chú: Toàn bộ các file nháp, code sinh trung gian và bảng biểu phụ đã được chuyển vào thư mục lưu trữ `archive/eval-legacy/` để đảm bảo thư mục `eval/` đạt chuẩn tinh gọn, minh bạch nhất).*

---

## 3. Cấu Trúc Bộ Golden Set (`golden_set_20_cases.json`)
Bộ Golden Set gồm đúng 20 trường hợp kiểm thử, tuân thủ nghiêm ngặt cơ cấu quy định tại `02-guide.md` §2.6:
1. **Phủ đủ 4 lớp chỗ khó theo Taxonomy (R3 & R4):**
   - *Lớp ① (Nguồn sự thật):* 4 cases (STT 1–4) — Giải quyết lỗi bịa số trang 304, nhầm token index 957, sập RAG cross-slide.
   - *Lớp ② (Mơ hồ / Thiếu thông tin):* 3 cases (STT 11–13) — Chặn các thao tác bôi nhầm chữ cái đơn 'r', mũi tên '--> &' trong 0ms.
   - *Lớp ③ (Ngoài phạm vi / Thẩm quyền):* 3 cases (STT 4, 14, 15) — Thừa nhận trung thực thuật toán PPO chưa dạy, chặn prompt injection.
   - *Lớp ④ (Đặc thù domain AI):* 10 cases (STT 5–10, 16–20) — Phân tầng nhận thức cho các khái niệm khó (Attention, Context rot, BERT vs GPT).
2. **Căn cứ dữ liệu thật:** Có tới **14 / 20 test cases** được trích xuất trực tiếp từ các mã Turn ID có thật trong log (`T12701`, `TC_LIVE_04`, `T00213`, `T10457`, `T12378`, `T12377`, `T12379`, `T10506`, `T00185`, `T00924`, `T00823`, v.v.).

Mỗi test case trong file JSON có cấu trúc tường minh:
```json
{
  "stt": 1,
  "group_id": 1,
  "group_name": "Nhóm 1: Ảo giác số trang & Metadata",
  "category": "Liệt kê mô hình & Giới hạn slide",
  "turn_id_base": "T12701",
  "user_input": "cho tôi 5 loại mô hình xử lý ngôn ngữ được dùng nhiều nhất",
  "slide_key": "d1",
  "custom_query": "cho tôi 5 loại mô hình xử lý ngôn ngữ được dùng nhiều nhất",
  "baseline_flaw": "Cite 'trang 304 [trang 304]' ảo giác (slide chỉ có 8 trang); dài 1.472 ký tự.",
  "baseline_len": 1472,
  "baseline_cite": "ẢO GIÁC [trang 304]",
  "expected_behavior": "Trả lời đúng 5 mô hình trên slide Trang 8 (RNN, LSTM, Transformer, BERT, GPT), cite đúng Trang 8, không bịa số trang."
}
```

---

## 4. Quality Bar & Kết Quả Thực Nghiệm

| Chỉ số Chất lượng | Quality Bar Cam Kết (CP4) | Kết quả Đo lường Thực tế | Trạng thái Đạt |
| :--- | :---: | :---: | :---: |
| **Tỷ lệ Pass Golden Set** | $\ge \mathbf{85.0\%}$ | **$100.0\%$ (20 / 20 Cases)** | **VƯỢT CHUẨN** |
| **Tỷ lệ Trích dẫn Nguồn Hợp lệ** | $\ge \mathbf{95.0\%}$ | **$100.0\%$** | **VƯỢT CHUẨN** |
| **Tỷ lệ Ảo giác Số trang** | $\mathbf{0.0\%}$ | **$0.0\%$** (Triệt tiêu 100% trang ảo) | **VƯỢT CHUẨN** |
| **Độ dài Phản hồi Trung bình** | $\le \mathbf{280}$ ký tự | **$205.2$ ký tự** (Giảm 80.5% văn bản rác) | **VƯỢT CHUẨN** |
| **Độ trễ trung bình** | $< 4.000$ ms | **$2.682$ ms** (0 ms cho Guardrail) | **ĐẠT** |

---

## 5. Hướng Dẫn Tái Hiện Kết Quả (Reproducibility)
Bất kỳ ai cũng có thể tự động chạy lại toàn bộ 20 test case bằng 2 bước đơn giản:

```bash
# Bước 1: Khởi động backend server (nếu chưa chạy)
python3 server.py

# Bước 2: Chạy bộ kiểm thử tự động
python3 eval/run_full_evaluation_suite.py
```
Kết quả đo lường trực tiếp sẽ được in ra console và tự động cập nhật vào file `eval/Bao_cao_kiem_chung_toan_bo_20_test_cases_tu_dong.xlsx`.
