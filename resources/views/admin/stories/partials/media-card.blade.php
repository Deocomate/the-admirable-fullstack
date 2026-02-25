{{-- ── Media Card ─────────────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-4">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        Media
    </h2>

    {{-- Image upload --}}
    <div class="mb-5">
        <label for="image" class="block text-xs font-medium text-gray-600 mb-1.5">Hình ảnh minh họa</label>
        @if(isset($story) && $story->image_path)
            <div class="mb-2">
                <img src="{{ asset('storage/' . $story->image_path) }}"
                     alt="{{ $story->title }}"
                     class="w-full h-32 rounded-lg object-cover border border-gray-200">
                <span class="text-xs text-gray-400 mt-1 block">Ảnh hiện tại. Chọn file mới để thay thế.</span>
            </div>
        @endif
        <input type="file" id="image" name="image" accept="image/jpeg,image/png,image/webp"
               class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded file:border-0
                      file:text-xs file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
        <p class="mt-1 text-xs text-gray-400">JPG, PNG, WEBP. Tối đa 5MB.</p>
        @error('image')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>

    {{-- Audio upload --}}
    <div class="mb-5">
        <label for="audio" class="block text-xs font-medium text-gray-600 mb-1.5">File Audio</label>
        @if(isset($story) && $story->audio_path)
            <div class="mb-2">
                <audio controls class="w-full h-10">
                    <source src="{{ asset('storage/' . $story->audio_path) }}" type="audio/mpeg">
                </audio>
                <span class="text-xs text-gray-400">Audio hiện tại. Chọn file mới để thay thế.</span>
            </div>
        @endif
        <input type="file" id="audio" name="audio" accept="audio/mpeg,audio/wav"
               class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded file:border-0
                      file:text-xs file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
        <p class="mt-1 text-xs text-gray-400">MP3, WAV. Tối đa 20MB.</p>
        @error('audio')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>

    {{-- YouTube URL --}}
    <div>
        <label for="youtube_url" class="block text-xs font-medium text-gray-600 mb-1.5">Link YouTube</label>
        <input type="url" id="youtube_url" name="youtube_url"
               value="{{ old('youtube_url', $story->youtube_url ?? '') }}"
               placeholder="https://www.youtube.com/watch?v=..."
               class="w-full px-3 py-2.5 text-sm border border-gray-300 rounded outline-none transition-colors duration-150
                      bg-white text-gray-800 placeholder-gray-400"
               onfocus="this.style.borderColor='#A31D1D'"
               onblur="this.style.borderColor='#D1D5DB'">
        @error('youtube_url')
            <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
        @enderror
    </div>
</div>
