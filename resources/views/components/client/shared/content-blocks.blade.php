@props(['contentBlocks' => []])

@php
    // Ensure contentBlocks is always a valid array
    $contentBlocks = is_array($contentBlocks) ? $contentBlocks : [];
@endphp

@if(!empty($contentBlocks))
<article class="prose max-w-none">
    <div class="space-y-0">
        @foreach($contentBlocks as $index => $block)
            @php
                $type = $block['type'] ?? 'paragraph';
                $prevType = ($index > 0) ? ($contentBlocks[$index - 1]['type'] ?? 'paragraph') : null;
                $isFirstBlock = $index === 0;
                $textEn = trim($block['text_en'] ?? '');
            @endphp

            {{-- Skip blocks with no text content --}}
            @if(empty($textEn))
                @continue
            @endif

            @if($type === 'heading')
                {{-- ── Section heading with divider ── --}}
                @if(!$isFirstBlock)
                    <div class="pt-10 pb-2">
                        <hr class="border-t border-gray-200/80">
                    </div>
                @endif
                <h2 class="text-[22px] sm:text-[26px] font-bold text-apple-black tracking-apple-tight pt-2 pb-5 flex items-center gap-3">
                    <span class="w-1 h-6 sm:h-7 bg-apple-blue rounded-full flex-shrink-0"></span>
                    {{ $textEn }}
                </h2>

            @elseif($type === 'paragraph')
                {{-- ── Bilingual paragraph ── --}}
                @if(!$isFirstBlock && $prevType !== 'heading')
                    <div class="py-5">
                        <div class="flex items-center gap-3">
                            <div class="flex-1 border-t border-gray-100"></div>
                            <div class="w-1 h-1 rounded-full bg-gray-200"></div>
                            <div class="flex-1 border-t border-gray-100"></div>
                        </div>
                    </div>
                @endif
                <div class="group pb-1">
                    @if(!empty($block['heading_en']))
                        <h3 class="text-lg sm:text-xl font-bold text-apple-black tracking-apple-tight mb-3">
                            {{ $block['heading_en'] }}
                        </h3>
                    @endif
                    <p class="text-[17px] sm:text-[19px] leading-[1.85] text-apple-black/90 tracking-apple-tight mb-3">
                        {{ $textEn }}
                    </p>
                    @if(!empty(trim($block['text_vi'] ?? '')))
                        <p class="text-[15px] sm:text-[16px] leading-[1.75] text-apple-gray italic border-l-2 border-apple-blue/20 pl-4 mt-3">
                            {{ $block['text_vi'] }}
                        </p>
                    @endif
                </div>

            @elseif($type === 'quote')
                {{-- ── Quote block ── --}}
                <div class="py-6">
                    <blockquote class="pl-6 border-l-4 border-apple-blue bg-apple-bg rounded-r-2xl py-6 pr-6">
                        <p class="text-xl sm:text-2xl font-semibold text-apple-black leading-snug mb-3">
                            "{{ $textEn }}"
                        </p>
                        @if(!empty(trim($block['author'] ?? '')))
                            <footer class="text-sm font-medium text-apple-gray uppercase tracking-wider">— {{ $block['author'] }}</footer>
                        @endif
                    </blockquote>
                </div>

            @elseif($type === 'bilingual')
                {{-- ── Backward compatibility with old format ── --}}
                @if(!$isFirstBlock && $prevType !== 'heading')
                    <div class="py-5">
                        <div class="flex items-center gap-3">
                            <div class="flex-1 border-t border-gray-100"></div>
                            <div class="w-1 h-1 rounded-full bg-gray-200"></div>
                            <div class="flex-1 border-t border-gray-100"></div>
                        </div>
                    </div>
                @endif
                <div class="group pb-1">
                    @if(!empty($block['heading']))
                        <h3 class="text-lg sm:text-xl font-bold text-apple-black tracking-apple-tight mb-3">
                            {{ $block['heading'] }}
                        </h3>
                    @endif
                    <p class="text-[17px] sm:text-[19px] leading-[1.85] text-apple-black/90 tracking-apple-tight mb-3">
                        {{ $block['en'] ?? $textEn }}
                    </p>
                    @if(!empty(trim($block['vi'] ?? '')))
                        <p class="text-[15px] sm:text-[16px] leading-[1.75] text-apple-gray italic border-l-2 border-apple-blue/20 pl-4 mt-3">
                            {{ $block['vi'] }}
                        </p>
                    @endif
                </div>
            @endif
        @endforeach
    </div>
</article>
@endif
