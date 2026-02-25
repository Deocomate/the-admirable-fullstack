{{-- CTA Section Editor --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <div class="flex items-center gap-3 mb-5">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-gray-800">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
        </div>
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Call to Action</h2>
            <p class="text-xs text-gray-400">Phần kết trang — kêu gọi hành động</p>
        </div>
    </div>

    <div class="space-y-4">
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Câu trích dẫn
                <span class="text-gray-400 font-normal">(quote nhỏ phía trên)</span>
            </label>
            <input type="text" name="cta[quote]"
                   value="{{ old('cta.quote', $aboutData['cta']['quote'] ?? '') }}"
                   class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition italic"
                   placeholder='"Đọc là để sống nhiều hơn một lần."'>
        </div>
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Tiêu đề CTA</label>
            <input type="text" name="cta[headline]"
                   value="{{ old('cta.headline', $aboutData['cta']['headline'] ?? '') }}"
                   class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition font-semibold"
                   placeholder="Sẵn sàng để bắt đầu?">
        </div>
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Mô tả CTA</label>
            <textarea name="cta[description]" rows="2"
                      class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition resize-none"
                      placeholder="Lời mời gọi hành động...">{{ old('cta.description', $aboutData['cta']['description'] ?? '') }}</textarea>
        </div>
    </div>
</div>
