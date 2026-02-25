<x-admin.layout.app title="Quản lý mẩu chuyện" breadcrumb="Admin › Mẩu chuyện">

    {{-- Header --}}
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Danh sách mẩu chuyện</h2>
            <p class="text-xs text-gray-400 mt-0.5">Tổng cộng {{ $stories->total() }} mẩu chuyện</p>
        </div>
        <a href="{{ route('admin.stories.create') }}"
           class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white rounded transition-colors duration-200 self-start"
           style="background:#A31D1D;"
           onmouseover="this.style.background='#8A1818'"
           onmouseout="this.style.background='#A31D1D'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm mẩu chuyện
        </a>
    </div>

    {{-- Filter bar --}}
    <form method="GET" action="{{ route('admin.stories.index') }}" class="mb-5">
        <div class="flex flex-col sm:flex-row gap-3">
            <input type="text" name="search" value="{{ request('search') }}"
                   placeholder="Tìm tiêu đề mẩu chuyện..."
                   class="px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 w-full sm:w-64"
                   onfocus="this.style.borderColor='#A31D1D'"
                   onblur="this.style.borderColor='#D1D5DB'">
            <select name="figure_id"
                    class="px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800">
                <option value="">-- Tất cả nhân vật --</option>
                @foreach($figures as $fig)
                    <option value="{{ $fig->id }}" {{ request('figure_id') == $fig->id ? 'selected' : '' }}>
                        {{ $fig->name }}
                    </option>
                @endforeach
            </select>
            <button type="submit"
                    class="px-4 py-2 text-sm font-medium text-white rounded transition-colors duration-200"
                    style="background:#A31D1D;"
                    onmouseover="this.style.background='#8A1818'"
                    onmouseout="this.style.background='#A31D1D'">
                Lọc
            </button>
            @if(request('search') || request('figure_id'))
                <a href="{{ route('admin.stories.index') }}"
                   class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                    Xóa bộ lọc
                </a>
            @endif
        </div>
    </form>

    {{-- Table Card --}}
    <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <table class="w-full text-sm">
            <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-10">#</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Tiêu đề</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Nhân vật</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Media</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Ngày tạo</th>
                    <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thao tác</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                @forelse($stories as $story)
                    <tr class="hover:bg-gray-50 transition-colors duration-100">
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $stories->firstItem() + $loop->index }}
                        </td>
                        <td class="px-5 py-3.5">
                            <div class="flex items-center gap-3">
                                @if($story->image_path)
                                    <img src="{{ asset('storage/' . $story->image_path) }}"
                                         alt="{{ $story->title }}"
                                         class="w-9 h-9 rounded object-cover flex-shrink-0 border border-gray-200">
                                @endif
                                <span class="font-medium text-gray-800 truncate max-w-xs">{{ $story->title }}</span>
                            </div>
                        </td>
                        <td class="px-5 py-3.5">
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                                {{ $story->figure->name ?? '—' }}
                            </span>
                        </td>
                        <td class="px-5 py-3.5">
                            <div class="flex items-center gap-2">
                                @if($story->image_path)
                                    <span class="text-indigo-500" title="Có ảnh">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                        </svg>
                                    </span>
                                @endif
                                @if($story->audio_path)
                                    <span class="text-green-600" title="Có audio">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
                                        </svg>
                                    </span>
                                @endif
                                @if($story->youtube_url)
                                    <span class="text-red-500" title="Có video">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                        </svg>
                                    </span>
                                @endif
                            </div>
                        </td>
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $story->created_at->format('d/m/Y') }}
                        </td>
                        <td class="px-5 py-3.5 text-right">
                            <div class="inline-flex items-center gap-2">
                                <a href="{{ route('admin.stories.edit', $story->id) }}"
                                   class="px-2.5 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                                    Sửa
                                </a>
                                <form method="POST"
                                      action="{{ route('admin.stories.destroy', $story->id) }}"
                                      onsubmit="return confirm('Bạn có chắc chắn muốn xóa mẩu chuyện này?')">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit"
                                            class="px-2.5 py-1.5 text-xs font-medium text-white rounded transition-colors duration-150"
                                            style="background:#DC3545;"
                                            onmouseover="this.style.background='#bb2d3b'"
                                            onmouseout="this.style.background='#DC3545'">
                                        Xóa
                                    </button>
                                </form>
                            </div>
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="6" class="px-5 py-10 text-center text-sm text-gray-400">
                            Chưa có mẩu chuyện nào.
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>

        @if($stories->hasPages())
            <div class="px-5 py-3 border-t border-gray-100 bg-gray-50">
                {{ $stories->withQueryString()->links() }}
            </div>
        @endif
    </div>

</x-admin.layout.app>
