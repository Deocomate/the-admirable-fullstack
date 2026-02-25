<x-admin.layout.app
    title="{{ isset($contact) ? 'Chỉnh sửa liên hệ' : 'Thêm liên hệ' }}"
    breadcrumb="Admin › Liên hệ › {{ isset($contact) ? 'Chỉnh sửa' : 'Thêm mới' }}">

    <div class="max-w-lg">
        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">

            <h2 class="text-sm font-semibold text-gray-700 mb-5">
                {{ isset($contact) ? 'Chỉnh sửa thông tin liên hệ' : 'Thông tin liên hệ mới' }}
            </h2>

            <form method="POST"
                  action="{{ isset($contact) ? route('admin.contacts.update', $contact->id) : route('admin.contacts.store') }}"
                  class="space-y-4">
                @csrf
                @if(isset($contact))
                    @method('PUT')
                @endif

                {{-- Type --}}
                <div>
                    <label for="type" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Loại liên hệ <span class="text-red-500">*</span>
                    </label>
                    <select id="type" name="type" required
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 {{ $errors->has('type') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('type') ? '#f87171' : '#D1D5DB' }}'">
                        <option value="">-- Chọn loại --</option>
                        @foreach(['email' => 'Email', 'phone' => 'Số điện thoại', 'facebook' => 'Facebook', 'github' => 'GitHub', 'whatsapp' => 'WhatsApp', 'zalo' => 'Zalo', 'linkedin' => 'LinkedIn', 'twitter' => 'Twitter/X', 'website' => 'Website', 'other' => 'Khác'] as $typeVal => $typeLabel)
                            <option value="{{ $typeVal }}" {{ old('type', $contact->type ?? '') === $typeVal ? 'selected' : '' }}>
                                {{ $typeLabel }}
                            </option>
                        @endforeach
                    </select>
                    @error('type')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Label --}}
                <div>
                    <label for="label" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Nhãn hiển thị <span class="text-red-500">*</span>
                    </label>
                    <input type="text" id="label" name="label"
                        value="{{ old('label', $contact->label ?? '') }}"
                        required
                        placeholder="VD: Email liên hệ, Số điện thoại..."
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 placeholder-gray-400
                               {{ $errors->has('label') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('label') ? '#f87171' : '#D1D5DB' }}'">
                    @error('label')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Value --}}
                <div>
                    <label for="value" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Giá trị <span class="text-red-500">*</span>
                    </label>
                    <input type="text" id="value" name="value"
                        value="{{ old('value', $contact->value ?? '') }}"
                        required
                        placeholder="VD: email@example.com, https://facebook.com/..."
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 placeholder-gray-400
                               {{ $errors->has('value') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('value') ? '#f87171' : '#D1D5DB' }}'">
                    @error('value')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Sort Order --}}
                <div>
                    <label for="sort_order" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Thứ tự hiển thị
                    </label>
                    <input type="number" id="sort_order" name="sort_order"
                        value="{{ old('sort_order', $contact->sort_order ?? 0) }}"
                        min="0"
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 border-gray-300"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='#D1D5DB'">
                </div>

                {{-- Active --}}
                <div class="flex items-center gap-2">
                    <input type="hidden" name="is_active" value="0">
                    <input type="checkbox" id="is_active" name="is_active" value="1"
                        {{ old('is_active', $contact->is_active ?? true) ? 'checked' : '' }}
                        class="w-4 h-4 rounded border-gray-300 text-red-600 focus:ring-red-500">
                    <label for="is_active" class="text-sm text-gray-700">Hiển thị trên trang web</label>
                </div>

                {{-- Actions --}}
                <div class="flex items-center gap-3 pt-1">
                    <button type="submit"
                        class="px-5 py-2.5 text-sm font-semibold text-white rounded transition-colors duration-200"
                        style="background:#A31D1D;"
                        onmouseover="this.style.background='#8A1818'"
                        onmouseout="this.style.background='#A31D1D'">
                        {{ isset($contact) ? 'Lưu thay đổi' : 'Tạo liên hệ' }}
                    </button>
                    <a href="{{ route('admin.contacts.index') }}"
                       class="px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                        Hủy
                    </a>
                </div>
            </form>
        </div>
    </div>

</x-admin.layout.app>
