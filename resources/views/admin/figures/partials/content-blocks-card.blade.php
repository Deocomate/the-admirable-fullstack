{{-- ── Content Blocks Card ─────────────────────────────────────────────── --}}
@php
    $existingBlocks = old('content_blocks', isset($figure) ? ($figure->content_blocks ?? []) : []);
    if (is_string($existingBlocks)) {
        $existingBlocks = json_decode($existingBlocks, true) ?? [];
    }
@endphp

<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
            </svg>
            Nội dung bài viết (Song ngữ) <span class="text-red-500">*</span>
        </h2>
    </div>

    <p class="text-xs text-gray-400 mb-4">
        Thêm các đoạn văn song ngữ Anh–Việt và trích dẫn. Kéo thả để sắp xếp thứ tự hiển thị.
    </p>

    {{-- Add block buttons --}}
    <div class="flex flex-wrap gap-2 mb-5">
        <button type="button" onclick="addBlock('paragraph')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
            </svg>
            Đoạn văn song ngữ
        </button>
        <button type="button" onclick="addBlock('quote')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200 rounded-lg hover:bg-amber-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
            Trích dẫn (Quote)
        </button>
        <button type="button" onclick="addBlock('heading')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h10M7 12h10M7 17h4"/>
            </svg>
            Tiêu đề phần
        </button>
    </div>

    {{-- Blocks container --}}
    <div id="content-blocks-container" class="space-y-4">
        {{-- Populated by JS --}}
    </div>

    {{-- Empty state --}}
    <div id="blocks-empty-state" class="hidden text-center py-10 border-2 border-dashed border-gray-200 rounded-lg">
        <svg class="w-10 h-10 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
        </svg>
        <p class="text-sm text-gray-400 mb-1">Chưa có nội dung nào</p>
        <p class="text-xs text-gray-300">Bấm các nút trên đây để bắt đầu thêm nội dung song ngữ.</p>
    </div>

    @error('content_blocks')
        <p class="mt-2 text-xs text-red-600">{{ $message }}</p>
    @enderror
</div>

<script>
    const initialBlocks = @json($existingBlocks);
</script>
