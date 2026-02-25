@props(['snippet'])

@php
    $icons = [
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />',
    ];
    $icon = $icons[$snippet->id % count($icons)];
@endphp

<a href="{{ route('client.stories.show', $snippet->id) }}" class="group block bg-white rounded-[24px] p-6 card-hover h-full flex flex-col">
    <div class="w-10 h-10 rounded-full bg-apple-bg flex items-center justify-center mb-4 flex-shrink-0">
        <svg class="w-5 h-5 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {!! $icon !!}
        </svg>
    </div>
    <h3 class="text-[17px] font-semibold text-apple-black mb-2 leading-snug">{{ $snippet->title }}</h3>
    <p class="text-sm text-apple-gray leading-relaxed mb-4 line-clamp-2 flex-1">{{ $snippet->subtitle ?? Str::limit(strip_tags($snippet->content), 100) }}</p>
    <span class="text-apple-blue text-xs font-medium inline-flex items-center group-hover:underline mt-auto">
        Đọc mẩu chuyện
        <svg class="w-3.5 h-3.5 ml-1 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
        </svg>
    </span>
</a>
