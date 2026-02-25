<x-admin.layout.app title="Quản lý nhân vật" breadcrumb="Admin › Nhân vật">

    {{-- Header with filters --}}
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-5">
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Danh sách nhân vật</h2>
            <p class="text-xs text-gray-400 mt-0.5">Tổng cộng {{ $figures->total() }} nhân vật</p>
        </div>
        <a href="{{ route('admin.figures.create') }}"
           class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white rounded transition-colors duration-200 self-start"
           style="background:#A31D1D;"
           onmouseover="this.style.background='#8A1818'"
           onmouseout="this.style.background='#A31D1D'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm nhân vật
        </a>
    </div>

    {{-- Filter bar --}}
    <form method="GET" action="{{ route('admin.figures.index') }}" class="mb-5">
        <div class="flex flex-col sm:flex-row gap-3">
            <input type="text" name="search" value="{{ request('search') }}"
                   placeholder="Tìm tên nhân vật..."
                   class="px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800 placeholder-gray-400 w-full sm:w-64"
                   onfocus="this.style.borderColor='#A31D1D'"
                   onblur="this.style.borderColor='#D1D5DB'">
            <select name="category_id"
                    class="px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800">
                <option value="">-- Tất cả lĩnh vực --</option>
                @foreach($categories as $cat)
                    <option value="{{ $cat->id }}" {{ request('category_id') == $cat->id ? 'selected' : '' }}>
                        {{ $cat->name }}
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
            @if(request('search') || request('category_id'))
                <a href="{{ route('admin.figures.index') }}"
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
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Nhân vật</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Lĩnh vực</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Mẩu chuyện</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Media</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Ngày tạo</th>
                    <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thao tác</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                @forelse($figures as $figure)
                    <tr class="hover:bg-gray-50 transition-colors duration-100">
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $figures->firstItem() + $loop->index }}
                        </td>
                        <td class="px-5 py-3.5">
                            <div class="flex items-center gap-3">
                                @if($figure->avatar_path)
                                    <img src="{{ asset('storage/' . $figure->avatar_path) }}"
                                         alt="{{ $figure->name }}"
                                         class="w-9 h-9 rounded-full object-cover flex-shrink-0 border border-gray-200">
                                @else
                                    <div class="w-9 h-9 rounded-full flex items-center justify-center text-white text-xs font-semibold flex-shrink-0"
                                         style="background:#A31D1D;">
                                        {{ strtoupper(mb_substr($figure->name, 0, 1)) }}
                                    </div>
                                @endif
                                <div class="min-w-0">
                                    <p class="font-medium text-gray-800 truncate">{{ $figure->name }}</p>
                                    @if($figure->short_description)
                                        <p class="text-xs text-gray-400 truncate max-w-xs">{{ $figure->short_description }}</p>
                                    @endif
                                </div>
                            </div>
                        </td>
                        <td class="px-5 py-3.5">
                            <div class="flex flex-wrap gap-1">
                                @foreach($figure->categories as $cat)
                                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                                        {{ $cat->name }}
                                    </span>
                                @endforeach
                            </div>
                        </td>
                        <td class="px-5 py-3.5">
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-gray-700 bg-gray-100 border border-gray-200">
                                {{ $figure->story_snippets_count }}
                            </span>
                        </td>
                        <td class="px-5 py-3.5">
                            <div class="flex items-center gap-2">
                                @if($figure->audio_path)
                                    <span class="text-green-600" title="Có audio">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                  d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"/>
                                        </svg>
                                    </span>
                                @endif
                                @if($figure->youtube_url)
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
                            {{ $figure->created_at->format('d/m/Y') }}
                        </td>
                        <td class="px-5 py-3.5 text-right">
                            <div class="inline-flex items-center gap-2">
                                <a href="{{ route('client.figures.show', $figure->slug) }}"
                                   target="_blank"
                                   rel="noopener noreferrer"
                                   class="px-2.5 py-1.5 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded transition-colors duration-150">
                                    Preview
                                </a>
                                <a href="{{ route('admin.figures.edit', $figure->id) }}"
                                   class="px-2.5 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                                    Sửa
                                </a>
                                <form method="POST"
                                      action="{{ route('admin.figures.destroy', $figure->id) }}"
                                      onsubmit="return confirm('Bạn có chắc chắn muốn xóa nhân vật này? Tất cả mẩu chuyện liên quan cũng sẽ bị xóa.')">
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
                        <td colspan="7" class="px-5 py-10 text-center text-sm text-gray-400">
                            Chưa có nhân vật nào.
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>

        @if($figures->hasPages())
            <div class="px-5 py-3 border-t border-gray-100 bg-gray-50">
                {{ $figures->withQueryString()->links() }}
            </div>
        @endif
    </div>

</x-admin.layout.app>
