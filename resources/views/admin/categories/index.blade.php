<x-admin.layout.app title="Quản lý lĩnh vực" breadcrumb="Admin › Lĩnh vực">

    <div class="flex items-center justify-between mb-5">
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Danh sách lĩnh vực</h2>
            <p class="text-xs text-gray-400 mt-0.5">Tổng cộng {{ $categories->total() }} lĩnh vực</p>
        </div>
        <a href="{{ route('admin.categories.create') }}"
           class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white rounded transition-colors duration-200"
           style="background:#A31D1D;"
           onmouseover="this.style.background='#8A1818'"
           onmouseout="this.style.background='#A31D1D'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm lĩnh vực
        </a>
    </div>

    {{-- Table Card --}}
    <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <table class="w-full text-sm">
            <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-10">#</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Tên lĩnh vực</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Slug</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Số nhân vật</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Ngày tạo</th>
                    <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thao tác</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                @forelse($categories as $category)
                    <tr class="hover:bg-gray-50 transition-colors duration-100">
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $categories->firstItem() + $loop->index }}
                        </td>
                        <td class="px-5 py-3.5 font-medium text-gray-800">
                            {{ $category->name }}
                        </td>
                        <td class="px-5 py-3.5 text-gray-500 text-xs">
                            {{ $category->slug }}
                        </td>
                        <td class="px-5 py-3.5">
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-gray-700 bg-gray-100 border border-gray-200">
                                {{ $category->figures_count }}
                            </span>
                        </td>
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $category->created_at->format('d/m/Y') }}
                        </td>
                        <td class="px-5 py-3.5 text-right">
                            <div class="inline-flex items-center gap-2">
                                <a href="{{ route('admin.categories.edit', $category->id) }}"
                                   class="px-2.5 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                                    Sửa
                                </a>
                                <form method="POST"
                                      action="{{ route('admin.categories.destroy', $category->id) }}"
                                      onsubmit="return confirm('Bạn có chắc chắn muốn xóa lĩnh vực này?')">
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
                            Chưa có lĩnh vực nào.
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>

        @if($categories->hasPages())
            <div class="px-5 py-3 border-t border-gray-100 bg-gray-50">
                {{ $categories->links() }}
            </div>
        @endif
    </div>

</x-admin.layout.app>
