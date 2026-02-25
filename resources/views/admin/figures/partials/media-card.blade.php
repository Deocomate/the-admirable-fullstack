{{-- ── Media Card (Avatar, Audio, YouTube) ────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-5 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        Media
    </h2>

    <div class="space-y-5">
        {{-- Avatar upload --}}
        <div>
            <label for="avatar" class="block text-xs font-medium text-gray-600 mb-1.5">
                Ảnh đại diện / Cover
            </label>
            @if(isset($figure) && $figure->avatar_path)
                <div class="mb-2">
                    <img src="{{ asset('storage/' . $figure->avatar_path) }}"
                         alt="{{ $figure->name }}"
                         class="w-full h-32 rounded-lg object-cover border border-gray-200">
                    <span class="text-xs text-gray-400 mt-1 block">Chọn file mới để thay thế.</span>
                </div>
            @endif
            <input type="file" id="avatar" name="avatar" accept="image/jpeg,image/png,image/webp"
                   class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-3 file:rounded file:border-0
                          file:text-xs file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
            <p class="mt-1 text-xs text-gray-400">JPG, PNG, WEBP. Max 5MB.</p>
            @error('avatar')
                <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
            @enderror
        </div>

        <hr class="border-gray-100">

        {{-- Audio upload --}}
        <div>
            <label for="audio" class="block text-xs font-medium text-gray-600 mb-1.5">
                File Audio (Bài đọc)
            </label>
            @if(isset($figure) && $figure->audio_path)
                <div class="mb-2">
                    <audio controls class="w-full h-9" style="border-radius:6px;">
                        <source src="{{ asset('storage/' . $figure->audio_path) }}" type="audio/mpeg">
                    </audio>
                    <span class="text-xs text-gray-400 mt-1 block">Chọn file mới để thay thế.</span>
                </div>
            @endif
            <input type="file" id="audio" name="audio" accept="audio/mpeg,audio/wav"
                   class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-3 file:rounded file:border-0
                          file:text-xs file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
            <p class="mt-1 text-xs text-gray-400">MP3, WAV. Max 20MB.</p>
            @error('audio')
                <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
            @enderror
        </div>

        <hr class="border-gray-100">

        {{-- YouTube URL --}}
        <div>
            <label for="youtube_url" class="block text-xs font-medium text-gray-600 mb-1.5">
                Link YouTube
            </label>
            <input type="url" id="youtube_url" name="youtube_url"
                   value="{{ old('youtube_url', $figure->youtube_url ?? '') }}"
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
</div>
