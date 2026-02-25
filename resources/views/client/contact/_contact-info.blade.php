{{-- Contact Info Section --}}
<section class="bg-apple-bg py-16 sm:py-24">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6">
        <div class="text-center mb-12 reveal">
            <h2 class="text-3xl sm:text-4xl font-bold text-apple-black tracking-apple-headline mb-4">Thông tin liên hệ</h2>
            <p class="text-apple-gray text-base sm:text-lg leading-relaxed max-w-xl mx-auto">
                Chọn cách liên hệ phù hợp nhất với bạn.
            </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            @forelse($contacts as $index => $contact)
                <div class="bg-white p-6 sm:p-8 rounded-[20px] shadow-sm text-center reveal reveal-delay-{{ min($index + 1, 4) }}">
                    {{-- Icon --}}
                    <div class="w-12 h-12 rounded-2xl bg-apple-blue/10 flex items-center justify-center mx-auto mb-5">
                        @if($contact->type === 'email')
                            <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        @elseif($contact->type === 'phone')
                            <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                            </svg>
                        @elseif($contact->type === 'social')
                            <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                            </svg>
                        @else
                            <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                        @endif
                    </div>

                    <h3 class="text-base font-semibold text-apple-black mb-2">{{ $contact->label }}</h3>

                    @if($contact->type === 'email')
                        <a href="mailto:{{ $contact->value }}" class="text-sm text-apple-blue hover:underline transition-colors duration-300">{{ $contact->value }}</a>
                    @elseif($contact->type === 'phone')
                        <a href="tel:{{ $contact->value }}" class="text-sm text-apple-blue hover:underline transition-colors duration-300">{{ $contact->value }}</a>
                    @elseif($contact->type === 'link' || $contact->type === 'social')
                        <a href="{{ $contact->value }}" target="_blank" rel="noopener" class="text-sm text-apple-blue hover:underline transition-colors duration-300">{{ $contact->value }}</a>
                    @else
                        <p class="text-sm text-apple-gray">{{ $contact->value }}</p>
                    @endif
                </div>
            @empty
                {{-- Fallback khi chưa có thông tin liên hệ --}}
                <div class="bg-white p-6 sm:p-8 rounded-[20px] shadow-sm text-center reveal">
                    <div class="w-12 h-12 rounded-2xl bg-apple-blue/10 flex items-center justify-center mx-auto mb-5">
                        <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    </div>
                    <h3 class="text-base font-semibold text-apple-black mb-2">Email</h3>
                    <a href="mailto:contact@theadmirable.com" class="text-sm text-apple-blue hover:underline transition-colors duration-300">contact@theadmirable.com</a>
                </div>
            @endforelse
        </div>
    </div>
</section>
