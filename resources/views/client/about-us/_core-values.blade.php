{{-- Core Values Section --}}
@php
    $coreValues = $aboutUs['core_values'] ?? [];
    $valueIcons = [
        ['bg' => 'bg-blue-50', 'text' => 'text-apple-blue', 'path' => 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'],
        ['bg' => 'bg-green-50', 'text' => 'text-green-600', 'path' => 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'],
        ['bg' => 'bg-purple-50', 'text' => 'text-purple-600', 'path' => 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z'],
        ['bg' => 'bg-orange-50', 'text' => 'text-orange-600', 'path' => 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z'],
    ];
@endphp

<section class="bg-white py-16 sm:py-24">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6 text-center">
        <p class="text-apple-blue text-sm font-semibold tracking-wide mb-3 reveal">
            {{ $coreValues['tagline'] ?: 'Giá trị cốt lõi' }}
        </p>
        <h2 class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-12 reveal reveal-delay-1">
            {{ $coreValues['title'] ?: 'Những gì chúng tôi tin tưởng' }}
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            @foreach(($coreValues['items'] ?? []) as $i => $item)
                @if(!empty($item['title']))
                    @php $icon = $valueIcons[$i] ?? $valueIcons[0]; @endphp
                    <div class="p-6 bg-apple-bg rounded-[24px] text-left reveal reveal-delay-{{ min($i + 1, 4) }} transition-transform duration-500 hover:scale-[1.03]">
                        <div class="w-10 h-10 rounded-xl {{ $icon['bg'] }} flex items-center justify-center mb-4">
                            <svg class="w-5 h-5 {{ $icon['text'] }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{{ $icon['path'] }}" />
                            </svg>
                        </div>
                        <h3 class="text-base font-semibold text-apple-black mb-2">{{ $item['title'] }}</h3>
                        <p class="text-sm text-apple-gray leading-relaxed">{{ $item['description'] }}</p>
                    </div>
                @endif
            @endforeach
        </div>
    </div>
</section>
