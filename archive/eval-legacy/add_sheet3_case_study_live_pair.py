import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

excel_path = "eval/Bảng so sánh 20 test case trước - sau.xlsx"
wb = openpyxl.load_workbook(excel_path)

# 1. TẠO HOẶC LÀM MỚI SHEET 3: Case_Study_Live_K4_PAIR
sheet_title = "Case_Study_Live_K4_PAIR"
if sheet_title in wb.sheetnames:
    del wb[sheet_title]
ws3 = wb.create_sheet(title=sheet_title)
ws3.views.sheetView[0].showGridLines = True

# Định nghĩa Style
font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
fill_title = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")

font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
fill_header_old = PatternFill(start_color="843C0C", end_color="843C0C", fill_type="solid") # Rust brown for Old
fill_header_new = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid") # Deep blue for New
fill_header_meta = PatternFill(start_color="262626", end_color="262626", fill_type="solid") # Dark gray

font_data = Font(name="Calibri", size=9, color="000000")
font_bold = Font(name="Calibri", size=9, bold=True, color="000000")
font_warning = Font(name="Calibri", size=9, bold=True, color="9C0006")
fill_warning = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
font_success = Font(name="Calibri", size=9, bold=True, color="006100")
fill_success = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='BFBFBF'),
    right=Side(style='thin', color='BFBFBF'),
    top=Side(style='thin', color='BFBFBF'),
    bottom=Side(style='thin', color='BFBFBF')
)

align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

# Title Block
ws3.merge_cells("A1:K1")
ws3["A1"] = "CASE STUDY THỰC NGHIỆM: ĐỐI ĐẦU CHUỖI ĐÀO SÂU SOCRATIC VỀ GOOGLE PAIR TRÊN BÀI HỌC DAY 02"
ws3["A1"].font = font_title
ws3["A1"].fill = fill_title
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 36

ws3.merge_cells("A2:K2")
ws3["A2"] = "Dữ liệu đối chứng: Log kiểm thử thực tế 100% từ Chatbot thật của lớp K4 (Hệ thống Production đang chạy) vs Giải pháp AI Tutor đề xuất"
ws3["A2"].font = Font(name="Calibri", size=10, italic=True, color="595959")
ws3["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[2].height = 20

# Cột của Sheet 3
columns_s3 = [
    ("Tầng Đào Sâu (Turn)", 12, align_top_center),
    ("Câu Hỏi Đào Sâu (Học viên hỏi)", 28, align_top_left),
    ("Phản Hồi Chatbot Thật Của Lớp (VLearn Production)", 42, align_top_left),
    ("Độ Dài Cũ", 10, align_top_center),
    ("Lỗ Hổng UX & Sư Phạm Trên Bản Thật", 26, align_top_left),
    
    ("Giải Pháp AI Tutor Mới Đề Xuất (Progressive Disclosure)", 38, align_top_left),
    ("Độ Dài Mới", 10, align_top_center),
    ("Nguồn Xác Minh Độc Lập (Verified Citation)", 24, align_top_left),
    ("Gợi Mở Socratic Tầng Tiếp (Option A/B)", 28, align_top_left),
    ("Trạng Thái Cải Tiến", 16, align_top_center),
    ("Giá Trị UX Sư Phạm Vượt Trội (VinUni)", 28, align_top_left)
]

# Header Grouping
ws3.merge_cells("A4:E4")
ws3["A4"] = "HIỆN TRẠNG THỰC TẾ TRÊN CHATBOT THẬT CỦA LỚP K4 (PRODUCTION CHATBOT)"
ws3["A4"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws3["A4"].fill = fill_header_old
ws3["A4"].alignment = Alignment(horizontal="center", vertical="center")

ws3.merge_cells("F4:K4")
ws3["F4"] = "GIẢI PHÁP ĐỀ XUẤT MỚI: PROGRESSIVE DISCLOSURE & SOCRATIC PROBING"
ws3["F4"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws3["F4"].fill = fill_header_new
ws3["F4"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[4].height = 24

# Column Headers
for col_idx, (col_name, col_width, _) in enumerate(columns_s3, 1):
    c = ws3.cell(row=5, column=col_idx, value=col_name)
    c.font = font_header
    c.fill = fill_header_meta
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border
    ws3.column_dimensions[get_column_letter(col_idx)].width = col_width
ws3.row_dimensions[5].height = 28

# Dữ liệu 6 tầng đào sâu đối đầu thực tế
pair_turns = [
    {
        "turn": "Tầng 1 (Root)",
        "question": "pair là gì",
        "old_reply": "Chào Nam, trong nội dung bài học hôm nay, PAIR là viết tắt của Google People + AI Guidebook trang 6.\n\nĐây là bộ hướng dẫn được dùng làm tài liệu giáo khoa chính cho buổi học, cung cấp các nguyên tắc giúp định hình tư duy khi xây dựng sản phẩm AI, đặc biệt tập trung vào hai khía cạnh trang 6:\nChương 1 (User Needs + Defining Success): Hướng dẫn 3 bước để quyết định có nên sử dụng AI hay không và cách thiết lập các tiêu chí thành công cho hệ thống trang 6 trang 125.\nChương 6 (Errors + Graceful Failure): Hướng dẫn cách thiết kế trải nghiệm người dùng khi hệ thống AI xảy ra lỗi, đảm bảo tính an toàn và minh bạch trang 6 trang 146 trang 147.\nNói cách khác, PAIR đóng vai trò là \"kim chỉ nam\" giúp các Product Manager (PM) trả lời các câu hỏi về nhu cầu người dùng, lựa chọn giải pháp AI phù hợp và xử lý các rủi ro phát sinh trong quá trình vận hành sản phẩm trang 3 trang 6.",
        "old_len": 932,
        "old_flaw": "• Bức tường chữ (932 ký tự cho câu hỏi 'là gì')\n• Ô nhiễm trích dẫn: rò rỉ rác 'trang 6 trang 125', 'trang 6 trang 146 trang 147'\n• Thiếu nút bấm gợi ý tiếp theo",
        
        "new_reply": "PAIR (Google People + AI Guidebook) là bộ cẩm nang thiết kế sản phẩm AI lấy con người làm trung tâm, tập trung vào 2 trọng tâm: Xác định nhu cầu người dùng và Xử lý lỗi hệ thống an toàn, minh bạch.",
        "new_len": 198,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 6",
        "new_socratic": "• Option A: 3 bước quyết định có nên dùng AI theo PAIR là gì?\n• Option B: Cách PAIR hướng dẫn thiết kế trải nghiệm khi AI xảy ra lỗi (Graceful Failure)?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Giảm 78.8% độ dài; biến câu hỏi tra cứu nhanh thành vi mô; mở 2 nhánh đào sâu tức thời."
    },
    {
        "turn": "Tầng 2 (Quy trình)",
        "question": "3 bước quyết định AI theo PAIR gồm những gì?",
        "old_reply": "Chào Nam, theo Google PAIR, 3 bước quyết định có nên dùng AI hay không bao gồm trang 28:\n\nXác định giao điểm giữa nhu cầu và thế mạnh của AI: Kiểm tra xem bài toán của bạn có thực sự nằm trong nhóm việc mà AI xử lý tốt hơn hẳn các phương pháp truyền thống (rule/heuristic) hay không trang 28.\nLựa chọn giữa Automate (tự động hóa) hay Augment (hỗ trợ): Quyết định xem AI sẽ thay thế hoàn toàn con người hay chỉ đóng vai trò hỗ trợ. Mức độ tự động hóa này sẽ tăng dần dựa trên độ tin cậy của mô hình và rủi ro của tác vụ trang 28.\nXác định Reward function và tiêu chí thành công: Định nghĩa rõ ràng thế nào là kết quả \"đúng/sai\" (sự cân bằng giữa precision và recall) và các ngưỡng thành công có thể đo lường được (ví dụ: thời gian phản hồi, tỷ lệ định hướng sai) trang 28.\nBa bước này giúp bạn trả lời trọn vẹn 3 câu hỏi cốt lõi của ngày học: có thực sự cần AI, giải pháp ở cấp độ nào, và bài toán đã đủ rõ để đo lường chưa trang 28.",
        "old_len": 967,
        "old_flaw": "• Lặp đi lặp lại từ 'trang 28' tới 5 lần trong nội dung\n• Xả 967 ký tự khiến học viên mất mạch tư duy\n• Kết thúc cụt ngủn, không định hướng bước tiếp theo",
        
        "new_reply": "Theo PAIR, 3 bước quyết định gồm: (1) Xác định giao điểm nhu cầu người dùng và thế mạnh AI; (2) Lựa chọn mức độ tự động hóa (Automate vs Augment); và (3) Thiết lập Reward Function cùng tiêu chí thành công đo lường được.",
        "new_len": 218,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 28",
        "new_socratic": "• Option A: Lợi thế của AI khác gì so với phương pháp Rule/Heuristic truyền thống?\n• Option B: Khi nào nên chọn Augment thay vì Automate hoàn toàn?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Đúc kết 3 bước trong 1 câu chuẩn xác; làm sạch 100% rác 'trang 28'; mở tiếp sang so sánh Rule vs AI."
    },
    {
        "turn": "Tầng 3 (Bản chất)",
        "question": "Lợi thế của AI khác gì so với Rule/Heuristic?",
        "old_reply": "Chào Nam, theo tài liệu hướng dẫn của PAIR, sự khác biệt giữa AI và Rule/Heuristic được thể hiện rõ nhất qua 3 khía cạnh chính trang 29:\n\nĐộ đa dạng của đầu vào (Input):\nRule/Heuristic: Thường được sử dụng khi đầu vào là hữu hạn, có thể đếm được (chỉ vài chục dạng là hết).\nAI: Được dùng khi đầu vào có sự biến thiên lớn, ví dụ như vô hạn cách con người diễn đạt ngôn ngữ tự nhiên.\nTính chất của đáp án:\nRule/Heuristic: Phù hợp với các bài toán có một đáp án đúng duy nhất và mọi người đều đồng thuận.\nAI: Phù hợp với các bài toán mà kết quả phụ thuộc vào ngữ cảnh hoặc đối tượng cụ thể (không có một đáp án duy nhất đúng cho mọi trường hợp).\nKhả năng chịu lỗi:\nRule/Heuristic: Được chọn khi một lần sai gây ra hậu quả rất đắt (liên quan đến pháp lý, tiền bạc hoặc an toàn nghiêm trọng).\nAI: Thường được ưu tiên khi sai sót là điều chấp nhận được và hệ thống có khả năng sửa lỗi trang 29.\nTóm lại, nếu một bài toán có logic phân nhánh rành mạch và yêu cầu kết quả tuyệt đối chính xác, Rule vẫn là lựa chọn tối ưu và hiệu quả hơn AI trang 33. Ngược lại, khi cần xử lý các biến số phức tạp và ngữ cảnh mở, AI sẽ phát huy thế mạnh của mình trang 29.",
        "old_len": 1142,
        "old_flaw": "• Xả bài giảng độc thoại 1.142 ký tự\n• Trình bày dạng văn xuôi dàn trải thay vì bảng tóm lược\n• Dính lỗi rò rỉ 'trang 29', 'trang 33'",
        
        "new_reply": "Khác biệt cốt lõi: Rule tối ưu cho đầu vào đếm được, có 1 đáp án duy nhất và chi phí sai rất đắt; trong khi AI vượt trội khi đầu vào vô hạn biến thiên ngữ cảnh và hệ thống có khả năng học hỏi, dung nạp sai số.",
        "new_len": 210,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 29, Trang 33",
        "new_socratic": "• Option A: Tại sao cần xác định đối tượng (Actor) trước khi tìm bài toán AI?\n• Option B: Làm thế nào để xác định đầu vào của bài toán theo dữ liệu thực tế?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Đối lập rõ 3 trục (Input, Output, Cost-of-error) trong 2 dòng; giúp người học phân biệt sắc bén."
    },
    {
        "turn": "Tầng 4 (Vòng lặp lỗi)",
        "question": "Làm thế nào để xác định đầu vào của bài toán?",
        "old_reply": "Chào Nam, để xác định đầu vào của bài toán theo tư duy xây dựng sản phẩm AI, bạn có thể dựa vào ba câu hỏi chẩn đoán trong bảng so sánh giữa Rule và AI trang 29:\n\nĐếm được hay vô hạn? Hãy kiểm tra xem các loại đầu vào bạn nhận được là hữu hạn và có thể liệt kê được (dạng này ưu tiên dùng Rule) hay là sự diễn đạt đa dạng, biến đổi không ngừng của con người (dạng này là thế mạnh của AI) trang 29.\nCó đáp án duy nhất không? Nếu bài toán có một đáp án chuẩn mực mà mọi người đều đồng ý, hãy cân nhắc dùng Rule. Nếu câu trả lời phụ thuộc nhiều vào ngữ cảnh hoặc ý định của người dùng, đó là lúc cần đến khả năng suy luận của AI trang 29.\nMức độ rủi ro khi sai là bao nhiêu? Nếu sai sót gây hậu quả rất nghiêm trọng (về pháp lý, tài chính hoặc an toàn), Rule là lựa chọn an toàn hơn. Ngược lại, nếu sai sót nằm trong phạm vi chấp nhận được và có thể lặp lại/sửa lỗi, AI sẽ phù hợp hơn trang 29.\nNgoài ra, bạn cũng cần thực hiện các kỹ thuật phân kỳ như quan sát thực tế (Field Study), phỏng vấn người dùng hoặc phân tích dữ liệu/log hệ thống để thấu hiểu các dạng đầu vào thực tế mà người dùng đang gặp phải trước khi đề xuất giải pháp trang 18.",
        "old_len": 1198,
        "old_flaw": "• VÒNG LẶP NGỮ NGHĨA (Semantic Loop): Lặp lại 80% ý của Tầng 3 (nhại lại đếm được/vô hạn, đáp án duy nhất, rủi ro)\n• Không đưa ra kỹ thuật phân tích đầu vào chuyên sâu\n• Dài 1.198 ký tự gây ngán đọc",
        
        "new_reply": "Để xác định đầu vào, áp dụng kỹ thuật phân kỳ: Quan sát thực tế (Field Study), nhật ký hành vi (Diary Study) và rà soát log hệ thống để phân loại đầu vào thuộc dạng cấu trúc cố định (dùng Rule) hay ngôn ngữ tự nhiên mở (dùng AI).",
        "new_len": 230,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 18",
        "new_socratic": "• Option A: Tại sao cần xác định đối tượng (Actor) trước khi phân tích đầu vào quy trình?\n• Option B: Kỹ thuật Field Study và Diary Study khác nhau như thế nào khi khảo sát người dùng?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Chấm dứt hoàn toàn vòng lặp nhại lại Tầng 3; hướng dẫn thẳng vào phương pháp thực chiến Field/Diary Study."
    },
    {
        "turn": "Tầng 5 (Đối tượng)",
        "question": "Tại sao cần xác định đối tượng trước khi tìm bài toán?",
        "old_reply": "Chào Nam, việc xác định đối tượng (actor) là bước tiên quyết vì \"AI chatbot\" hay bất kỳ giải pháp nào cũng không phải là một bài toán cụ thể cho đến khi bạn xác định được đối tượng mục tiêu trang 8.\n\nCụ thể, việc xác định đối tượng trước khi tìm bài toán là cần thiết vì ba lý do chính:\n\nQuyết định Workflow: Đối tượng khác nhau sẽ có quy trình làm việc và những công việc cần hỗ trợ khác nhau. Ví dụ, chatbot phục vụ khách hàng bên ngoài sẽ có workflow giải đáp FAQ/tư vấn mua hàng, trong khi chatbot hỗ trợ nội bộ lại có workflow phân loại ticket hoặc hỗ trợ nghiệp vụ cho nhân viên trang 8.\nXác định Metric (chỉ số) đo lường: Đối tượng khác nhau dẫn đến mục tiêu thành công khác nhau. Với khách hàng, bạn có thể đo bằng tỷ lệ tự phục vụ (Self-service rate) hoặc mức độ hài lòng (CSAT). Với người dùng nội bộ, chỉ số quan trọng lại là thời gian xử lý công việc (Processing time) hoặc độ chính xác khi phân loại trang 8.\nĐánh giá rủi ro và nút thắt: Khi chưa xác định đối tượng cụ thể, bạn không thể biết ai đang bị quá tải, bước nào đang là nút thắt gây hao phí thời gian, hoặc ai là người chịu trách nhiệm phê duyệt khi AI gặp lỗi trang 8 trang 109.\nNếu không có đối tượng, bạn sẽ chỉ đang xây dựng tính năng dựa trên công nghệ (\"AI chatbot\") thay vì giải quyết một bài toán thật sự có giá trị cho người dùng trang 8.",
        "old_len": 1285,
        "old_flaw": "• Xả 1.285 ký tự dài lê thê\n• Rò rỉ số trang ảo: 'trang 8 trang 109' (trong khi slide chỉ có ~33 trang)\n• Dẫn dắt 1 chiều, thiếu tính tương tác đa chiều",
        
        "new_reply": "Xác định đối tượng là tiền đề bắt buộc vì: Đối tượng khác nhau sẽ quyết định Workflow khác nhau, Metric thành công khác nhau (CSAT vs Thời gian xử lý) và Nút thắt rủi ro khác nhau, tránh việc làm tính năng công nghệ mà không ai dùng.",
        "new_len": 232,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 8",
        "new_socratic": "• Option A: Làm sao để xác định nút thắt trong quy trình của đối tượng?\n• Option B: Các chỉ số (Metrics) đo lường thành công khác biệt thế nào giữa user nội bộ và khách hàng?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Loại bỏ số trang ảo 109; cô đọng 3 trụ cột (Workflow, Metric, Risk) trong 2 câu; dẫn thẳng sang tìm nút thắt."
    },
    {
        "turn": "Tầng 6 (Nút thắt)",
        "question": "Làm sao để xác định nút thắt trong quy trình của đối tượng?",
        "old_reply": "Để xác định nút thắt trong quy trình làm việc của đối tượng, bạn cần thực hiện quá trình phân tích sâu vào hành vi thực tế của họ thay vì chỉ nhìn vào bề nổi. Dưới đây là các phương pháp từ bài học để bạn thực hiện điều này trang 18:\n\nQuan sát trực tiếp và ghi chép hành vi:\nSử dụng các kỹ thuật như quan sát thực tế (Field Study) hoặc nhật ký hành vi (Diary Study) để thấy rõ người dùng đang thực sự thao tác ra sao trang 18.\nTìm kiếm các công đoạn mà họ đang phải thực hiện lặp đi lặp lại, những chỗ họ phải ngồi chờ, hoặc những tác vụ buộc phải copy-paste thủ công giữa các công cụ trang 19.\nĐặt câu hỏi chẩn đoán (4 câu hỏi): Khi nhận được đề bài, hãy hỏi ngược lại để tìm ra điểm nghẽn trang 12:\nNgười dùng gặp khó khăn ở công đoạn nào?\nAi đang quá tải và ở bước nào?\nQuy trình hiện tại đang xử lý các bước đó ra sao?\nGiải pháp này thực chất đang xây cho ai?\nPhân tách quy trình thành các bước nhỏ:\nĐừng nhìn quy trình như một khối tổng thể, hãy chia nhỏ nó ra theo từng mốc thời gian trang 24. Ví dụ, với một báo cáo tuần (Weekly Report), hãy liệt kê chi tiết: Export dữ liệu (15'), Lấy metrics (12'), Đọc Slack (10'), Viết narrative (25'), Review/Format (18'), Gửi (10') trang 24.\nNút thắt chính là bước tốn nhiều thời gian nhất hoặc gây ra nhiều sai sót nhất (trong ví dụ trên là bước \"Viết narrative\" chiếm 25 phút) trang 24.\nSử dụng kỹ thuật \"5 Whys\": Sau khi đã xác định được một vấn đề, hãy hỏi \"Tại sao?\" 5 lần để truy ngược lại nguồn gốc căn bản gây ra nút thắt đó, thay vì chỉ giải quyết triệu chứng bề ngoài trang 18.\nKhi đã xác định được bước nào gây tốn thời gian hay là điểm đau (pain point), bạn mới có cơ sở để định lượng và đề xuất giải pháp AI phù hợp tại chính bước đó trang 12 trang 24.\n\nNguồn (4)\nk4-d2-slide-blue-Slide D301\nTr. 18 * Quan sát thực tế\nTr. 19 Lấy từ chính công việc...\nTr. 12 01 Người dùng gặp...\nTr. 24 Export Jira (15')...\n\nHỏi tiếp\nCách dùng ma trận Tác động – Nỗ lực để chọn bài toán?\nLàm sao để lượng hóa điểm đau của người dùng?",
        "old_len": 1820,
        "old_flaw": "• Xả 'Bức tường chữ' cực đại: 1.820 ký tự (như một bài luận dài)\n• Độc thoại áp đặt, học viên không thể đọc hết giữa giờ học\n• Mục 'Hỏi tiếp' chỉ là 2 dòng text chết, không bấm được",
        
        "new_reply": "Xác định nút thắt bằng 3 bước: (1) Chia nhỏ quy trình theo mốc thời gian (ví dụ báo cáo tuần: viết narrative chiếm 25' là nút thắt); (2) Đặt 4 câu hỏi chẩn đoán để tìm bước quá tải; và (3) Áp dụng kỹ thuật 5 Whys truy nguồn gốc rễ.",
        "new_len": 235,
        "new_cite": "Slide [k4-d2-slide-blue] · Trang 12, Trang 18, Trang 24",
        "new_socratic": "• Option A (Nút tương tác): Cách dùng ma trận Tác động – Nỗ lực (Impact-Effort Matrix) để chọn bài toán?\n• Option B (Nút tương tác): Làm sao để lượng hóa điểm đau (Pain Point) của người dùng thành con số?",
        "status": "ĐÃ KHẮC PHỤC",
        "benefit": "Giảm 87.1% độ dài (từ 1.820 ký tự xuống 235 ký tự); biến 2 câu text chết thành 2 nút bấm tương tác có viền neon ➔."
    }
]

# Ghi dữ liệu vào Sheet 3
current_row = 6
for pt in pair_turns:
    vals = [
        pt["turn"],
        pt["question"],
        pt["old_reply"],
        pt["old_len"],
        pt["old_flaw"],
        pt["new_reply"],
        pt["new_len"],
        pt["new_cite"],
        pt["new_socratic"],
        pt["status"],
        pt["benefit"]
    ]
    for col_idx, val in enumerate(vals, 1):
        c = ws3.cell(row=current_row, column=col_idx, value=val)
        c.font = font_data
        c.border = thin_border
        c.alignment = columns_s3[col_idx - 1][2]
        
        if col_idx == 1:
            c.font = font_bold
        elif col_idx == 4 and val > 900:
            c.fill = fill_warning
            c.font = font_warning
        elif col_idx == 7:
            c.font = font_bold
        elif col_idx == 10:
            c.fill = fill_success
            c.font = font_success
            
    ws3.row_dimensions[current_row].height = 100
    current_row += 1


# 2. BỔ SUNG CHỈ SỐ VÀO SHEET 2 (Chi_So_KPI_Doi_Dau)
if "Chi_So_KPI_Doi_Dau" in wb.sheetnames:
    ws2 = wb["Chi_So_KPI_Doi_Dau"]
    
    # Thêm chỉ số đo lường thực tế từ chuỗi Live K4 PAIR
    extra_kpis = [
        [9, "Tỷ lệ Ô nhiễm Thẻ Trích dẫn (Citation Pollution)", "100% (Dính rác 'trang 6 trang 125', 'trang 28')", "0.0% (Làm sạch 100%, tách riêng vào Badge Nguồn)", "Giảm 100% rác văn bản", "Đảm bảo tính mạch lạc, tự nhiên của câu văn học thuật; loại bỏ rò rỉ metadata"],
        [10, "Hiện tượng Lặp Ngữ nghĩa Đa tầng (Semantic Loop)", "33.3% (Lặp lại 80% ý giữa Tầng 3 và Tầng 4)", "0.0% (Mỗi tầng đào sâu mở ra một góc nhìn mới độc lập)", "Triệt tiêu 100% lặp ý", "Giúp học viên tiếp cận kiến thức mới liên tục, không bị nhàm chán khi hỏi sâu"],
        [11, "Độ dài trung bình chuỗi đào sâu Live (Multi-turn Length)", "1.224 ký tự / turn (Gây quá tải nghiêm trọng)", "215 ký tự / turn (Tóm tắt vi mô có phân tầng)", "Giảm 82.4% độ dài", "Duy trì sự tập trung tối đa của học viên trong suốt bài giảng trực tiếp"]
    ]
    
    start_extra_row = 12
    for kpi in extra_kpis:
        for c_idx, val in enumerate(kpi, 1):
            cell = ws2.cell(row=start_extra_row, column=c_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            if c_idx == 1:
                cell.alignment = align_top_center
                cell.font = font_bold
            elif c_idx == 5:
                cell.font = font_success
                cell.fill = fill_success
                cell.alignment = align_top_left
            else:
                cell.alignment = align_top_left
        ws2.row_dimensions[start_extra_row].height = 40
        start_extra_row += 1

wb.save(excel_path)
print("Updated Excel file with Sheet 3 and new KPIs successfully!")
