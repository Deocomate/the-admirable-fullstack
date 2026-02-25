<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Services\AuthService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;
use Illuminate\View\View;

class AuthController extends Controller
{
    public function __construct(private readonly AuthService $authService) {}

    // ─── Login ───────────────────────────────────────────────────────────────

    public function showLogin(): View
    {
        return view('admin.auth.login');
    }

    public function login(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email'    => ['required', 'email'],
            'password' => ['required', 'string'],
        ]);

        $credentials['remember'] = $request->boolean('remember');

        if (!$this->authService->login($credentials)) {
            return back()
                ->withInput($request->only('email', 'remember'))
                ->withErrors(['email' => 'Email hoặc mật khẩu không đúng.']);
        }

        return redirect()->route('admin.dashboard')
            ->with('success', 'Đăng nhập thành công. Chào mừng bạn!');
    }

    // ─── Dashboard ───────────────────────────────────────────────────────────

    public function dashboard(): View
    {
        return view('admin.dashboard');
    }

    // ─── Logout ──────────────────────────────────────────────────────────────

    public function logout(Request $request): RedirectResponse
    {
        $this->authService->logout();

        return redirect()->route('admin.auth.login')
            ->with('success', 'Bạn đã đăng xuất thành công.');
    }

    // ─── Forgot Password ─────────────────────────────────────────────────────

    public function showForgotPassword(): View
    {
        return view('admin.auth.forgot-password');
    }

    public function forgotPassword(Request $request): RedirectResponse
    {
        $request->validate([
            'email' => ['required', 'email'],
        ]);

        $status = $this->authService->forgotPassword($request->input('email'));

        if ($status === Password::RESET_LINK_SENT) {
            return back()->with('success', 'Chúng tôi đã gửi link đặt lại mật khẩu vào email của bạn.');
        }

        return back()
            ->withInput($request->only('email'))
            ->withErrors(['email' => __($status)]);
    }

    // ─── Reset Password ──────────────────────────────────────────────────────

    public function showResetPassword(Request $request, string $token): View
    {
        return view('admin.auth.reset', [
            'token' => $token,
            'email' => $request->query('email', ''),
        ]);
    }

    public function resetPassword(Request $request): RedirectResponse
    {
        $data = $request->validate([
            'token'                 => ['required'],
            'email'                 => ['required', 'email'],
            'password'              => ['required', 'min:8', 'confirmed'],
            'password_confirmation' => ['required'],
        ]);

        $status = $this->authService->resetPassword($data);

        if ($status === \Illuminate\Support\Facades\Password::PASSWORD_RESET) {
            return redirect()->route('admin.auth.login')
                ->with('success', 'Mật khẩu đã được đặt lại thành công. Vui lòng đăng nhập.');
        }

        return back()
            ->withInput($request->only('email'))
            ->withErrors(['email' => __($status)]);
    }
}
