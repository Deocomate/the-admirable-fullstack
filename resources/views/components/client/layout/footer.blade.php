@php
    $categories = \App\Models\Category::orderBy('name')->get();
    $contacts = \App\Models\Contact::active()->orderBy('sort_order')->get();
@endphp

<footer class="bg-apple-white border-t border-apple-gray-light/50">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6">
        {{-- Main footer content --}}
        <div class="py-10 sm:py-12">
            {{-- Brand + description --}}
            <div class="mb-8 sm:mb-10 reveal">
                <h2 class="text-[21px] font-semibold text-apple-black tracking-apple-tight mb-2">The Admirable</h2>
                <p class="text-sm text-apple-gray leading-relaxed max-w-md">
                    Khám phá cuộc đời và di sản của những nhân vật vĩ đại. Truyền cảm hứng qua những câu chuyện đáng ngưỡng mộ.
                </p>
            </div>

            {{-- Links grid --}}
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-6 sm:gap-8 pb-8 border-b border-apple-gray-light/50 reveal">
                <div>
                    <h3 class="text-xs font-semibold text-apple-black mb-3">Khám phá</h3>
                    <ul class="space-y-2">
                        <li><a href="{{ route('client.home') }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">Trang chủ</a></li>
                        <li><a href="{{ route('client.categories.index') }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">Lĩnh vực</a></li>
                        <li><a href="{{ route('client.search') }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">Tìm kiếm</a></li>
                        <li><a href="{{ route('client.about-us') }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">Giới thiệu</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-xs font-semibold text-apple-black mb-3">Lĩnh vực</h3>
                    <ul class="space-y-2">
                        @foreach($categories->take(5) as $cat)
                            <li><a href="{{ route('client.categories.show', $cat->slug) }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">{{ $cat->name }}</a></li>
                        @endforeach
                    </ul>
                </div>
                <div>
                    <h3 class="text-xs font-semibold text-apple-black mb-3">Thêm nữa</h3>
                    <ul class="space-y-2">
                        @foreach($categories->skip(5)->take(5) as $cat)
                            <li><a href="{{ route('client.categories.show', $cat->slug) }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">{{ $cat->name }}</a></li>
                        @endforeach
                    </ul>
                </div>
                <div>
                    <h3 class="text-xs font-semibold text-apple-black mb-3">Liên hệ</h3>
                    <ul class="space-y-2">
                        @foreach($contacts as $contact)
                            @if($contact->type === 'email')
                                <li><a href="mailto:{{ $contact->value }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">{{ $contact->value }}</a></li>
                            @elseif($contact->type === 'phone')
                                <li><a href="tel:{{ $contact->value }}" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">{{ $contact->value }}</a></li>
                            @elseif($contact->type === 'link' || $contact->type === 'social')
                                <li><a href="{{ $contact->value }}" target="_blank" rel="noopener" class="text-xs text-apple-gray hover:text-apple-black transition-colors duration-300 cursor-pointer">{{ $contact->label }}</a></li>
                            @else
                                <li class="text-xs text-apple-gray">{{ $contact->label }}: {{ $contact->value }}</li>
                            @endif
                        @endforeach
                        @if($contacts->isEmpty())
                            <li class="text-xs text-apple-gray">contact@theadmirable.com</li>
                        @endif
                    </ul>
                </div>
            </div>
        </div>

        {{-- Bottom bar --}}
        <div class="pb-6 flex flex-col sm:flex-row items-center justify-between gap-2 reveal">
            <p class="text-apple-gray text-[11px]">Copyright &copy; {{ date('Y') }} The Admirable. All rights reserved.</p>
            <p class="text-apple-gray/60 text-[11px]">Được xây dựng với mục đích giáo dục và truyền cảm hứng.</p>
        </div>
    </div>
</footer>
