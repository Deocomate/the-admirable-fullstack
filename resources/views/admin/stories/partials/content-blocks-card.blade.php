{{-- ── Content Blocks Card ─────────────────────────────────────────────── --}}
@php
    $existingBlocks = old('content_blocks', isset($story) ? ($story->content_blocks ?? []) : []);
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
            Nội dung song ngữ <span class="text-red-500">*</span>
        </h2>
    </div>

    <p class="text-xs text-gray-400 mb-4">
        Thêm các đoạn văn song ngữ Anh–Việt. Mỗi đoạn gồm nội dung tiếng Anh (bắt buộc) và bản dịch tiếng Việt. Kéo thả để sắp xếp thứ tự.
    </p>

    {{-- Add block buttons --}}
    <div class="flex flex-wrap gap-2 mb-5">
        <button type="button" onclick="addStoryBlock('paragraph')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Đoạn văn
        </button>
        <button type="button" onclick="addStoryBlock('heading')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
            </svg>
            Tiêu đề phần
        </button>
        <button type="button" onclick="addStoryBlock('quote')"
                class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200 rounded-lg hover:bg-amber-100 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
            </svg>
            Trích dẫn
        </button>
    </div>

    {{-- Blocks container --}}
    <div id="story-blocks-container" class="space-y-4">
        {{-- Populated by JS --}}
    </div>

    {{-- Empty state --}}
    <div id="story-blocks-empty"
         class="hidden border-2 border-dashed border-gray-200 rounded-lg p-8 text-center">
        <svg class="w-10 h-10 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p class="text-sm text-gray-400">Chưa có đoạn văn nào. Nhấn "Thêm đoạn văn song ngữ" để bắt đầu.</p>
    </div>

    @error('content_blocks')
        <p class="mt-2 text-xs text-red-600">{{ $message }}</p>
    @enderror
</div>
