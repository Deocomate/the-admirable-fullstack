<?php

namespace App\Services;

use App\Models\Setting;

class SettingService
{
    /**
     * Default structure for the About Us page data.
     */
    private function getDefaultAboutUsData(): array
    {
        return [
            'hero' => [
                'tagline'     => '',
                'headline'    => '',
                'headline_gradient' => '',
                'description' => '',
            ],
            'stats' => [
                ['value' => '', 'label' => ''],
                ['value' => '', 'label' => ''],
                ['value' => '', 'label' => ''],
                ['value' => '', 'label' => ''],
            ],
            'problem' => [
                'title'       => '',
                'description' => '',
            ],
            'solution' => [
                'title'       => '',
                'description' => '',
                'bullets'     => ['', '', ''],
            ],
            'core_values' => [
                'tagline' => '',
                'title'   => '',
                'items'   => [
                    ['title' => '', 'description' => ''],
                    ['title' => '', 'description' => ''],
                    ['title' => '', 'description' => ''],
                    ['title' => '', 'description' => ''],
                ],
            ],
            'audience' => [
                'title'       => '',
                'description' => '',
                'items'       => [
                    ['title' => '', 'description' => ''],
                    ['title' => '', 'description' => ''],
                    ['title' => '', 'description' => ''],
                ],
            ],
            'cta' => [
                'quote'       => '',
                'headline'    => '',
                'description' => '',
            ],
        ];
    }

    /**
     * Get structured About Us data as an array.
     */
    public function getAboutUsData(): array
    {
        $raw = Setting::getValue('about_us_data');
        $data = $raw ? json_decode($raw, true) : [];

        return array_replace_recursive($this->getDefaultAboutUsData(), $data ?: []);
    }

    /**
     * Update the structured About Us data.
     */
    public function updateAboutUsData(array $data): void
    {
        Setting::setValue('about_us_data', json_encode($data, JSON_UNESCAPED_UNICODE));
    }
}
