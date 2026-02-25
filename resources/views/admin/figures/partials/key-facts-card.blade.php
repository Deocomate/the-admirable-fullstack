{{-- ── Key Facts Card ──────────────────────────────────────────────────── --}}
@php
    $existingFacts = old('key_facts', isset($figure) ? ($figure->key_facts ?? []) : []);
    if (is_string($existingFacts)) {
        $existingFacts = json_decode($existingFacts, true) ?? [];
    }
@endphp

<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Thông tin nhanh
        </h2>
        <button type="button" onclick="addKeyFact()"
                class="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-white rounded transition-colors duration-150"
                style="background:#A31D1D;" onmouseover="this.style.background='#8A1818'" onmouseout="this.style.background='#A31D1D'">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm
        </button>
    </div>

    <p class="text-xs text-gray-400 mb-3">Hiển thị dạng thẻ thông tin nhanh phía trên bài viết (VD: Năm sinh, Quốc tịch, Giải thưởng...).</p>

    <div id="key-facts-container" class="space-y-2">
        {{-- Populated by JS or from existing data --}}
    </div>

    @error('key_facts')
        <p class="mt-2 text-xs text-red-600">{{ $message }}</p>
    @enderror
</div>

<script>
    const initialKeyFacts = @json($existingFacts);
</script>
