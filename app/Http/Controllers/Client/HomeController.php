<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\Category;
use App\Models\Figure;
use App\Models\StorySnippet;
use App\Services\FeaturedFigureService;

class HomeController extends Controller
{
    public function __construct(
        private readonly FeaturedFigureService $featuredFigureService,
    ) {}

    /**
     * Display the homepage with featured figure, latest figures, categories and stats.
     */
    public function index()
    {
        $categories = Category::orderBy('name')->get();

        $featuredRecords = $this->featuredFigureService->getOrderedWithFigure(limit: 7);
        $featuredFigures = $featuredRecords
            ->pluck('figure')
            ->filter()
            ->values();

        $featuredFigures->each(function (Figure $figure) {
            $figure->setAttribute('is_featured', true);
        });

        $featuredFigure = $featuredFigures->first();
        $latestFigures = $featuredFigures->slice(1, 6)->values();

        if ($latestFigures->count() < 6) {
            $excludeFigureIds = $featuredFigures->pluck('id')->filter()->values();
            $fallbackFigures = Figure::with('categories')
                ->withCount('storySnippets')
                ->when($excludeFigureIds->isNotEmpty(), fn ($q) => $q->whereNotIn('id', $excludeFigureIds))
                ->latest()
                ->take(6 - $latestFigures->count())
                ->get();

            $fallbackFigures->each(function (Figure $figure) {
                $figure->setAttribute('is_featured', false);
            });

            $latestFigures = $latestFigures->concat($fallbackFigures)->values();
        }

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
