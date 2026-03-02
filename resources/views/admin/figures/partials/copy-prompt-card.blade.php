{{-- ── Copy AI Prompt Card ────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        Trợ lý AI
    </h2>
    <p class="text-xs text-gray-400 mb-4">
        Copy prompt → dán vào AI chatbot → nhận JSON → paste vào ô bên dưới để tự động điền form.
    </p>

    {{-- Step 1: Copy prompt --}}
    <button type="button"
            id="copy-prompt-btn"
            onclick="copyAIPrompt()"
            class="w-full inline-flex items-center justify-center gap-2 px-5 py-2.5 text-sm font-semibold text-white rounded transition-all duration-200"
            style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);"
            onmouseover="this.style.opacity='0.9'"
            onmouseout="this.style.opacity='1'">
        <svg id="copy-prompt-icon" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
        </svg>
        <svg id="copy-prompt-icon-success" class="w-4 h-4 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        <span id="copy-prompt-text">① Copy Prompt cho AI</span>
    </button>

    {{-- Step 2: Paste JSON data --}}
    <div class="mt-4 pt-4 border-t border-gray-100">
        <label class="block text-xs font-medium text-gray-600 mb-1.5 flex items-center gap-1">
            <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            ② Paste JSON từ AI
        </label>
        <textarea id="json-import-textarea" rows="4"
                  placeholder='Dán JSON mà AI trả về vào đây... (bắt đầu bằng { và kết thúc bằng })'
                  class="w-full px-3 py-2 text-xs border border-gray-200 rounded outline-none bg-gray-50 text-gray-700 placeholder-gray-400 focus:border-indigo-400 resize-y font-mono"></textarea>
        <button type="button"
                onclick="importJsonData()"
                class="w-full mt-2 inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold text-white rounded transition-all duration-200"
                style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);"
                onmouseover="this.style.opacity='0.9'"
                onmouseout="this.style.opacity='1'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            Import dữ liệu
        </button>
        <p id="json-import-status" class="mt-2 text-xs font-medium hidden"></p>
    </div>

    <p class="mt-3 text-[11px] text-gray-400 leading-relaxed">
        <strong>Hướng dẫn:</strong> Copy prompt → dán vào ChatGPT/Gemini/Claude → AI trả JSON → copy toàn bộ JSON → dán vào ô trên → bấm "Import dữ liệu".
    </p>
</div>

{{-- Prompt template (hidden, used by JS) --}}
<script>
    function buildAIPrompt() {
        // Collect available categories from the form
        const categoryLabels = [];
        document.querySelectorAll('input[name="category_ids[]"]').forEach(cb => {
            const label = cb.closest('label')?.querySelector('span')?.textContent?.trim();
            if (label) categoryLabels.push(label);
        });
        const categoryList = categoryLabels.length > 0
            ? categoryLabels.join(', ')
            : 'Khoa học, Nghệ thuật, Thể thao, Kinh doanh, Xã hội, Giáo dục';

        return `You are a professional bilingual content writer for "The Admirable" – a Vietnamese educational website about inspiring historical figures. Write a concise, engaging, and inspiring bilingual (English–Vietnamese) article.

⚠️ OUTPUT FORMAT: Return ONLY valid JSON (no markdown, no explanation). The response must be parseable by JSON.parse().

⚠️ WRITING RULES:
- English at IELTS Band 6.5 level (clear, well-structured, accessible)
- Keep it CONCISE and ENGAGING – each paragraph should be impactful, not padded
- Total article: ~1200-1800 words English (quality over quantity)
- Tone: inspiring, motivational – reader should feel energized after reading
- Use vivid storytelling, specific details, dates, anecdotes
- Vietnamese translation: natural, fluent, journalistic style
- NO filler content – every sentence must add value

📋 RETURN THIS EXACT JSON STRUCTURE:

{
  "name": "Full name of the figure",
  "short_description": "1-2 câu mô tả ngắn bằng tiếng Việt, nêu bật điểm nổi bật nhất",
  "categories": ["Category1", "Category2"],
  "youtube_url": "YouTube URL or empty string",
  "key_facts": [
    { "label": "Họ tên đầy đủ", "value": "..." },
    { "label": "Năm sinh – mất", "value": "..." },
    { "label": "Quốc tịch", "value": "..." },
    { "label": "Lĩnh vực", "value": "..." },
    { "label": "Thành tựu nổi bật", "value": "..." },
    { "label": "Câu nói nổi tiếng", "value": "..." }
  ],
  "content_blocks": [
    { "type": "heading", "text_en": "Section Title in English" },
    { "type": "paragraph", "text_en": "English paragraph...", "text_vi": "Vietnamese paragraph..." },
    { "type": "quote", "text_en": "Famous quote in English", "author": "Author Name" }
  ]
}

📐 CONTENT BLOCKS RULES:
- Use 3 types: "heading", "paragraph", "quote"
- Total: 10-15 blocks
- Each PARAGRAPH: 80-150 words English (concise, impactful)
- Include 2-3 QUOTE blocks (real quotes from the figure or related people)
- HEADING blocks separate major sections
- Structure should be UNIQUE to each figure's story – no rigid template
- Cover: early life, key turning points, achievements, philosophy, legacy
- Categories must match from this list: ${categoryList}

⚠️ IMPORTANT:
- Return ONLY the JSON object, nothing else
- All strings must be properly escaped for JSON
- No trailing commas in arrays/objects
- Every paragraph must be engaging – if it doesn't inspire, rewrite it

Now write about: [NHẬP TÊN NHÂN VẬT TẠI ĐÂY]`;
    }

    function copyAIPrompt() {
        const prompt = buildAIPrompt();
        const btn = document.getElementById('copy-prompt-btn');
        const iconDefault = document.getElementById('copy-prompt-icon');
        const iconSuccess = document.getElementById('copy-prompt-icon-success');
        const textEl = document.getElementById('copy-prompt-text');

        navigator.clipboard.writeText(prompt).then(() => {
            // Success feedback
            iconDefault.classList.add('hidden');
            iconSuccess.classList.remove('hidden');
            textEl.textContent = 'Đã copy prompt!';
            btn.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';

            setTimeout(() => {
                iconDefault.classList.remove('hidden');
                iconSuccess.classList.add('hidden');
                textEl.textContent = '① Copy Prompt cho AI';
                btn.style.background = 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)';
            }, 2500);
        }).catch(() => {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = prompt;
            textarea.style.cssText = 'position:fixed;left:-9999px;';
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                iconDefault.classList.add('hidden');
                iconSuccess.classList.remove('hidden');
                textEl.textContent = 'Đã copy prompt!';
                btn.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';

                setTimeout(() => {
                    iconDefault.classList.remove('hidden');
                    iconSuccess.classList.add('hidden');
                    textEl.textContent = '① Copy Prompt cho AI';
                    btn.style.background = 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)';
                }, 2500);
            } catch (e) {
                textEl.textContent = 'Lỗi, thử lại!';
                setTimeout(() => {
                    textEl.textContent = '① Copy Prompt cho AI';
                }, 2000);
            }
            document.body.removeChild(textarea);
        });
    }
</script>
