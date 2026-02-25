{{-- Popular Searches & Trending (when no query) --}}
<div class="grid grid-cols-1 lg:grid-cols-5 gap-12 reveal">
    {{-- Popular searches --}}
    <div class="lg:col-span-3">
        <p class="text-apple-blue text-xs font-semibold uppercase tracking-widest mb-6">Tìm kiếm phổ biến</p>
        <div class="flex flex-wrap gap-3">
            @php
                $popularSearches = ['Steve Jobs', 'Elon Musk', 'Einstein', 'Khoa học', 'Công nghệ', 'Nghệ thuật', 'Nelson Mandela', 'Marie Curie'];
            @endphp
            @foreach($popularSearches as $term)
                <a href="{{ route('client.search', ['q' => $term]) }}"
                   class="inline-flex items-center gap-2 px-4 py-2.5 bg-apple-bg hover:bg-apple-black/[0.06] text-apple-black rounded-full text-sm font-medium transition-all duration-300 hover:shadow-sm active:scale-[0.97]">
                    <svg class="w-3.5 h-3.5 text-apple-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    {{ $term }}
                </a>
            @endforeach
        </div>
    </div>

    {{-- Trending figures --}}
    <div class="lg:col-span-2">
        <p class="text-apple-blue text-xs font-semibold uppercase tracking-widest mb-6">Nhân vật nổi bật</p>
        <div class="space-y-3">
            @foreach($trendingFigures as $index => $trending)
                <a href="{{ route('client.figures.show', $trending->slug) }}"
                   class="flex items-center gap-4 p-3 rounded-2xl hover:bg-apple-bg transition-all duration-300 group">
                    <span class="text-xl font-bold text-apple-gray/30 tabular-nums w-8 text-center group-hover:text-apple-blue/30 transition-colors">
                        {{ str_pad($index + 1, 2, '0', STR_PAD_LEFT) }}
                    </span>
                    <div class="w-10 h-10 rounded-full overflow-hidden bg-apple-bg flex-shrink-0">
                        @if($trending->avatar_path)
                            <img src="{{ asset('storage/' . $trending->avatar_path) }}" alt="{{ $trending->name }}"
                                 class="w-full h-full object-cover" loading="lazy" />
                        @endif
                    </div>
                    <div class="min-w-0">
                        <p class="text-sm font-semibold text-apple-black truncate group-hover:text-apple-blue transition-colors">{{ $trending->name }}</p>
                        <p class="text-xs text-apple-gray">{{ $trending->story_snippets_count ?? 0 }} mẩu chuyện</p>
                    </div>
                </a>
            @endforeach
        </div>
    </div>
</div>
