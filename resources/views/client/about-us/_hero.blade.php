{{-- Hero Section --}}
<section class="bg-apple-white overflow-hidden border-b border-apple-gray-light/30">
    <div class="max-w-[980px] mx-auto px-4 sm:px-6 pt-16 pb-12 sm:pt-20 sm:pb-16 lg:pt-28 lg:pb-20 text-center">
        <p class="text-apple-blue text-sm sm:text-base font-semibold tracking-wide mb-3 animate-fade-in-up">
            {{ $aboutUs['hero']['tagline'] ?: 'Câu chuyện của chúng tôi' }}
        </p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-apple-display text-apple-black leading-[1.05] mb-6 animate-fade-in-up animate-delay-1">
            {{ $aboutUs['hero']['headline'] ?: 'Học ngôn ngữ qua' }} <br class="hidden sm:block" />
            <span class="gradient-text" data-typing='["{{ $aboutUs['hero']['headline_gradient'] ?: 'những tầm cao nhân loại.' }}", "những câu chuyện vĩ đại.", "niềm cảm hứng bất tận."]' data-typing-speed="80" data-typing-pause="2200">{{ $aboutUs['hero']['headline_gradient'] ?: 'những tầm cao nhân loại.' }}</span>
        </h1>
        <p class="text-apple-gray text-lg sm:text-[19px] leading-relaxed max-w-2xl mx-auto tracking-apple-tight animate-fade-in-up animate-delay-2">
            {{ $aboutUs['hero']['description'] ?: '"The Admirable" ra đời mang theo một sứ mệnh: Biến quá trình học tiếng Anh đầy gian nan trở thành một hành trình tận hưởng những giá trị tốt đẹp nhất của tri thức.' }}
        </p>
    </div>
</section>
