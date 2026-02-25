<?php

use App\Http\Controllers\Admin\AuthController;
use App\Http\Controllers\Admin\CategoryController;
use App\Http\Controllers\Admin\ContactController;
use App\Http\Controllers\Admin\FigureController;
use App\Http\Controllers\Admin\SettingController;
use App\Http\Controllers\Admin\StorySnippetController;
use App\Http\Controllers\Admin\UserController;
use App\Http\Controllers\Client\HomeController as ClientHomeController;
use App\Http\Controllers\Client\CategoryController as ClientCategoryController;
use App\Http\Controllers\Client\FigureController as ClientFigureController;
use App\Http\Controllers\Client\StorySnippetController as ClientStorySnippetController;
use App\Http\Controllers\Client\SearchController as ClientSearchController;
use App\Http\Controllers\Client\AboutUsController as ClientAboutUsController;
use Illuminate\Support\Facades\Route;

// ─────────────────────────────────────────────────────────────────────────────
// Client routes (public-facing)
// ─────────────────────────────────────────────────────────────────────────────
Route::name('client.')->group(function () {
    Route::get('/', [ClientHomeController::class, 'index'])->name('home');
    Route::get('/linh-vuc', [ClientCategoryController::class, 'index'])->name('categories.index');
    Route::get('/linh-vuc/{slug}', [ClientCategoryController::class, 'show'])->name('categories.show');
    Route::get('/nhan-vat/{slug}', [ClientFigureController::class, 'show'])->name('figures.show');
    Route::get('/cau-chuyen/{id}', [ClientStorySnippetController::class, 'show'])->name('stories.show');
    Route::get('/tim-kiem', [ClientSearchController::class, 'index'])->name('search');
    Route::get('/ve-chung-toi', [ClientAboutUsController::class, 'index'])->name('about-us');
});

// ─────────────────────────────────────────────────────────────────────────────
// Admin routes
// ─────────────────────────────────────────────────────────────────────────────
Route::prefix('admin')->name('admin.')->group(function () {

    // ── Guest routes (unauthenticated only) ──────────────────────────────────
    Route::middleware('guest')->group(function () {
        Route::get('login', [AuthController::class, 'showLogin'])
            ->name('auth.login');
        Route::post('login', [AuthController::class, 'login'])
            ->name('auth.login.submit');

        Route::get('forgot-password', [AuthController::class, 'showForgotPassword'])
            ->name('auth.forgot-password');
        Route::post('forgot-password', [AuthController::class, 'forgotPassword'])
            ->name('auth.forgot-password.submit');

        Route::get('reset-password/{token}', [AuthController::class, 'showResetPassword'])
            ->name('auth.reset-password');
        Route::post('reset-password', [AuthController::class, 'resetPassword'])
            ->name('auth.reset-password.submit');
    });

    // ── Authenticated routes ──────────────────────────────────────────────────
    Route::middleware('auth')->group(function () {
        Route::get('/', fn () => redirect()->route('admin.dashboard'))->name('home');
        Route::get('dashboard', [AuthController::class, 'dashboard'])->name('dashboard');
        Route::post('logout', [AuthController::class, 'logout'])->name('auth.logout');

        // ── Superadmin-only: account management ──────────────────────────────
        Route::middleware('role:superadmin')->group(function () {
            Route::get('users', [UserController::class, 'index'])->name('users.index');
            Route::get('users/create', [UserController::class, 'create'])->name('users.create');
            Route::post('users', [UserController::class, 'store'])->name('users.store');
            Route::get('users/{user}/edit', [UserController::class, 'edit'])->name('users.edit');
            Route::put('users/{user}', [UserController::class, 'update'])->name('users.update');
            Route::delete('users/{user}', [UserController::class, 'destroy'])->name('users.destroy');
        });
        // ── Content management ───────────────────────────────────────────
        Route::resource('categories', CategoryController::class)->except(['show']);
        Route::resource('figures', FigureController::class)->except(['show']);
        Route::resource('stories', StorySnippetController::class)->except(['show']);
        Route::resource('contacts', ContactController::class)->except(['show']);

        // ── Settings ─────────────────────────────────────────────────────
        Route::get('settings/about-us', [SettingController::class, 'editAboutUs'])->name('settings.about-us');
        Route::post('settings/about-us', [SettingController::class, 'updateAboutUs'])->name('settings.about-us.submit');    });
});
