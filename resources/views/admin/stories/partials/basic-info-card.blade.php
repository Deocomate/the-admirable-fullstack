{{-- ── Basic Info Card ─────────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-4">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
        </svg>
        Thông tin cơ bản
    </h2>

    {{-- Figure selection --}}
    <div class="mb-4">
        <label for="figure_id" class="block text-xs font-medium text-gray-600 mb-1.5">
            Nhân vật <span class="text-red-500">*</span>
        </label>
        <select id="figure_id" name="figure_id" required
                class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                       bg-white text-gray-800
                       {{ $errors->has('figure_id') ? 'border-red-400' : 'border-gray-300' }}"
                onfocus="this.style.borderColor='#A31D1D'"
                onblur="this.style.borderColor='{{ $errors->has('figure_id') ? '#f87171' : '#D1D5DB' }}'">
            <option value="">-- Chọn nhân vật --</option>
            @foreach($figures as $fig)
                <option value="{{ $fig->id }}"
                    {{ old('figure_id', $story->figure_id ?? ($selectedFigureId ?? '')) == $fig->id ? 'selected' : '' }}>
                    {{ $fig->name }}
                </option>
            @endforeach
        </select>
        @error('figure_id')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>

    {{-- Title (EN) --}}
    <div class="mb-4">
        <label for="title" class="block text-xs font-medium text-gray-600 mb-1.5">
            Tiêu đề (Tiếng Anh) <span class="text-red-500">*</span>
        </label>
        <input type="text" id="title" name="title"
               value="{{ old('title', $story->title ?? '') }}"
               required
               placeholder="VD: The Radioactive Notebooks"
               class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                      bg-white text-gray-800 placeholder-gray-400
                      {{ $errors->has('title') ? 'border-red-400' : 'border-gray-300' }}"
               onfocus="this.style.borderColor='#A31D1D'"
               onblur="this.style.borderColor='{{ $errors->has('title') ? '#f87171' : '#D1D5DB' }}'">
        @error('title')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>

    {{-- Subtitle (VI) --}}
    <div>
        <label for="subtitle" class="block text-xs font-medium text-gray-600 mb-1.5">
            Phụ đề (Tiếng Việt)
        </label>
        <input type="text" id="subtitle" name="subtitle"
               value="{{ old('subtitle', $story->subtitle ?? '') }}"
               placeholder="VD: Sổ ghi chép nhiễm phóng xạ — Hơn một thế kỷ sau..."
               class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                      bg-white text-gray-800 placeholder-gray-400 border-gray-300"
               onfocus="this.style.borderColor='#A31D1D'"
               onblur="this.style.borderColor='#D1D5DB'">
        <p class="mt-1 text-xs text-gray-400">Mô tả ngắn bằng tiếng Việt hiển thị dưới tiêu đề.</p>
        @error('subtitle')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>
</div>
