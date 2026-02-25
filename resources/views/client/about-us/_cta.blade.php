{{-- CTA Section --}}
@php
    $cta = $aboutUs['cta'] ?? [];
@endphp

<section class="bg-apple-black py-16 sm:py-20 text-center">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6">
        <p class="text-apple-gray text-sm font-medium mb-4 reveal">
            "{{ $cta['quote'] ?: 'Đọc là để sống nhiều hơn một lần.' }}"
        </p>
        <h2 class="text-3xl sm:text-4xl font-bold text-white tracking-apple-headline mb-6 reveal reveal-delay-1">
            {{ $cta['headline'] ?: 'Sẵn sàng để bắt đầu?' }}
        </h2>
        <p class="text-apple-gray text-base sm:text-lg leading-relaxed max-w-xl mx-auto mb-8 reveal reveal-delay-2">
            {{ $cta['description'] ?: 'Hãy khám phá những câu chuyện đã truyền cảm hứng cho hàng triệu người trên thế giới — hoàn toàn miễn phí.' }}
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 reveal reveal-delay-3">
            <a href="{{ route('client.home') }}"
               class="inline-flex items-center justify-center px-7 py-3 bg-apple-blue hover:bg-apple-blue-hover text-white text-sm font-normal rounded-full transition-all duration-300 cursor-pointer hover:shadow-lg hover:shadow-apple-blue/30 active:scale-[0.97]">
                Khám phá các nhân vật ngay
            </a>
            <a href="{{ route('client.search') }}"
               class="inline-flex items-center justify-center px-7 py-3 bg-white/10 hover:bg-white/20 text-white text-sm font-normal rounded-full transition-all duration-300 cursor-pointer border border-white/20 active:scale-[0.97]">
                Tìm kiếm chủ đề
            </a>
        </div>
    </div>
</section>
