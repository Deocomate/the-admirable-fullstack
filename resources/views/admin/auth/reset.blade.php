<x-admin.layout.auth title="Đặt lại mật khẩu">

    <h2 class="text-lg font-semibold text-gray-800 mb-1">Đặt lại mật khẩu</h2>
    <p class="text-xs text-gray-500 mb-5">Nhập mật khẩu mới cho tài khoản của bạn.</p>

    <form method="POST" action="{{ route('admin.auth.reset-password.submit') }}" class="space-y-4">
        @csrf

        <input type="hidden" name="token" value="{{ $token }}">

        {{-- Email --}}
        <div>
            <label for="email" class="block text-xs font-medium text-gray-600 mb-1.5">Email</label>
            <input
                type="email"
                id="email"
                name="email"
                value="{{ old('email', $email) }}"
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

        {{-- New Password --}}
        <div>
            <label for="password" class="block text-xs font-medium text-gray-600 mb-1.5">Mật khẩu mới</label>
            <input
                type="password"
                id="password"
                name="password"
                required
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
                Xác nhận mật khẩu
            </label>
            <input
                type="password"
                id="password_confirmation"
                name="password_confirmation"
                required
                placeholder="Nhập lại mật khẩu mới"
                class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                       bg-white text-gray-800 placeholder-gray-400 border-gray-300"
                onfocus="this.style.borderColor='#A31D1D'"
                onblur="this.style.borderColor='#D1D5DB'"
            >
        </div>

        <button
            type="submit"
            class="w-full py-2.5 px-4 text-sm font-semibold text-white rounded transition-colors duration-200"
            style="background:#A31D1D;"
            onmouseover="this.style.background='#8A1818'"
            onmouseout="this.style.background='#A31D1D'">
            Đặt lại mật khẩu
        </button>
    </form>

</x-admin.layout.auth>
