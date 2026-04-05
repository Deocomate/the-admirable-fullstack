<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the users table with a default superadmin account.
     */
    public function run(): void
    {
        // Create default superadmin — only if it doesn't already exist
        User::firstOrCreate(
            ['email' => 'admin@gmail.com'],
            [
                'name'     => 'Super Admin',
                'role'     => 'superadmin',
                'password' => Hash::make('Admin@123'),
            ]
        );
    }
}
