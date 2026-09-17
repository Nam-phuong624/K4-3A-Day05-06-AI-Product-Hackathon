# Worksheet JTBD — Nhóm LearnLoop (CP1 Deliverable)

**Nhóm:** LearnLoop · **Lớp:** 3A · **Phòng:** E403 · **Cụm:** Bàn 1  
**Hướng:** [x] A — VLearn Tutor  [ ] B — Trợ lý Học viên  [ ] C — Làn mở  
**Đề bài:** Track A1 — Tối ưu AI Tutor hiện có trên VLearn (Grounding & Hallucination Defense)

---

## 1. Chọn Job Executor
- **Job executor:** Học viên khóa AI20k đang theo dõi bài giảng, thực hành bài lab và ôn tập trên VLearn.
- **Vì sao là người này:** Đây là người trực tiếp bôi đen văn bản hoặc gõ câu hỏi vào cửa sổ AI Tutor để hiểu bài. Khi AI Tutor trả lời sai hoặc không có căn cứ, chính học viên này phải gánh chịu hậu quả mất thời gian và hiểu sai kiến thức.

---

## 2. Workflow thật của Job Executor

| Chặng | Họ đang cố làm gì? | Hiện tại họ dùng gì? | Kẹt ở đâu? | Mức đau |
|---|---|---|---|---|
| **Trước buổi** | Đọc trước slide / transcript bài giảng | Đọc lướt tài liệu | Gặp từ viết tắt hoặc thuật ngữ mới chưa hiểu | Medium |
| **Trong buổi** | Nghe giảng và làm bài lab code trên máy | Bôi đen câu hỏi trong bài giảng hỏi AI Tutor | Tutor trả lời lan man, không có số trang/mã đoạn để kiểm chứng | **High** |
| **Ngay sau buổi** | Hoàn thiện bài tập nộp lab | Hỏi lại các chỗ chưa rõ | Tutor tự bịa câu trả lời ngoài giáo trình, gây mâu thuẫn | **High** |
| **Khi ôn lại** | Ôn thi lý thuyết và làm quiz | Tra cứu lại tài liệu | Mất công xem lại cả video để tìm đoạn thầy giảng do không có dẫn nguồn chính xác | **High** |

- **Hai chỗ đau nhất trong workflow:**
  1. *Chỗ đau #1:* Tutor trả lời khẳng định như thật các kiến thức không có trong bài giảng (hallucination).
  2. *Chỗ đau #2:* Tutor không hỏi lại khi câu hỏi cộc lốc / mơ hồ, tự sinh câu trả lời dài dòng không đúng trọng tâm.
- **Bằng chứng ban đầu:** Khai phá từ 13.494 log chat thật của VLearn Tutor (28% không có trích dẫn nguồn, chỉ 28 lần hỏi lại làm rõ).

---

## 3. Core JTBD
- **Công thức:** `[verb] + [object] + [contextual clarifier]`
- **Core JTBD bản chốt:**
  > *"Xác thực và làm rõ ngay lập tức các khái niệm khó hiểu trong bài học dựa trên tài liệu chính thống mà không bị sai lệch kiến thức hoặc mất thời gian kiểm tra chéo."*
  *(Đáp ứng chuẩn 3 tiêu chí: không chứa từ AI/sản phẩm, loại bỏ giải pháp, tập trung vào mục tiêu của người học).*

---

## 4. Ba Job Stories (JTBD Stories)

| # | When (Khi nào) | I want to (Tôi muốn) | So I can (Để tôi có thể) | Story này cho thấy gì |
|---|---|---|---|---|
| **JS1** | Khi gặp một đoạn giải thích khó hiểu trong bài giảng đang xem | Được giải thích ngắn gọn với dẫn chứng cụ thể đến số đoạn bài giảng | Nắm vững ngay ý nghĩa và an tâm tiếp tục học mà không phải tua lại cả video | Cần Grounding & Trích dẫn chính xác (Citation) |
| **JS2** | Khi tò mò hỏi một chủ đề nâng cao chưa có trong bài học hiện tại | Được thông báo rõ ràng rằng nội dung này nằm ngoài phạm vi bài học và nhận gợi ý nguồn đọc chính thức | Tránh hiểu nhầm hoặc học kiến thức chắp vá chưa có căn cứ | Cần Hallucination Defense & Phân định ranh giới |
| **JS3** | Khi bôi đen nhanh một từ khóa kỹ thuật ngắn | Được người hỗ trợ hỏi lại xem tôi đang thắc mắc khía cạnh lý thuyết hay cách lập trình | Nhận được câu trả lời đúng kích cỡ và đúng trọng tâm nhu cầu | Cần Probing Question khi câu hỏi mơ hồ |

---

## 5. Current Alternatives & Hạn chế

- **ChatGPT bên ngoài:** Không có quyền truy cập giáo trình và slide đặc thù của khóa học, thường giải thích theo thư viện tổng quát không khớp quy ước lớp học.
- **Hỏi bạn bè / Discord:** Mất thời gian chờ đợi phản hồi (từ vài chục phút đến vài giờ), làm đứt gãy mạch tập trung học tập.
- **Tua lại video bài giảng:** Rất mất thời gian (trung bình 10–20 phút để tìm đúng vị trí đoạn giảng viên nói).

---

## 6. AI Leverage Point (Nộp vào CP1)

- **Điểm đòn bẩy của AI:** AI có khả năng đọc hiểu và rà soát tức thời (semantic search & verification) toàn bộ transcript và slide bài học để:
  1. Đối chiếu tính có căn cứ (groundedness) của câu trả lời với tốc độ tính bằng mili-giây.
  2. Tự động nhận diện mức độ mơ hồ của câu hỏi để kích hoạt câu hỏi làm rõ (Socratic probing).
- **Mức tự động hóa:** **Conditional Automation** — Tự động trả lời khi bằng chứng $\ge$ ngưỡng tin cậy; chuyển sang từ chối hoặc hỗ trợ định hướng khi không có căn cứ trong tài liệu bài học.
