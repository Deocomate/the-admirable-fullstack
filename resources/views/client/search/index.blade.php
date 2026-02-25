@php
    $searchDescription = $query
        ? 'Kết quả tìm kiếm cho "' . $query . '" trên The Admirable.'
        : 'Tìm kiếm nhân vật và câu chuyện song ngữ trên The Admirable.';
@endphp

<x-client.layout.app title="Tìm kiếm — The Admirable"
                      :description="$searchDescription"
                      :canonicalUrl="route('client.search')"
                      robots="noindex,follow"
                      keywords="tìm kiếm nhân vật, câu chuyện song ngữ, The Admirable"
                      activePage="search">

    <main class="max-w-6xl mx-auto px-4 sm:px-6 pt-10 sm:pt-16 pb-20">

        {{-- Hero --}}
        <div class="text-center mb-10 sm:mb-14 max-w-2xl mx-auto">
            <p class="text-apple-blue text-xs font-semibold uppercase tracking-widest mb-3 animate-fade-in-up">Tìm kiếm</p>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-apple-black tracking-apple-headline mb-4 animate-fade-in-up animate-delay-1">
                Khám phá nhân vật
            </h1>
            <p class="text-apple-gray text-base sm:text-lg leading-relaxed tracking-apple-tight animate-fade-in-up animate-delay-2">
                Tìm nhân vật truyền cảm hứng và đọc câu chuyện song ngữ Anh–Việt
            </p>
        </div>

        {{-- Search form --}}
        <div class="animate-fade-in-up animate-delay-3">
            @include('client.search._search-form')
        </div>

        {{-- Category pills --}}
        <div class="mb-10 reveal">
            @include('client.search._category-pills')
        </div>

        {{-- Results (always show when we have figures or a filter is active) --}}
        @include('client.search._results')

        @if(!$query && !$categorySlug)
            {{-- Popular searches & trending --}}
            @include('client.search._popular-trending')
        @endif

    </main>

</x-client.layout.app>
