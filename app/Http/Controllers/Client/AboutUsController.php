<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Services\SettingService;

class AboutUsController extends Controller
{
    /**
     * Display the About Us page.
     */
    public function index()
    {
        $settingService = new SettingService();
        $aboutUs = $settingService->getAboutUsData();

        return view('client.about-us.index', compact('aboutUs'));
    }
}
