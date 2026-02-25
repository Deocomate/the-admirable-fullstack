@props([
    'audioPath' => null,
    'variant' => 'blue',
])

@if($audioPath)
<div data-audio-player class="bg-apple-bg rounded-[24px] p-4 sm:p-5 mb-10 flex flex-col sm:flex-row items-center gap-4 sm:gap-6 shadow-sm border border-black/5">
    <button onclick="toggleAudio(this)"
        class="audio-play-btn w-12 h-12 rounded-full {{ $variant === 'blue' ? 'bg-apple-blue hover:bg-apple-blue-hover' : 'bg-apple-black hover:bg-gray-800' }} text-white flex items-center justify-center flex-shrink-0 transition-colors shadow-md focus:outline-none focus:ring-4 {{ $variant === 'blue' ? 'focus:ring-apple-blue/20' : 'focus:ring-gray-300' }}">
        <svg class="w-5 h-5 ml-1 play-icon" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
        </svg>
        <svg class="w-5 h-5 pause-icon hidden" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
        </svg>
    </button>
    <div class="flex-1 w-full flex flex-col justify-center">
        <div class="flex justify-between text-[11px] text-apple-gray font-medium mb-1.5 px-1">
            <span class="audio-current-time">0:00</span>
            <span class="audio-duration">0:00</span>
        </div>
        <input type="range" min="0" max="100" value="0" class="w-full audio-seek" oninput="seekAudio(this)">
    </div>
    <div class="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-start">
        <select class="audio-speed bg-white border border-apple-gray-light/50 text-apple-black text-xs rounded-lg px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-apple-blue cursor-pointer font-medium" onchange="changeSpeed(this)">
            <option value="0.75">0.75x</option>
            <option value="1" selected>1x Speed</option>
            <option value="1.25">1.25x</option>
            <option value="1.5">1.5x</option>
        </select>
        {{-- Volume boost control --}}
        <div class="relative">
            <button type="button" onclick="toggleVolumePopup(this)" class="audio-volume-btn flex items-center gap-1 text-apple-gray hover:text-apple-black transition-colors" title="Âm lượng">
                <svg class="w-5 h-5 volume-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.5H3a1 1 0 00-1 1v5a1 1 0 001 1h3.5l5 4V4.5l-5 4z" />
                </svg>
                <span class="audio-volume-label text-[11px] font-semibold min-w-[32px] text-center">100%</span>
            </button>
            <div class="audio-volume-popup hidden absolute bottom-full left-1/2 -translate-x-1/2 mb-2 bg-white rounded-xl shadow-lg border border-black/10 p-3 w-[52px] z-50">
                <input type="range" min="0" max="300" value="100" class="audio-volume-slider" orient="vertical" oninput="changeVolume(this)" />
                <div class="text-[10px] text-apple-gray text-center mt-1 font-medium audio-volume-value">100%</div>
            </div>
        </div>
        <a href="{{ asset('storage/' . $audioPath) }}" download class="text-apple-gray hover:text-apple-black transition-colors" title="Tải xuống Audio">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
        </a>
    </div>
    <audio class="hidden audio-element" preload="metadata" crossorigin="anonymous">
        <source src="{{ asset('storage/' . $audioPath) }}" type="audio/mpeg">
    </audio>
</div>
@endif
