<x-admin.layout.app
    title="{{ isset($category) ? 'Chỉnh sửa lĩnh vực' : 'Thêm lĩnh vực' }}"
    breadcrumb="Admin › Lĩnh vực › {{ isset($category) ? 'Chỉnh sửa' : 'Thêm mới' }}">

    <div class="max-w-lg">
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">

            <h2 class="text-sm font-semibold text-gray-700 mb-5">
                {{ isset($category) ? 'Chỉnh sửa lĩnh vực' : 'Thông tin lĩnh vực' }}
            </h2>

            <form method="POST"
                  action="{{ isset($category) ? route('admin.categories.update', $category->id) : route('admin.categories.store') }}"
                  class="space-y-4">
                @csrf
                @if(isset($category))
                    @method('PUT')
                @endif

                {{-- Name --}}
                <div>
                    <label for="name" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Tên lĩnh vực <span class="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value="{{ old('name', $category->name ?? '') }}"
                        required
                        autofocus
                        placeholder="VD: Chính trị, Khoa học, Nghệ thuật..."
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 placeholder-gray-400
                               {{ $errors->has('name') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('name') ? '#f87171' : '#D1D5DB' }}'"
                    >
                    @error('name')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Actions --}}
                <div class="flex items-center gap-3 pt-1">
                    <button
                        type="submit"
                        class="px-5 py-2.5 text-sm font-semibold text-white rounded transition-colors duration-200"
                        style="background:#A31D1D;"
                        onmouseover="this.style.background='#8A1818'"
                        onmouseout="this.style.background='#A31D1D'">
                        {{ isset($category) ? 'Lưu thay đổi' : 'Tạo lĩnh vực' }}
                    </button>
                    <a href="{{ route('admin.categories.index') }}"
                       class="px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                        Hủy
                    </a>
                </div>
            </form>
        </div>
    </div>

</x-admin.layout.app>
