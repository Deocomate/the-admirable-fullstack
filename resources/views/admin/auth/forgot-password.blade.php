<x-admin.layout.auth title="Quên mật khẩu">

    <h2 class="text-lg font-semibold text-gray-800 mb-1">Quên mật khẩu</h2>
    <p class="text-xs text-gray-500 mb-5">
        Nhập email của bạn — chúng tôi sẽ gửi link đặt lại mật khẩu.
    </p>

    {{-- Success --}}
    @if(session('success'))
        <div class="mb-4 flex items-start gap-2 px-3 py-2.5 rounded text-sm text-green-800 bg-green-50 border border-green-200">
            <svg class="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            {{ session('success') }}
        </div>
    @endif

    <form method="POST" action="{{ route('admin.auth.forgot-password.submit') }}" class="space-y-4">
        @csrf

        {{-- Email --}}
        <div>
            <label for="email" class="block text-xs font-medium text-gray-600 mb-1.5">Email</label>
            <input
                type="email"
                id="email"
                name="email"
                value="{{ old('email') }}"
                required
                autofocus
                placeholder="admin@thceramics.vn"
                class="w-full px-3 py-2.5 text-sm border rounded outline-none transition-colors duration-150
                       bg-white text-gray-800 placeholder-gray-400
                       {{ $errors->has('email') ? 'border-red-400' : 'border-gray-300' }}"
                onfocus="this.style.borderColor='#A31D1D'"
                onblur="this.style.borderColor='{{ $errors->has('email') ? '#f87171' : '#D1D5DB' }}'"
            >
            @error('email')
                <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
            @enderror
        </div>

        <button
            type="submit"
            class="w-full py-2.5 px-4 text-sm font-semibold text-white rounded transition-colors duration-200"
            style="background:#A31D1D;"
            onmouseover="this.style.background='#8A1818'"
            onmouseout="this.style.background='#A31D1D'">
            Gửi link đặt lại
        </button>
    </form>

    <div class="mt-4 text-center">
        <a href="{{ route('admin.auth.login') }}"
           class="text-xs text-gray-400 hover:text-gray-600 transition-colors duration-150">
            ← Quay lại đăng nhập
        </a>
    </div>

</x-admin.layout.auth>
