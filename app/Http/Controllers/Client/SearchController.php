<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\Category;
use App\Models\Figure;
use Illuminate\Http\Request;

class SearchController extends Controller
{
    /**
     * Display search results page.
     */
    public function index(Request $request)
    {
        $query = $request->input('q', '');
        $categorySlug = $request->input('category', '');
        $categories = Category::orderBy('name')->get();

        $figuresQuery = Figure::with('categories');

        if (!empty($query)) {
            $figuresQuery->where(function ($q) use ($query) {
                $q->where('name', 'like', "%{$query}%")
                  ->orWhere('short_description', 'like', "%{$query}%")
                  ->orWhere('content', 'like', "%{$query}%");
            });
        }

        if (!empty($categorySlug)) {
            $figuresQuery->whereHas('categories', function ($q) use ($categorySlug) {
                $q->where('slug', $categorySlug);
            });
        }

        $figures = $figuresQuery->latest()->paginate(12)->appends($request->query());

        // Trending figures (most story snippets)
        $trendingFigures = Figure::withCount('storySnippets')
            ->orderByDesc('story_snippets_count')
            ->limit(4)
            ->get();

        return view('client.search.index', compact(
            'query',
            'categorySlug',
            'categories',
            'figures',
            'trendingFigures'
        ));
    }
}
