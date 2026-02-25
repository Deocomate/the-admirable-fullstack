<x-client.layout.app
    title="The Admirable — Những tấm gương đáng ngưỡng mộ"
    description="Khám phá những câu chuyện truyền cảm hứng từ các nhân vật nổi tiếng trên thế giới. Luyện IELTS qua bài đọc song ngữ, audio và video."
    :canonicalUrl="route('client.home')"
    keywords="nhân vật truyền cảm hứng, học tiếng anh, luyện IELTS, câu chuyện song ngữ"
    activePage="home">

    {{-- HERO --}}
    <section class="bg-apple-white overflow-hidden">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 pt-16 pb-10 sm:pt-20 sm:pb-12 lg:pt-28 lg:pb-16 text-center">
            <p class="text-apple-blue text-sm sm:text-base font-semibold tracking-wide mb-3 animate-fade-in-up">
                Truyền cảm hứng qua từng câu chuyện
            </p>
            <h1 class="text-4xl sm:text-5xl lg:text-7xl font-bold tracking-apple-display text-apple-black leading-[1.05] mb-5 animate-fade-in-up animate-delay-1">
                Những tấm gương<br />
                <span class="gradient-text" data-typing='["đáng ngưỡng mộ.", "truyền cảm hứng.", "thay đổi thế giới."]' data-typing-speed="90" data-typing-pause="2500">đáng ngưỡng mộ.</span>
            </h1>
            <p class="text-apple-gray text-lg sm:text-xl lg:text-[21px] leading-relaxed max-w-2xl mx-auto mb-8 tracking-apple-tight animate-fade-in-up animate-delay-2">
                Khám phá cuộc đời những nhân vật vĩ đại. Đọc chữ, nghe audio, xem video — luyện IELTS một cách tự nhiên và đầy cảm hứng.
            </p>
            <div class="flex flex-col sm:flex-row gap-3 justify-center items-center animate-fade-in-up animate-delay-3">
                <a href="#featured"
                   class="inline-flex items-center justify-center px-7 py-3 bg-apple-blue hover:bg-apple-blue-hover text-white text-sm font-normal rounded-full transition-all duration-300 cursor-pointer min-w-[160px] hover:shadow-lg hover:shadow-apple-blue/20 active:scale-[0.97]">
                    Khám phá ngay
                </a>
                <a href="{{ route('client.search') }}"
                   class="inline-flex items-center justify-center text-apple-blue hover:underline text-sm font-normal cursor-pointer group">
                    Tìm kiếm nhân vật
                    <svg class="w-3.5 h-3.5 ml-1 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                    </svg>
                </a>
            </div>
        </div>
    </section>

    {{-- STATS --}}
    <section class="bg-apple-bg border-y border-apple-gray-light/30">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 py-8 sm:py-10">
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-8 text-center">
                <div class="reveal">
                    <p class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-1" data-count-to="{{ $stats['figures'] }}" data-count-suffix="+">0</p>
                    <p class="text-xs sm:text-sm text-apple-gray">Nhân vật truyền cảm hứng</p>
                </div>
                <div class="reveal reveal-delay-1">
                    <p class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-1" data-count-to="{{ $stats['categories'] }}">0</p>
                    <p class="text-xs sm:text-sm text-apple-gray">Lĩnh vực đa dạng</p>
                </div>
                <div class="reveal reveal-delay-2">
                    <p class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-1" data-count-to="{{ $stats['stories'] }}" data-count-suffix="+">0</p>
                    <p class="text-xs sm:text-sm text-apple-gray">Mẩu chuyện thú vị</p>
                </div>
                <div class="reveal reveal-delay-3">
                    <p class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-1">100%</p>
                    <p class="text-xs sm:text-sm text-apple-gray">Miễn phí, không quảng cáo</p>
                </div>
            </div>
        </div>
    </section>

    {{-- CATEGORY PILLS --}}
    <section class="bg-apple-white py-6 sm:py-8">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 reveal">
            <x-client.shared.category-pills :categories="$categories" />
        </div>
    </section>

    {{-- FEATURED FIGURE --}}
    @if($featuredFigure)
    <section id="featured" class="bg-apple-bg py-5">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6 reveal">
            <a href="{{ route('client.figures.show', $featuredFigure->slug) }}"
               class="group block bg-white rounded-2xl lg:rounded-[28px] overflow-hidden card-hover cursor-pointer">
                <div class="grid grid-cols-1 lg:grid-cols-2">
                    <div class="relative aspect-[4/3] lg:aspect-[4/5] overflow-hidden">
                        <img src="{{ $featuredFigure->avatar_path ? asset('storage/' . $featuredFigure->avatar_path) : 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=800&h=1000&fit=crop' }}"
                             alt="{{ $featuredFigure->name }}"
                             class="img-zoom w-full h-full object-cover" loading="lazy" />
                    </div>
                    <div class="p-7 sm:p-10 lg:p-12 flex flex-col justify-center">
                        <p class="text-apple-blue text-xs font-semibold uppercase tracking-wider mb-3">Nhân vật tiêu biểu</p>
                        <h2 class="text-2xl sm:text-3xl lg:text-[34px] font-bold text-apple-black tracking-apple-headline leading-tight mb-4">
                            {{ $featuredFigure->name }}
                        </h2>
                        <p class="text-apple-gray text-base sm:text-[17px] leading-relaxed mb-7 tracking-apple-tight">
                            {{ $featuredFigure->short_description }}
                        </p>
                        @include('client.home._media-badges', ['figure' => $featuredFigure])
                        <div class="mt-7">
                            <span class="text-apple-blue text-sm font-normal inline-flex items-center group-hover:underline">
                                Đọc hồ sơ
                                <svg class="w-3.5 h-3.5 ml-1 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                                </svg>
                            </span>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </section>
    @endif

    {{-- LATEST FIGURES --}}
    @if($latestFigures->isNotEmpty())
    <section class="bg-apple-bg py-5">
        <div class="max-w-[980px] mx-auto px-4 sm:px-6">
            <div class="flex items-end justify-between mb-5 reveal">
                <h2 class="text-2xl sm:text-3xl font-bold text-apple-black tracking-apple-headline">Mới nhất</h2>
                <a href="{{ route('client.categories.index') }}"
                   class="inline-flex items-center text-apple-blue text-sm font-normal hover:underline cursor-pointer group">
                    Xem tất cả
                    <svg class="w-3.5 h-3.5 ml-0.5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                    </svg>
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-5">
                @foreach($latestFigures as $index => $figure)
                    <div class="reveal reveal-delay-{{ min($index + 1, 3) }}">
                        <x-client.shared.figure-card :figure="$figure" />
                    </div>
                @endforeach
            </div>
            <div class="mt-8 text-center reveal">
                <a href="{{ route('client.categories.index') }}"
                   class="inline-flex items-center gap-2 px-6 py-2.5 bg-apple-bg hover:bg-apple-gray-light/60 text-apple-black text-sm font-medium rounded-full transition-all duration-300 border border-apple-gray-light/50 cursor-pointer">
                    Xem tất cả nhân vật
                    <svg class="w-3.5 h-3.5 transition-transform duration-300 group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
                    </svg>
                </a>
            </div>
        </div>
    </section>
    @endif

    @include('client.home._quote-section')
    @include('client.home._how-it-works')
    @include('client.home._newsletter')

</x-client.layout.app>
