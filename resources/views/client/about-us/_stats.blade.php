{{-- Stats Section --}}
<section class="bg-apple-white border-b border-apple-gray-light/30">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6 py-10">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            @foreach($aboutUs['stats'] as $index => $stat)
                @if(!empty($stat['value']) || !empty($stat['label']))
                    <div class="reveal reveal-delay-{{ min($index + 1, 4) }}">
                        <p class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-display">{{ $stat['value'] }}</p>
                        <p class="text-xs text-apple-gray mt-1">{{ $stat['label'] }}</p>
                    </div>
                @endif
            @endforeach
        </div>
    </div>
</section>
