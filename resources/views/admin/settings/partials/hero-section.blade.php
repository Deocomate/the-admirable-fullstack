{{-- Hero Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-blue-50">
            <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Hero Section</h2>
            <p class="text-xs text-gray-400">Khu vực chào đón đầu tiên của trang</p>
        </div>
    </div>

    <div class="space-y-4">
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1" for="hero_tagline">Tagline
                <span class="text-gray-400 font-normal">(ví dụ: "Câu chuyện của chúng tôi")</span>
            </label>
            <input type="text" id="hero_tagline" name="hero[tagline]"
                   value="{{ old('hero.tagline', $aboutData['hero']['tagline'] ?? '') }}"
                   class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                   placeholder="Câu chuyện của chúng tôi">
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1" for="hero_headline">Headline chính</label>
                <input type="text" id="hero_headline" name="hero[headline]"
                       value="{{ old('hero.headline', $aboutData['hero']['headline'] ?? '') }}"
                       class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                       placeholder="Học ngôn ngữ qua">
            </div>
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1" for="hero_headline_gradient">Headline gradient
                    <span class="text-gray-400 font-normal">(dòng nổi bật)</span>
                </label>
                <input type="text" id="hero_headline_gradient" name="hero[headline_gradient]"
                       value="{{ old('hero.headline_gradient', $aboutData['hero']['headline_gradient'] ?? '') }}"
                       class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
                       placeholder="những tầm cao nhân loại.">
            </div>
        </div>

        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1" for="hero_description">Mô tả</label>
            <textarea id="hero_description" name="hero[description]" rows="3"
                      class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none"
                      placeholder="Mô tả ngắn về sứ mệnh...">{{ old('hero.description', $aboutData['hero']['description'] ?? '') }}</textarea>
        </div>
    </div>
</div>
