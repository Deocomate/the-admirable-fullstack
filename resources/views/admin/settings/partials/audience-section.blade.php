{{-- Target Audience Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-orange-50">
            <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Đối tượng mục tiêu</h2>
            <p class="text-xs text-gray-400">Nền tảng này dành cho ai?</p>
        </div>
    </div>

    <div class="space-y-4">
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Tiêu đề section</label>
            <input type="text" name="audience[title]"
                   value="{{ old('audience.title', $aboutData['audience']['title'] ?? '') }}"
                   class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                   placeholder="Nền tảng này dành cho ai?">
        </div>
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Mô tả</label>
            <textarea name="audience[description]" rows="2"
                      class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none"
                      placeholder="Mô tả chung...">{{ old('audience.description', $aboutData['audience']['description'] ?? '') }}</textarea>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            @for($i = 0; $i < 3; $i++)
            <div class="p-3 bg-gray-50/50 rounded-lg border border-gray-100">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-5 h-5 rounded flex items-center justify-center bg-orange-100 text-[10px] font-bold text-orange-600 flex-shrink-0">
                        {{ $i + 1 }}
                    </div>
                    <span class="text-xs font-medium text-gray-500">Nhóm {{ $i + 1 }}</span>
                </div>
                <input type="text" name="audience[items][{{ $i }}][title]"
                       value="{{ old("audience.items.{$i}.title", $aboutData['audience']['items'][$i]['title'] ?? '') }}"
                       class="w-full px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition mb-2"
                       placeholder="Tên nhóm đối tượng">
                <textarea name="audience[items][{{ $i }}][description]" rows="3"
                          class="w-full px-2.5 py-1.5 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none"
                          placeholder="Mô tả đối tượng...">{{ old("audience.items.{$i}.description", $aboutData['audience']['items'][$i]['description'] ?? '') }}</textarea>
            </div>
            @endfor
        </div>
    </div>
</div>
