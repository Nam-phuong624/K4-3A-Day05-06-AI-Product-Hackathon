import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load full chatlog
df_chatlog = pd.read_csv('data/vlearn-pack/chatlog/tutor_turns.csv')

# Define groups and their cards/descriptions
groups = [
    {
        "group_id": 1,
        "name": "NHÓM 1: ẢO GIÁC TRÍCH DẪN & SAI LỆCH SỐ TRANG (PHANTOM CITATION & HALLUCINATION)",
        "card_title": "🏷️ THẺ MÔ TẢ NHÓM 1: ẢO GIÁC TRÍCH DẪN & SAI LỆCH SỐ TRANG (PHANTOM CITATIONS)",
        "card_desc": "MÔ TẢ VẤN ĐỀ: Hệ thống RAG gặp lỗi không đồng bộ giữa metadata của slide gốc và vector chunk, dẫn đến tình trạng bot tự sinh (hallucinate) các số trang không có thật (trang 304, 957, 1077 trong khi slide chỉ có ~80 trang), hoặc số trang trích dẫn mâu thuẫn trực tiếp với câu hỏi (hỏi trang 4 nhưng cite trang 70), hoặc tự tóm tắt video khi chưa có dữ liệu gỡ băng. HẬU QUẢ: Học viên bấm vào liên kết bị lỗi 404/dead link, làm mất hoàn toàn niềm tin vào tính xác thực của trợ lý AI.",
        "fill_color": "1F4E79", # Deep Blue
        "cases": [
            {
                "stt": 1,
                "type": "csv",
                "turn_id": "T12701",
                "lo_hong_chinh": "Ảo giác số trang nghiêm trọng: Cite 'trang 304 [trang 304]' trong khi slide Day 04 chỉ có ~80 trang; câu trả lời dài tới 1.472 ký tự.",
                "hau_qua_ux": "Học sinh đánh giá Thumbs Down (tiêu cực); link dẫn tới trang 304 bị chết hoặc không tìm thấy trong slide.",
                "ky_vong_cai_tien": "Strict Slide Grounding: Chỉ cho phép cite số trang thực tế hiện hữu của bài giảng (<= max_page)."
            },
            {
                "stt": 2,
                "type": "live",
                "turn_id": "TC_LIVE_04",
                "cohort_hint": "K4-Live",
                "lecture_title": "Day04_(Mr.Dang Duc Huy)_Prompt-Engineering-Tool-Calling",
                "lecture_code": "Day04",
                "is_preset": False,
                "student_question": "Giải thích rõ đoạn này giúp mình. Đoạn đang hỏi: “context loop harness”",
                "tutor_reply": "Chào Nam, trong khuôn khổ bài học ngày hôm nay, \"Context Loop Harness\" là khái niệm chỉ lớp hệ thống (framework hoặc bộ quy trình) bao bọc lấy quá trình tương tác giữa Agent, LLM và các Công cụ (Tools) trang 957 trang 1077.\n\nEm có thể hiểu đơn giản như sau:\nTại sao gọi là \"Harness\" (Bộ dây cương/Khung bảo vệ): Agent không thể tự chạy một cách tự do mà thiếu kiểm soát. \"Harness\" đóng vai trò như một bộ khung kỹ thuật giúp hệ thống kiểm soát toàn bộ vòng lặp (loop): đưa dữ liệu vào, thu nhận kết quả từ tool, bắt lỗi (nếu có), và quản lý trạng thái (state).\n\nCách hoạt động của vòng lặp:\nNhận đầu vào: Lấy dữ liệu và chỉ thị từ người dùng/hệ thống.\nGửi đến Model: Chuyển ngữ cảnh vào LLM để quyết định hành động tiếp theo.\nGọi Tool & Đón nhận: Thực thi lệnh mà LLM yêu cầu (ví dụ: gọi API, truy vấn cơ sở dữ liệu).\nKhép kín vòng lặp (Loop): Lấy kết quả từ tool nhồi ngược lại vào ngữ cảnh để LLM tiếp tục xử lý cho đến khi có câu trả lời cuối cùng.\n\nMục tiêu cốt lõi: Giúp ngăn chặn việc Agent bị \"mất kiểm soát\" (vòng lặp vô tận, tràn bộ nhớ, hoặc rò rỉ ngữ cảnh ngoài ý muốn). Nếu LLM là \"trí não\", thì Context Loop Harness chính là bộ khung vận hành (cơ sở hạ tầng) giúp trí não đó tương tác với thế giới thực một cách ổn định, an toàn và đúng quy trình trang 1077.",
                "reply_len": 1328,
                "has_citation": False,
                "rating": None,
                "reply_ms": 3200,
                "lo_hong_chinh": "Ảo giác cite 'trang 957 trang 1077' và mục Nguồn tài liệu hoàn toàn trống trơn; lấy nhầm token index thay vì số trang slide.",
                "hau_qua_ux": "Học viên hoang mang vì slide không có trang 957 hay 1077; tài liệu nguồn bị biến mất.",
                "ky_vong_cai_tien": "Loại bỏ hoàn toàn chunk token ảo giác; chỉ trích dẫn tài liệu đang mở kèm tiêu đề trang cụ thể."
            },
            {
                "stt": 3,
                "type": "csv",
                "turn_id": "T00213",
                "lo_hong_chinh": "Mâu thuẫn số trang: Học viên bôi đen 'Trang 4, Giải thích slide 4 cho tôi' nhưng bot trích dẫn 'Slide 4 [trang 70]'.",
                "hau_qua_ux": "Đánh giá Thumbs Down (tiêu cực); học viên thấy câu trả lời bất nhất và thiếu tin cậy.",
                "ky_vong_cai_tien": "Neo câu trả lời đúng vào trang mà học viên đang tương tác, không lấy chéo metadata từ bài khác."
            },
            {
                "stt": 4,
                "type": "csv",
                "turn_id": "T10457",
                "lo_hong_chinh": "Tự bịa nội dung (Un-grounded generation): Video chưa có bản ghi transcript nhưng bot tự sinh 988 ký tự tóm tắt không nguồn.",
                "hau_qua_ux": "Rủi ro cung cấp kiến thức sai lệch do không có căn cứ tài liệu chính thức.",
                "ky_vong_cai_tien": "Minh bạch hóa giới hạn: Nếu chưa có transcript, thừa nhận rõ ràng và hướng dẫn học sinh xem slide liên quan."
            }
        ]
    },
    {
        "group_id": 2,
        "name": "NHÓM 2: HỘI CHỨNG 'BỨC TƯỜNG CHỮ' & QUÁ TẢI NHẬN THỨC (WALL-OF-TEXT > 1.000 KÝ TỰ)",
        "card_title": "🏷️ THẺ MÔ TẢ NHÓM 2: HỘI CHỨNG 'BỨC TƯỜNG CHỮ' & QUÁ TẢI NHẬN THỨC (COGNITIVE OVERLOAD)",
        "card_desc": "MÔ TẢ VẤN ĐỀ: Chatbot luôn phản hồi theo kiểu độc thoại giảng bài (Lecture Dump), trả về khối văn bản khổng lồ từ 900 đến 1.400 ký tự cho một câu hỏi tra cứu nhanh hoặc một cụm từ ngắn. Không áp dụng nguyên lý phân tầng thông tin (Progressive Disclosure) của Google PAIR. HẬU QUẢ: Học viên đang theo dõi bài giảng live bị phân tâm, mất mạch nghe giảng viên và thường bỏ qua không đọc các đoạn trả lời quá dài.",
        "fill_color": "C55A11", # Deep Orange/Brown
        "cases": [
            {
                "stt": 5,
                "type": "live",
                "turn_id": "TC_LIVE_03",
                "cohort_hint": "K4-Live",
                "lecture_title": "Day04_(Mr.Dang Duc Huy)_Prompt-Engineering-Tool-Calling",
                "lecture_code": "Day04",
                "is_preset": False,
                "student_question": "Giải thích rõ đoạn này giúp mình. Đoạn đang hỏi: “Tính nhất quán”",
                "tutor_reply": "Chào Nam, trong ngữ cảnh của trang này trang 55, \"Tính nhất quán\" là nguyên tắc quan trọng khi em thiết lập cấu trúc cho prompt.\nGiải thích cụ thể:\nSự đồng bộ trong định dạng: Khi em chọn sử dụng một loại thẻ phân tách nào đó (ví dụ: thẻ XML <user_query> hay dấu ngoặc kép \"\"\"), em cần duy trì việc sử dụng nó một cách xuyên suốt trong toàn bộ prompt.\nGiúp mô hình dễ nhận diện: Nếu em thay đổi phong cách phân tách giữa các phần (lúc thì dùng XML, lúc lại dùng dấu gạch ngang, lúc khác dùng ngoặc), mô hình sẽ dễ bị bối rối và không phân loại chính xác đâu là lệnh, đâu là dữ liệu.\nSự ổn định: Việc nhất quán giúp hành vi của mô hình trở nên ổn định hơn qua nhiều lượt gọi khác nhau. Nếu hệ thống của em luôn tuân thủ một chuẩn phân tách, mô hình sẽ học được \"thói quen\" đó và xử lý các yêu cầu sau này của em chuẩn xác hơn.\nVì vậy, giảng viên khuyên rằng nếu không dùng thẻ XML, em có thể dùng dấu ngoặc kép, nhưng quan trọng nhất là phải duy trì sự nhất quán đó trong suốt cấu trúc prompt của mình trang 55.\nNguồn (1)\nDay04_(Mr.Dang Duc Huy)_Prompt-Engineering-Tool-Calling\nTr. 55Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries vào trong các thẻ định danh rõ ràng.",
                "reply_len": 1050,
                "has_citation": True,
                "rating": None,
                "reply_ms": 2800,
                "lo_hong_chinh": "Xả bài văn dài hơn 1.050 ký tự chia 5 đoạn cho một cụm từ bôi đen chỉ gồm 3 chữ ('Tính nhất quán').",
                "hau_qua_ux": "Gây ngợp thông tin (Cognitive Overload) giữa giờ học; học viên không nắm được ý cốt lõi.",
                "ky_vong_cai_tien": "Tầng 1: Tóm gọn 2 câu (<= 250 ký tự); Tầng 2: Nút mở rộng giải thích sâu về Delimiters."
            },
            {
                "stt": 6,
                "type": "csv",
                "turn_id": "T12378",
                "lo_hong_chinh": "Độ dài phản hồi cực lớn (1.369 ký tự), lặp lại nguyên văn từng gạch đầu dòng của slide bài học.",
                "hau_qua_ux": "Học sinh không đọc hết; làm loãng mục tiêu học tập chính.",
                "ky_vong_cai_tien": "Tóm lược cấu trúc Role/Task/Context/Format trong 2 câu, kèm nút xem prompt ví dụ minh họa."
            },
            {
                "stt": 7,
                "type": "csv",
                "turn_id": "T12377",
                "lo_hong_chinh": "Phản hồi dài 1.149 ký tự mang tính học thuật hàn lâm khi học sinh bôi đen một câu ngắn về System Prompt.",
                "hau_qua_ux": "Độc thoại 1 chiều, không kích thích học sinh đặt câu hỏi phản biện.",
                "ky_vong_cai_tien": "Giải thích 3 ranh giới của System Prompt trong 2 câu; gợi mở nút thử nghiệm prompt."
            },
            {
                "stt": 8,
                "type": "csv",
                "turn_id": "T12379",
                "lo_hong_chinh": "Phản hồi 1.275 ký tự liệt kê dàn trải toàn bộ kiến thức buổi học thành danh sách dài.",
                "hau_qua_ux": "Quá tải nhận thức, học viên không định vị được phần kiến thức mình đang cần nhất.",
                "ky_vong_cai_tien": "Hiển thị bản đồ tư duy 3 cụm kiến thức chính, cho phép học sinh click vào cụm muốn xem."
            },
            {
                "stt": 9,
                "type": "csv",
                "turn_id": "T10506",
                "lo_hong_chinh": "Học viên chỉ gõ từ 'tóm tắt' nhưng bot xả ra 929 ký tự và hoàn toàn không có trích dẫn nguồn.",
                "hau_qua_ux": "Đánh giá Thumbs Down (tiêu cực); phản hồi không tương xứng với độ dài câu hỏi ngắn.",
                "ky_vong_cai_tien": "Tóm tắt micro-summary đúng 2 câu cho bài lab, kèm link dẫn thẳng tới vị trí tài liệu."
            }
        ]
    },
    {
        "group_id": 3,
        "name": "NHÓM 3: MẤT KẾT NỐI TÀI LIỆU SLIDE / RAG RETRIEVAL THẤT BẠI (RAG RETRIEVAL FAILURE)",
        "card_title": "🏷️ THẺ MÔ TẢ NHÓM 3: MẤT KẾT NỐI TÀI LIỆU SLIDE / RAG THẤT BẠI (RETRIEVAL FAILURES)",
        "card_desc": "MÔ TẢ VẤN ĐỀ: Module RAG bị đứt gãy kết nối giữa trang slide học viên đang xem và chỉ mục tìm kiếm (search index). Bot liên tục đưa ra câu trả lời từ chối: 'Rất tiếc không tìm thấy nội dung', 'hệ thống slide không có dữ liệu cho trang X' dù trang đó đang hiển thị sờ sờ trước mắt người học. HẬU QUẢ: Đây là nhóm lỗi nhận tỷ lệ Thumbs Down (đánh giá 1 sao) cao nhất hệ thống, biến AI Tutor thành một công cụ vô dụng.",
        "fill_color": "7030A0", # Purple
        "cases": [
            {
                "stt": 10,
                "type": "csv",
                "turn_id": "T00079",
                "lo_hong_chinh": "Bôi đen trang 33 yêu cầu tóm tắt slide nhưng bot báo 'chưa tìm thấy nội dung cụ thể của slide 33'.",
                "hau_qua_ux": "Đánh giá Thumbs Down; học viên thất vọng vì tài liệu hiển thị trước mặt nhưng bot không đọc được.",
                "ky_vong_cai_tien": "Đọc trực tiếp DOM/text content của trang hiện tại thay vì phụ thuộc hoàn toàn vào vector search."
            },
            {
                "stt": 11,
                "type": "csv",
                "turn_id": "T00362",
                "lo_hong_chinh": "Bôi đen yêu cầu giải thích slide 26 nhưng bot trả lời 'hệ thống slide hiện tại không có dữ liệu cho slide 26'.",
                "hau_qua_ux": "Đánh giá Thumbs Down; đứt gãy luồng học tập của học viên.",
                "ky_vong_cai_tien": "Auto-sync slide index: Luôn đảm bảo slide ID khớp 100% giữa PDF viewer và retriever."
            },
            {
                "stt": 12,
                "type": "csv",
                "turn_id": "T00758",
                "lo_hong_chinh": "Yêu cầu giải thích trang 32 nhưng bot từ chối 'nội dung tài liệu tôi nhận được không bao gồm trang 32'.",
                "hau_qua_ux": "Đánh giá Thumbs Down; gây ức chế cho người học.",
                "ky_vong_cai_tien": "Đảm bảo pipeline ingest đầy đủ 100% các trang slide, không bỏ sót chunk."
            },
            {
                "stt": 13,
                "type": "csv",
                "turn_id": "T00841",
                "lo_hong_chinh": "Yêu cầu giải thích trang 12 nhưng bot từ chối 'không thể truy cập trực tiếp nội dung trang 12'.",
                "hau_qua_ux": "Đánh giá Thumbs Down; bot liên tục xin lỗi thay vì hỗ trợ.",
                "ky_vong_cai_tien": "Cơ chế fallback: Nếu RAG thiếu text, tự động đọc text layer từ slide hiện tại để giải thích."
            },
            {
                "stt": 14,
                "type": "csv",
                "turn_id": "T00450",
                "lo_hong_chinh": "Hỏi tóm tắt nội dung ghi nhớ trang 42 nhưng bot báo 'không thể truy cập nội dung cụ thể từ slide hôm nay'.",
                "hau_qua_ux": "Đánh giá Thumbs Down; chatbot từ chối phục vụ trên câu hỏi tổng hợp.",
                "ky_vong_cai_tien": "Hỗ trợ lệnh 'Summarize current view' bằng prompt chuyên biệt lấy context tức thời."
            }
        ]
    },
    {
        "group_id": 4,
        "name": "NHÓM 4: HOÀN TOÀN MẤT TRÍCH DẪN NGUỒN (MISSING CITATION / 0% GROUNDING)",
        "card_title": "🏷️ THẺ MÔ TẢ NHÓM 4: HOÀN TOÀN MẤT TRÍCH DẪN NGUỒN (0% GROUNDING / MISSING CITATION)",
        "card_desc": "MÔ TẢ VẤN ĐỀ: Chatbot trả lời các câu hỏi kỹ thuật cốt lõi (phân biệt GenAI vs LLM, nguyên tắc thiết kế System Prompt, mục tiêu bài Lab) nhưng bỏ qua hoàn toàn việc dẫn nguồn trích dẫn slide (has_citation=False). Trong tập dữ liệu K4, có tới 28.02% phản hồi bị mất nguồn. HẬU QUẢ: Học viên không thể kiểm chứng tính chính xác của kiến thức, không biết mở slide trang nào để ôn tập lại.",
        "fill_color": "385723", # Dark Green
        "cases": [
            {
                "stt": 15,
                "type": "csv",
                "turn_id": "T10288",
                "lo_hong_chinh": "Học viên hỏi mục tiêu bài Lab baseline nhưng bot trả lời 629 ký tự không hề có trích dẫn nguồn (has_citation=False).",
                "hau_qua_ux": "Học sinh không biết tài liệu hướng dẫn nằm ở đâu trong repo hoặc slide.",
                "ky_vong_cai_tien": "Bắt buộc gắn thẻ nguồn slide/file [Trang X] ở cuối câu trả lời Tầng 1."
            },
            {
                "stt": 16,
                "type": "csv",
                "turn_id": "T10411", # Thay thế TC16
                "lo_hong_chinh": "Câu hỏi nền tảng 'sự khác nhau giữa LLM và generative AI' nhưng bot xả 901 ký tự hoàn toàn không có trích dẫn (has_citation=False).",
                "hau_qua_ux": "Kiến thức cốt lõi buổi 1 bị trả lời dạng văn bản trôi nổi, không neo vào trang bài giảng chính thức.",
                "ky_vong_cai_tien": "Tóm tắt 2 câu phân biệt GenAI vs LLM kèm trích dẫn chính xác [Trang 6, day01-slide]."
            },
            {
                "stt": 17,
                "type": "csv",
                "turn_id": "T12563", # Thay thế TC17
                "lo_hong_chinh": "Học viên hỏi phân tích quiz 'Tại sao lại không cần ghi chú từ nhà cung cấp?' nhưng bot xả 1.254 ký tự không nguồn (has_citation=False).",
                "hau_qua_ux": "Học sinh phải đọc bài văn quá dài mà không thấy liên kết tới nguyên tắc lọc nhiễu ở slide Day 04.",
                "ky_vong_cai_tien": "Tóm tắt 2 câu: Loại bỏ nhiễu và phòng ngừa Prompt Injection [Trang 55]; gợi ý nút xem ví dụ rủi ro."
            }
        ]
    },
    {
        "group_id": 5,
        "name": "NHÓM 5: LỖI XỬ LÝ BÔI ĐEN KÉM & THIẾU TƯƠNG TÁC GỢI MỞ SOCRATIC (SELECTION ERRORS & MONOLOGUE)",
        "card_title": "🏷️ THẺ MÔ TẢ NHÓM 5: LỖI XỬ LÝ BÔI ĐEN KÉM & THIẾU TƯƠNG TÁC GỢI MỞ (SELECTION & SOCRATIC)",
        "card_desc": "MÔ TẢ VẤN ĐỀ: Hệ thống thiếu bộ lọc Guardrail ở tầng Client để xử lý các thao tác bôi đen vô tình (chuột quét trúng 1 chữ cái vô nghĩa như 'r', 'e') dẫn đến việc bot xả ra hàng trăm chữ xin lỗi vô ích. Đồng thời, khi học viên bôi đen đúng câu lệnh kỹ thuật, bot chỉ phản hồi độc thoại lặp lại thay vì mở ra khung hội thoại tương tác Socratic. HẬU QUẢ: Trải nghiệm người dùng thô sơ, thiếu tinh tế, giảm động lực tự khám phá của học viên.",
        "fill_color": "833C0C", # Dark Red/Rust
        "cases": [
            {
                "stt": 18,
                "type": "csv",
                "turn_id": "T00185",
                "lo_hong_chinh": "Học viên nhỡ tay bôi đen đúng 1 chữ cái 'r', bot gọi cả quy trình RAG rồi trả về 240 ký tự xin lỗi vì không tìm thấy.",
                "hau_qua_ux": "Đánh giá Thumbs Down; lãng phí tài nguyên LLM và gây bực bội cho người học.",
                "ky_vong_cai_tien": "Client Guardrail: Nếu bôi đen < 3 ký tự hoặc từ vô nghĩa, nhắc nhẹ người dùng chọn cụm từ hoàn chỉnh."
            },
            {
                "stt": 19,
                "type": "csv",
                "turn_id": "T00924",
                "lo_hong_chinh": "Học viên bôi đen nhầm chữ 'e' ở trang 18, bot trả lời dài dòng 349 ký tự xin lỗi và giải thích vô ích.",
                "hau_qua_ux": "Đánh giá Thumbs Down; trải nghiệm tương tác thiếu thông minh.",
                "ky_vong_cai_tien": "Bộ lọc Minimum Selection Threshold: Không trigger API nếu đoạn bôi đen không tạo thành từ có nghĩa."
            },
            {
                "stt": 20,
                "type": "live",
                "turn_id": "TC_LIVE_01",
                "cohort_hint": "K4-Live",
                "lecture_title": "Day04_(Mr.Dang Duc Huy)_Prompt-Engineering-Tool-Calling",
                "lecture_code": "Day04",
                "is_preset": False,
                "student_question": "Giải thích rõ đoạn này giúp mình. Đoạn đang hỏi: “Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries”",
                "tutor_reply": "Chào Nam, ở trang này trang 55, giảng viên đang hướng dẫn kỹ thuật Cô Lập Dữ Liệu Bằng Delimiters để tăng tính ổn định cho prompt.\n\nGiải thích cụ thể về đoạn em hỏi: \"Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries\" có nghĩa là em nên đặt tất cả nội dung không phải là chỉ dẫn (instruction) của lập trình viên vào trong các thẻ đánh dấu rõ ràng.\n\nViệc này giúp ích cho hệ thống ở các điểm sau:\nPhân định ranh giới (Separation): Giúp mô hình phân biệt rõ đâu là \"lệnh\" của em (ví dụ: \"Hãy tóm tắt văn bản này\") và đâu là \"dữ liệu thô\" cần xử lý. Khi không có delimiters, mô hình dễ bị lẫn lộn giữa hai thành phần này.\nNgăn chặn Context Bleed: Khi dữ liệu đầu vào chứa các câu lệnh độc hại (ví dụ: \"Hãy bỏ qua mọi lệnh trước đó...\"), việc bao bọc trong delimiters giúp cô lập nội dung đó, giảm nguy cơ mô hình nhầm tưởng đó là chỉ dẫn mới cần thực hiện theo.\nTăng độ nhất quán: Khi mô hình biết chính xác dữ liệu nằm ở đâu, nó sẽ xử lý tập trung hơn và tránh việc \"bịa đặt\" (hallucination) dựa trên những thông tin nằm ngoài phạm vi cần xử lý.\n\nTóm lại, kỹ thuật này giúp em đóng gói dữ liệu đầu vào một cách sạch sẽ và an toàn trước khi đưa vào mô hình trang 55.\n\nNguồn (1)\nDay04_(Mr.Dang Duc Huy)_Prompt-Engineering-Tool-Calling\nTr. 55Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries vào trong các thẻ định danh rõ ràng.",
                "reply_len": 905,
                "has_citation": True,
                "rating": None,
                "reply_ms": 2500,
                "lo_hong_chinh": "Độc thoại dài 905 ký tự lặp lại khái niệm; không đưa ra câu hỏi gợi mở hay khung nhập câu hỏi tùy chỉnh ngay tại pop-up.",
                "hau_qua_ux": "Học sinh đóng vai trò thụ động đọc một bài giảng dài, không kích thích tư duy giải quyết vấn đề.",
                "ky_vong_cai_tien": "Tầng 1 súc tích 2 câu + Tầng 2 với 2 câu hỏi gợi mở Socratic và ô nhập Custom Query ngay tại pop-up."
            }
        ]
    }
]

# Create Workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "20_Test_Cases_Lo_Hong"
ws.views.sheetView[0].showGridLines = True

# Define Styles
font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
fill_title = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")

font_card_title = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_card_desc = Font(name="Calibri", size=10, italic=True, color="FFFFFF")

font_header = Font(name="Calibri", size=11, bold=True, color="000000")
fill_header = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

font_data = Font(name="Calibri", size=10, color="000000")
font_bold_id = Font(name="Calibri", size=10, bold=True, color="1F4E79")

thin_border = Border(
    left=Side(style='thin', color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin', color='BFBFBF'),
    bottom=Side(style='thin', color='BFBFBF')
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

# Columns setup
columns = [
    ("STT", 6, align_top_center),
    ("Mã Turn ID", 14, align_top_center),
    ("Nhóm Vấn Đề", 26, align_top_left),
    ("Khóa Học", 10, align_top_center),
    ("Bài Giảng / Slide", 30, align_top_left),
    ("Câu Hỏi / Thao Tác Bôi Đen (User Input)", 42, align_top_left),
    ("Phản Hồi Đầy Đủ Của Bot (Tutor Reply)", 55, align_top_left),
    ("Độ Dài (Ký tự)", 12, align_top_center),
    ("Có Nguồn? (has_citation)", 12, align_top_center),
    ("Đánh Giá (Rating)", 12, align_top_center),
    ("Lỗ Hổng Kỹ Thuật Chính", 35, align_top_left),
    ("Hậu Quả UX / Rủi Ro Sư Phạm", 35, align_top_left),
    ("Kỳ Vọng Cải Tiến (Giải Pháp Mới)", 35, align_top_left),
    ("Preset Query?", 12, align_top_center),
    ("Thời Gian (ms)", 12, align_top_center)
]

# Write Title Block
ws.merge_cells("A1:O1")
ws["A1"] = "BẢNG ĐÁNH GIÁ 20 TEST CASES GẶP LỖ HỔNG TRÊN HỆ THỐNG VLEARN CHATBOT"
ws["A1"].font = font_title
ws["A1"].fill = fill_title
ws["A1"].alignment = align_center
ws.row_dimensions[1].height = 40

ws.merge_cells("A2:O2")
ws["A2"] = "Nguồn dữ liệu: Trích xuất từ chatlog thực tế tutor_turns.csv (K1-K4) và Dữ liệu kiểm thử Live trên bài Day 04 | Phục vụ mốc CP3 Hackathon AI"
ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="595959")
ws["A2"].alignment = align_center
ws.row_dimensions[2].height = 20

current_row = 4

# Write Table Column Headers
for col_idx, (col_name, col_width, col_align) in enumerate(columns, 1):
    cell = ws.cell(row=current_row, column=col_idx, value=col_name)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = align_center
    cell.border = thin_border
ws.row_dimensions[current_row].height = 28
current_row += 1

# Iterate through groups and write card + data rows
for g in groups:
    group_fill = PatternFill(start_color=g["fill_color"], end_color=g["fill_color"], fill_type="solid")
    
    # 1. Thẻ mô tả dòng 1: Title
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(columns))
    card_title_cell = ws.cell(row=current_row, column=1, value=g["card_title"])
    card_title_cell.font = font_card_title
    card_title_cell.fill = group_fill
    card_title_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[current_row].height = 26
    # border for merged cell
    for c in range(1, len(columns) + 1):
        ws.cell(row=current_row, column=c).border = thin_border
        ws.cell(row=current_row, column=c).fill = group_fill
    current_row += 1

    # 2. Thẻ mô tả dòng 2: Description
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(columns))
    card_desc_cell = ws.cell(row=current_row, column=1, value=g["card_desc"])
    card_desc_cell.font = font_card_desc
    card_desc_cell.fill = group_fill
    card_desc_cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[current_row].height = 42
    for c in range(1, len(columns) + 1):
        ws.cell(row=current_row, column=c).border = thin_border
        ws.cell(row=current_row, column=c).fill = group_fill
    current_row += 1

    # 3. Write data rows for this group
    for case_info in g["cases"]:
        tid = case_info["turn_id"]
        
        # Populate data from CSV or Live
        if case_info["type"] == "csv":
            row_data = df_chatlog[df_chatlog["turn_id"] == tid].iloc[0]
            cohort = str(row_data.get("cohort_hint", ""))
            lecture = str(row_data.get("lecture_title", ""))
            q_text = str(row_data.get("student_question", ""))
            ans_text = str(row_data.get("tutor_reply", ""))
            rep_len = int(row_data.get("reply_len", len(ans_text)))
            has_cite = bool(row_data.get("has_citation", False))
            rating = str(row_data.get("rating", ""))
            if rating == "nan" or not rating:
                rating = "None"
            is_preset = bool(row_data.get("is_preset", False))
            rep_ms = int(row_data.get("reply_ms", 0)) if pd.notna(row_data.get("reply_ms")) else 0
        else:
            cohort = case_info["cohort_hint"]
            lecture = case_info["lecture_title"]
            q_text = case_info["student_question"]
            ans_text = case_info["tutor_reply"]
            rep_len = case_info["reply_len"]
            has_cite = case_info["has_citation"]
            rating = "None" if case_info["rating"] is None else str(case_info["rating"])
            is_preset = case_info["is_preset"]
            rep_ms = case_info["reply_ms"]

        values = [
            case_info["stt"],
            tid,
            g["name"],
            cohort,
            lecture,
            q_text,
            ans_text,
            rep_len,
            "TRUE" if has_cite else "FALSE",
            rating,
            case_info["lo_hong_chinh"],
            case_info["hau_qua_ux"],
            case_info["ky_vong_cai_tien"],
            "TRUE" if is_preset else "FALSE",
            rep_ms
        ]

        for col_idx, val in enumerate(values, 1):
            c = ws.cell(row=current_row, column=col_idx, value=val)
            c.font = font_bold_id if col_idx == 2 else font_data
            c.alignment = columns[col_idx - 1][2]
            c.border = thin_border
            
            # Highlight special cells
            if col_idx == 9 and val == "FALSE":
                c.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # light red
                c.font = Font(name="Calibri", size=10, bold=True, color="C00000")
            elif col_idx == 10 and val == "down":
                c.fill = PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid") # red orange
                c.font = Font(name="Calibri", size=10, bold=True, color="C00000")
            elif col_idx == 8 and int(val) > 1000:
                c.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # yellow
                c.font = Font(name="Calibri", size=10, bold=True, color="B25900")

        ws.row_dimensions[current_row].height = 65
        current_row += 1

    # Optional empty separator row between groups
    current_row += 1

# Auto-adjust column widths based on defined widths
for col_idx, (_, col_width, _) in enumerate(columns, 1):
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = col_width

# Save workbook
output_path = "eval/bang_20_test_cases_lo_hong.xlsx"
wb.save(output_path)
print(f"Successfully generated {output_path} with all 20 cases and group cards!")
