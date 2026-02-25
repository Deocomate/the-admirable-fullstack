{{-- Problem & Solution Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-red-50">
            <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Vấn đề & Giải pháp</h2>
            <p class="text-xs text-gray-400">Nêu lên vấn đề của người học và cách The Admirable giải quyết</p>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {{-- Problem --}}
        <div class="p-4 bg-red-50/30 rounded-xl border border-red-100/50">
            <p class="text-xs font-semibold text-red-600/70 uppercase tracking-wider mb-3">Vấn đề</p>
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Tiêu đề</label>
                    <input type="text" name="problem[title]"
                           value="{{ old('problem.title', $aboutData['problem']['title'] ?? '') }}"
                           class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition bg-white"
                           placeholder="Nỗi trăn trở của người học">
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Mô tả</label>
                    <textarea name="problem[description]" rows="4"
                              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none bg-white"
                              placeholder="Mô tả vấn đề mà người học gặp phải...">{{ old('problem.description', $aboutData['problem']['description'] ?? '') }}</textarea>
                </div>
            </div>
        </div>

        {{-- Solution --}}
        <div class="p-4 bg-blue-50/30 rounded-xl border border-blue-100/50">
            <p class="text-xs font-semibold text-blue-600/70 uppercase tracking-wider mb-3">Giải pháp</p>
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Tiêu đề</label>
                    <input type="text" name="solution[title]"
                           value="{{ old('solution.title', $aboutData['solution']['title'] ?? '') }}"
                           class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition bg-white"
                           placeholder='Giải pháp mang tên "The Admirable"'>
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">Mô tả</label>
                    <textarea name="solution[description]" rows="3"
                              class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none bg-white"
                              placeholder="Mô tả giải pháp...">{{ old('solution.description', $aboutData['solution']['description'] ?? '') }}</textarea>
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">
                        Điểm nổi bật <span class="text-gray-400 font-normal">(mỗi dòng một ý)</span>
                    </label>
                    @for($i = 0; $i < 3; $i++)
                    <input type="text" name="solution[bullets][{{ $i }}]"
                           value="{{ old("solution.bullets.{$i}", $aboutData['solution']['bullets'][$i] ?? '') }}"
                           class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition bg-white {{ $i > 0 ? 'mt-2' : '' }}"
                           placeholder="Điểm nổi bật {{ $i + 1 }}">
                    @endfor
                </div>
            </div>
        </div>
    </div>
</div>
