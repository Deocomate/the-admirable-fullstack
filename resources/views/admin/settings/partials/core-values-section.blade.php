{{-- Core Values Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-purple-50">
            <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Giá trị cốt lõi</h2>
            <p class="text-xs text-gray-400">Những giá trị mà The Admirable theo đuổi</p>
        </div>
    </div>

    <div class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Tagline</label>
                <input type="text" name="core_values[tagline]"
                       value="{{ old('core_values.tagline', $aboutData['core_values']['tagline'] ?? '') }}"
                       class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                       placeholder="Giá trị cốt lõi">
            </div>
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Tiêu đề</label>
                <input type="text" name="core_values[title]"
                       value="{{ old('core_values.title', $aboutData['core_values']['title'] ?? '') }}"
                       class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                       placeholder="Những gì chúng tôi tin tưởng">
            </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            @for($i = 0; $i < 4; $i++)
            <div class="p-3 bg-gray-50/50 rounded-lg border border-gray-100">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-5 h-5 rounded flex items-center justify-center bg-purple-100 text-[10px] font-bold text-purple-600 flex-shrink-0">
                        {{ $i + 1 }}
                    </div>
                    <span class="text-xs font-medium text-gray-500">Giá trị {{ $i + 1 }}</span>
                </div>
                <input type="text" name="core_values[items][{{ $i }}][title]"
                       value="{{ old("core_values.items.{$i}.title", $aboutData['core_values']['items'][$i]['title'] ?? '') }}"
                       class="w-full px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition mb-2"
                       placeholder="Tên giá trị">
                <textarea name="core_values[items][{{ $i }}][description]" rows="2"
                          class="w-full px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none"
                          placeholder="Mô tả ngắn...">{{ old("core_values.items.{$i}.description", $aboutData['core_values']['items'][$i]['description'] ?? '') }}</textarea>
            </div>
            @endfor
        </div>
    </div>
</div>
