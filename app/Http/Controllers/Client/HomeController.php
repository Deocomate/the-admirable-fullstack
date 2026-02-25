<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\Category;
use App\Models\Figure;
use App\Models\StorySnippet;

class HomeController extends Controller
{
    /**
     * Display the homepage with featured figure, latest figures, categories and stats.
     */
    public function index()
    {
        $categories = Category::orderBy('name')->get();

        $featuredFigure = Figure::with('categories')
            ->withCount('storySnippets')
            ->latest()
            ->first();

        $latestFigures = Figure::with('categories')
            ->latest()
            ->skip($featuredFigure ? 1 : 0)
            ->take(6)
            ->get();

        $stats = [
            'figures'  => Figure::count(),
            'categories' => Category::count(),
            'stories'  => StorySnippet::count(),
        ];

        return view('client.home.index', compact(
            'categories',
            'featuredFigure',
            'latestFigures',
            'stats'
        ));
    }
}
