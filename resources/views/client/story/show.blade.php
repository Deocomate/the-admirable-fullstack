@php
    $figure = $snippet->figure;
    $firstCategory = $figure->categories->first();
    $storyDescription = Str::limit(strip_tags($snippet->content ?? $snippet->subtitle ?? ''), 160);
    $storyTags = $figure->categories->pluck('name')->push($figure->name)->values()->all();
@endphp

<x-client.layout.app :title="$snippet->title . ' — The Admirable'"
                      :description="$storyDescription"
                      :canonicalUrl="route('client.stories.show', $snippet->id)"
                      ogType="article"
                      :ogImage="$snippet->image_path ? asset('storage/' . $snippet->image_path) : ($figure->avatar_path ? asset('storage/' . $figure->avatar_path) : asset('assets/images/logo.png'))"
                      :publishedTime="$snippet->created_at?->toIso8601String()"
                      :modifiedTime="$snippet->updated_at?->toIso8601String()"
                      :articleSection="$firstCategory?->name"
                      :articleTags="$storyTags"
                      :keywords="$snippet->title . ', ' . $figure->name . ', The Admirable'">

    <main class="max-w-[800px] mx-auto px-4 sm:px-6 pt-10 sm:pt-16 pb-20">

        {{-- Breadcrumb --}}
        <nav class="mb-6 flex items-center gap-2 text-xs text-apple-gray flex-wrap animate-fade-in-up" aria-label="Breadcrumb">
            <a href="{{ route('client.home') }}" class="hover:text-apple-black transition-colors cursor-pointer">Trang chủ</a>
            <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            @if($firstCategory)
                <a href="{{ route('client.categories.show', $firstCategory->slug) }}" class="hover:text-apple-black transition-colors cursor-pointer">{{ $firstCategory->name }}</a>
                <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            @endif
            <a href="{{ route('client.figures.show', $figure->slug) }}" class="hover:text-apple-black transition-colors cursor-pointer">{{ $figure->name }}</a>
            <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            <span class="text-apple-black font-medium truncate">{{ $snippet->title }}</span>
        </nav>

        {{-- Back to figure --}}
        <a href="{{ route('client.figures.show', $figure->slug) }}"
           class="inline-flex items-center gap-2 text-apple-blue text-sm font-medium hover:underline mb-6 transition-colors animate-fade-in-up animate-delay-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Quay lại {{ $figure->name }}
        </a>

        {{-- Badge --}}
        <div class="mb-4 animate-fade-in-up animate-delay-1">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-apple-black/5 text-apple-gray rounded-full text-[11px] font-semibold uppercase tracking-wider">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Mảnh ghép câu chuyện
            </span>
        </div>

        {{-- Title --}}
        <h1 class="text-3xl sm:text-4xl lg:text-[44px] font-bold text-apple-black tracking-apple-headline leading-[1.1] mb-4 animate-fade-in-up animate-delay-2">
            {{ $snippet->title }}
        </h1>

        {{-- Subtitle --}}
        @if($snippet->subtitle)
            <p class="text-apple-gray text-lg sm:text-[21px] leading-relaxed mb-10 tracking-apple-tight animate-fade-in-up animate-delay-3">
                {{ $snippet->subtitle }}
            </p>
        @endif

        {{-- Audio player --}}
        <div class="reveal">
            <x-client.shared.audio-player :audioPath="$snippet->audio_path" variant="black" />
        </div>

        {{-- Cover image --}}
        @if($snippet->image_path)
            <div class="w-full rounded-[24px] overflow-hidden mb-10 relative bg-apple-bg reveal">
                <img src="{{ asset('storage/' . $snippet->image_path) }}" alt="{{ $snippet->title }}"
                     class="w-full h-auto object-contain" loading="lazy" />
            </div>
        @endif

        {{-- YouTube embed --}}
        @if($snippet->youtube_url)
            @php
                preg_match('/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))([a-zA-Z0-9_-]{11})/', $snippet->youtube_url, $matches);
                $videoId = $matches[1] ?? null;
            @endphp
            @if($videoId)
                <div class="w-full aspect-video rounded-[24px] overflow-hidden mb-12 shadow-sm bg-black reveal">
                    <iframe class="w-full h-full" src="https://www.youtube.com/embed/{{ $videoId }}?rel=0"
                            title="{{ $snippet->title }} Video" frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>
                </div>
            @endif
        @endif

        {{-- Content blocks --}}
        <div class="reveal">
            <x-client.shared.content-blocks :contentBlocks="$snippet->content_blocks ?? []" />
        </div>

        {{-- Share --}}
        <div class="reveal">
            <x-client.shared.share-buttons
                :shareUrl="route('client.stories.show', $snippet->id)"
                :shareTitle="$snippet->title"
                label="Chia sẻ mẩu chuyện" />
        </div>
    </main>

    {{-- Other Stories --}}
    @if($otherStories->isNotEmpty())
        @include('client.story._other-stories-section')
    @endif

</x-client.layout.app>
