<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\Category;
use App\Models\Figure;

class CategoryController extends Controller
{
    /**
     * Display all categories with all figures (no filter).
     */
    public function index()
    {
        $categories = Category::orderBy('name')->get();

        $baseQuery = Figure::with(['categories', 'featuredFigure'])
            ->leftJoin('featured_figures', 'featured_figures.figure_id', '=', 'figures.id')
            ->select('figures.*');

        $featuredFigure = (clone $baseQuery)
            ->whereNotNull('featured_figures.id')
            ->orderBy('featured_figures.priority')
            ->first();

        $figures = $baseQuery
            ->orderByRaw('CASE WHEN featured_figures.id IS NULL THEN 1 ELSE 0 END')
            ->orderBy('featured_figures.priority')
            ->orderByDesc('figures.created_at')
            ->paginate(12);

        $figures->getCollection()->transform(function (Figure $figure) {
            $figure->setAttribute('is_featured', (bool) $figure->featuredFigure);

            return $figure;
        });

        if ($featuredFigure instanceof Figure) {
            $featuredFigure->setAttribute('is_featured', true);
        }

        return view('client.category.index', compact(
            'categories',
            'featuredFigure',
            'figures'
        ));
    }

    /**
     * Display figures filtered by a specific category slug.
     */
    public function show(string $slug)
    {
        $category = Category::where('slug', $slug)->firstOrFail();
        $categories = Category::orderBy('name')->get();

        $baseQuery = $category->figures()
            ->with(['categories', 'featuredFigure'])
            ->leftJoin('featured_figures', 'featured_figures.figure_id', '=', 'figures.id')
            ->select('figures.*');

        $featuredFigure = (clone $baseQuery)
            ->whereNotNull('featured_figures.id')
            ->orderBy('featured_figures.priority')
            ->first();

        $figures = $baseQuery
            ->orderByRaw('CASE WHEN featured_figures.id IS NULL THEN 1 ELSE 0 END')
            ->orderBy('featured_figures.priority')
            ->orderByDesc('figures.created_at')
            ->paginate(12);

        $figures->getCollection()->transform(function (Figure $figure) {
            $figure->setAttribute('is_featured', (bool) $figure->featuredFigure);

            return $figure;
        });

        if ($featuredFigure instanceof Figure) {
            $featuredFigure->setAttribute('is_featured', true);
        }

        return view('client.category.index', compact(
            'categories',
            'category',
            'featuredFigure',
            'figures'
        ));
    }
}
