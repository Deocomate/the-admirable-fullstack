{{-- components.admin.layout.sidebar --}}
<aside class="fixed inset-y-0 left-0 z-40 w-64 flex flex-col bg-[#0f0f13]">

    {{-- Brand --}}
    <div class="flex items-center gap-3 px-5 py-5 border-b border-white/[0.06]">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center bg-gradient-to-br from-[#A31D1D] to-[#d94444] shadow-lg shadow-red-900/30">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
            </svg>
        </div>
        <div class="min-w-0">
            <span class="text-white font-bold text-[15px] tracking-tight block leading-tight">The Admirable</span>
            <span class="text-gray-500 text-[10px] font-medium uppercase tracking-widest">Admin Panel</span>
        </div>
    </div>

    {{-- Navigation --}}
    <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">

        {{-- Dashboard --}}
        @php $isDashboard = request()->routeIs('admin.dashboard'); @endphp
        <a href="{{ route('admin.dashboard') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isDashboard ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isDashboard ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 5a1 1 0 011-1h4a1 1 0 011 1v5a1 1 0 01-1 1H5a1 1 0 01-1-1V5zm10 0a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 15a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H5a1 1 0 01-1-1v-4zm10-2a1 1 0 011-1h4a1 1 0 011 1v6a1 1 0 01-1 1h-4a1 1 0 01-1-1v-6z"/>
            </svg>
            Tổng quan
        </a>

        {{-- Superadmin section --}}
        @if(auth()->user()?->isSuperAdmin())
        <div class="pt-4 pb-1">
            <p class="px-3 text-[10px] font-semibold uppercase tracking-[0.15em] text-gray-600">
                Hệ thống
            </p>
        </div>

        @php $isUsers = request()->routeIs('admin.users.*'); @endphp
        <a href="{{ route('admin.users.index') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isUsers ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isUsers ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            Quản trị viên
        </a>
        @endif

        {{-- Content Management --}}
        <div class="pt-4 pb-1">
            <p class="px-3 text-[10px] font-semibold uppercase tracking-[0.15em] text-gray-600">
                Nội dung
            </p>
        </div>

        @php $isCategories = request()->routeIs('admin.categories.*'); @endphp
        <a href="{{ route('admin.categories.index') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isCategories ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isCategories ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
            </svg>
            Lĩnh vực
        </a>

        @php $isFigures = request()->routeIs('admin.figures.*'); @endphp
        <a href="{{ route('admin.figures.index') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isFigures ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isFigures ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Nhân vật
        </a>

        @php $isStories = request()->routeIs('admin.stories.*'); @endphp
        <a href="{{ route('admin.stories.index') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isStories ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isStories ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            Mẩu chuyện
        </a>

        {{-- Settings --}}
        <div class="pt-4 pb-1">
            <p class="px-3 text-[10px] font-semibold uppercase tracking-[0.15em] text-gray-600">
                Cài đặt
            </p>
        </div>

        @php $isContacts = request()->routeIs('admin.contacts.*'); @endphp
        <a href="{{ route('admin.contacts.index') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isContacts ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isContacts ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Liên hệ
        </a>

        @php $isAboutUs = request()->routeIs('admin.settings.*'); @endphp
        <a href="{{ route('admin.settings.about-us') }}"
           class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200
               {{ $isAboutUs ? 'text-white bg-white/[0.08]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]' }}">
            <svg class="w-[18px] h-[18px] flex-shrink-0 {{ $isAboutUs ? 'text-[#A31D1D]' : '' }}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            Về chúng tôi
        </a>

    </nav>

    {{-- User info + Logout --}}
    <div class="px-3 py-4 border-t border-white/[0.06]">
        <div class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-white/[0.04] mb-2">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold flex-shrink-0 bg-gradient-to-br from-[#A31D1D] to-[#d94444]">
                {{ strtoupper(substr(auth()->user()?->name ?? 'A', 0, 1)) }}
            </div>
            <div class="min-w-0 flex-1">
                <p class="text-white text-[13px] font-medium truncate">{{ auth()->user()?->name }}</p>
                <p class="text-gray-500 text-[11px] truncate capitalize">{{ auth()->user()?->role }}</p>
            </div>
        </div>
        <form method="POST" action="{{ route('admin.auth.logout') }}">
            @csrf
            <button type="submit"
                    class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-[13px] text-gray-500 hover:text-gray-300 hover:bg-white/[0.04] transition-all duration-200">
                <svg class="w-[18px] h-[18px] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                </svg>
                Đăng xuất
            </button>
        </form>
    </div>
</aside>
