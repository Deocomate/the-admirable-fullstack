{{-- Audience Section --}}
@php
    $audience = $aboutUs['audience'] ?? [];
@endphp

<section class="bg-white py-16 sm:py-24">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6 text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-4 reveal">
            {{ $audience['title'] ?: 'Nền tảng này dành cho ai?' }}
        </h2>
        <p class="text-apple-gray text-lg sm:text-[19px] leading-relaxed max-w-2xl mx-auto mb-12 reveal reveal-delay-1">
            {{ $audience['description'] ?: 'Không cần tạo tài khoản rườm rà. Hệ thống được mở hoàn toàn công khai để mang tri thức đến với tất cả mọi người.' }}
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 lg:gap-8">
            @foreach(($audience['items'] ?? []) as $index => $item)
                @if(!empty($item['title']))
                    <div class="p-6 bg-apple-bg rounded-[24px] reveal reveal-delay-{{ min($index + 1, 3) }} transition-transform duration-500 hover:scale-[1.03]">
                        <h3 class="text-lg font-semibold text-apple-black mb-2">{{ $item['title'] }}</h3>
                        <p class="text-apple-gray text-sm leading-relaxed">{{ $item['description'] }}</p>
                    </div>
                @endif
            @endforeach
        </div>
    </div>
</section>
