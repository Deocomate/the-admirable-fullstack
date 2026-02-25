<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Support\Str;

class AuthService
{
    /**
     * Attempt to authenticate a user.
     *
     * @param array{email: string, password: string, remember: bool} $credentials
     * @return bool
     */
    public function login(array $credentials): bool
    {
        $remember = $credentials['remember'] ?? false;

        $attempt = Auth::attempt(
            [
                'email'    => $credentials['email'],
                'password' => $credentials['password'],
            ],
            $remember
        );

        if ($attempt) {
            request()->session()->regenerate();
        }

        return $attempt;
    }

    /**
     * Log the current user out and invalidate the session.
     */
    public function logout(): void
    {
        Auth::logout();
        request()->session()->invalidate();
        request()->session()->regenerateToken();
    }

    /**
     * Send a password-reset link to the given email address.
     *
     * @return string  One of the Password::* status constants.
     */
    public function forgotPassword(string $email): string
    {
        return Password::sendResetLink(['email' => $email]);
    }

    /**
     * Reset the user's password using the provided token.
     *
     * @param array{token: string, email: string, password: string, password_confirmation: string} $data
     * @return string  One of the Password::* status constants.
     */
    public function resetPassword(array $data): string
    {
        return Password::reset($data, function (User $user, string $password): void {
            $user->forceFill([
                'password'       => Hash::make($password),
                'remember_token' => Str::random(60),
            ])->save();

            event(new PasswordReset($user));
        });
    }
}
