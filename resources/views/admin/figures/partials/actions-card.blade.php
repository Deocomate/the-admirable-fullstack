{{-- ── Actions Card ────────────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Hành động
    </h2>

    <div class="space-y-3">
        @if(isset($figure))
            <a href="{{ route('client.figures.show', $figure->slug) }}"
               target="_blank"
               rel="noopener noreferrer"
               class="block w-full text-center px-5 py-2.5 text-sm font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 rounded transition-colors duration-150">
                Mở preview client
            </a>
        @endif

        <button type="submit"
                class="w-full px-5 py-2.5 text-sm font-semibold text-white rounded transition-colors duration-200"
                style="background:#A31D1D;"
                onmouseover="this.style.background='#8A1818'"
                onmouseout="this.style.background='#A31D1D'">
            {{ isset($figure) ? 'Lưu thay đổi' : 'Tạo nhân vật' }}
        </button>

        <a href="{{ route('admin.figures.index') }}"
           class="block w-full text-center px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
            Hủy
        </a>
    </div>

    @if(isset($figure))
        <div class="mt-4 pt-4 border-t border-gray-100">
            <p class="text-xs text-gray-400">
                Tạo lúc: {{ $figure->created_at->format('d/m/Y H:i') }}<br>
                Cập nhật: {{ $figure->updated_at->format('d/m/Y H:i') }}
            </p>
        </div>
    @endif
</div>
