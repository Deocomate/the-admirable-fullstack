{{-- Stats Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-green-50">
            <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Thống kê nổi bật</h2>
            <p class="text-xs text-gray-400">4 con số ấn tượng hiển thị ngay dưới hero</p>
        </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        @for($i = 0; $i < 4; $i++)
        <div class="flex items-center gap-3 p-3 bg-gray-50/50 rounded-lg border border-gray-100">
            <div class="w-6 h-6 rounded flex items-center justify-center bg-white text-xs font-semibold text-gray-400 border border-gray-200 flex-shrink-0">
                {{ $i + 1 }}
            </div>
            <div class="flex-1 grid grid-cols-2 gap-2">
                <input type="text" name="stats[{{ $i }}][value]"
                       value="{{ old("stats.{$i}.value", $aboutData['stats'][$i]['value'] ?? '') }}"
                       class="px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition font-semibold"
                       placeholder="50+">
                <input type="text" name="stats[{{ $i }}][label]"
                       value="{{ old("stats.{$i}.label", $aboutData['stats'][$i]['label'] ?? '') }}"
                       class="px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                       placeholder="Nhân vật vĩ đại">
            </div>
        </div>
        @endfor
    </div>
</div>
