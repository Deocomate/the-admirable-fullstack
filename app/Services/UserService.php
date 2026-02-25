<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\Hash;

class UserService
{
    /**
     * Get paginated list of all admin users.
     */
    public function getAllAdmins(int $perPage = 15): LengthAwarePaginator
    {
        return User::allAdmins()->latest()->paginate($perPage);
    }

    /**
     * Find a user by ID.
     */
    public function findById(int $id): User
    {
        return User::findOrFail($id);
    }

    /**
     * Create a new admin account.
     * Only "admin" role is allowed — superadmin cannot be created via UI.
     *
     * @param array{name: string, email: string, password: string} $data
     */
    public function createAdmin(array $data): User
    {
        return User::create([
            'name'     => $data['name'],
            'role'     => 'admin',               // always admin, never superadmin
            'email'    => $data['email'],
            'password' => Hash::make($data['password']),
        ]);
    }

    /**
     * Update an existing admin account.
     * Cannot update to superadmin role via this method.
     *
     * @param array{name: string, email: string, password?: string} $data
     */
    public function updateAdmin(int $id, array $data): User
    {
        $user = $this->findById($id);

        $fillable = [
            'name'  => $data['name'],
            'email' => $data['email'],
        ];

        if (!empty($data['password'])) {
            $fillable['password'] = Hash::make($data['password']);
        }

        $user->update($fillable);

        return $user->fresh();
    }

    /**
     * Delete an admin account.
     * - Cannot delete a superadmin user.
     * - Cannot delete yourself.
     *
     * @throws \RuntimeException
     */
    public function deleteAdmin(int $id): void
    {
        $user = $this->findById($id);

        if ($user->isSuperAdmin()) {
            throw new \RuntimeException('Không thể xóa tài khoản superadmin.');
        }

        if (auth()->id() === $user->id) {
            throw new \RuntimeException('Bạn không thể tự xóa tài khoản của mình.');
        }

        $user->delete();
    }
}
