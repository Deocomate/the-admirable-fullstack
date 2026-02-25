{{-- ── Story Content Blocks Script ──────────────────────────────────────── --}}
@php
    $existingBlocks = old('content_blocks', isset($story) ? ($story->content_blocks ?? []) : []);
    if (is_string($existingBlocks)) {
        $existingBlocks = json_decode($existingBlocks, true) ?? [];
    }
@endphp
<script>
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('story-blocks-container');
    const emptyState = document.getElementById('story-blocks-empty');
    const initialBlocks = @json($existingBlocks);

    // ── Block type config ────────────────────────────────────────────
    const blockTypeLabels = {
        paragraph: { label: 'Đoạn văn', color: 'bg-blue-100 text-blue-700' },
        heading:   { label: 'Tiêu đề',  color: 'bg-purple-100 text-purple-700' },
        quote:     { label: 'Trích dẫn', color: 'bg-amber-100 text-amber-700' },
    };

    // ── Render initial blocks ────────────────────────────────────────
    if (initialBlocks.length > 0) {
        initialBlocks.forEach((block, idx) => {
            const type = block.type || 'paragraph';
            container.appendChild(createBlock(type, idx, block));
        });
    }
    toggleEmptyState();
    initDragDrop();

    // ── Add block by type ────────────────────────────────────────────
    window.addStoryBlock = function (type) {
        type = type || 'paragraph';
        const idx = container.children.length;
        const defaults = {
            paragraph: { type: 'paragraph', heading_en: '', text_en: '', text_vi: '' },
            heading:   { type: 'heading', text_en: '' },
            quote:     { type: 'quote', text_en: '', author: '' },
        };
        const el = createBlock(type, idx, defaults[type] || defaults.paragraph);
        container.appendChild(el);
        toggleEmptyState();
        reindexBlocks();
        initDragDrop();
        const firstInput = el.querySelector('textarea, input[type="text"]');
        if (firstInput) firstInput.focus();
    };

    // ── Remove block ─────────────────────────────────────────────────
    window.removeStoryBlock = function (btn) {
        btn.closest('.story-block-item').remove();
        reindexBlocks();
        toggleEmptyState();
    };

    // ── Create block by type ─────────────────────────────────────────
    function createBlock(type, idx, data) {
        switch (type) {
            case 'heading': return createHeadingBlock(idx, data);
            case 'quote':   return createQuoteBlock(idx, data);
            default:        return createParagraphBlock(idx, data);
        }
    }

    // ── Block header helper ──────────────────────────────────────────
    function blockHeader(type, idx) {
        const cfg = blockTypeLabels[type] || blockTypeLabels.paragraph;
        return `
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <span class="cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500 drag-handle" title="Kéo để sắp xếp">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                        </svg>
                    </span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold ${cfg.color} uppercase tracking-wider">
                        ${cfg.label} #<span class="block-number">${idx + 1}</span>
                    </span>
                </div>
                <button type="button" onclick="removeStoryBlock(this)"
                        class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all p-1" title="Xóa đoạn">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                </button>
            </div>`;
    }

    // ── Create heading block ─────────────────────────────────────────
    function createHeadingBlock(idx, data) {
        const div = document.createElement('div');
        div.className = 'story-block-item group bg-purple-50 border border-purple-200 rounded-lg p-4 relative transition-all hover:border-purple-400';
        div.draggable = true;

        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="heading">
            ${blockHeader('heading', idx)}
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    Tiêu đề phần (Tiếng Anh) <span class="text-red-500">*</span>
                </label>
                <input type="text" name="content_blocks[${idx}][text_en]" required
                       value="${escapeAttr(data.text_en || '')}"
                       placeholder="VD: Early Life and Education"
                       class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 font-semibold"
                       onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">
            </div>
        `;

        return div;
    }

    // ── Create paragraph block ───────────────────────────────────────
    function createParagraphBlock(idx, data) {
        const div = document.createElement('div');
        div.className = 'story-block-item group bg-gray-50 border border-gray-200 rounded-lg p-4 relative transition-all hover:border-blue-300';
        div.draggable = true;

        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="paragraph">
            ${blockHeader('paragraph', idx)}

            <div class="mb-3">
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    Tiêu đề phụ (Tiếng Anh, tuỳ chọn)
                </label>
                <input type="text" name="content_blocks[${idx}][heading_en]"
                       value="${escapeAttr(data.heading_en || '')}"
                       placeholder="VD: A Curious Mind"
                       class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400"
                       onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">
            </div>

            <div class="mb-3">
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 rounded bg-blue-600 text-white text-[9px] font-bold flex items-center justify-center">EN</span>
                        Nội dung tiếng Anh <span class="text-red-500">*</span>
                    </span>
                </label>
                <textarea name="content_blocks[${idx}][text_en]" rows="4" required
                          placeholder="English paragraph content..."
                          class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 resize-y"
                          onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">${escapeHtml(data.text_en || '')}</textarea>
            </div>

            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 rounded bg-red-600 text-white text-[9px] font-bold flex items-center justify-center">VI</span>
                        Bản dịch tiếng Việt
                    </span>
                </label>
                <textarea name="content_blocks[${idx}][text_vi]" rows="4"
                          placeholder="Nội dung dịch tiếng Việt..."
                          class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 resize-y"
                          onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">${escapeHtml(data.text_vi || '')}</textarea>
            </div>
        `;

        return div;
    }

    // ── Create quote block ───────────────────────────────────────────
    function createQuoteBlock(idx, data) {
        const div = document.createElement('div');
        div.className = 'story-block-item group bg-amber-50 border border-amber-200 rounded-lg p-4 relative transition-all hover:border-amber-400';
        div.draggable = true;

        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="quote">
            ${blockHeader('quote', idx)}

            <div class="mb-3">
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    Nội dung trích dẫn (Tiếng Anh) <span class="text-red-500">*</span>
                </label>
                <textarea name="content_blocks[${idx}][text_en]" rows="3" required
                          placeholder="VD: Imagination is more important than knowledge..."
                          class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 resize-y italic"
                          onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">${escapeHtml(data.text_en || '')}</textarea>
            </div>

            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">
                    Tác giả / Nguồn
                </label>
                <input type="text" name="content_blocks[${idx}][author]"
                       value="${escapeAttr(data.author || '')}"
                       placeholder="VD: Albert Einstein"
                       class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400"
                       onfocus="this.style.borderColor='#A31D1D'" onblur="this.style.borderColor='#D1D5DB'">
            </div>
        `;

        return div;
    }

    // ── Reindex all blocks ───────────────────────────────────────────
    function reindexBlocks() {
        container.querySelectorAll('.story-block-item').forEach((el, i) => {
            el.querySelector('.block-number').textContent = i + 1;
            el.querySelectorAll('[name]').forEach(input => {
                input.name = input.name.replace(/content_blocks\[\d+\]/, `content_blocks[${i}]`);
            });
        });
    }

    // ── Toggle empty state ───────────────────────────────────────────
    function toggleEmptyState() {
        if (container.children.length === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');
        }
    }

    // ── Drag & drop ──────────────────────────────────────────────────
    let dragEl = null;

    function initDragDrop() {
        container.querySelectorAll('.story-block-item').forEach(item => {
            item.removeEventListener('dragstart', onDragStart);
            item.removeEventListener('dragend', onDragEnd);
            item.addEventListener('dragstart', onDragStart);
            item.addEventListener('dragend', onDragEnd);
        });

        container.removeEventListener('dragover', onDragOver);
        container.removeEventListener('drop', onDrop);
        container.addEventListener('dragover', onDragOver);
        container.addEventListener('drop', onDrop);
    }

    function onDragStart(e) {
        dragEl = e.currentTarget;
        dragEl.classList.add('opacity-50');
        e.dataTransfer.effectAllowed = 'move';
    }

    function onDragEnd(e) {
        e.currentTarget.classList.remove('opacity-50');
        dragEl = null;
    }

    function onDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const afterEl = getDragAfterElement(container, e.clientY);
        if (afterEl) {
            container.insertBefore(dragEl, afterEl);
        } else {
            container.appendChild(dragEl);
        }
    }

    function onDrop(e) {
        e.preventDefault();
        reindexBlocks();
    }

    function getDragAfterElement(container, y) {
        const elements = [...container.querySelectorAll('.story-block-item:not(.opacity-50)')];
        return elements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset, element: child };
            }
            return closest;
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    // ── Escape helpers ───────────────────────────────────────────────
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function escapeAttr(str) {
        return String(str).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/'/g,'&#39;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
});
</script>
