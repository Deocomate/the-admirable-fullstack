{{-- Buy Me a Coffee Section --}}
<section class="bg-apple-bg py-16 sm:py-24">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6">
        <div class="bg-white rounded-[24px] lg:rounded-[32px] shadow-sm overflow-hidden">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-0">
                {{-- Left: Info --}}
                <div class="p-8 sm:p-10 lg:p-12 flex flex-col justify-center reveal">
                    <div class="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center mb-6">
                        <svg class="w-6 h-6 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                    </div>
                    <h2 class="text-2xl sm:text-3xl font-bold text-apple-black tracking-apple-headline mb-4">
                        Ủng hộ dự án
                    </h2>
                    <p class="text-apple-gray text-[17px] leading-relaxed mb-6">
                        Nếu bạn thấy The Admirable hữu ích và muốn ủng hộ chúng tôi tiếp tục phát triển nội dung chất lượng, bạn có thể "mua cho chúng tôi một ly cà phê" qua chuyển khoản ngân hàng.
                    </p>
                    <p class="text-apple-gray text-sm leading-relaxed">
                        Mọi đóng góp đều là nguồn động lực to lớn giúp chúng tôi duy trì và mở rộng dự án. Cảm ơn bạn rất nhiều! ☕
                    </p>
                </div>

                {{-- Right: Bank Info --}}
                <div class="bg-apple-bg p-8 sm:p-10 lg:p-12 flex flex-col justify-center reveal reveal-delay-2">
                    <div class="bg-white rounded-[20px] p-6 sm:p-8 shadow-sm">
                        <h3 class="text-lg font-semibold text-apple-black mb-6 text-center">Thông tin chuyển khoản</h3>

                        <div class="space-y-4">
                            <div class="flex items-center justify-between py-3 border-b border-apple-gray-light/30">
                                <span class="text-sm text-apple-gray">Ngân hàng</span>
                                <span class="text-sm font-semibold text-apple-black">MB Bank</span>
                            </div>
                            <div class="flex items-center justify-between py-3 border-b border-apple-gray-light/30">
                                <span class="text-sm text-apple-gray">Số tài khoản</span>
                                <div class="flex items-center gap-2">
                                    <span id="account-number" class="text-sm font-semibold text-apple-black font-mono tracking-wide">0565651189</span>
                                    <button onclick="copyAccountNumber()" class="p-1.5 rounded-lg hover:bg-apple-bg transition-colors duration-300 cursor-pointer group" title="Sao chép số tài khoản">
                                        <svg id="copy-icon" class="w-4 h-4 text-apple-gray group-hover:text-apple-blue transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                        </svg>
                                        <svg id="check-icon" class="w-4 h-4 text-green-500 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <div class="flex items-center justify-between py-3">
                                <span class="text-sm text-apple-gray">Chủ tài khoản</span>
                                <span class="text-sm font-semibold text-apple-black">NGUYEN VU MINH LONG</span>
                            </div>
                        </div>

                        <div class="mt-6 p-4 bg-amber-50 rounded-2xl text-center">
                            <p class="text-xs text-amber-700">
                                Nội dung chuyển khoản: <span class="font-semibold">THE ADMIRABLE UNG HO</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
    function copyAccountNumber() {
        const accountNumber = document.getElementById('account-number').textContent;
        navigator.clipboard.writeText(accountNumber).then(() => {
            const copyIcon = document.getElementById('copy-icon');
            const checkIcon = document.getElementById('check-icon');
            copyIcon.classList.add('hidden');
            checkIcon.classList.remove('hidden');
            setTimeout(() => {
                copyIcon.classList.remove('hidden');
                checkIcon.classList.add('hidden');
            }, 2000);
        });
    }
</script>
