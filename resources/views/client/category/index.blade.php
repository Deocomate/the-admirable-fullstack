@php
    $activeCategory = $category ?? null;
    $pageTitle = $activeCategory
        ? $activeCategory->name . ' — The Admirable'
        : 'Lĩnh vực — The Admirable';
    $pageDescription = $activeCategory
        ? 'Khám phá các nhân vật truyền cảm hứng thuộc lĩnh vực ' . $activeCategory->name . ' tại The Admirable.'
        : 'Khám phá các lĩnh vực và những nhân vật truyền cảm hứng nổi bật tại The Admirable.';
    $activeSlug = $activeCategory?->slug;
@endphp

<x-client.layout.app
    :title="$pageTitle"
    :description="$pageDescription"
    :canonicalUrl="$activeCategory ? route('client.categories.show', $activeCategory->slug) : route('client.categories.index')"
    :keywords="$activeCategory ? ($activeCategory->name . ', nhân vật truyền cảm hứng, The Admirable') : 'lĩnh vực, nhân vật truyền cảm hứng, The Admirable'"
    activePage="category">

    {{-- HERO + PILLS --}}
    <section class="bg-apple-white overflow-hidden border-b border-apple-gray-light/30">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 pt-12 pb-8 sm:pt-16 sm:pb-10 lg:pt-20 lg:pb-12 text-center">
            <h1 class="text-3xl sm:text-4xl lg:text-[48px] font-bold tracking-apple-headline text-apple-black leading-[1.05] mb-4 animate-fade-in-up">
                Lĩnh vực.
            </h1>
            <p class="text-apple-gray text-lg sm:text-[19px] leading-relaxed max-w-2xl mx-auto mb-8 tracking-apple-tight animate-fade-in-up animate-delay-1">
                Khám phá cuộc đời và di sản của những nhân vật vĩ đại theo từng nhóm ngành cụ thể.
            </p>
            <div class="animate-fade-in-up animate-delay-2">
                <x-client.shared.category-pills :categories="$categories" :activeSlug="$activeSlug" />
            </div>
        </div>
    </section>

    {{-- FEATURED CATEGORY CARD --}}
    @if($featuredFigure)
    <section class="bg-apple-white border-b border-apple-gray-light/30">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 py-8 sm:py-10">
            <a href="{{ route('client.figures.show', $featuredFigure->slug) }}" class="group block bg-apple-bg rounded-2xl lg:rounded-[28px] overflow-hidden card-hover cursor-pointer reveal">
                <div class="grid grid-cols-1 sm:grid-cols-2">
                    <div class="relative aspect-[4/3] sm:aspect-auto overflow-hidden">
                        <img src="{{ $featuredFigure->avatar_path ? asset('storage/' . $featuredFigure->avatar_path) : 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=800&h=600&fit=crop' }}"
                             alt="{{ $featuredFigure->name }}" class="img-zoom w-full h-full object-cover" loading="lazy" />
                        <div class="absolute top-4 left-4">
                            <span class="inline-flex items-center px-3 py-1 bg-apple-blue text-white rounded-full text-[11px] font-semibold uppercase tracking-wider shadow-sm">Nổi bật</span>
                        </div>
                    </div>
                    <div class="p-6 sm:p-8 lg:p-10 flex flex-col justify-center">
                        @if($featuredFigure->categories->isNotEmpty())
                            <p class="text-apple-gray text-[11px] font-semibold uppercase tracking-wider mb-2">{{ $featuredFigure->categories->first()->name }}</p>
                        @endif
                        <h2 class="text-xl sm:text-2xl lg:text-[28px] font-bold text-apple-black tracking-apple-headline leading-tight mb-3">
                            {{ $featuredFigure->name }}
                        </h2>
                        <p class="text-apple-gray text-[15px] leading-relaxed mb-5 line-clamp-3">
                            {{ $featuredFigure->short_description }}
                        </p>
                        @include('client.home._media-badges', ['figure' => $featuredFigure])
                        <span class="text-apple-blue text-sm font-normal inline-flex items-center group-hover:underline mt-4">
                            Đọc hồ sơ
                            <svg class="w-3.5 h-3.5 ml-1 transition-transform duration-300 group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg>
                        </span>
                    </div>
                </div>
            </a>
        </div>
    </section>
    @endif

    {{-- FIGURES GRID --}}
    <section class="bg-apple-bg py-10 sm:py-14 min-h-[50vh]">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6">
            <div class="mb-6 flex items-end justify-between reveal">
                <h2 class="text-[21px] font-semibold text-apple-black tracking-apple-tight">
                    @if($activeCategory)
                        Nhân vật {{ $activeCategory->name }}
                    @else
                        Tất cả nhân vật
                    @endif
                    <span class="text-apple-gray font-normal text-lg ml-1">({{ $figures->total() }})</span>
                </h2>
            </div>

            @if($figures->isNotEmpty())
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-5">
                    @foreach($figures as $index => $figure)
                        <div class="reveal" style="transition-delay: {{ ($index % 6) * 80 }}ms">
                            <x-client.shared.figure-card :figure="$figure" />
                        </div>
                    @endforeach
                </div>
                <x-client.shared.pagination :paginator="$figures" />
            @else
                <div class="text-center py-20 reveal">
                    <p class="text-apple-gray text-lg">Chưa có nhân vật nào trong lĩnh vực này.</p>
                </div>
            @endif
        </div>
    </section>

</x-client.layout.app>
