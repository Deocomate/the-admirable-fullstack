@props(['shareUrl' => '', 'shareTitle' => '', 'label' => 'Chia sẻ bài viết'])

<div class="mt-12 pt-8 border-t border-apple-gray-light/50">
    <div class="flex items-center justify-between flex-wrap gap-4">
        <div>
            <p class="text-xs font-semibold text-apple-gray uppercase tracking-wider mb-3">{{ $label }}</p>
            <button onclick="copyArticleLink(this, '{{ $shareUrl }}')"
                    class="inline-flex items-center gap-2 px-4 py-2 bg-apple-bg hover:bg-apple-gray-light/80 rounded-full text-sm text-apple-gray hover:text-apple-black transition-all duration-300 cursor-pointer active:scale-[0.97]">
                <svg class="w-4 h-4 copy-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                <svg class="w-4 h-4 check-icon hidden text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                <span class="copy-label">Sao chép liên kết</span>
            </button>
        </div>
    </div>
</div>
