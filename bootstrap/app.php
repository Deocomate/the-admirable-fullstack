<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        $middleware->alias([
            'role' => \App\Http\Middleware\RoleMiddleware::class,
        ]);

        // Redirect unauthenticated users to the admin login page
        $middleware->redirectGuestsTo(function (\Illuminate\Http\Request $request) {
            return route('admin.auth.login');
        });

        // Redirect authenticated users away from guest-only pages (e.g. login) to admin dashboard
        $middleware->redirectUsersTo(function (\Illuminate\Http\Request $request) {
            return route('admin.dashboard');
        });
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        //
    })->create();
