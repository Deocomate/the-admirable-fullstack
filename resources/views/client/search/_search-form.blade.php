{{-- Search Form --}}
<form action="{{ route('client.search') }}" method="GET" class="max-w-xl mx-auto mb-8">
    <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-apple-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
        </div>
        <input type="text" name="q" value="{{ $query ?? '' }}"
               placeholder="Tìm kiếm nhân vật, lĩnh vực..."
               class="w-full pl-12 pr-12 py-3.5 bg-apple-bg border-0 rounded-2xl text-apple-black placeholder-apple-gray/60 text-base focus:outline-none focus:ring-2 focus:ring-apple-blue/30 transition-all" />
        @if($query)
            <a href="{{ route('client.search') }}"
               class="absolute inset-y-0 right-12 flex items-center pr-2 text-apple-gray hover:text-apple-black transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </a>
        @endif
        <button type="submit"
                class="absolute inset-y-0 right-0 flex items-center pr-4 text-apple-blue hover:text-apple-blue/70 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
        </button>
    </div>
    @if($categorySlug)
        <input type="hidden" name="category" value="{{ $categorySlug }}" />
    @endif
</form>
