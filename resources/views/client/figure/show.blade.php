@php
    $firstCategory = $figure->categories->first();
    $articleTags = $figure->categories->pluck('name')->values()->all();
@endphp

<x-client.layout.app :title="$figure->name . ' — The Admirable'"
                      :description="$figure->short_description"
                      :canonicalUrl="route('client.figures.show', $figure->slug)"
                      ogType="article"
                      :ogImage="$figure->avatar_path ? asset('storage/' . $figure->avatar_path) : asset('assets/images/logo.png')"
                      :publishedTime="$figure->created_at?->toIso8601String()"
                      :modifiedTime="$figure->updated_at?->toIso8601String()"
                      :articleSection="$firstCategory?->name"
                      :articleTags="$articleTags"
                      :keywords="$figure->name . ', nhân vật truyền cảm hứng, The Admirable'">

    @push('after-navbar')
        {{-- Reading progress bar --}}
        <div id="reading-progress" class="fixed top-12 left-0 h-0.5 bg-apple-blue z-[60]" style="width: 0%;"></div>
    @endpush

    <main class="max-w-[800px] mx-auto px-4 sm:px-6 pt-10 sm:pt-16 pb-20">

        {{-- Breadcrumb --}}
        <nav class="mb-6 flex items-center gap-2 text-xs text-apple-gray animate-fade-in-up" aria-label="Breadcrumb">
            <a href="{{ route('client.home') }}" class="hover:text-apple-black transition-colors cursor-pointer">Trang chủ</a>
            <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            @if($firstCategory)
                <a href="{{ route('client.categories.show', $firstCategory->slug) }}" class="hover:text-apple-black transition-colors cursor-pointer">{{ $firstCategory->name }}</a>
                <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            @endif
            <span class="text-apple-black font-medium truncate">{{ $figure->name }}</span>
        </nav>

        {{-- Category tags --}}
        <div class="mb-4 flex flex-wrap gap-2 animate-fade-in-up animate-delay-1">
            @foreach($figure->categories as $cat)
                <a href="{{ route('client.categories.show', $cat->slug) }}"
                   class="inline-flex items-center px-3 py-1 bg-apple-bg text-apple-gray hover:text-apple-black rounded-full text-[11px] font-semibold uppercase tracking-wider transition-all duration-300 hover:bg-apple-gray-light/60">
                    {{ $cat->name }}
                </a>
            @endforeach
        </div>

        {{-- Title & description --}}
        <h1 class="text-3xl sm:text-4xl lg:text-[44px] font-bold text-apple-black tracking-apple-headline leading-[1.1] mb-5 animate-fade-in-up animate-delay-2">
            {{ $figure->name }}
        </h1>
        <p class="text-apple-gray text-lg sm:text-[21px] leading-relaxed mb-10 tracking-apple-tight animate-fade-in-up animate-delay-3">
            {{ $figure->short_description }}
        </p>

        {{-- Key facts --}}
        @if(!empty($figure->key_facts))
            <div class="reveal">
                @include('client.figure._key-facts', ['keyFacts' => $figure->key_facts])
            </div>
        @endif

        {{-- Audio player --}}
        <div class="reveal">
            <x-client.shared.audio-player :audioPath="$figure->audio_path" variant="blue" />
        </div>

        {{-- Cover image --}}
        @if($figure->avatar_path)
            <div class="w-full rounded-[24px] overflow-hidden mb-10 relative bg-apple-bg reveal">
                <img src="{{ asset('storage/' . $figure->avatar_path) }}" alt="{{ $figure->name }} Cover"
                     class="w-full h-auto object-contain" loading="lazy" />
            </div>
        @endif

        {{-- YouTube embed --}}
        @if($figure->youtube_url)
            @php
                preg_match('/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))([a-zA-Z0-9_-]{11})/', $figure->youtube_url, $matches);
                $videoId = $matches[1] ?? null;
            @endphp
            @if($videoId)
                <div class="w-full aspect-video rounded-[24px] overflow-hidden mb-12 shadow-sm bg-black reveal">
                    <iframe class="w-full h-full" src="https://www.youtube.com/embed/{{ $videoId }}?rel=0"
                            title="{{ $figure->name }} Video" frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>
                </div>
            @endif
        @endif

        {{-- Content blocks --}}
        <div class="reveal">
            <x-client.shared.content-blocks :contentBlocks="$figure->content_blocks ?? []" />
        </div>

        {{-- Share --}}
        <div class="reveal">
            <x-client.shared.share-buttons
                :shareUrl="route('client.figures.show', $figure->slug)"
                :shareTitle="$figure->name"
                label="Chia sẻ bài viết" />
        </div>
    </main>

    {{-- Story Snippets --}}
    @if($figure->storySnippets->isNotEmpty())
        @include('client.figure._story-snippets-section')
    @endif

    {{-- Related Figures --}}
    @if($relatedFigures->isNotEmpty())
        @include('client.figure._related-figures-section')
    @endif

</x-client.layout.app>
