<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\User;
use App\Services\UserService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    public function __construct(private readonly UserService $userService) {}

    // ─── Index ───────────────────────────────────────────────────────────────

    public function index(): View
    {
        $users = $this->userService->getAllAdmins();

        return view('admin.users.index', compact('users'));
    }

    // ─── Create ──────────────────────────────────────────────────────────────

    public function create(): View
    {
        return view('admin.users.create');
    }

    public function store(Request $request): RedirectResponse
    {
        $data = $request->validate([
            'name'     => ['required', 'string', 'max:255'],
            'email'    => ['required', 'email', 'unique:users,email'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);

        $this->userService->createAdmin($data);

        return redirect()->route('admin.users.index')
            ->with('success', 'Tài khoản admin đã được tạo thành công.');
    }

    // ─── Edit ────────────────────────────────────────────────────────────────

    public function edit(User $user): View
    {
        return view('admin.users.edit', compact('user'));
    }

    public function update(Request $request, User $user): RedirectResponse
    {
        $data = $request->validate([
            'name'     => ['required', 'string', 'max:255'],
            'email'    => ['required', 'email', 'unique:users,email,' . $user->id],
            'password' => ['nullable', 'string', 'min:8', 'confirmed'],
        ]);

        $this->userService->updateAdmin($user->id, $data);

        return redirect()->route('admin.users.index')
            ->with('success', 'Thông tin tài khoản đã được cập nhật.');
    }

    // ─── Delete ──────────────────────────────────────────────────────────────

    public function destroy(User $user): RedirectResponse
    {
        try {
            $this->userService->deleteAdmin($user->id);
        } catch (\RuntimeException $e) {
            return redirect()->route('admin.users.index')
                ->with('error', $e->getMessage());
        }

        return redirect()->route('admin.users.index')
            ->with('success', 'Tài khoản đã bị xóa thành công.');
    }
}
