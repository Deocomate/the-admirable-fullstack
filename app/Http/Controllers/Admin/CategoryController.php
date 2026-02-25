<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreCategoryRequest;
use App\Http\Requests\UpdateCategoryRequest;
use App\Services\CategoryService;
use Illuminate\Http\RedirectResponse;
use Illuminate\View\View;

class CategoryController extends Controller
{
    public function __construct(private readonly CategoryService $categoryService) {}

    /**
     * Display a listing of categories.
     */
    public function index(): View
    {
        $categories = $this->categoryService->getAll();

        return view('admin.categories.index', compact('categories'));
    }

    /**
     * Show the form for creating a new category.
     */
    public function create(): View
    {
        return view('admin.categories.form');
    }

    /**
     * Store a newly created category.
     */
    public function store(StoreCategoryRequest $request): RedirectResponse
    {
        $this->categoryService->create($request->validated());

        return redirect()->route('admin.categories.index')
            ->with('success', 'Lĩnh vực đã được tạo thành công.');
    }

    /**
     * Show the form for editing a category.
     */
    public function edit(int $category): View
    {
        $category = $this->categoryService->findById($category);

        return view('admin.categories.form', compact('category'));
    }

    /**
     * Update the specified category.
     */
    public function update(UpdateCategoryRequest $request, int $category): RedirectResponse
    {
        $this->categoryService->update($category, $request->validated());

        return redirect()->route('admin.categories.index')
            ->with('success', 'Lĩnh vực đã được cập nhật thành công.');
    }

    /**
     * Remove the specified category.
     */
    public function destroy(int $category): RedirectResponse
    {
        try {
            $this->categoryService->delete($category);
        } catch (\Exception $e) {
            return redirect()->route('admin.categories.index')
                ->with('error', 'Không thể xóa lĩnh vực: ' . $e->getMessage());
        }

        return redirect()->route('admin.categories.index')
            ->with('success', 'Lĩnh vực đã được xóa thành công.');
    }
}
