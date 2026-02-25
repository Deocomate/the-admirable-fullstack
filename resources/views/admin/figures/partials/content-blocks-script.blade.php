{{-- ── Content Blocks & Key Facts JavaScript ──────────────────────────── --}}
<script>
document.addEventListener('DOMContentLoaded', function () {

    // ═════════════════════════════════════════════════════════════════════
    // KEY FACTS MANAGEMENT
    // ═════════════════════════════════════════════════════════════════════
    const factsContainer = document.getElementById('key-facts-container');

    function renderKeyFact(fact = { label: '', value: '' }, index = null) {
        const idx = index !== null ? index : factsContainer.children.length;
        const div = document.createElement('div');
        div.className = 'flex items-center gap-2 group';
        div.setAttribute('data-fact-index', idx);
        div.innerHTML = `
            <button type="button" class="cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500 flex-shrink-0 drag-handle-fact" title="Kéo để sắp xếp">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                </svg>
            </button>
            <input type="text" name="key_facts[${idx}][label]" value="${escapeHtml(fact.label)}"
                   placeholder="Nhãn (VD: Năm sinh – mất)"
                   class="flex-1 px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-700 placeholder-gray-400 focus:border-gray-400">
            <input type="text" name="key_facts[${idx}][value]" value="${escapeHtml(fact.value)}"
                   placeholder="Giá trị (VD: 1867 – 1934)"
                   class="flex-1 px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-700 placeholder-gray-400 focus:border-gray-400">
            <button type="button" onclick="this.closest('[data-fact-index]').remove(); reindexKeyFacts();"
                    class="flex-shrink-0 p-1.5 text-gray-300 hover:text-red-500 transition-colors" title="Xóa">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
            </button>
        `;
        factsContainer.appendChild(div);
    }

    window.addKeyFact = function () {
        renderKeyFact();
    };

    window.reindexKeyFacts = function () {
        const facts = factsContainer.querySelectorAll('[data-fact-index]');
        facts.forEach((el, i) => {
            el.setAttribute('data-fact-index', i);
            el.querySelector('input[name*="[label]"]').name = `key_facts[${i}][label]`;
            el.querySelector('input[name*="[value]"]').name = `key_facts[${i}][value]`;
        });
    };

    // Load initial key facts
    if (typeof initialKeyFacts !== 'undefined' && initialKeyFacts.length > 0) {
        initialKeyFacts.forEach((fact, i) => renderKeyFact(fact, i));
    }

    // Drag-and-drop for key facts
    initDragDrop(factsContainer, '.drag-handle-fact', '[data-fact-index]', reindexKeyFacts);


    // ═════════════════════════════════════════════════════════════════════
    // CONTENT BLOCKS MANAGEMENT
    // ═════════════════════════════════════════════════════════════════════
    const blocksContainer = document.getElementById('content-blocks-container');
    const emptyState = document.getElementById('blocks-empty-state');
    let blockCounter = 0;

    function updateEmptyState() {
        const hasBlocks = blocksContainer.children.length > 0;
        emptyState.classList.toggle('hidden', hasBlocks);
    }

    function createParagraphBlock(data = {}) {
        const idx = blockCounter++;
        const div = document.createElement('div');
        div.className = 'border border-blue-200 bg-blue-50/30 rounded-lg p-4 relative group';
        div.setAttribute('data-block-index', idx);
        div.setAttribute('data-block-type', 'paragraph');
        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="paragraph">

            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <button type="button" class="cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500 drag-handle-block" title="Kéo để sắp xếp">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                        </svg>
                    </button>
                    <span class="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-blue-100 text-blue-700 rounded">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
                        Đoạn văn
                    </span>
                </div>
                <button type="button" onclick="removeBlock(this)"
                        class="p-1 text-gray-300 hover:text-red-500 transition-colors" title="Xóa block">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <div class="space-y-3">
                <div>
                    <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase tracking-wider">Tiêu đề phần (EN, tùy chọn)</label>
                    <input type="text" name="content_blocks[${idx}][heading_en]" value="${escapeHtml(data.heading_en || '')}"
                           placeholder="VD: Early Life and Education"
                           class="w-full px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-800 placeholder-gray-400 focus:border-blue-400">
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
                    <div>
                        <label class="block text-[11px] font-medium text-blue-600 mb-1 uppercase tracking-wider">
                            🇬🇧 Tiếng Anh <span class="text-red-400">*</span>
                        </label>
                        <textarea name="content_blocks[${idx}][text_en]" rows="5"
                                  placeholder="English paragraph content..."
                                  class="w-full px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-800 placeholder-gray-400 focus:border-blue-400 resize-y">${escapeHtml(data.text_en || '')}</textarea>
                    </div>
                    <div>
                        <label class="block text-[11px] font-medium text-green-600 mb-1 uppercase tracking-wider">
                            🇻🇳 Tiếng Việt
                        </label>
                        <textarea name="content_blocks[${idx}][text_vi]" rows="5"
                                  placeholder="Nội dung đoạn văn bằng tiếng Việt..."
                                  class="w-full px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-800 placeholder-gray-400 focus:border-green-400 resize-y">${escapeHtml(data.text_vi || '')}</textarea>
                    </div>
                </div>
            </div>
        `;
        blocksContainer.appendChild(div);
        updateEmptyState();
    }

    function createQuoteBlock(data = {}) {
        const idx = blockCounter++;
        const div = document.createElement('div');
        div.className = 'border border-amber-200 bg-amber-50/30 rounded-lg p-4 relative group';
        div.setAttribute('data-block-index', idx);
        div.setAttribute('data-block-type', 'quote');
        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="quote">

            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <button type="button" class="cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500 drag-handle-block" title="Kéo để sắp xếp">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                        </svg>
                    </button>
                    <span class="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-amber-100 text-amber-700 rounded">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                        Trích dẫn
                    </span>
                </div>
                <button type="button" onclick="removeBlock(this)"
                        class="p-1 text-gray-300 hover:text-red-500 transition-colors" title="Xóa block">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <div class="space-y-3">
                <div>
                    <label class="block text-[11px] font-medium text-amber-600 mb-1 uppercase tracking-wider">Câu trích dẫn (EN) <span class="text-red-400">*</span></label>
                    <textarea name="content_blocks[${idx}][text_en]" rows="3"
                              placeholder='"Nothing in life is to be feared, it is only to be understood."'
                              class="w-full px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-800 placeholder-gray-400 focus:border-amber-400 resize-y italic">${escapeHtml(data.text_en || '')}</textarea>
                </div>
                <div>
                    <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase tracking-wider">Tác giả</label>
                    <input type="text" name="content_blocks[${idx}][author]" value="${escapeHtml(data.author || '')}"
                           placeholder="VD: Marie Curie"
                           class="w-full px-3 py-2 text-sm border border-gray-200 rounded outline-none bg-white text-gray-700 placeholder-gray-400 focus:border-amber-400">
                </div>
            </div>
        `;
        blocksContainer.appendChild(div);
        updateEmptyState();
    }

    function createHeadingBlock(data = {}) {
        const idx = blockCounter++;
        const div = document.createElement('div');
        div.className = 'border border-purple-200 bg-purple-50/30 rounded-lg p-4 relative group';
        div.setAttribute('data-block-index', idx);
        div.setAttribute('data-block-type', 'heading');
        div.innerHTML = `
            <input type="hidden" name="content_blocks[${idx}][type]" value="heading">

            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <button type="button" class="cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500 drag-handle-block" title="Kéo để sắp xếp">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                        </svg>
                    </button>
                    <span class="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-purple-100 text-purple-700 rounded">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h10M7 12h10M7 17h4"/></svg>
                        Tiêu đề
                    </span>
                </div>
                <button type="button" onclick="removeBlock(this)"
                        class="p-1 text-gray-300 hover:text-red-500 transition-colors" title="Xóa block">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>

            <div>
                <label class="block text-[11px] font-medium text-purple-600 mb-1 uppercase tracking-wider">Tiêu đề (EN) <span class="text-red-400">*</span></label>
                <input type="text" name="content_blocks[${idx}][text_en]" value="${escapeHtml(data.text_en || '')}"
                       placeholder="VD: The Discovery of Radioactivity"
                       class="w-full px-3 py-2.5 text-sm font-semibold border border-gray-200 rounded outline-none bg-white text-gray-800 placeholder-gray-400 focus:border-purple-400">
            </div>
        `;
        blocksContainer.appendChild(div);
        updateEmptyState();
    }

    // Public API
    window.addBlock = function (type) {
        switch (type) {
            case 'paragraph': createParagraphBlock(); break;
            case 'quote':     createQuoteBlock();     break;
            case 'heading':   createHeadingBlock();   break;
        }
        // Scroll to the new block
        const lastBlock = blocksContainer.lastElementChild;
        if (lastBlock) lastBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
    };

    window.removeBlock = function (btn) {
        const block = btn.closest('[data-block-index]');
        if (confirm('Xóa block này?')) {
            block.remove();
            reindexBlocks();
            updateEmptyState();
        }
    };

    function reindexBlocks() {
        const blocks = blocksContainer.querySelectorAll('[data-block-index]');
        blockCounter = 0;
        blocks.forEach((block, i) => {
            block.setAttribute('data-block-index', i);
            block.querySelectorAll('input, textarea, select').forEach(input => {
                if (input.name) {
                    input.name = input.name.replace(/content_blocks\[\d+\]/, `content_blocks[${i}]`);
                }
            });
            blockCounter = i + 1;
        });
    }

    // Load initial blocks
    if (typeof initialBlocks !== 'undefined' && initialBlocks.length > 0) {
        initialBlocks.forEach(block => {
            switch (block.type) {
                case 'paragraph': createParagraphBlock(block); break;
                case 'quote':     createQuoteBlock(block);     break;
                case 'heading':   createHeadingBlock(block);   break;
            }
        });
    }

    updateEmptyState();

    // Drag-and-drop for content blocks
    initDragDrop(blocksContainer, '.drag-handle-block', '[data-block-index]', reindexBlocks);


    // ═════════════════════════════════════════════════════════════════════
    // UTILITIES
    // ═════════════════════════════════════════════════════════════════════

    // Form submit: no special handling needed, all data is in form fields
});

// ═══════════════════════════════════════════════════════════════════════════
// SHARED UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Simple drag-and-drop using native HTML5 DnD API.
 */
function initDragDrop(container, handleSelector, itemSelector, onReorder) {
    let dragItem = null;

    container.addEventListener('mousedown', function (e) {
        const handle = e.target.closest(handleSelector);
        if (!handle) return;
        const item = handle.closest(itemSelector);
        if (!item) return;
        item.setAttribute('draggable', 'true');
    });

    container.addEventListener('dragstart', function (e) {
        const item = e.target.closest(itemSelector);
        if (!item) return;
        dragItem = item;
        item.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
    });

    container.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const afterElement = getDragAfterElement(container, e.clientY, itemSelector);
        if (afterElement == null) {
            container.appendChild(dragItem);
        } else {
            container.insertBefore(dragItem, afterElement);
        }
    });

    container.addEventListener('dragend', function (e) {
        const item = e.target.closest(itemSelector);
        if (item) {
            item.style.opacity = '1';
            item.removeAttribute('draggable');
        }
        dragItem = null;
        if (onReorder) onReorder();
    });
}

function getDragAfterElement(container, y, itemSelector) {
    const items = [...container.querySelectorAll(itemSelector + ':not([style*="opacity: 0.5"])')];
    return items.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset, element: child };
        }
        return closest;
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}
</script>
