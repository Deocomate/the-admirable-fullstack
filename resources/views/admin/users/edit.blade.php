<x-admin.layout.app title="Chỉnh sửa tài khoản" breadcrumb="Admin › Tài khoản › Chỉnh sửa">

    <div class="max-w-lg">

        <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">

            <div class="flex items-center gap-3 mb-5">
                <div class="w-9 h-9 rounded-full flex items-center justify-center text-white text-sm font-semibold flex-shrink-0"
                     style="background:#A31D1D;">
                    {{ strtoupper(substr($user->name, 0, 1)) }}
                </div>
                <div>
                    <h2 class="text-sm font-semibold text-gray-700">{{ $user->name }}</h2>
                    <p class="text-xs text-gray-400 capitalize">{{ $user->role }}</p>
                </div>
            </div>

            <form method="POST" action="{{ route('admin.users.update', $user) }}" class="space-y-4">
                @csrf
                @method('PUT')

                {{-- Name --}}
                <div>
                    <label for="name" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Tên hiển thị <span class="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value="{{ old('name', $user->name) }}"
                        required
                        autofocus
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800
                               {{ $errors->has('name') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('name') ? '#f87171' : '#D1D5DB' }}'"
                    >
                    @error('name')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Email --}}
                <div>
                    <label for="email" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Email <span class="text-red-500">*</span>
                    </label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value="{{ old('email', $user->email) }}"
                        required
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800
                               {{ $errors->has('email') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('email') ? '#f87171' : '#D1D5DB' }}'"
                    >
                    @error('email')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                <hr class="border-gray-100">

                <p class="text-xs text-gray-400">Để trống nếu không muốn thay đổi mật khẩu.</p>

                {{-- New Password --}}
                <div>
                    <label for="password" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Mật khẩu mới
                    </label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="Tối thiểu 8 ký tự"
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 placeholder-gray-400
                               {{ $errors->has('password') ? 'border-red-400' : 'border-gray-300' }}"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='{{ $errors->has('password') ? '#f87171' : '#D1D5DB' }}'"
                    >
                    @error('password')
                        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
                    @enderror
                </div>

                {{-- Confirm Password --}}
                <div>
                    <label for="password_confirmation" class="block text-xs font-medium text-gray-600 mb-1.5">
                        Xác nhận mật khẩu mới
                    </label>
                    <input
                        type="password"
                        id="password_confirmation"
                        name="password_confirmation"
                        placeholder="Nhập lại mật khẩu mới"
                        class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                               bg-white text-gray-800 placeholder-gray-400 border-gray-300"
                        onfocus="this.style.borderColor='#A31D1D'"
                        onblur="this.style.borderColor='#D1D5DB'"
                    >
                </div>

                {{-- Actions --}}
                <div class="flex items-center gap-3 pt-1">
                    <button
                        type="submit"
                        class="px-5 py-2.5 text-sm font-semibold text-white rounded transition-colors duration-200"
                        style="background:#A31D1D;"
                        onmouseover="this.style.background='#8A1818'"
                        onmouseout="this.style.background='#A31D1D'">
                        Lưu thay đổi
                    </button>
                    <a href="{{ route('admin.users.index') }}"
                       class="px-5 py-2.5 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded transition-colors duration-150">
                        Hủy
                    </a>
                </div>
            </form>
        </div>
    </div>

</x-admin.layout.app>
