# AI SPEC — VLearn Grounded & Calibrated Tutor · Nhóm LearnLoop · Zone E403
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở  
Loại: [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới  

---

## §1. User & Job
- **Job executor + workflow:** Học viên khóa AI20k đang học và xem lại bài giảng trực tiếp qua slide trên nền tảng VLearn; khi gặp một thuật ngữ khó hiểu, học viên bôi đen từ khóa hoặc bấm câu hỏi mẫu để được giải thích ngay trong lúc bài giảng đang diễn ra.
- **Core JTBD (Đồng bộ chuẩn từ `jtbd-worksheet.md`):** Xác thực và làm rõ ngay lập tức bản chất các khái niệm kỹ thuật khó hiểu trên bài giảng dựa trên tài liệu chính thống trong vòng 10 giây để không bị sai lệch kiến thức hoặc đứt mạch tư duy. *(Chuẩn công thức: [verb] + [object] + [contextual clarifier], tuyệt đối không chứa chữ AI/tên sản phẩm)*
- **Problem statement:** Khi học viên cần làm rõ một khái niệm trên bài giảng, người hỗ trợ thường đưa ra các câu trả lời phỏng đoán không có nguồn kiểm chứng hoặc tuôn cả bài văn dài hàng nghìn ký tự, khiến người học bị quá tải nhận thức và hoang mang về tính chính xác học thuật. *(Không chứa chữ AI/tên sản phẩm)*
- **Three Core Job Stories (Trích xuất từ `jtbd-worksheet.md`):**
  1. *JS1 (Grounding & Citation):* Khi gặp đoạn giải thích khó hiểu trên slide $\rightarrow$ muốn được giải thích súc tích kèm trích dẫn số trang/mã đoạn bài giảng $\rightarrow$ để nắm vững bài mà không phải tua lại cả video.
  2. *JS2 (Hallucination Defense):* Khi tò mò hỏi khái niệm nâng cao chưa dạy (VD: PPO) $\rightarrow$ muốn được thông báo rõ ràng nội dung nằm ngoài phạm vi $\rightarrow$ để tránh hiểu nhầm kiến thức chắp vá.
  3. *JS3 (Socratic Probing):* Khi bôi đen từ khóa ngắn/mơ hồ $\rightarrow$ muốn được gợi mở đào sâu 2 khía cạnh $\rightarrow$ để nhận câu trả lời đúng kích cỡ nhu cầu nhận thức.
- **Evidence (Dữ liệu khai phá từ 13.494 turns log thực tế trong `data/vlearn-pack/`):**
  - **Số liệu mining:**
    - **28.02%** câu trả lời (3.781 / 13.494 lượt chat) hoàn toàn mất nguồn trích dẫn (`citations = []`).
    - **22.73%** câu hỏi bôi đen/chọn mẫu (`is_preset = True`) bị chatbot chọn hành vi **tuôn lý thuyết dài dòng một chiều** (chiếm 89.87%), độ dài trung bình lên tới **1.051 ký tự** (~213 từ).
    - Chỉ **0.21%** (28 / 13.494 lượt) tutor đặt câu hỏi gợi mở đào sâu (Socratic Probing).
    - Hiện tượng **ảo giác số trang (Phantom Citations)** xuất hiện trong 15%–20% câu hỏi bôi đen (cite nhầm token index thô thành `[trang 957 trang 1077]` hoặc bịa `[trang 304]` dù slide chỉ có 8 trang).
  - **≥5 Quote/ví dụ nguyên văn có mã đối soát từ dữ liệu thật:**
    1. *Turn `T10457`:* Học viên hỏi thuật toán PPO -> Bot tự bịa bài văn dài **988 ký tự** trôi nổi hoàn toàn không có nguồn, không cảnh báo bài chưa dạy.
    2. *Turn `T12701`:* Học viên hỏi "5 loại mô hình xử lý ngôn ngữ" -> Bot xả bài văn dài **1.472 ký tự** và cite ảo giác `[trang 304]` (trong khi slide bài giảng chỉ có 8 trang).
    3. *Turn `TC_LIVE_04`:* Học viên bôi đen từ "Transformer" -> Bot nhầm token index thành `[trang 957 trang 1077]`, box trích dẫn bị rỗng, văn bản dài **1.328 ký tự**.
    4. *Turn `T00213`:* Học viên hỏi bài Delimiters ở slide Trang 55 -> Bot mâu thuẫn metadata, cite nhầm sang `[trang 70]` dài **845 ký tự**.
    5. *Turn `T00185`:* Học viên bôi nhầm 1 ký tự rác `"r"` -> Bot vẫn gọi RAG tốn chi phí rồi xả **240 ký tự** xin lỗi lòng vòng thay vì chặn lỗi tức thì.

---

## §2. Impact & quyết định chọn
- **Bảng impact so sánh 3 ứng viên bài toán:**
  | Ứng viên bài toán | Quy mô ảnh hưởng | Tần suất | Chi phí sai lầm mỗi lần (Cost-of-Error) | Tính khả thi trong 48h | Đánh giá |
  |---|---|---|---|---|---|
  | **1. Tối ưu VLearn Tutor: Micro-summary + Socratic Probing + Dynamic Grounding (Đề A1)** | **1.617 học viên** (~100% người dùng xem slide) | Rất cao (liên tục mỗi buổi học) | Mất 15–30 phút tra cứu lại, sai lệch kiến thức thi, mất niềm tin vào hệ sinh thái học tập | Rất cao (đầy đủ chatlog thật, slide PDF và 6 file transcript) | **CHỌN** |
  | 2. Chatbot hỏi đáp chung toàn khóa học | ~40% học viên | Thấp–Trung bình (khi có thắc mắc bài tập lớn) | Thấp (học viên tự hỏi bạn bè hoặc TA) | Thấp (phạm vi quá rộng, thiếu benchmark chuẩn) | ĐÃ LOẠI |
  | 3. Tự động sinh bài tập trắc nghiệm (Quiz) từ slide | ~30% học viên chủ động | Thấp (cuối mỗi chương) | Trung bình (sinh câu hỏi lệch trọng tâm) | Trung bình (dễ làm bề nổi, khó kiểm soát chất lượng sư phạm) | ĐÃ LOẠI |
- **Ứng viên ĐÃ LOẠI + vì sao:** Ứng viên 2 và 3 bị loại vì chi phí sai lầm không quá nghiêm trọng và là tính năng mở rộng (nice-to-have). Chưa giải quyết "vết thương chí mạng" đang làm đứt gãy trải nghiệm học tập là hội chứng xả văn bản và trích dẫn số trang ma.
- **Ứng viên CHỌN + vì sao (bằng con số):** Chọn **Ứng viên 1** vì:
  - Giải quyết trực tiếp điểm nghẽn của **13.494 lượt chat thực tế** (loại bỏ 28.02% lỗi mất nguồn và 89.87% lỗi quá tải chữ).
  - Có thể đo lường định lượng chính xác 100% trước/sau qua bộ Golden Set 20 Test Cases đối soát trực diện A/B.

---

## §3. Giải pháp tương tự đã nghiên cứu
- **Google NotebookLM:**
  - *Flow:* Nhận tài liệu $\rightarrow$ Học viên hỏi $\rightarrow$ Trả lời gắn số trích dẫn trực tiếp $\rightarrow$ Click vào số trích dẫn nhảy tới đúng vị trí nguồn.
  - *Đáng học:* Cơ chế Source Grounding cực kỳ nghiêm ngặt; không bịa số trang hoặc trích dẫn rỗng khi tài liệu không đề cập.
  - *Đáng né:* Quá thụ động, câu trả lời còn mang tính tra cứu tài liệu một chiều, thiếu định hướng sư phạm cho người học.
  - *LearnLoop khác biệt:* Áp dụng nguyên tắc **Progressive Disclosure** (giới hạn < 250 ký tự) kết hợp **Socratic Probing** (chủ động sinh 2 nút gợi ý đào sâu đa tầng) và trích dẫn kép đồng thời Slide PDF + Transcript MD.
- **Khan Academy Khanmigo:**
  - *Flow:* Đóng vai trò gia sư định hướng (Socratic Tutor), liên tục hỏi ngược học viên để khơi gợi tư duy.
  - *Đáng học:* Kỹ thuật hỏi ngược thông minh giúp học viên nhớ lâu và hiểu bản chất.
  - *Đáng né:* Quá cứng nhắc, bắt người học phải trả lời vòng vo ngay cả khi họ chỉ đang cần tra cứu nhanh một định nghĩa cơ bản.
  - *LearnLoop khác biệt:* Phân tầng rõ ràng: Trả lời ngắn gọn ngay bản chất cốt lõi trước, sau đó đưa ra lựa chọn đào sâu tiếp qua nút bấm tiện lợi.

---

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** Khi học viên bôi đen một thuật ngữ trên slide bài giảng VLearn, AI Tutor cung cấp micro-summary dưới 250 ký tự kèm trích dẫn kép Slide-Transcript chính xác và 2 câu hỏi gợi ý Socratic để học viên chủ động đào sâu mà không bị quá tải nhận thức.
- **Non-goals (3 thứ KHÔNG build):**
  1. Không làm chatbot tán gẫu tự do hoặc giải quyết các vấn đề ngoài phạm vi học phần AI.
  2. Không làm công cụ viết code hoặc làm bài tập thay học viên.
  3. Không thay thế vai trò giải đáp chuyên sâu 1-1 của Giảng viên và Trợ giảng trong các buổi chữa bài.
- **Mức prototype nhắm tới:** `[x] Working Prototype` — Ứng dụng Web hoàn chỉnh gồm Slide Viewer PDF đồng bộ hai chiều, kết nối trực tiếp với backend dynamic RAG qua OpenAI Live API (`gpt-4o-mini`).
- **Automation Level:** `[x] Conditional Automation` — Tự động trả lời khi thuật ngữ có căn cứ trong tài liệu; tự động chặn và nhắc nhở trong 0ms khi thao tác lỗi; từ chối trung thực khi vượt thẩm quyền (như thuật toán PPO chưa dạy). *(Lý do cost-of-error: Kiến thức sai lệch làm học viên hiểu sai bản chất mô hình và thi rớt).*
- **§4b. Nguyên tắc HAX & PAIR đã áp dụng:**
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **PAIR: Progressive Disclosure** | Hộp giải thích hiển thị micro-summary 1-3 câu (< 250 ký tự) để học viên nắm nhanh ý chính, ẩn các thông tin chi tiết vào các nút bấm đào sâu Socratic. |
  | **HAX G11: Make clear why the system did what it did** | Badge nguồn hiển thị tách biệt rõ ràng ở chân hộp thoại: `Slide [file.pdf] · Trang N & Transcript [transcript.md] · Đoạn [Mã]` để học viên đối soát 1 chạm. |
  | **HAX G2: Make clear how well the system can do what it can do** | Giới hạn ranh giới rõ ràng: Khi học viên hỏi thuật toán PPO, hệ thống nêu rõ PPO thuộc học phần RLHF chuyên sâu chưa học và từ chối suy đoán bừa. |
  | **HAX G8: Support efficient correction (Dual-layer Guardrail)** | Bộ lọc Guardrail 2 lớp (Client `app.js` + Server `server.py`) chặn đứng trong 0ms các thao tác bôi nhầm chữ cái đơn (`r`), ký hiệu (`--> &`) và hướng dẫn bôi lại trọn vẹn. |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8 kịch bản)
*Bảng cụ thể hóa 4 lớp chỗ khó theo HAX Playbook và PAIR Chapter 6:*

| STT | Tình huống cụ thể | Thuộc lớp chỗ khó | Hành vi mong muốn (Nói gì / Hiện gì / Cho user làm gì) | Nguyên tắc áp dụng |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Bôi đen thuật ngữ "5 loại mô hình ngôn ngữ" ở Slide Trang 8 | **① Nguồn sự thật** | Trả lời đúng 5 mô hình trên slide (RNN, LSTM, Transformer, BERT, GPT), cite đúng Slide Trang 8, triệt tiêu hoàn toàn ảo giác cite `[trang 304]`. | HAX G11 / PAIR Trust |
| 2 | Bôi đen từ khóa "Transformer" trên Slide Trang 8 | **① Nguồn sự thật** | Trả về micro-summary < 200 ký tự, trích dẫn đúng `Slide [d1-slide-hackathon.pdf] · Trang 8 & Transcript [transcript-04-clean.md] · Đoạn [T04-038]`, xóa bỏ mã `trang 957`. | HAX G11 / PAIR Explainability |
| 3 | Bôi nhầm 1 ký tự rác `"r"` | **② Mơ hồ / Thiếu thông tin** | Chặn trong 0ms, không gọi API tốn chi phí: Hiện thông báo nhắc nhở nội dung quá ngắn, hướng dẫn bôi đen trọn vẹn thuật ngữ. | HAX G8 / PAIR Errors |
| 4 | Bôi nhầm ký hiệu mũi tên `"--> &"` | **② Mơ hồ / Thiếu thông tin** | Chặn ngay tại Client/Server trong 0ms, triệt tiêu 100% tình trạng đoán mò sang embedding lung tung. | HAX G8 / PAIR Graceful Failure |
| 5 | Hỏi về thuật toán huấn luyện PPO (Proximal Policy Optimization) | **③ Ngoài phạm vi / Thẩm quyền** | Thừa nhận trung thực: PPO thuộc học phần RLHF chuyên sâu chưa dạy trong buổi này. Ghi chú phạm vi bài học, không tự chém gió. | HAX G2 / PAIR Mental Models |
| 6 | Thử chèn câu lệnh prompt injection / vượt quyền hệ thống | **③ Ngoài phạm vi / Thẩm quyền** | Hệ thống giữ vững vai trò AI Tutor, từ chối thực thi câu lệnh phá hoại, đặt `is_out_of_scope: true`. | HAX G2 / An toàn hệ thống |
| 7 | Bôi đen thuật ngữ "Context rot" và cửa sổ 1 triệu token | **④ Đặc thù domain** | Giải thích chính xác hiện tượng suy giảm chú ý khi ngữ cảnh quá dài và bùng nổ chi phí, trích dẫn đúng đoạn `[T04-052]`. | PAIR Factuality / Domain Accuracy |
| 8 | So sánh mô hình hiểu hai chiều (BERT) và mô hình sinh văn bản (GPT) | **④ Đặc thù domain** | Phân biệt rõ ràng bản chất 2 chiều (Bidirectional) của BERT vs sinh tuần tự (Generative) của GPT kèm trích dẫn Slide Trang 8 & Transcript `[T04-049]`. | PAIR Domain Accuracy |

---

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** Học viên bôi đen trọn vẹn thuật ngữ trên slide (VD: "Kỹ thuật Delimiters") $\rightarrow$ Hệ thống hiển thị micro-summary súc tích 2 câu (< 250 ký tự) $\rightarrow$ Đính kèm badge trích dẫn kép `Slide [d4-slide-hackathon.pdf] · Trang 55 & Transcript [transcript-04-clean.md] · Đoạn [T-Delimiters]` $\rightarrow$ Hiển thị 2 nút bấm Socratic để học viên bấm chọn đào sâu tiếp.
- **Low-confidence path:** Học viên bôi đen khái niệm ngắn nhưng hợp lệ $\rightarrow$ Hệ thống giải thích cô đọng ý cốt lõi, đồng thời chủ động đặt câu hỏi định hướng để làm rõ bối cảnh học viên muốn áp dụng.
- **Failure / Không căn cứ (Out-of-scope):** Học viên hỏi khái niệm ngoài phạm vi bài học (VD: PPO) $\rightarrow$ Hệ thống từ chối lịch sự, giải thích rõ đây là nội dung thuộc học phần nâng cao, trích dẫn ghi chú phạm vi bài học và không suy diễn bừa bãi.
- **Correction path (Khắc phục lỗi thao tác):** Học viên bôi nhầm 1 chữ cái hoặc ký hiệu đồ họa $\rightarrow$ Guardrail chặn ngay lập tức (< 10ms), hiển thị hướng dẫn thân thiện mời người học bôi đen trọn vẹn cụm từ trên slide.

---

## §7. Kiểm thử & Quality Bar (Khóa cứng tại CP4)
- **Chiều chất lượng & Định nghĩa kiểm chứng được:**
  1. *Progressive Disclosure (Độ dài nhận thức):* Câu trả lời tóm tắt vi mô phải dưới 280 ký tự (giảm $\ge 70\%$ so với mức trung bình 1.051 ký tự cũ).
  2. *Source Grounding (Độ chính xác nguồn):* 100% câu hỏi nội dung phải có trích dẫn đúng tên file slide thật, số trang thật và mã đoạn transcript thật; triệt tiêu 100% ảo giác số trang (như trang 304, 957, 1077).
  3. *Socratic Interaction (Tính tương tác đa tầng):* 100% câu trả lời học thuật sinh ra đúng 2 lựa chọn đào sâu Option A và Option B.
  4. *Guardrail Efficiency (Hiệu quả lọc rác):* Chặn 100% ký tự rác trong thời gian $\le 10$ ms mà không tốn chi phí gọi LLM.
- **Golden Set (Bộ 20 Test Cases chuẩn hóa trong `eval/run_full_evaluation_suite.py`):**
  - Gồm 20 test cases phủ trọn 5 nhóm lỗ hổng kiến trúc đối đầu trực diện với hệ thống cũ:
    - *Nhóm 1:* Ảo giác số trang & Metadata (4 cases).
    - *Nhóm 2:* Bức tường chữ & Phân tầng nhận thức (5 cases).
    - *Nhóm 3:* Sập RAG & Mất kết nối tài liệu slide (5 cases).
    - *Nhóm 4:* Mất nguồn & Kiến thức trôi nổi (3 cases).
    - *Nhóm 5:* Thao tác lỗi & Luồng Socratic (3 cases).
- **Quality Bar (Chốt tại 21:00 17/9 và giữ nguyên sau đó):**
  > **"Sản phẩm đạt chuẩn khi: Tỷ lệ Pass bộ Golden Set $\ge$ 85.0%, Tỷ lệ trích dẫn nguồn hợp lệ $\ge$ 95.0%, Tỷ lệ ảo giác số trang = 0.0%, và Độ dài phản hồi trung bình $\le$ 280 ký tự."**
- **Kết quả thực tế đo lường tự động qua API (Cập nhật ngày 17/9):**
  - **Tỷ lệ Pass Golden Set:** **100.0% (20 / 20 Test Cases ĐẠT CHUẨN)** (Hệ thống cũ: 0/20 do dính lỗi kiến trúc).
  - **Tỷ lệ Trích dẫn Nguồn Hợp lệ:** **100.0%** (triệt tiêu hoàn toàn 28.02% lỗi mất nguồn).
  - **Tỷ lệ Ảo giác Số trang:** **0.0%** (100% trích dẫn đúng trang slide thật và đoạn transcript thật).
  - **Độ dài phản hồi trung bình:** **205.2 ký tự** (~45 từ) $\rightarrow$ **Giảm 80.5%** độ dài văn bản quá tải so với mức 1.051 ký tự cũ.
  - **Độ trễ trung bình:** **2.682 ms** trên Live API GPT-4o-mini; **0 ms** đối với các case guardrail chặn lỗi thao tác.
  - *File báo cáo đối soát master:* [`eval/Bao_cao_kiem_chung_toan_bo_20_test_cases_tu_dong.xlsx`](file:///home/namphuong/Desktop/vin_lab/K4-3A-Day05-06-AI-Product-Hackathon/eval/Bao_cao_kiem_chung_toan_bo_20_test_cases_tu_dong.xlsx).

---

## §8. Phân công & Kế hoạch nhóm LearnLoop
- **Phân công trách nhiệm:**
  - **Nguyễn Đức Phát** (Đội trưởng / PM): Quản lý tiến độ các mốc CP1–CP6, hoàn thiện AI Spec, xây dựng kịch bản thuyết trình và quay video demo.
  - **Chử Trần Phương Nam** (Tech Lead / Dev): Thiết kế kiến trúc Dynamic RAG ingestion đa nguồn (59 trang PDF, 701 đoạn Markdown), xây dựng server API (`server.py`) và bộ lọc Dual-layer Guardrail.
  - **Đỗ Thành Đạt** (AI Evaluation Engineer): Khai phá dữ liệu chatlog 13.494 turns, xây dựng bộ Golden Set 20 test cases chuẩn hóa, lập trình script đo lường tự động và xuất báo cáo Excel A/B Benchmark.
  - **Nguỵ Khắc Phi Long** (UX & User Research): Thiết kế giao diện tương tác Slide Canvas hai chiều, tích hợp các nút bấm Socratic Probing, thu thập phản hồi và khảo sát người dùng.
- **Willing users (Đăng ký từ CP1 cho vòng kiểm thử LAB 18/9):**
  1. Hoàng Văn Nam (Học viên Phòng E403 - Lớp 3A)
  2. Lê Minh Tuấn (Học viên Phòng E403 - Lớp 3A)
  3. Trần Đức Anh (Học viên Phòng E403 - Lớp 3A)
- **Kế hoạch cho LAB 18/9:**
  - *13:00 18/9 (CP5):* Hoàn thành slide thuyết trình 6 trang (`demo-slides.pdf`) và video demo dự phòng.
  - *14:00–16:00 18/9:* Chạy thử nghiệm người dùng thật với 2 Willing Users, ghi nhận feedback log vào thư mục `validation/`.

---

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (Trỏ về feedback / case lỗi nào) |
|---|---|---|
| 16/9 · 19:30 | Khởi tạo Problem Canvas & AI Spec v1.0 | Định hình bài toán theo phân tích 13.494 turns log từ `tutor_turns.csv` |
| 17/9 · 11:30 | Thêm bộ lọc Dual-layer Guardrail (Client & Server) | Khắc phục case lỗi `T00185` (bôi nhầm 1 chữ "r") và `T00924` (bôi nhầm mũi tên "--> &") |
| 17/9 · 14:00 | Bổ sung module Socratic Probing (2 Option gợi ý đào sâu) | Chấm dứt tình trạng độc thoại 1 chiều (chỉ 0.21% lượt chat cũ có câu hỏi gợi mở) |
| 17/9 · 16:30 | Nâng cấp Dynamic RAG ingestion toàn diện 59 trang PDF & 701 đoạn Markdown | Khắc phục triệt để lỗi ảo giác cite `[trang 304]` (`T12701`), `[trang 957]` (`TC_LIVE_04`) và sập RAG cross-slide |
| 17/9 · 18:30 | Hoàn tất kiểm thử tự động 20/20 Test Cases (100% Pass Rate) | Đồng bộ dữ liệu thực đo vào master Excel và khóa cứng Quality Bar tại mốc CP4 |

