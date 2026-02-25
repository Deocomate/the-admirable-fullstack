{{-- Problem & Solution Section --}}
<section class="bg-apple-bg py-16 sm:py-24">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 lg:gap-20 items-center">
            {{-- Problem card --}}
            <div class="bg-white p-8 sm:p-10 rounded-[24px] lg:rounded-[32px] shadow-sm reveal">
                <div class="w-12 h-12 rounded-2xl bg-red-50 flex items-center justify-center mb-6">
                    <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
                <h2 class="text-2xl font-bold text-apple-black tracking-apple-headline mb-4">
                    {{ $aboutUs['problem']['title'] ?: 'Nỗi trăn trở của người học' }}
                </h2>
                <p class="text-apple-gray text-[17px] leading-relaxed">
                    {{ $aboutUs['problem']['description'] ?: 'Chúng tôi thấu hiểu rằng việc học IELTS hay nâng cao vốn tiếng Anh thường đi kèm với những bài báo học thuật khô khan, phức tạp. Người học rất dễ cảm thấy chán nản, buồn ngủ và gặp khó khăn trong việc ghi nhớ từ vựng cũng như duy trì động lực mỗi ngày.' }}
                </p>
            </div>

            {{-- Solution --}}
            <div class="reveal reveal-delay-2">
                <h2 class="text-3xl font-bold text-apple-black tracking-apple-headline mb-6">
                    {{ $aboutUs['solution']['title'] ?: 'Giải pháp mang tên "The Admirable"' }}
                </h2>
                <p class="text-apple-gray text-[17px] leading-relaxed mb-6">
                    {{ $aboutUs['solution']['description'] ?: 'Thay vì ép bản thân đọc những nội dung vô hồn, chúng tôi cung cấp các bài viết song ngữ chất lượng cao kể về những tấm gương vĩ đại trên toàn thế giới—từ văn hóa, kinh tế, khoa học đến chính trị.' }}
                </p>
                @php
                    $bullets = $aboutUs['solution']['bullets'] ?? [];
                    $defaultBullets = [
                        'Nội dung truyền cảm hứng, tích cực và sâu sắc.',
                        'Hệ sinh thái đa phương tiện: Text, Audio, Video YouTube.',
                        'Ghi nhớ từ vựng tự nhiên thông qua bối cảnh câu chuyện.',
                    ];
                @endphp
                <ul class="space-y-4">
                    @foreach($bullets as $i => $bullet)
                        @if(!empty($bullet) || !empty($defaultBullets[$i] ?? ''))
                            <li class="flex items-start gap-3">
                                <svg class="w-6 h-6 text-apple-blue flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                <span class="text-apple-black text-[17px]">{{ $bullet ?: ($defaultBullets[$i] ?? '') }}</span>
                            </li>
                        @endif
                    @endforeach
                </ul>
            </div>
        </div>
    </div>
</section>
