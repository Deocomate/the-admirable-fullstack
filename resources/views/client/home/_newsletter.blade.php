{{-- Newsletter CTA section --}}
<section class="bg-apple-bg py-16 sm:py-20 border-t border-apple-gray-light/30">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6 text-center">
        <div class="max-w-xl mx-auto">
            <div class="w-12 h-12 rounded-2xl bg-apple-blue/10 flex items-center justify-center mx-auto mb-5 reveal">
                <svg class="w-6 h-6 text-apple-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
            </div>
            <h2 class="text-2xl sm:text-3xl font-bold text-apple-black tracking-apple-headline mb-3 reveal reveal-delay-1">
                Đừng bỏ lỡ bài viết mới.
            </h2>
            <p class="text-apple-gray text-base sm:text-[17px] leading-relaxed mb-7 tracking-apple-tight reveal reveal-delay-2">
                Nhận thông báo mỗi khi có câu chuyện truyền cảm hứng mới được đăng tải. Không spam, chỉ giá trị.
            </p>
            <form class="flex flex-col sm:flex-row gap-3 max-w-md mx-auto reveal reveal-delay-3" onsubmit="event.preventDefault();">
                <input type="email"
                       class="flex-1 px-5 py-3 bg-white rounded-full text-[15px] text-apple-black placeholder-apple-gray border border-apple-gray-light/50 focus:border-apple-blue/40 focus:ring-4 focus:ring-apple-blue/10 transition-all duration-300 outline-none shadow-sm"
                       placeholder="Email của bạn" required />
                <button type="submit"
                        class="px-7 py-3 bg-apple-blue hover:bg-apple-blue-hover text-white text-sm font-medium rounded-full transition-all duration-300 cursor-pointer shadow-sm whitespace-nowrap hover:shadow-lg hover:shadow-apple-blue/20 active:scale-[0.97]">
                    Đăng ký
                </button>
            </form>
            <p class="text-apple-gray/60 text-[11px] mt-4 reveal reveal-delay-4">Bạn có thể hủy đăng ký bất cứ lúc nào. Chúng tôi tôn trọng quyền riêng tư của bạn.</p>
        </div>
    </div>
</section>
