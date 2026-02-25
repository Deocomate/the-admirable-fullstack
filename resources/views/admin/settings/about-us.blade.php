<x-admin.layout.app title="Về chúng tôi" breadcrumb="Admin › Cài đặt › Về chúng tôi">

    <form method="POST" action="{{ route('admin.settings.about-us.submit') }}">
        @csrf

        {{-- Header with save button --}}
        <div class="flex items-center justify-between mb-6">
            <div>
                <h1 class="text-lg font-bold text-gray-800">Quản lý trang "Về chúng tôi"</h1>
                <p class="text-xs text-gray-400 mt-0.5">Chỉnh sửa nội dung từng section trên trang About Us.</p>
            </div>
            <button type="submit"
                    class="px-5 py-2.5 text-sm font-semibold text-white rounded-lg transition-colors duration-200 shadow-sm"
                    style="background:#A31D1D;"
                    onmouseover="this.style.background='#8A1818'"
                    onmouseout="this.style.background='#A31D1D'">
                Lưu tất cả
            </button>
        </div>

        {{-- Sections --}}
        <div class="space-y-6 max-w-4xl">
            @include('admin.settings.partials.hero-section')
            @include('admin.settings.partials.stats-section')
            @include('admin.settings.partials.problem-solution-section')
            @include('admin.settings.partials.core-values-section')
            @include('admin.settings.partials.audience-section')
            @include('admin.settings.partials.cta-section')
        </div>

        {{-- Bottom save --}}
        <div class="max-w-4xl mt-6 flex justify-end">
            <button type="submit"
                    class="px-5 py-2.5 text-sm font-semibold text-white rounded-lg transition-colors duration-200 shadow-sm"
                    style="background:#A31D1D;"
                    onmouseover="this.style.background='#8A1818'"
                    onmouseout="this.style.background='#A31D1D'">
                Lưu tất cả
            </button>
        </div>
    </form>

</x-admin.layout.app>
