{{-- Key Facts Card --}}
<div class="bg-apple-bg rounded-[20px] p-6 sm:p-8 mb-10">
    <h3 class="text-sm font-semibold text-apple-gray uppercase tracking-widest mb-4">Thông tin nổi bật</h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
        @foreach($keyFacts as $index => $fact)
            <div class="flex items-start gap-3 reveal" style="transition-delay: {{ $index * 80 }}ms">
                <div class="w-8 h-8 rounded-full bg-apple-blue/10 flex items-center justify-center flex-shrink-0 mt-0.5 transition-transform duration-300 hover:scale-110">
                    <svg class="w-4 h-4 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <div>
                    <p class="text-sm font-semibold text-apple-black mb-0.5">{{ $fact['label'] ?? '' }}</p>
                    <p class="text-sm text-apple-gray">{{ $fact['value'] ?? '' }}</p>
                </div>
            </div>
        @endforeach
    </div>
</div>
