# VLearn Socratic & Grounded AI Tutor — Prototype Mockup (CP2)

Tài liệu bàn giao cho **Checkpoint 2 (CP2 · 21:00 16/9)**: Chứng minh luồng hoạt động từ đầu đến cuối (*Clickable Prototype Mockup*).

---

## 1. Luồng hoạt động tổng quát (Operational Flow)

```mermaid
flowchart TD
    Start([1. Học viên mở Slide VLearn]) --> AutoSelect[2. Dùng chuột bôi đen văn bản & THẢ CHUỘT]
    AutoSelect --> AutoTrigger[⚡ Tự động phân tích ngay lập tức]
    AutoTrigger --> AIDecision{3. AI Decision Engine Phân loại Input}
    
    AIDecision -- Bôi đen khái niệm cộc lốc: Progressive Disclosure --> Tier1[4a. TẦNG 1: Cung cấp ngay Tóm tắt cốt lõi 2 câu kèm [Trang N]]
    Tier1 --> Tier2[4b. TẦNG 2: Mở Khung đào sâu gồm Lựa chọn A/B + Ô gõ câu hỏi riêng]
    Tier2 -- Học viên bấm chọn A hoặc B --> BranchAnswer[AI giải thích sâu theo hướng đã chọn]
    Tier2 -- Học viên gõ câu hỏi riêng vào ô --> CustomAnswer[AI trả lời đúng trọng tâm câu hỏi của học viên]
    
    AIDecision -- Bôi đen cả câu dài đầy đủ ngữ cảnh --> GroundedPath[4c. Nước đi Trực tiếp: Giải thích <= 3 câu + Trích nguồn]
    AIDecision -- Hỏi ngoài tài liệu Day 1 --> OutScopePath[4d. Từ chối lịch sự: Báo rõ tài liệu không có + Không bịa]
    
    BranchAnswer --> Finish([5. Học viên hiểu sâu, hoàn toàn chủ động, không bị overload])
    CustomAnswer --> Finish
    GroundedPath --> Finish
    OutScopePath --> Finish
```

---

## 2. Các tính năng tương tác đột phá (Key UX Innovations)
1. **Auto-lookup on Selection (Tự động tra cứu khi thả chuột):** Học viên chỉ cần quét chuột qua văn bản và thả tay, hệ thống sẽ kích hoạt phản hồi mà không cần nút trung gian.
2. **Cơ chế Tiết lộ tiệm tiến (Progressive Disclosure - 2 Tầng):**
   - **Tầng 1 (Instant Satisfaction):** Trả lời ngay 1–2 câu bản chất cốt lõi của khái niệm kèm trích dẫn `[Trang 6]` để người học không phải chờ đợi.
   - **Tầng 2 (Socratic & Flexible Control):** Cung cấp 2 gợi ý đào sâu nhanh (A/B) **VÀ 1 ô nhập câu hỏi riêng** ngay trong khung trả lời (theo nguyên tắc **HAX G9** & **Google PAIR Feedback & Control**).

---

## 3. Các kịch bản kiểm thử luồng có sẵn (Built-in Scenarios)

Bạn có thể bôi đen tự do hoặc bấm các nút kịch bản nhanh trên giao diện:

### Kịch bản 1: Bôi đen khái niệm "Transformer" (Progressive Disclosure)
* **Thao tác:** Bôi đen từ *"Transformer"* rồi thả chuột (hoặc bấm nút kịch bản 1).
* **Kết quả:** 
  1. AI đưa ra định nghĩa cốt lõi trong 2 câu: giải thích vai trò nền tảng và việc giải quyết nghẽn cổ chai của RNN.
  2. Xuất hiện khung đào sâu với 2 nút gợi mở (A/B) và **1 ô nhập liệu câu hỏi riêng**.
  3. Bạn có thể bấm chọn A, B hoặc gõ bất kỳ câu hỏi nào vào ô đó rồi nhấn Enter $\rightarrow$ AI giải thích tiếp theo đúng ý bạn!

### Kịch bản 2: Bôi đen cả câu dài cụ thể ("Transformer giải quyết triệt để...")
* **Thao tác:** Bôi đen cả câu dài rồi thả chuột.
* **Kết quả:** AI trả lời trực tiếp trong 3 câu ngắn gọn kèm trích dẫn nguồn `[Trang 6]`.

### Kịch bản 3: Bôi đen kiến thức ngoài bài ("Thuật toán PPO...")
* **Thao tác:** Bôi đen cụm từ *"Thuật toán PPO..."* ở dòng ghi chú cuối slide.
* **Kết quả:** AI từ chối lịch sự theo HAX G1/G2, nói rõ không nằm trong nội dung Day 1.

---

## 4. Cách mở và chạy thử Mockup
File là bản Web tĩnh hoàn chỉnh (HTML/CSS/JS thuần):
* Đang chạy trực tiếp tại: `http://localhost:8000`
