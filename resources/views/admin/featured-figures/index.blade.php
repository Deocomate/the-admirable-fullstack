<x-admin.layout.app title="Nhân vật tiêu biểu" breadcrumb="Admin › Nhân vật tiêu biểu">

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-5">
        <div class="lg:col-span-1 bg-white rounded-lg border border-gray-200 shadow-sm p-5">
            <h2 class="text-sm font-semibold text-gray-700">Thêm vào danh sách tiêu biểu</h2>
            <p class="text-xs text-gray-400 mt-1 mb-4">Chọn nhân vật từ danh sách chưa được gắn tiêu biểu.</p>

            <form method="GET" action="{{ route('admin.featured-figures.index') }}" class="mb-3">
                <input type="text" name="search" value="{{ request('search') }}"
                       placeholder="Tìm tên nhân vật..."
                       class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none"
                       onfocus="this.style.borderColor='#A31D1D'"
                       onblur="this.style.borderColor='#D1D5DB'">
            </form>

            <form method="POST" action="{{ route('admin.featured-figures.store') }}" class="space-y-3">
                @csrf
                <select name="figure_id" required
                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded outline-none bg-white text-gray-800"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='#D1D5DB'">
                    <option value="">-- Chọn nhân vật --</option>
                    @foreach($availableFigures as $figure)
                        <option value="{{ $figure->id }}">{{ $figure->name }}</option>
                    @endforeach
                </select>

                <button type="submit"
                        class="w-full px-4 py-2 text-sm font-semibold text-white rounded transition-colors duration-200"
                        style="background:#A31D1D;"
                        onmouseover="this.style.background='#8A1818'"
                        onmouseout="this.style.background='#A31D1D'">
                    Thêm vào danh sách
                </button>
            </form>
        </div>

        <div class="lg:col-span-2 bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
            <div class="px-5 py-4 border-b border-gray-100 flex items-center justify-between gap-3">
                <div>
                    <h2 class="text-sm font-semibold text-gray-700">Danh sách nhân vật tiêu biểu</h2>
                    <p class="text-xs text-gray-400 mt-0.5">Kéo thả để đổi thứ tự hiển thị (ưu tiên từ trên xuống).</p>
                </div>
                <span class="text-xs text-gray-500">Tổng: {{ $featuredFigures->count() }}</span>
            </div>

            @if($featuredFigures->isEmpty())
                <div class="px-5 py-12 text-center text-sm text-gray-400">
                    Chưa có nhân vật tiêu biểu nào.
                </div>
            @else
                <div id="featured-update-message" class="hidden mx-5 mt-4 px-3 py-2 text-xs rounded border"></div>
                <table class="w-full text-sm">
                    <thead>
                    <tr class="border-b border-gray-100 bg-gray-50">
                        <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-16">Ưu tiên</th>
                        <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Nhân vật</th>
                        <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Lĩnh vực</th>
                        <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Thao tác</th>
                    </tr>
                    </thead>
                    <tbody id="featured-sortable" class="divide-y divide-gray-100">
                    @foreach($featuredFigures as $item)
                        <tr data-figure-id="{{ $item->figure_id }}" class="hover:bg-gray-50">
                            <td class="px-5 py-3.5">
                                <span class="inline-flex items-center gap-1 text-xs text-gray-500 font-medium">
                                    <svg class="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"/>
                                    </svg>
                                    #{{ $loop->iteration }}
                                </span>
                            </td>
                            <td class="px-5 py-3.5">
                                <div class="flex items-center gap-3">
                                    @if($item->figure?->avatar_path)
                                        <img src="{{ asset('storage/' . $item->figure->avatar_path) }}"
                                             alt="{{ $item->figure->name }}"
                                             class="w-9 h-9 rounded-full object-cover border border-gray-200">
                                    @else
                                        <div class="w-9 h-9 rounded-full flex items-center justify-center text-white text-xs font-semibold"
                                             style="background:#A31D1D;">
                                            {{ strtoupper(mb_substr($item->figure?->name ?? '?', 0, 1)) }}
                                        </div>
                                    @endif
                                    <div class="min-w-0">
                                        <p class="font-medium text-gray-800 truncate">{{ $item->figure?->name }}</p>
                                        @if($item->figure?->short_description)
                                            <p class="text-xs text-gray-400 truncate max-w-xs">{{ $item->figure->short_description }}</p>
                                        @endif
                                    </div>
                                </div>
                            </td>
                            <td class="px-5 py-3.5">
                                <div class="flex flex-wrap gap-1">
                                    @foreach($item->figure?->categories ?? [] as $category)
                                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                                            {{ $category->name }}
                                        </span>
                                    @endforeach
                                </div>
                            </td>
                            <td class="px-5 py-3.5 text-right">
                                <form method="POST"
                                      action="{{ route('admin.featured-figures.destroy', $item->id) }}"
                                      onsubmit="return confirm('Bạn có chắc chắn muốn gỡ nhân vật này khỏi danh sách tiêu biểu?')"
                                      class="inline-block">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit"
                                            class="px-2.5 py-1.5 text-xs font-medium text-white rounded transition-colors duration-150"
                                            style="background:#DC3545;"
                                            onmouseover="this.style.background='#bb2d3b'"
                                            onmouseout="this.style.background='#DC3545'">
                                        Gỡ
                                    </button>
                                </form>
                            </td>
                        </tr>
                    @endforeach
                    </tbody>
                </table>
            @endif
        </div>
    </div>

    @if($featuredFigures->isNotEmpty())
        <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.2/Sortable.min.js"></script>
        <script>
            (() => {
                const container = document.getElementById('featured-sortable');
                const messageBox = document.getElementById('featured-update-message');
                if (!container || !messageBox) return;

                const showMessage = (text, type = 'success') => {
                    messageBox.textContent = text;
                    messageBox.classList.remove('hidden', 'text-green-700', 'bg-green-50', 'border-green-200', 'text-red-700', 'bg-red-50', 'border-red-200');
                    messageBox.classList.add('border');
                    if (type === 'success') {
                        messageBox.classList.add('text-green-700', 'bg-green-50', 'border-green-200');
                    } else {
                        messageBox.classList.add('text-red-700', 'bg-red-50', 'border-red-200');
                    }
                };

                new Sortable(container, {
                    animation: 150,
                    onEnd: async () => {
                        const figureIds = Array.from(container.querySelectorAll('tr[data-figure-id]'))
                            .map((row) => Number(row.dataset.figureId));

                        try {
                            const response = await fetch('{{ route('admin.featured-figures.reorder') }}', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                                    'Accept': 'application/json',
                                },
                                body: JSON.stringify({ figure_ids: figureIds }),
                            });

                            if (!response.ok) {
                                throw new Error('Request failed');
                            }

                            showMessage('Cập nhật vị trí thành công.');
                        } catch (error) {
                            showMessage('Không thể cập nhật vị trí, vui lòng thử lại.', 'error');
                        }
                    },
                });
            })();
        </script>
    @endif

</x-admin.layout.app>
