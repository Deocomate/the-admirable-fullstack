{{-- ── Basic Information Card ──────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-5 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
        </svg>
        Thông tin cơ bản
    </h2>

    <div class="space-y-4">
        {{-- Name --}}
        <div>
            <label for="name" class="block text-xs font-medium text-gray-600 mb-1.5">
                Tên nhân vật <span class="text-red-500">*</span>
            </label>
            <input type="text" id="name" name="name"
                   value="{{ old('name', $figure->name ?? '') }}"
                   required autofocus
                   placeholder="VD: Marie Curie"
                   class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                          bg-white text-gray-800 placeholder-gray-400
                          {{ $errors->has('name') ? 'border-red-400' : 'border-gray-300' }}"
                   onfocus="this.style.borderColor='#A31D1D'"
                   onblur="this.style.borderColor='{{ $errors->has('name') ? '#f87171' : '#D1D5DB' }}'">
            @error('name')
                <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
            @enderror
        </div>

        {{-- Short description --}}
        <div>
            <label for="short_description" class="block text-xs font-medium text-gray-600 mb-1.5">
                Mô tả ngắn (Tiếng Việt)
            </label>
            <textarea id="short_description" name="short_description"
                      rows="2"
                      placeholder="VD: Người phụ nữ đầu tiên giành giải Nobel và là người duy nhất giành giải Nobel trong hai lĩnh vực khoa học khác nhau."
                      class="w-full px-3 py-2.5 text-sm border border-gray-300 rounded outline-none transition-colors duration-150
                             bg-white text-gray-800 placeholder-gray-400 resize-none"
                      onfocus="this.style.borderColor='#A31D1D'"
                      onblur="this.style.borderColor='#D1D5DB'">{{ old('short_description', $figure->short_description ?? '') }}</textarea>
            <p class="mt-1 text-xs text-gray-400">Hiển thị bên dưới tiêu đề trên trang chi tiết.</p>
            @error('short_description')
                <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
            @enderror
        </div>
    </div>
</div>
