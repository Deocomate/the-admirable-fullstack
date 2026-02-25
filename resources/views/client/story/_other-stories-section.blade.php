{{-- Other Stories from Same Figure --}}
<section class="bg-apple-bg py-16 sm:py-20 px-4">
    <div class="max-w-[980px] mx-auto">
        <div class="text-center mb-10 sm:mb-12 reveal">
            <p class="text-apple-blue text-xs font-semibold uppercase tracking-widest mb-2">Cùng nhân vật</p>
            <h2 class="text-2xl sm:text-3xl font-bold text-apple-black tracking-apple-tight">
                Các mẩu chuyện khác về {{ $snippet->figure->name }}
            </h2>
        </div>

        <div data-paginated-grid="3" class="reveal">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-5 paginated-items">
                @foreach($otherStories as $index => $story)
                    <div class="paginated-item">
                        <x-client.shared.story-card :snippet="$story" />
                    </div>
                @endforeach
            </div>
            <div class="flex items-center justify-center gap-3 mt-8 paginated-controls hidden">
                <button class="paginated-prev w-9 h-9 rounded-full bg-white hover:bg-apple-gray-light/80 flex items-center justify-center text-apple-gray hover:text-apple-black transition-all duration-300 cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed" aria-label="Trang trước">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                </button>
                <span class="paginated-info text-xs text-apple-gray font-medium"></span>
                <button class="paginated-next w-9 h-9 rounded-full bg-white hover:bg-apple-gray-light/80 flex items-center justify-center text-apple-gray hover:text-apple-black transition-all duration-300 cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed" aria-label="Trang sau">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
                </button>
            </div>
        </div>

        <div class="text-center mt-10 reveal">
            <a href="{{ route('client.figures.show', $snippet->figure->slug) }}"
               class="inline-flex items-center gap-2 text-apple-blue font-semibold text-sm hover:underline transition-colors">
                Xem tất cả về {{ $snippet->figure->name }}
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
            </a>
        </div>
    </div>
</section>
