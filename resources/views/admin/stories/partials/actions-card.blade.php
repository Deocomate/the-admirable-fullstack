{{-- ── Actions Card ────────────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-4">Thao tác</h2>

    <div class="space-y-3">
        <button type="submit"
                class="w-full px-5 py-2.5 text-sm font-semibold text-white rounded transition-colors duration-200"
                style="background:#A31D1D;"
                onmouseover="this.style.background='#8A1818'"
                onmouseout="this.style.background='#A31D1D'">
            {{ isset($story) ? 'Lưu thay đổi' : 'Tạo mẩu chuyện' }}
        </button>
        <a href="{{ route('admin.stories.index') }}"
           class="block w-full px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150 text-center">
            Hủy
        </a>
    </div>

    @if(isset($story))
        <div class="mt-4 pt-4 border-t border-gray-100 text-xs text-gray-400 space-y-1">
            <p>Tạo: {{ $story->created_at->format('d/m/Y H:i') }}</p>
            <p>Sửa: {{ $story->updated_at->format('d/m/Y H:i') }}</p>
            @if($story->figure)
                <p class="mt-2">
                    <a href="{{ route('admin.figures.edit', $story->figure->id) }}"
                       class="text-blue-600 hover:underline inline-flex items-center gap-1">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                        </svg>
                        Xem hồ sơ nhân vật
                    </a>
                </p>
            @endif
        </div>
    @endif
</div>
