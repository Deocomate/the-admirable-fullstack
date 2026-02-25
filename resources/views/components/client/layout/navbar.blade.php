@props(['activePage' => ''])

<header id="main-navbar" class="fixed top-0 left-0 right-0 z-50 bg-apple-white/80 backdrop-blur-xl backdrop-saturate-150 border-b border-black/5 transition-all duration-500">
    <nav class="max-w-[980px] mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-12">
            <!-- Logo -->
            <a href="{{ route('client.home') }}" class="flex items-center gap-1.5 cursor-pointer group" aria-label="Trang chủ The Admirable">
                <span class="text-[21px] font-semibold text-apple-black tracking-apple-tight transition-opacity duration-300 group-hover:opacity-70">The Admirable</span>
            </a>

            <!-- Desktop Navigation -->
            <div class="hidden md:flex items-center gap-7">
                @php $navItems = [
                    ['route' => 'client.home', 'label' => 'Trang chủ', 'key' => 'home'],
                    ['route' => 'client.categories.index', 'label' => 'Lĩnh vực', 'key' => 'category'],
                    ['route' => 'client.search', 'label' => 'Tìm kiếm', 'key' => 'search'],
                    ['route' => 'client.about-us', 'label' => 'Về chúng tôi', 'key' => 'about-us'],
                ]; @endphp
                @foreach($navItems as $item)
                    <a href="{{ route($item['route']) }}"
                       class="relative text-xs font-normal {{ $activePage === $item['key'] ? 'text-apple-black' : 'text-apple-gray hover:text-apple-black' }} transition-colors duration-300 cursor-pointer py-1">
                        {{ $item['label'] }}
                        @if($activePage === $item['key'])
                            <span class="absolute -bottom-[1px] left-0 right-0 h-[1.5px] bg-apple-black rounded-full"></span>
                        @endif
                    </a>
                @endforeach
            </div>

            <!-- Search + Mobile -->
            <div class="flex items-center gap-3">
                <a href="{{ route('client.search') }}" class="hidden md:flex p-1 cursor-pointer text-apple-gray hover:text-apple-black transition-colors duration-300" aria-label="Tìm kiếm">
                    <svg class="w-[15px] h-[15px]" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </a>
                <button id="mobile-menu-btn" type="button" class="md:hidden p-1 text-apple-black cursor-pointer" aria-label="Mở menu" aria-expanded="false" aria-controls="mobile-menu">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path id="menu-icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                </button>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden pb-5 pt-2 transition-all duration-300">
            <div class="flex flex-col gap-0 border-t border-black/5 pt-3">
                @foreach($navItems as $item)
                    <a href="{{ route($item['route']) }}" class="py-2.5 text-sm {{ $activePage === $item['key'] ? 'font-medium text-apple-black' : 'text-apple-gray hover:text-apple-black' }} cursor-pointer transition-colors duration-300">{{ $item['label'] }}</a>
                @endforeach
            </div>
        </div>
    </nav>
</header>
