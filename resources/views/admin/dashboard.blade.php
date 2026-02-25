<x-admin.layout.app title="Dashboard" breadcrumb="Tổng quan hệ thống">

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">

        {{-- Welcome card --}}
        <div class="col-span-full bg-white rounded-lg border border-gray-200 p-6 flex items-center gap-5 shadow-sm">
            <div class="w-12 h-12 rounded flex items-center justify-center flex-shrink-0"
                 style="background:#A31D1D;">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
            </div>
            <div>
                <p class="text-xs text-gray-400 font-medium uppercase tracking-wide">Chào mừng</p>
                <p class="text-gray-800 font-semibold text-base mt-0.5">
                    {{ auth()->user()->name }}
                </p>
                <p class="text-xs text-gray-400 mt-0.5 capitalize">
                    {{ auth()->user()->role }} — Đăng nhập lần cuối: {{ now()->format('d/m/Y H:i') }}
                </p>
            </div>
        </div>

        {{-- Stat: Total Admins (superadmin only) --}}
        @if(auth()->user()->isSuperAdmin())
        <div class="bg-white rounded-lg border border-gray-200 p-5 shadow-sm">
            <div class="flex items-center justify-between mb-3">
                <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Tài khoản Admin</p>
                <div class="w-8 h-8 rounded flex items-center justify-center" style="background:#FEF2F2;">
                    <svg class="w-4 h-4" style="color:#A31D1D;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                    </svg>
                </div>
            </div>
            <p class="text-2xl font-bold text-gray-800">
                {{ \App\Models\User::allAdmins()->count() }}
            </p>
            <a href="{{ route('admin.users.index') }}"
               class="inline-flex items-center gap-1 text-xs mt-2 transition-colors duration-150"
               style="color:#A31D1D;">
                Xem danh sách
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </a>
        </div>
        @endif

        {{-- Stat: Categories --}}
        <div class="bg-white rounded-lg border border-gray-200 p-5 shadow-sm">
            <div class="flex items-center justify-between mb-3">
                <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Lĩnh vực</p>
                <div class="w-8 h-8 rounded flex items-center justify-center" style="background:#EFF6FF;">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                    </svg>
                </div>
            </div>
            <p class="text-2xl font-bold text-gray-800">
                {{ \App\Models\Category::count() }}
            </p>
            <a href="{{ route('admin.categories.index') }}"
               class="inline-flex items-center gap-1 text-xs mt-2 transition-colors duration-150"
               style="color:#A31D1D;">
                Xem danh sách
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </a>
        </div>

        {{-- Stat: Figures --}}
        <div class="bg-white rounded-lg border border-gray-200 p-5 shadow-sm">
            <div class="flex items-center justify-between mb-3">
                <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Nhân vật</p>
                <div class="w-8 h-8 rounded flex items-center justify-center" style="background:#F0FDF4;">
                    <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                </div>
            </div>
            <p class="text-2xl font-bold text-gray-800">
                {{ \App\Models\Figure::count() }}
            </p>
            <a href="{{ route('admin.figures.index') }}"
               class="inline-flex items-center gap-1 text-xs mt-2 transition-colors duration-150"
               style="color:#A31D1D;">
                Xem danh sách
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </a>
        </div>

        {{-- Stat: Story Snippets --}}
        <div class="bg-white rounded-lg border border-gray-200 p-5 shadow-sm">
            <div class="flex items-center justify-between mb-3">
                <p class="text-xs font-medium text-gray-500 uppercase tracking-wide">Mẩu chuyện</p>
                <div class="w-8 h-8 rounded flex items-center justify-center" style="background:#FFF7ED;">
                    <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
                    </svg>
                </div>
            </div>
            <p class="text-2xl font-bold text-gray-800">
                {{ \App\Models\StorySnippet::count() }}
            </p>
            <a href="{{ route('admin.stories.index') }}"
               class="inline-flex items-center gap-1 text-xs mt-2 transition-colors duration-150"
               style="color:#A31D1D;">
                Xem danh sách
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </a>
        </div>

    </div>

</x-admin.layout.app>
