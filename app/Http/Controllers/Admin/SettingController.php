<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Services\SettingService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class SettingController extends Controller
{
    public function __construct(private readonly SettingService $settingService) {}

    /**
     * Show the About Us structured editor.
     */
    public function editAboutUs(): View
    {
        $aboutData = $this->settingService->getAboutUsData();

        return view('admin.settings.about-us', compact('aboutData'));
    }

    /**
     * Update the About Us structured data.
     */
    public function updateAboutUs(Request $request): RedirectResponse
    {
        $data = $request->validate([
            // Hero
            'hero.tagline'          => ['nullable', 'string', 'max:200'],
            'hero.headline'         => ['nullable', 'string', 'max:200'],
            'hero.headline_gradient' => ['nullable', 'string', 'max:200'],
            'hero.description'      => ['nullable', 'string', 'max:1000'],
            // Stats
            'stats'                 => ['nullable', 'array', 'max:4'],
            'stats.*.value'         => ['nullable', 'string', 'max:50'],
            'stats.*.label'         => ['nullable', 'string', 'max:100'],
            // Problem
            'problem.title'         => ['nullable', 'string', 'max:200'],
            'problem.description'   => ['nullable', 'string', 'max:2000'],
            // Solution
            'solution.title'        => ['nullable', 'string', 'max:200'],
            'solution.description'  => ['nullable', 'string', 'max:2000'],
            'solution.bullets'      => ['nullable', 'array', 'max:5'],
            'solution.bullets.*'    => ['nullable', 'string', 'max:300'],
            // Core values
            'core_values.tagline'   => ['nullable', 'string', 'max:200'],
            'core_values.title'     => ['nullable', 'string', 'max:200'],
            'core_values.items'     => ['nullable', 'array', 'max:6'],
            'core_values.items.*.title'       => ['nullable', 'string', 'max:100'],
            'core_values.items.*.description' => ['nullable', 'string', 'max:500'],
            // Audience
            'audience.title'        => ['nullable', 'string', 'max:200'],
            'audience.description'  => ['nullable', 'string', 'max:1000'],
            'audience.items'        => ['nullable', 'array', 'max:5'],
            'audience.items.*.title'       => ['nullable', 'string', 'max:100'],
            'audience.items.*.description' => ['nullable', 'string', 'max:500'],
            // CTA
            'cta.quote'             => ['nullable', 'string', 'max:300'],
            'cta.headline'          => ['nullable', 'string', 'max:200'],
            'cta.description'       => ['nullable', 'string', 'max:1000'],
        ]);

        $this->settingService->updateAboutUsData($data);

        return redirect()->route('admin.settings.about-us')
            ->with('success', 'Nội dung "Về chúng tôi" đã được cập nhật thành công.');
    }
}
