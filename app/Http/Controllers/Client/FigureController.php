<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\Figure;

class FigureController extends Controller
{
    /**
     * Display figure detail page with story snippets and related figures.
     */
    public function show(string $slug)
    {
        $figure = Figure::with(['categories', 'storySnippets'])
            ->where('slug', $slug)
            ->firstOrFail();

        // Get related figures from the same categories
        $categoryIds = $figure->categories->pluck('id');

        $relatedFigures = Figure::with('categories')
            ->where('id', '!=', $figure->id)
            ->whereHas('categories', function ($q) use ($categoryIds) {
                $q->whereIn('categories.id', $categoryIds);
            })
            ->limit(3)
            ->get();

        return view('client.figure.show', compact('figure', 'relatedFigures'));
    }
}
