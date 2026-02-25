{{-- Search Results --}}
<div class="mb-6 reveal">
    <p class="text-sm text-apple-gray">
        @if($query)
            Kết quả cho "<span class="font-semibold text-apple-black">{{ $query }}</span>"
        @endif
        — {{ $figures->total() }} nhân vật
    </p>
</div>

@if($figures->isNotEmpty())
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
        @foreach($figures as $index => $figure)
            <div class="reveal reveal-delay-{{ min(($index % 3) + 1, 3) }}">
                <x-client.shared.figure-card :figure="$figure" />
            </div>
        @endforeach
    </div>

    <x-client.shared.pagination :paginator="$figures" />
@else
    <div class="text-center py-20 reveal">
        <div class="w-16 h-16 bg-apple-bg rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-apple-gray" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
        </div>
        <h3 class="text-lg font-semibold text-apple-black mb-2">Không tìm thấy kết quả</h3>
        <p class="text-sm text-apple-gray max-w-md mx-auto">
            Hãy thử tìm kiếm với từ khoá khác hoặc duyệt qua các lĩnh vực bên trên.
        </p>
    </div>
@endif

{{-- Trending sidebar --}}
@if($trendingFigures->isNotEmpty())
    <div class="mt-16 border-t border-apple-border pt-12 reveal">
        <div class="flex items-center justify-between mb-6">
            <p class="text-apple-blue text-xs font-semibold uppercase tracking-widest">Xu hướng</p>
            <a href="{{ route('client.search') }}"
               class="text-apple-blue text-xs font-medium hover:underline inline-flex items-center gap-1 cursor-pointer group">
                Xem thêm
                <svg class="w-3 h-3 transition-transform duration-300 group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                </svg>
            </a>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            @foreach($trendingFigures as $index => $trending)
                <a href="{{ route('client.figures.show', $trending->slug) }}"
                   class="flex items-center gap-4 p-4 rounded-2xl hover:bg-apple-bg transition-all duration-300 group reveal reveal-delay-{{ min($index + 1, 4) }}">
                    <span class="text-2xl font-bold text-apple-gray/30 tabular-nums group-hover:text-apple-blue/30 transition-colors">
                        {{ str_pad($index + 1, 2, '0', STR_PAD_LEFT) }}
                    </span>
                    <div class="w-12 h-12 rounded-full overflow-hidden bg-apple-bg flex-shrink-0">
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
@endif
