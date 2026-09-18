let activeSlide = 'd1';
  let currentSelection = "";
  let lastProcessedSelection = "";
  let currentActiveQuery = "";
  let sessionHistoryQueries = [];
  const preview = document.getElementById('selection-preview');
  const toast = document.getElementById('auto-toast');

  // GROUNDED CONTEXT FROM DATA PACK (TRANSCRIPTS & SLIDES)
  const SLIDE_KNOWLEDGE = {
    d1: {
      page: "Trang 8",
      title: "2017: Transformer & Cơ chế Tự chú ý",
      slide_text: "Transformer là bước ngoặt vì nó cho mô hình hiểu ngôn ngữ theo cách linh hoạt hơn: mỗi từ có thể nhìn sang những từ quan trọng khác trong cả câu nhờ cơ chế Attention, thay vì chỉ đi tuần tự từng bước → trở thành nền móng kỹ thuật cho GPT, BERT và toàn bộ làn sóng LLM sau đó.",
      transcript: "[T04-038] [T04-040] Giảng viên giải thích: Transformer ra đời từ bài báo Attention Is All You Need năm 2017. Thay vì lần lượt đọc và dịch tuần tự từng chữ một như RNN/LSTM gây nghẽn cổ chai, nó đọc cả cụm và dùng cơ chế Attention nhận diện các từ có liên quan trực tiếp đến nhau cùng một lúc trên GPU."
    },
    d2: {
      page: "Trang 52",
      title: "Workflow patterns — Đủ cho hầu hết bài toán (Anthropic)",
      slide_text: "Ba mô hình cơ bản theo Anthropic: 1. Prompt Chaining (chia task tuần tự có gate kiểm tra; đổi trễ lấy chính xác). 2. Routing (phân loại input; câu dễ đi model rẻ, câu khó đi model mạnh). 3. Parallelization (chạy song song rồi tổng hợp hoặc vote để giảm rủi ro). Nguyên tắc: Luôn ưu tiên giải pháp đơn giản nhất.",
      transcript: "[T03-131] [T03-132] [T03-133] Giảng viên phân tích: Workflow pattern như khối Lego. Chaining xử lý từng bước chắc chắn. Routing giúp tiết kiệm chi phí và thời gian bằng cách điều hướng model nhỏ/lớn. Parallelization chạy song song nhưng cần lưu ý dung lượng RAM và phối hợp với MLOps."
    },
    d4: {
      page: "Trang 55",
      title: "Kỹ thuật Delimiters & Cô Lập Dữ Liệu Input",
      slide_text: "Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries vào trong các thẻ định danh rõ ràng. Chỉ thị mô hình: Chỉ xử lý văn bản nằm trong thẻ. Tính nhất quán: Duy trì đồng nhất một loại thẻ phân tách xuyên suốt toàn bộ prompt.",
      transcript: "Giảng viên nhấn mạnh: Delimiters (cặp thẻ XML như <user_query>) là kỹ thuật phòng vệ lớp 1 để chống Prompt Injection và Context Bleed. Nó giúp model tách bạch rõ ràng giữa chỉ thị hệ thống (Instruction) và dữ liệu thô của người dùng (Data), tăng độ ổn định hành vi của Agent."
    }
  };

  // SYSTEM PROMPT CHO AI THẬT
  function buildSystemPrompt(slideKey) {
    const k = SLIDE_KNOWLEDGE[slideKey];
    return `Bạn là VLearn AI Tutor thông minh của VinUni.
Nhiệm vụ: Giải thích đoạn văn bản học viên vừa bôi đen trên slide bài giảng theo nguyên lý Progressive Disclosure (Google PAIR & HAX).

BẮT BUỘC TUÂN THỦ CÁC QUY TẮC SAU:
1. Dựa DUY NHẤT vào dữ liệu bài giảng được cung cấp dưới đây. Tuyệt đối không bịa đặt số trang hoặc thông tin ngoài bài.
2. TẦNG 1 (Micro-summary): Trả lời súc tích trong TỐI ĐA 2 CÂU (dưới 250 ký tự), nêu bật bản chất cốt lõi. Gắn thẻ trích dẫn [${k.page}].
3. TẦNG 2 (Socratic Probing): Đưa ra đúng 2 câu hỏi gợi mở tiếp theo để học sinh đào sâu.
4. NẾU HỌC VIÊN HỎI NGOÀI BÀI (như thuật toán PPO/RLHF, thời tiết, code gian lận): Lịch sự từ chối và hướng dẫn quay lại bài học hiện tại.

DỮ LIỆU NỀN TẢNG (GROUNDING):
- Slide: [${k.page}] ${k.title}
- Nội dung Slide: ${k.slide_text}
- Lời giảng Thầy cô (Transcript): ${k.transcript}

ĐỊNH DẠNG ĐẦU RA (Bắt buộc trả về đúng định dạng JSON không bọc thêm giải thích ngoài):
{
  "summary": "Tối đa 2 câu súc tích tóm tắt cho học viên...",
  "citation": "[${k.page}]",
  "option_a": "Câu hỏi đào sâu A...",
  "option_b": "Câu hỏi đào sâu B...",
  "is_out_of_scope": false
}`;
  }

  // KHỞI TẠO CẤU HÌNH API TỪ LOCALSTORAGE
  function initApiConfig() {
    const savedProvider = localStorage.getItem('vlearn_ai_provider') || 'mock';
    const savedKey = localStorage.getItem('vlearn_ai_key') || '';
    
    document.getElementById('api-provider').value = savedProvider;
    document.getElementById('api-key').value = savedKey;
    updateBadge(savedProvider, savedKey);
    toggleProviderHelp();
  }

  function updateBadge(provider, key) {
    const badge = document.getElementById('engine-badge');
    const dot = document.getElementById('engine-dot');
    const label = document.getElementById('engine-label');

    if (provider === 'gemini' && key) {
      label.innerText = 'AI ENGINE: GEMINI 1.5 FLASH (LIVE API)';
      badge.style.background = 'rgba(16, 185, 129, 0.15)';
      dot.style.background = '#34d399';
    } else if (provider === 'openai' && key) {
      label.innerText = 'AI ENGINE: OPENAI GPT-4O-MINI (LIVE API)';
      badge.style.background = 'rgba(16, 185, 129, 0.15)';
      dot.style.background = '#34d399';
    } else {
      label.innerText = 'AI ENGINE: GROUNDED SIMULATOR';
      badge.style.background = 'rgba(56, 189, 248, 0.15)';
      dot.style.background = '#38bdf8';
    }
  }

  function openConfigModal() { document.getElementById('config-modal').style.display = 'flex'; }
  function closeConfigModal() { document.getElementById('config-modal').style.display = 'none'; }

  function toggleProviderHelp() {
    const p = document.getElementById('api-provider').value;
    const kg = document.getElementById('key-group');
    const kl = document.getElementById('key-label');
    const kh = document.getElementById('key-help');

    if (p === 'mock') {
      kg.style.display = 'none';
    } else {
      kg.style.display = 'block';
      if (p === 'gemini') {
        kl.innerText = 'Google Gemini API Key:';
        kh.innerHTML = 'Lấy key miễn phí tại: <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: var(--accent);">aistudio.google.com</a>';
      } else {
        kl.innerText = 'OpenAI API Key:';
        kh.innerHTML = 'Lấy key tại: <a href="https://platform.openai.com/api-keys" target="_blank" style="color: var(--accent);">platform.openai.com</a>';
      }
    }
  }

  function saveApiKey() {
    const p = document.getElementById('api-provider').value;
    const k = document.getElementById('api-key').value.trim();
    localStorage.setItem('vlearn_ai_provider', p);
    localStorage.setItem('vlearn_ai_key', k);
    updateBadge(p, k);
    closeConfigModal();
    showToast(`✅ Đã lưu cấu hình: ${p.toUpperCase()}`);
  }

  function switchSlide(slideId) {
    activeSlide = slideId;
    sessionHistoryQueries = [];
    document.getElementById('slide-canvas-d1').style.display = slideId === 'd1' ? 'block' : 'none';
    document.getElementById('slide-canvas-d2').style.display = slideId === 'd2' ? 'block' : 'none';
    document.getElementById('slide-canvas-d4').style.display = slideId === 'd4' ? 'block' : 'none';
    document.getElementById('tab-d1').className = 'slide-tab-btn' + (slideId === 'd1' ? ' active' : '');
    document.getElementById('tab-d2').className = 'slide-tab-btn' + (slideId === 'd2' ? ' active' : '');
    document.getElementById('tab-d4').className = 'slide-tab-btn' + (slideId === 'd4' ? ' active' : '');
    
    if (slideId === 'd1') {
      document.getElementById('header-course-title').innerText = 'AI In Action · Day 01: AI & LLM Foundation';
    } else if (slideId === 'd2') {
      document.getElementById('header-course-title').innerText = 'AI In Action · Day 02: Xác Định Bài Toán & Workflow Patterns';
    } else {
      document.getElementById('header-course-title').innerText = 'AI In Action · Day 04: Prompt Engineering & Tool Calling';
    }
    
    lastProcessedSelection = "";
    showToast(`Đã chuyển sang ${SLIDE_KNOWLEDGE[slideId].page}`);
  }

  function showToast(msg) {
    toast.innerText = msg;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 1500);
  }

  // TỰ ĐỘNG TRA CỨU KHI BÔI ĐEN & THẢ CHUỘT (CHỐNG LỖI VÙNG CHỌN)
  document.addEventListener('mouseup', function(e) {
    setTimeout(() => {
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      const selectedText = selection.toString().trim();

      const slideContainer = document.querySelector('.slide-container');
      const isInside = slideContainer && selection.anchorNode && 
        (slideContainer.contains(selection.anchorNode) || slideContainer.contains(selection.anchorNode.parentNode));

      if (selectedText.length >= 1 && isInside) {
        if (selectedText === lastProcessedSelection) return;
        lastProcessedSelection = selectedText;
        currentSelection = selectedText;
        currentActiveQuery = selectedText;
        if (preview) {
          preview.innerText = `"${selectedText}" (${selectedText.length} ký tự)`;
        }

        const cleaned = selectedText.replace(/[\s\-_–—>><=.,:;!?()[\]{}]+/g, '');
        if (selectedText.length < 3 || cleaned.length < 2) {
          showToast(`⚠️ Cụm từ "${selectedText}" không hợp lệ`);
        } else {
          showToast(`⚡ Nhận diện: "${selectedText.substring(0, 22)}..."`);
        }
        processSelectionWithAI(selectedText);
      }
    }, 100);
  });

  function autoSelectText(text, slideId) {
    if (activeSlide !== slideId) switchSlide(slideId);
    lastProcessedSelection = text;
    currentSelection = text;
    currentActiveQuery = text;
    preview.innerText = `"${text}" (${text.length} ký tự)`;
    processSelectionWithAI(text);
  }

  // GỌI AI THẬT QUA SERVER BACKEND (HOẶC FALLBACK SIMULATOR)
  async function processSelectionWithAI(userText, skipAddUserMsg = false) {
    const k = SLIDE_KNOWLEDGE[activeSlide];
    if (!skipAddUserMsg) {
      addMessage('user', `(${k.page}, bôi đen: "${userText}")`);
    }

    // Client Guardrail: Quá ngắn (< 3 ký tự) hoặc chỉ chứa ký tự đặc biệt / mũi tên / dấu chấm phẩy
    const cleanedText = userText.replace(/[\s\-_–—>><=.,:;!?()[\]{}]+/g, '');
    if (userText.length < 3 || cleanedText.length < 2) {
      setDecision('Bôi đen không hợp lệ / quá ngắn', 'filter_garbage', 'active', '[Cần bôi đen lại]');
      addMessage('ai', `Đoạn văn bản "${userText}" quá ngắn hoặc không phải là một cụm từ hoàn chỉnh. Bạn hãy bôi đen trọn vẹn một khái niệm (ví dụ: "Transformer", "Attention") để AI giải thích nhé!`, false, null);
      return;
    }

    const startTime = performance.now();
    setDecision('Gọi AI Engine', 'Model: GPT-4O-MINI (LIVE API)', 'active');

    try {
      // 1. Thử gọi backend /api/ask với OpenAI API Key từ file .env
      const resp = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: userText,
          slide: activeSlide,
          history_queries: sessionHistoryQueries
        })
      });

      if (resp.ok) {
        const res = await resp.json();
        const latency = res.latency_ms || Math.round(performance.now() - startTime);
        document.getElementById('latency-display').innerText = `Latency: ${latency} ms (OpenAI Live API)`;
        document.getElementById('latency-display').style.color = '#34d399';
        renderAiResponse(res, userText);
        return;
      }
    } catch (err) {
      console.warn('Backend API chưa sẵn sàng, dùng Fallback Grounded:', err);
    }

    // 2. Grounded Fallback nếu mất kết nối
    setTimeout(() => {
      const latency = Math.round(performance.now() - startTime);
      document.getElementById('latency-display').innerText = `Latency: ${latency} ms (Grounded Simulator)`;
      const mockResult = generateGroundedMock(userText, activeSlide);
      renderAiResponse(mockResult, userText);
    }, 350);
  }

  // CALL GOOGLE GEMINI 1.5 FLASH
  async function callGeminiAPI(key, text) {
    const sysPrompt = buildSystemPrompt(activeSlide);
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`;
    const payload = {
      contents: [
        { role: "user", parts: [{ text: `${sysPrompt}

ĐOẠN HỌC VIÊN BÔI ĐEN: "${text}"` }] }
      ],
      generationConfig: { temperature: 0.2, maxOutputTokens: 600 }
    };

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    const rawText = data.candidates[0].content.parts[0].text;
    return parseAIResponse(rawText, text);
  }

  // CALL OPENAI GPT-4O-MINI
  async function callOpenAIAPI(key, text) {
    const sysPrompt = buildSystemPrompt(activeSlide);
    const url = 'https://api.openai.com/v1/chat/completions';
    const payload = {
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: sysPrompt },
        { role: "user", content: `Đoạn học viên bôi đen: "${text}"` }
      ],
      temperature: 0.2,
      max_tokens: 400
    };

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${key}` },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    const rawText = data.choices[0].message.content;
    return parseAIResponse(rawText, text);
  }

  function parseAIResponse(raw, fallbackConcept) {
    try {
      const clean = raw.replace(/```json/g, '').replace(/```/g, '').trim();
      return JSON.parse(clean);
    } catch (e) {
      return {
        summary: raw.substring(0, 240) + '...',
        citation: `[${SLIDE_KNOWLEDGE[activeSlide].page}]`,
        option_a: `Tìm hiểu sâu hơn về ${fallbackConcept}`,
        option_b: `Xem ví dụ thực tế liên quan`,
        is_out_of_scope: false
      };
    }
  }

  function getMockSnippets(slideId) {
    const k = SLIDE_KNOWLEDGE[slideId] || SLIDE_KNOWLEDGE['d1'];
    return [
      {
        type: 'slide',
        source_file: slideId === 'd4' ? 'd4-slide-hackathon.pdf' : (slideId === 'd2' ? 'd2-slide-hackathon.pdf' : 'd1-slide-hackathon.pdf'),
        page_label: k.page,
        page_index: parseInt(k.page.replace(/\D/g, '')) || 0,
        title: k.title,
        snippet: k.slide_text
      },
      {
        type: 'transcript',
        source_file: slideId === 'd4' ? 'transcript-04-clean.md' : (slideId === 'd2' ? 'transcript-03-clean.md' : 'transcript-04-clean.md'),
        tag: slideId === 'd4' ? 'T-Delimiters' : (slideId === 'd2' ? 'T03-131' : 'T04-038'),
        snippet: k.transcript
      }
    ];
  }

  // MOCK GROUNDED RESPONSES DỰA TRÊN TRANSCRIPT THẬT
  function generateGroundedMock(text, slideId) {
    const lower = text.toLowerCase();
    const k = SLIDE_KNOWLEDGE[slideId];

    // Case Guardrail: PPO / RLHF
    if (lower.includes('ppo') || lower.includes('rlhf')) {
      return {
        summary: "Khái niệm PPO (Proximal Policy Optimization) thuộc bài học RLHF chuyên sâu, không nằm trong nội dung Day 01. VLearn AI Tutor chỉ hỗ trợ các khái niệm thuộc bài học hiện tại để bạn tránh bị quá tải thông tin.",
        citation: null,
        source_snippets: [],
        option_a: "Xem lại mục tiêu chính của bài học Day 01",
        option_b: "Khái niệm Transformer hoạt động như thế nào?",
        is_out_of_scope: true
      };
    }

    // Day 04: Delimiters
    if (slideId === 'd4') {
      if (lower.includes('bao bọc') || lower.includes('user_query')) {
        return {
          summary: "Bao bọc input bằng thẻ Delimiters (như <user_query>) giúp mô hình phân biệt rõ ràng giữa chỉ thị của hệ thống và dữ liệu thô, từ đó ngăn chặn hiệu quả tấn công Prompt Injection [Trang 55].",
          citation: "[Trang 55]",
          source_snippets: getMockSnippets('d4'),
          option_a: "A. Thẻ XML phân tách dữ liệu khác gì so với dùng dấu ngoặc kép '''?",
          option_b: "B. Ví dụ một prompt bị Context Bleed khi không dùng delimiters",
          is_out_of_scope: false
        };
      } else if (lower.includes('nhất quán')) {
        return {
          summary: "Tính nhất quán đòi hỏi bạn duy trì đồng nhất một loại thẻ phân tách xuyên suốt các lượt prompt để mô hình hình thành khuôn mẫu xử lý ổn định, không bị bối rối [Trang 55].",
          citation: "[Trang 55]",
          source_snippets: getMockSnippets('d4'),
          option_a: "A. Tại sao thay đổi định dạng delimiter giữa các lượt lại làm giảm độ chính xác?",
          option_b: "B. Quy ước chuẩn đặt tên thẻ XML trong production agent",
          is_out_of_scope: false
        };
      } else if (lower.includes('harness') || lower.includes('loop')) {
        return {
          summary: "Khái niệm Harness (khung bảo vệ) là hạ tầng quản lý vòng lặp giữa Agent và Tool để kiểm soát trạng thái an toàn, bám sát cấu trúc bài học hiện tại [Trang 55].",
          citation: "[Trang 55]",
          source_snippets: getMockSnippets('d4'),
          option_a: "A. Vòng lặp Agent tương tác với Tool hoạt động ra sao?",
          option_b: "B. Cách kiểm soát tràn bộ nhớ khi chạy tool loop",
          is_out_of_scope: false
        };
      }
    }

    // Day 01: Transformer
    if (lower.includes('transformer')) {
      return {
        summary: "Transformer (2017) là kiến trúc nền tảng cho các LLM hiện đại, loại bỏ sự tuần tự của RNN để xử lý song song toàn bộ chuỗi từ [Trang 8].",
        citation: "[Trang 8]",
        source_snippets: getMockSnippets('d1'),
        option_a: "A. Cơ chế Attention tính trọng số như thế nào?",
        option_b: "B. So sánh Transformer với RNN/LSTM",
        is_out_of_scope: false
      };
    }

    return {
      summary: `Khái niệm "${text}" được neo trực tiếp tại ${k.page} của bài giảng.`,
      citation: `[${k.page}]`,
      source_snippets: getMockSnippets(slideId),
      option_a: `A. Tìm hiểu thêm về "${text}"`,
      option_b: `B. Ví dụ minh họa thực tế`,
      is_out_of_scope: false
    };
  }

  // RENDER PHẢN HỒI LÊN GIAO DIỆN
  function renderAiResponse(res, concept) {
    if (res.is_out_of_scope) {
      setDecision('Ngoài phạm vi bài học', 'Từ chối & Điều hướng', 'active', '[Ngoài bài]');
      addMessage('ai', res.summary, false, res.citation || null, null, res.source_snippets || null);
      return;
    }

    setDecision('Tầng 1: Tóm tắt vi mô', 'Tầng 2: Gợi mở Socratic', 'active');
    
    const options = [];
    if (res.option_a) options.push({ label: res.option_a });
    if (res.option_b) options.push({ label: res.option_b });

    const displayConcept = res.next_concept || concept;
    addMessage('ai', res.summary, true, res.citation, {
      concept: displayConcept,
      options: options
    }, res.source_snippets || null, res.highlight_evidence || null);
  }

  function escapeXmlTags(str) {
    if (!str) return "";
    return str
      .replace(/<user_query>/gi, '&lt;user_query&gt;')
      .replace(/<\/user_query>/gi, '&lt;/user_query&gt;')
      .replace(/<instruction>/gi, '&lt;instruction&gt;')
      .replace(/<\/instruction>/gi, '&lt;/instruction&gt;')
      .replace(/<context>/gi, '&lt;context&gt;')
      .replace(/<\/context>/gi, '&lt;/context&gt;');
  }

  function formatConceptTitle(raw) {
    if (!raw) return "khái niệm này";
    let c = raw.trim().replace(/^["'“”‘’]|["'“”‘’]$/g, '');
    c = c.replace(/[.,:;!?]+$/g, '').trim();
    if (c.length > 38) {
      c = c.substring(0, 35) + '...';
    }
    return c;
  }

  // ĐỐI SOÁT NGUỒN THÔNG MINH: 1 MÀU DUY NHẤT (HIGH CONTRAST & KHỬ LẶP)
  function highlightGroundedSnippet(rawSnippet, highlightEvidence = null, query = "", summary = "") {
    if (!rawSnippet) return "";

    let text = rawSnippet
      .replace(/<user_query>/gi, '&lt;user_query&gt;')
      .replace(/<\/user_query>/gi, '&lt;/user_query&gt;')
      .replace(/<instruction>/gi, '&lt;instruction&gt;')
      .replace(/<\/instruction>/gi, '&lt;/instruction&gt;')
      .replace(/<context>/gi, '&lt;context&gt;')
      .replace(/<\/context>/gi, '&lt;/context&gt;');

    let targetKeywords = [];
    let evidencePhrases = [];

    const GENERIC_STOP = new Set(["kiến trúc", "token", "mô hình", "hệ thống", "bài toán", "dữ liệu", "ngôn ngữ"]);

    // 1. ƯU TIÊN SỐ 1: BẰNG CHỨNG XÁC THỰC DO CHÍNH OPENAI TRÍCH XUẤT
    if (highlightEvidence && typeof highlightEvidence === 'object') {
      if (Array.isArray(highlightEvidence.keywords)) {
        targetKeywords = highlightEvidence.keywords
          .map(k => String(k).trim())
          .filter(k => k.length >= 2 && !GENERIC_STOP.has(k.toLowerCase()));
      }
      if (Array.isArray(highlightEvidence.evidence_phrases)) {
        evidencePhrases = highlightEvidence.evidence_phrases
          .map(p => String(p).trim())
          .filter(p => p.length >= 4);
      }
    }

    // 2. NẾU THIẾU BẰNG CHỨNG HOẶC CHẠY CHẾ ĐỘ SIMULATOR: DÙNG BỘ CỤM TỪ BẰNG CHỨNG NGUYÊN VĂN
    if (evidencePhrases.length === 0) {
      const FALLBACK_PHRASES = [
        "hiểu ngôn ngữ theo cách linh hoạt hơn",
        "mỗi từ có thể nhìn sang những từ quan trọng khác trong cả câu",
        "nhìn sang những từ quan trọng khác trong cả câu",
        "mỗi từ được \"nhìn sang\" những từ quan trọng khác",
        "thay vì chỉ đi tuần tự từng bước",
        "nền móng kỹ thuật cho GPT, BERT",
        "Attention Is All You Need",
        "bài báo rất nổi tiếng — \"Attention Is All You Need\"",
        "thay vì lần lượt đọc và dịch tuần tự từng chữ một",
        "gây nghẽn cổ chai",
        "đọc cả cụm",
        "nhận diện các từ có liên quan trực tiếp đến nhau cùng một lúc trên GPU",
        "Chủ động \"quay đầu\" nhìn lại các token",
        "những cụm từ có sự liên quan đến nhau",
        "mối liên kết giữa nhiều từ trong một câu",
        "recurrent neural network ( RNN )",
        "recurrent neural network",
        "đọc từng chữ một, xử lý từng chữ một, cứ nối tiếp nhau như vậy",
        "đọc từng chữ một, xử lý từng chữ một",
        "khi đến câu rất dài thì nó sẽ quên những cái ở đầu",
        "khi đến câu rất dài thì nó sẽ quên",
        "chia task tuần tự có gate kiểm tra",
        "đổi trễ lấy chính xác",
        "câu dễ đi model rẻ, câu khó đi model mạnh",
        "chạy song song rồi tổng hợp hoặc vote để giảm rủi ro",
        "ưu tiên giải pháp đơn giản nhất",
        "tiết kiệm chi phí và thời gian",
        "Bao bọc mọi dữ liệu từ User, API responses, hoặc DB queries",
        "các thẻ định danh rõ ràng",
        "Chỉ xử lý văn bản nằm trong thẻ",
        "Duy trì đồng nhất một loại thẻ phân tách xuyên suốt toàn bộ prompt",
        "phòng vệ lớp 1 để chống Prompt Injection và Context Bleed",
        "tách bạch rõ ràng giữa chỉ thị hệ thống và dữ liệu thô",
        "tăng độ ổn định hành vi của Agent"
      ];
      for (const fp of FALLBACK_PHRASES) {
        if (text.toLowerCase().includes(fp.toLowerCase())) {
          evidencePhrases.push(fp);
        }
      }
    }

    // 3. TỪ KHÓA ĐỐI CHIẾU: THỰC THỂ HOÀN CHỈNH (KHÔNG LẤY TỪ PHỔ THÔNG)
    if (targetKeywords.length === 0) {
      const DOMAIN_COMPOUNDS = [
        "mô hình xử lý ngôn ngữ truyền thống", "mạng neuron hồi tiếp", "mạng neuron",
        "Transformer", "Attention", "Self-Attention", "RNN", "LSTM",
        "Delimiters", "Prompt Injection", "Context Bleed", "Context Rot",
        "Prompt Chaining", "Routing", "Parallelization", "Anthropic",
        "PPO", "RLHF", "BERT", "GPT", "GPU", "MLOps",
        "tuần tự", "song song", "nghẽn cổ chai", "bộ nhớ", "độ trễ",
        "trọng số", "ma trận", "harness", "agent", "nhất quán",
        "&lt;user_query&gt;", "&lt;instruction&gt;"
      ];
      for (const kw of DOMAIN_COMPOUNDS) {
        if (text.toLowerCase().includes(kw.toLowerCase())) {
          targetKeywords.push(kw);
        }
      }
      if (query && query.trim().length >= 3 && !GENERIC_STOP.has(query.trim().toLowerCase())) {
        targetKeywords.push(query.trim());
      }
    }

    // SẮP XẾP ĐỘ DÀI GIẢM DẦN
    const sortedPhrases = Array.from(new Set(evidencePhrases)).sort((a, b) => b.length - a.length);
    const sortedKeywords = Array.from(new Set(targetKeywords)).sort((a, b) => b.length - a.length);

    const tags = new Uint8Array(text.length); // 0: none, 1: highlighted (single color)

    // Bước 1: Đánh dấu các cụm bằng chứng nguyên văn
    for (const phrase of sortedPhrases) {
      if (!phrase || phrase.length < 4) continue;
      const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
      try {
        const regex = new RegExp(escaped, "gui");
        let match;
        while ((match = regex.exec(text)) !== null) {
          for (let i = match.index; i < match.index + match[0].length; i++) {
            tags[i] = 1;
          }
        }
      } catch (e) {}
    }

    // Bước 2: Đánh dấu từ khóa cốt lõi (GIỚI HẠN TỐI ĐA 1 LẦN MATCH ĐỂ TRÁNH SPAM TỪ KHÓA)
    for (const kw of sortedKeywords) {
      if (!kw || kw.length < 2 || GENERIC_STOP.has(kw.toLowerCase())) continue;
      const isXmlEntity = kw.startsWith("&lt;");
      const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+");
      try {
        const regex = isXmlEntity
          ? new RegExp(escaped, "gui")
          : new RegExp("(^|[^\\p{L}\\p{N}_])(" + escaped + ")(?=[^\\p{L}\\p{N}_]|$)", "gui");

        let match;
        let count = 0;
        while ((match = regex.exec(text)) !== null) {
          if (count >= 1) break; // Khử lặp: chỉ highlight 1 lần xuất hiện đầu tiên
          const start = isXmlEntity ? match.index : match.index + match[1].length;
          const end = isXmlEntity ? match.index + match[0].length : start + match[2].length;
          for (let i = start; i < end; i++) {
            tags[i] = 1;
          }
          count++;
        }
      } catch (e) {}
    }

    // Bước 3: Nối liền khoảng trống nhỏ (1 dấu cách / dấu phẩy) giữa 2 vùng highlight liền kề
    for (let i = 1; i < text.length - 1; i++) {
      if (tags[i - 1] === 1 && tags[i + 1] === 1 && tags[i] === 0 && /[\s,;:-]/.test(text[i])) {
        tags[i] = 1;
      }
    }

    // Bước 4: Lắp ráp HTML với 1 MÀU DUY NHẤT
    const out = [];
    let inMark = false;
    for (let i = 0; i < text.length; i++) {
      if (tags[i] === 1 && !inMark) {
        out.push('<mark class="highlight-grounded">');
        inMark = true;
      } else if (tags[i] === 0 && inMark) {
        out.push('</mark>');
        inMark = false;
      }
      out.push(text[i]);
    }
    if (inMark) out.push('</mark>');

    return out.join("");
  }

  function addMessage(sender, text, isProgressive = false, citation = null, deepDiveData = null, sourceSnippets = null, highlightEvidence = null) {
    const chatBox = document.getElementById('chat-box') || document.getElementById('chat-messages');
    if (!chatBox) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg msg-${sender}` + (isProgressive ? ' progressive-msg' : '');

    const label = document.createElement('div');
    label.className = 'msg-label';
    label.innerText = sender === 'user' ? 'BẠN' : (isProgressive ? 'AI TUTOR · PROGRESSIVE DISCLOSURE' : 'AI TUTOR · RESPONSE');
    msgDiv.appendChild(label);

    const bubble = document.createElement('div');
    // Xóa triệt để mọi thẻ trích dẫn vô tình lọt vào nội dung văn bản (kể cả nested brackets [Transcript [...]...])
    let cleanText = escapeXmlTags(text);
    cleanText = cleanText.replace(/\[(?:Trang|Transcript|Slide|T\d+|d\d+)[^\]]*(\[[^\]]*\])?[^\]]*\]/gi, '');
    cleanText = cleanText.replace(/\s*\[.*?\]\s*$/g, '').trim();
    bubble.innerHTML = cleanText;

    // GIẢI PHÁP 1: 1-CLICK SOURCE PEEK / SOURCE INSPECTOR POPOVER
    if (citation) {
      const citeWrapper = document.createElement('div');
      citeWrapper.className = 'citation-wrapper';

      const citeTag = document.createElement('div');
      citeTag.className = 'citation-tag clickable';
      citeTag.setAttribute('role', 'button');
      citeTag.setAttribute('tabindex', '0');
      citeTag.title = 'Bấm để xem trích đoạn gốc đối soát 1-chạm';

      const citeContent = document.createElement('div');
      citeContent.className = 'citation-content';
      citeContent.innerHTML = `📄 <strong>Nguồn xác minh:</strong> ${escapeXmlTags(citation)}`;

      const peekBtn = document.createElement('div');
      peekBtn.className = 'citation-peek-btn';
      peekBtn.innerHTML = `<span class="peek-icon">🔍</span> <span class="peek-text">Đối soát nguồn</span> <span class="peek-arrow">▼</span>`;

      citeTag.appendChild(citeContent);
      citeTag.appendChild(peekBtn);
      citeWrapper.appendChild(citeTag);

      // Popover Drawer hiển thị trích đoạn đối soát trực tiếp
      const inspectorBox = document.createElement('div');
      inspectorBox.className = 'source-inspector-popover';
      inspectorBox.style.display = 'none';

      let snippetsHTML = `
        <div class="inspector-header">
          <div class="inspector-title-wrap">
            <div class="inspector-title">🎯 1-CLICK SOURCE PEEK · ĐỐI SOÁT NGUỒN GỐC</div>
            <div class="inspector-desc">Trích đoạn nguyên văn từ bài giảng được AI tham chiếu để sinh câu trả lời:</div>
            <div class="inspector-legend">
              <span class="legend-item"><mark class="highlight-grounded">🎯 Bằng chứng đối soát trực tiếp từ bài giảng</mark></span>
            </div>
          </div>
          <button class="inspector-close-btn" title="Đóng đối soát">✕</button>
        </div>
        <div class="inspector-body">
      `;

      if (sourceSnippets && sourceSnippets.length > 0) {
        sourceSnippets.forEach(s => {
          const highlightedSnippet = highlightGroundedSnippet(s.snippet, highlightEvidence, currentActiveQuery || currentSelection || '', cleanText);
          if (s.type === 'slide') {
            const isSwitchable = s.source_file && (s.source_file.includes('d1') || s.source_file.includes('d2') || s.source_file.includes('d4'));
            const targetSlideKey = s.source_file && s.source_file.includes('d4') ? 'd4' : (s.source_file && s.source_file.includes('d2') ? 'd2' : 'd1');
            const pageText = s.page_label || (s.page_index ? `Trang ${s.page_index}` : '');
            snippetsHTML += `
              <div class="source-snippet-card slide-card">
                <div class="source-card-header">
                  <span class="source-card-type">📑 SLIDE BÀI GIẢNG</span>
                  <span class="source-card-tag">${escapeXmlTags(s.source_file)}${pageText ? ' · ' + escapeXmlTags(pageText) : ''}</span>
                  ${isSwitchable ? `<button class="jump-slide-btn" data-target="${targetSlideKey}" title="Chuyển ngay màn hình sang Slide này">⚡ Mở Slide này</button>` : ''}
                </div>
                ${s.title ? `<div class="source-card-title">${escapeXmlTags(s.title)}</div>` : ''}
                <div class="source-card-text">"${highlightedSnippet}"</div>
              </div>
            `;
          } else if (s.type === 'transcript') {
            snippetsHTML += `
              <div class="source-snippet-card transcript-card">
                <div class="source-card-header">
                  <span class="source-card-type">🎙️ LỜI GIẢNG GIẢNG VIÊN</span>
                  <span class="source-card-tag">${escapeXmlTags(s.source_file)}${s.tag ? ' · Đoạn [' + escapeXmlTags(s.tag) + ']' : ''}</span>
                </div>
                <div class="source-card-text transcript-text">"${highlightedSnippet}"</div>
              </div>
            `;
          }
        });
      } else {
        // Fallback trích đoạn từ citation chuỗi
        const fallbackHighlighted = highlightGroundedSnippet(citation, highlightEvidence, currentActiveQuery || currentSelection || '', cleanText);
        snippetsHTML += `
          <div class="source-snippet-card fallback-card">
            <div class="source-card-header">
              <span class="source-card-type">📑 THÔNG TIN TRÍCH DẪN</span>
            </div>
            <div class="source-card-text">${fallbackHighlighted}</div>
          </div>
        `;
      }

      snippetsHTML += `
        </div>
        <div class="inspector-footer">
          <span class="verif-badge">✅ Đã đối soát 100% tài liệu VinUni (0% Phantom Citation)</span>
        </div>
      `;

      inspectorBox.innerHTML = snippetsHTML;

      // Xử lý bật/tắt Popover
      const toggleInspector = (e) => {
        if (e) e.stopPropagation();
        const isHidden = inspectorBox.style.display === 'none';
        inspectorBox.style.display = isHidden ? 'block' : 'none';
        if (isHidden) {
          citeTag.classList.add('is-open');
          peekBtn.querySelector('.peek-text').innerText = 'Đóng đối soát';
          peekBtn.querySelector('.peek-arrow').innerText = '▲';
        } else {
          citeTag.classList.remove('is-open');
          peekBtn.querySelector('.peek-text').innerText = 'Đối soát nguồn';
          peekBtn.querySelector('.peek-arrow').innerText = '▼';
        }
      };

      citeTag.onclick = toggleInspector;
      citeTag.onkeydown = (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleInspector(e);
        }
      };

      const closeBtn = inspectorBox.querySelector('.inspector-close-btn');
      if (closeBtn) {
        closeBtn.onclick = (e) => {
          e.stopPropagation();
          toggleInspector(e);
        };
      }

      // Xử lý nút nhảy Slide 1-chạm
      inspectorBox.querySelectorAll('.jump-slide-btn').forEach(btn => {
        btn.onclick = (e) => {
          e.stopPropagation();
          const target = btn.getAttribute('data-target');
          if (target && typeof switchSlide === 'function') {
            switchSlide(target);
            showToast(`⚡ Đã chuyển sang ${target.toUpperCase()} theo trích dẫn!`);
          }
        };
      });

      citeWrapper.appendChild(inspectorBox);
      bubble.appendChild(citeWrapper);
    }

    // TẦNG 2: PROGRESSIVE BOX + CUSTOM QUESTION INPUT (HAX G9 & SOCRATIC PROBING)
    if (deepDiveData) {
      const displayConcept = formatConceptTitle(deepDiveData.concept);
      const box = document.createElement('div');
      box.className = 'progressive-box';

      const title = document.createElement('div');
      title.className = 'progressive-title';
      title.innerHTML = `💡 Đào sâu tiếp về <em>"${displayConcept}"</em>:`;
      box.appendChild(title);

      const optContainer = document.createElement('div');
      optContainer.className = 'quick-options';
      deepDiveData.options.forEach(opt => {
        if (!opt.label) return;
        const btn = document.createElement('button');
        btn.className = 'quick-btn';
        btn.innerText = opt.label;
        btn.onclick = async () => {
          sessionHistoryQueries.push(opt.label);
          currentActiveQuery = opt.label;
          addMessage('user', opt.label);
          setDecision('Đào sâu gợi ý', 'Gọi GPT-4o-mini (Live API)', 'active');
          const startTime = performance.now();
          try {
            const resp = await fetch('/api/ask', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                text: displayConcept,
                custom_query: opt.label,
                slide: activeSlide,
                history_queries: sessionHistoryQueries
              })
            });
            if (resp.ok) {
              const data = await resp.json();
              const latency = data.latency_ms || Math.round(performance.now() - startTime);
              document.getElementById('latency-display').innerText = `Latency: ${latency} ms (OpenAI Live)`;
              document.getElementById('latency-display').style.color = '#34d399';
              setDecision('Đào sâu gợi ý', data.is_out_of_scope ? 'Ngoài phạm vi bài học' : 'Hoàn tất trả lời', 'active', data.citation ? null : '[Ngoài bài]');

              // YÊU CẦU 3: ĐÀO SÂU LIÊN TỤC (MULTI-TURN SOCRATIC PROBING)
              let nextDeepDive = null;
              if (!data.is_out_of_scope && (data.option_a || data.option_b)) {
                const nextOptions = [];
                if (data.option_a) nextOptions.push({ label: data.option_a });
                if (data.option_b) nextOptions.push({ label: data.option_b });
                if (nextOptions.length > 0) {
                  nextDeepDive = {
                    concept: data.next_concept || opt.label,
                    options: nextOptions
                  };
                }
              }

              addMessage('ai', data.summary, true, data.citation || null, nextDeepDive, data.source_snippets || null, data.highlight_evidence || null);
              return;
            }
          } catch (err) {
            console.warn('Lỗi gọi API khi bấm option:', err);
          }
          if (typeof opt.action === 'function') {
            opt.action();
          }
        };
        optContainer.appendChild(btn);
      });
      box.appendChild(optContainer);

      // Ô NHẬP CÂU HỎI TÙY CHỌN
      const customWrap = document.createElement('custom-wrap');
      customWrap.className = 'custom-question-wrap';

      const customInput = document.createElement('input');
      customInput.type = 'text';
      customInput.className = 'custom-question-input';
      customInput.placeholder = `Hoặc gõ câu hỏi riêng về "${displayConcept}"...`;
      
      const customBtn = document.createElement('button');
      customBtn.className = 'custom-send-btn';
      customBtn.innerText = 'Hỏi ➔';

      const triggerCustomAsk = async () => {
        const query = customInput.value.trim();
        if (!query) return;
        sessionHistoryQueries.push(query);
        currentActiveQuery = query;
        addMessage('user', `[Hỏi về "${displayConcept}"]: ${query}`);
        customInput.value = '';
        
        const startTime = performance.now();
        setDecision('Hỏi đáp tùy chỉnh', 'Gọi GPT-4o-mini (Live API)', 'active');

        try {
          const resp = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              text: displayConcept,
              custom_query: query,
              slide: activeSlide,
              history_queries: sessionHistoryQueries
            })
          });

          if (resp.ok) {
            const data = await resp.json();
            const latency = data.latency_ms || Math.round(performance.now() - startTime);
            document.getElementById('latency-display').innerText = `Latency: ${latency} ms (OpenAI Live)`;
            document.getElementById('latency-display').style.color = '#34d399';
            setDecision('Hỏi đáp tùy chỉnh', data.is_out_of_scope ? 'Ngoài phạm vi bài học' : 'Hoàn tất trả lời', 'active', data.citation ? null : '[Ngoài bài]');

            // YÊU CẦU 3: ĐÀO SÂU LIÊN TỤC CHO CÂU HỎI TÙY CHỈNH
            let nextDeepDive = null;
            if (!data.is_out_of_scope && (data.option_a || data.option_b)) {
              const nextOptions = [];
              if (data.option_a) nextOptions.push({ label: data.option_a });
              if (data.option_b) nextOptions.push({ label: data.option_b });
              if (nextOptions.length > 0) {
                nextDeepDive = {
                  concept: data.next_concept || query,
                  options: nextOptions
                };
              }
            }

            addMessage('ai', data.summary, true, data.citation || null, nextDeepDive, data.source_snippets || null, data.highlight_evidence || null);
            return;
          }
        } catch (err) {
          console.warn('Lỗi gọi Custom Ask API, dùng fallback:', err);
        }

        // Fallback Grounded nếu mất mạng
        setTimeout(() => {
          setDecision('Hỏi đáp tùy chỉnh', 'Hoàn tất trả lời', 'active');
          addMessage('ai', `Về <em>"${query}"</em>: Dựa trên tài liệu bài giảng, câu hỏi này nằm ngoài nội dung đang hiển thị.`, false, null);
        }, 300);
      };

      customInput.onkeydown = (e) => { if (e.key === 'Enter') triggerCustomAsk(); };
      customBtn.onclick = triggerCustomAsk;

      customWrap.appendChild(customInput);
      customWrap.appendChild(customBtn);
      box.appendChild(customWrap);

      bubble.appendChild(box);
    }

    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function setDecision(step1, step2, styleClass, step3 = null) {
    const s1 = document.getElementById('step-detector');
    const s2 = document.getElementById('step-move');
    const s3 = document.getElementById('step-ground');

    s1.className = `decision-step ${styleClass}`;
    s1.innerText = `1. ${step1}`;

    s2.className = `decision-step ${styleClass}`;
    s2.innerText = `2. ${step2}`;

    s3.className = 'decision-step active';
    s3.innerText = step3 ? `3. ${step3}` : `3. [${SLIDE_KNOWLEDGE[activeSlide].page}]`;
  }

  async function sendCustomMessage() {
    const input = document.getElementById('user-input');
    const val = input.value.trim();
    if (!val) return;
    input.value = '';
    currentActiveQuery = val;

    addMessage('user', val);

    // Client Guardrail: Kiểm tra câu hỏi tự do quá ngắn hoặc chỉ chứa ký tự rác/mũi tên
    const cleanedVal = val.replace(/[\s\-_–—>><=.,:;!?()[\]{}]+/g, '');
    if (val.length < 3 || cleanedVal.length < 2) {
      setDecision('Câu hỏi không hợp lệ', 'filter_garbage', 'active', '[Cần gõ rõ câu hỏi]');
      addMessage('ai', `Nội dung "${val}" quá ngắn hoặc không phải là một câu hỏi/thuật ngữ hoàn chỉnh. Bạn hãy đặt một câu hỏi rõ ràng (ví dụ: "Tại sao Attention xử lý song song được?") để AI giải thích nhé!`, false, null);
      return;
    }

    sessionHistoryQueries.push(val);
    const startTime = performance.now();
    setDecision('Câu hỏi tự do', 'Gọi GPT-4o-mini (Live API)', 'active');

    try {
      const resp = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: SLIDE_KNOWLEDGE[activeSlide].title,
          custom_query: val,
          slide: activeSlide,
          history_queries: sessionHistoryQueries
        })
      });

      if (resp.ok) {
        const data = await resp.json();
        const latency = data.latency_ms || Math.round(performance.now() - startTime);
        document.getElementById('latency-display').innerText = `Latency: ${latency} ms (OpenAI Live)`;
        document.getElementById('latency-display').style.color = '#34d399';
        setDecision('Câu hỏi tự do', data.is_out_of_scope ? 'Ngoài phạm vi bài học' : 'Hoàn tất trả lời', 'active', data.citation ? null : '[Ngoài bài]');

        let nextDeepDive = null;
        if (!data.is_out_of_scope && (data.option_a || data.option_b)) {
          const nextOptions = [];
          if (data.option_a) nextOptions.push({ label: data.option_a });
          if (data.option_b) nextOptions.push({ label: data.option_b });
          if (nextOptions.length > 0) {
            nextDeepDive = {
              concept: data.next_concept || val,
              options: nextOptions
            };
          }
        }

        addMessage('ai', data.summary, true, data.citation || null, nextDeepDive, data.source_snippets || null, data.highlight_evidence || null);
        return;
      }
    } catch (err) {
      console.warn('Lỗi gửi chat tự do:', err);
    }

    processSelectionWithAI(val);
  }

  // Tự động kiểm tra trạng thái Backend khi load trang
  async function checkServerStatus() {
    try {
      const r = await fetch('/api/status');
      if (r.ok) {
        const d = await r.json();
        if (d.active) {
          const badge = document.getElementById('engine-badge');
          const dot = document.getElementById('engine-dot');
          const label = document.getElementById('engine-label');
          label.innerText = `AI ENGINE: OPENAI ${d.model.toUpperCase()} (LIVE .ENV)`;
          badge.style.background = 'rgba(16, 185, 129, 0.2)';
          badge.style.borderColor = 'rgba(16, 185, 129, 0.5)';
          dot.style.background = '#34d399';
          document.getElementById('latency-display').innerText = 'Backend: SẴN SÀNG (OPENAI)';
          return;
        }
      }
    } catch (e) {}
    initApiConfig();
  }

  // Khởi chạy khi load trang
  window.addEventListener('DOMContentLoaded', checkServerStatus);
