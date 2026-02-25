<x-admin.layout.app title="Quản lý liên hệ" breadcrumb="Admin › Liên hệ">

    <div class="flex items-center justify-between mb-5">
        <div>
            <h2 class="text-sm font-semibold text-gray-700">Danh sách thông tin liên hệ</h2>
            <p class="text-xs text-gray-400 mt-0.5">Tổng cộng {{ $contacts->total() }} liên hệ</p>
        </div>
        <a href="{{ route('admin.contacts.create') }}"
           class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white rounded transition-colors duration-200"
           style="background:#A31D1D;"
           onmouseover="this.style.background='#8A1818'"
           onmouseout="this.style.background='#A31D1D'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Thêm liên hệ
        </a>
    </div>

    {{-- Table Card --}}
    <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
        <table class="w-full text-sm">
            <thead>
                <tr class="border-b border-gray-100 bg-gray-50">
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-10">#</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Loại</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Nhãn</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Giá trị</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Trạng thái</th>
                    <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thứ tự</th>
                    <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thao tác</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                @forelse($contacts as $contact)
                    <tr class="hover:bg-gray-50 transition-colors duration-100">
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $contacts->firstItem() + $loop->index }}
                        </td>
                        <td class="px-5 py-3.5">
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-gray-700 bg-gray-100 border border-gray-200">
                                {{ $contact->type }}
                            </span>
                        </td>
                        <td class="px-5 py-3.5 font-medium text-gray-800">
                            {{ $contact->label }}
                        </td>
                        <td class="px-5 py-3.5 text-gray-500 text-xs max-w-xs truncate">
                            {{ $contact->value }}
                        </td>
                        <td class="px-5 py-3.5">
                            @if($contact->is_active)
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-green-700 bg-green-50 border border-green-200">
                                    Hiển thị
                                </span>
                            @else
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium text-gray-500 bg-gray-50 border border-gray-200">
                                    Ẩn
                                </span>
                            @endif
                        </td>
                        <td class="px-5 py-3.5 text-xs text-gray-400">
                            {{ $contact->sort_order }}
                        </td>
                        <td class="px-5 py-3.5 text-right">
                            <div class="inline-flex items-center gap-2">
                                <a href="{{ route('admin.contacts.edit', $contact->id) }}"
                                   class="px-2.5 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                                    Sửa
                                </a>
                                <form method="POST"
                                      action="{{ route('admin.contacts.destroy', $contact->id) }}"
                                      onsubmit="return confirm('Xác nhận xóa liên hệ này?')"
                                      class="inline">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit"
                                            class="px-2.5 py-1.5 text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded transition-colors duration-150">
                                        Xóa
                                    </button>
                                </form>
                            </div>
                        </td>
                    </tr>
                @empty
                    <tr>
                        <td colspan="7" class="px-5 py-10 text-center text-sm text-gray-400">
                            Chưa có thông tin liên hệ nào.
                        </td>
                    </tr>
                @endforelse
            </tbody>
        </table>
    </div>

    {{-- Pagination --}}
    @if($contacts->hasPages())
        <div class="mt-5">
            {{ $contacts->links() }}
        </div>
    @endif

</x-admin.layout.app>
