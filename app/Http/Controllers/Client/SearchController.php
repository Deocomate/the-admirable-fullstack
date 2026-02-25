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
        $query = trim((string) $request->input('q', ''));
        $categorySlug = trim((string) $request->input('category', ''));
        $categories = Category::orderBy('name')->get();

        $figuresQuery = Figure::with(['categories', 'featuredFigure'])
            ->leftJoin('featured_figures', 'featured_figures.figure_id', '=', 'figures.id')
            ->select('figures.*');

        if ($query !== '') {
            $figuresQuery->where(function ($q) use ($query) {
                $q->where('figures.name', 'like', "%{$query}%")
                  ->orWhere('figures.short_description', 'like', "%{$query}%")
                  ->orWhere('figures.content', 'like', "%{$query}%");
            });
        }

        if ($categorySlug !== '') {
            $figuresQuery->whereHas('categories', function ($q) use ($categorySlug) {
                $q->where('slug', $categorySlug);
            });
        }

        $figures = $figuresQuery
            ->orderByRaw('CASE WHEN featured_figures.id IS NULL THEN 1 ELSE 0 END')
            ->orderBy('featured_figures.priority')
            ->orderByDesc('figures.created_at')
            ->paginate(12)
            ->appends($request->query());

        $figures->getCollection()->transform(function (Figure $figure) {
            $figure->setAttribute('is_featured', (bool) $figure->featuredFigure);

            return $figure;
        });

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
