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

        $featuredFigure = Figure::with('categories')
            ->latest()
            ->first();

        $figures = Figure::with('categories')
            ->latest()
            ->paginate(12);

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

        $featuredFigure = $category->figures()
            ->with('categories')
            ->latest()
            ->first();

        $figures = $category->figures()
            ->with('categories')
            ->latest()
            ->paginate(12);

        return view('client.category.index', compact(
            'categories',
            'category',
            'featuredFigure',
            'figures'
        ));
    }
}
