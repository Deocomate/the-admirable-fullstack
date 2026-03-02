{{-- ── Copy AI Prompt Card ────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
        Trợ lý AI
    </h2>
    <p class="text-xs text-gray-400 mb-4">
        Copy prompt bên dưới và dán vào ChatGPT, Gemini, Claude hoặc bất kỳ AI chatbot nào để tự động tạo bài viết song ngữ.
    </p>

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
        <span id="copy-prompt-text">Copy Prompt cho AI</span>
    </button>

    <p class="mt-3 text-[11px] text-gray-400 leading-relaxed">
        <strong>Hướng dẫn:</strong> Sau khi copy, dán prompt vào AI → Nhập tên nhân vật bạn muốn viết → AI sẽ trả về toàn bộ nội dung đúng format. Bạn chỉ cần copy từng phần vào form này.
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

        return `You are a professional bilingual content writer for "The Admirable" – a Vietnamese educational website about inspiring figures throughout history. Your task is to write a comprehensive, detailed, and inspiring bilingual (English–Vietnamese) article about an inspiring figure.

⚠️ IMPORTANT INSTRUCTIONS:
- English content MUST be at IELTS Band 6.5 level (upper-intermediate: clear, well-structured, uses a good range of vocabulary and complex sentence structures, but remains accessible to learners)
- The article MUST be LONG and DETAILED (at least 2000+ words total across both languages)
- The tone must be INSPIRING and MOTIVATIONAL – the reader should feel moved and motivated after reading
- Cover the figure's early life, challenges, achievements, philosophy, legacy, and life lessons
- Use vivid storytelling, specific details, dates, and anecdotes to bring the figure to life
- Vietnamese translation must be natural and fluent, not machine-translated

📋 Please provide ALL of the following fields in the EXACT format below. I will copy each section into my website's admin form.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. TÊN NHÂN VẬT (NAME)
[Tên đầy đủ của nhân vật - VD: Marie Curie]

## 2. MÔ TẢ NGẮN (SHORT DESCRIPTION - Tiếng Việt, 1-2 câu)
[Mô tả ngắn gọn bằng tiếng Việt, nêu bật điểm nổi bật nhất của nhân vật]
VD: "Người phụ nữ đầu tiên giành giải Nobel và là người duy nhất giành giải Nobel trong hai lĩnh vực khoa học khác nhau."

## 3. LĨNH VỰC (CATEGORIES)
[Chọn 1 hoặc nhiều từ danh sách sau: ${categoryList}]

## 4. THÔNG TIN NHANH (KEY FACTS)
Cung cấp 6-8 thông tin nhanh dạng Nhãn/Giá trị:
| Nhãn | Giá trị |
|------|---------|
| Họ tên đầy đủ | ... |
| Năm sinh – mất | ... |
| Quốc tịch | ... |
| Lĩnh vực | ... |
| Thành tựu nổi bật | ... |
| Giải thưởng | ... |
| Câu nói nổi tiếng | "..." |
| Di sản để lại | ... |

## 5. NỘI DUNG BÀI VIẾT SONG NGỮ (CONTENT BLOCKS)
Viết bài viết chi tiết về cuộc đời nhân vật. Mỗi block là một phần riêng biệt.

⚠️ QUAN TRỌNG VỀ CẤU TRÚC:
- KHÔNG viết theo khuôn mẫu cứng nhắc. Mỗi nhân vật có cuộc đời khác nhau → cấu trúc bài viết phải KHÁC NHAU, phản ánh đúng câu chuyện riêng của họ.
- Hãy nghiên cứu kỹ về nhân vật, sau đó TỰ QUYẾT ĐỊNH các phần/chủ đề phù hợp nhất để kể câu chuyện cuộc đời họ một cách hấp dẫn và chi tiết nhất.
- VD: Với một nhà khoa học có thể viết về phát minh cụ thể, với một nghệ sĩ có thể viết về tác phẩm tiêu biểu, với một nhà hoạt động xã hội có thể viết về các phong trào họ dẫn dắt...
- Kể CHI TIẾT vào từng giai đoạn cuộc đời: bối cảnh gia đình, thời thơ ấu, sự kiện then chốt thay đổi cuộc đời, những người ảnh hưởng, các bước ngoặt quan trọng, thất bại cụ thể, cách họ vượt qua...

📌 YÊU CẦU:
- TỐI THIỂU 15-20 blocks
- Xen kẽ đủ 3 loại: HEADING, PARAGRAPH, QUOTE
- Ít nhất 1 - 2 QUOTE blocks (trích dẫn thật của nhân vật hoặc người liên quan)
- Mỗi PARAGRAPH phải dài 150-300 từ tiếng Anh
- Tổng bài viết tối thiểu 2500+ từ tiếng Anh

📐 CÓ 3 LOẠI BLOCK, viết theo format sau:

**Loại HEADING** (tiêu đề phân chia phần lớn):
\`\`\`
### BLOCK [số] — Loại: HEADING
text_en: [Tiêu đề tiếng Anh]
\`\`\`

**Loại PARAGRAPH** (đoạn văn song ngữ có tiêu đề phụ):
\`\`\`
### BLOCK [số] — Loại: PARAGRAPH
heading_en: [Tiêu đề phụ tiếng Anh, tùy chọn]
text_en:
[Đoạn văn tiếng Anh dài 150-300 từ, IELTS 6.5]
text_vi:
[Bản dịch tiếng Việt tự nhiên, trôi chảy]
\`\`\`

**Loại QUOTE** (trích dẫn):
\`\`\`
### BLOCK [số] — Loại: QUOTE
text_en: "[Câu trích dẫn tiếng Anh]"
author: [Tên tác giả]
\`\`\`

Hãy tự sáng tạo cấu trúc bài viết phù hợp nhất với nhân vật. Đảm bảo bài viết đi sâu vào câu chuyện cuộc đời, không hời hợt, không chung chung.

## 6. YOUTUBE URL (Tùy chọn)
[Nếu biết, cung cấp link YouTube về nhân vật này. Nếu không biết chính xác, ghi "Không có".]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 LƯU Ý QUAN TRỌNG:
- KHÔNG dùng cấu trúc cứng nhắc – tự sáng tạo cấu trúc phù hợp với từng nhân vật
- Kể CHI TIẾT câu chuyện cuộc đời: bối cảnh, sự kiện cụ thể, con người xung quanh, bước ngoặt, thất bại, thành công
- Mỗi đoạn PARAGRAPH phải dài ít nhất 150-300 từ tiếng Anh
- Tổng bài viết phải có ít nhất 2500 từ tiếng Anh
- Phải có ít nhất 3-4 QUOTE blocks xen kẽ trong bài (trích dẫn thật)
- Tiếng Anh phải chuẩn IELTS 6.5: dùng linking words (However, Furthermore, Nevertheless, In addition, Consequently...), câu phức (complex sentences), collocations, và idiomatic expressions
- Tiếng Việt phải tự nhiên, không dịch máy, phù hợp văn phong báo chí Việt Nam
- Giọng văn phải TRUYỀN CẢM HỨNG: tạo cảm xúc, khơi gợi động lực cho người đọc
- Nêu chi tiết cụ thể: ngày tháng, địa điểm, con số, sự kiện, tên người liên quan
- Phải có ít nhất 15-20 blocks tổng cộng

Bây giờ, hãy viết bài về nhân vật: [HÃY NHẬP TÊN NHÂN VẬT TẠI ĐÂY]`;
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
                textEl.textContent = 'Copy Prompt cho AI';
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
                    textEl.textContent = 'Copy Prompt cho AI';
                    btn.style.background = 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)';
                }, 2500);
            } catch (e) {
                textEl.textContent = 'Lỗi, thử lại!';
                setTimeout(() => {
                    textEl.textContent = 'Copy Prompt cho AI';
                }, 2000);
            }
            document.body.removeChild(textarea);
        });
    }
</script>
