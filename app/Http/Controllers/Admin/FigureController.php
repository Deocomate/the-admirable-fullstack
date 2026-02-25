<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreFigureRequest;
use App\Http\Requests\UpdateFigureRequest;
use App\Services\CategoryService;
use App\Services\FigureService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class FigureController extends Controller
{
    public function __construct(
        private readonly FigureService $figureService,
        private readonly CategoryService $categoryService,
    ) {}

    /**
     * Display a listing of figures.
     */
    public function index(Request $request): View
    {
        $figures    = $this->figureService->getAll(
            search: $request->input('search'),
            categoryId: $request->input('category_id') ? (int) $request->input('category_id') : null,
        );
        $categories = $this->categoryService->getAllForSelect();

        return view('admin.figures.index', compact('figures', 'categories'));
    }

    /**
     * Show the form for creating a new figure.
     */
    public function create(): View
    {
        $categories = $this->categoryService->getAllForSelect();

        return view('admin.figures.form', compact('categories'));
    }

    /**
     * Store a newly created figure.
     */
    public function store(StoreFigureRequest $request): RedirectResponse
    {
        $data = $request->validated();

        $this->figureService->create(
            data: array_merge($data, [
                'avatar'         => $request->file('avatar'),
                'audio'          => $request->file('audio'),
                'key_facts'      => $data['key_facts'] ?? [],
                'content_blocks' => $data['content_blocks'] ?? [],
            ]),
            categoryIds: $data['category_ids'] ?? [],
        );

        return redirect()->route('admin.figures.index')
            ->with('success', 'Nhân vật đã được tạo thành công.');
    }

    /**
     * Show the form for editing a figure.
     */
    public function edit(int $figure): View
    {
        $figure     = $this->figureService->findById($figure);
        $categories = $this->categoryService->getAllForSelect();

        return view('admin.figures.form', compact('figure', 'categories'));
    }

    /**
     * Update the specified figure.
     */
    public function update(UpdateFigureRequest $request, int $figure): RedirectResponse
    {
        $data = $request->validated();

        $this->figureService->update(
            id: $figure,
            data: array_merge($data, [
                'avatar'         => $request->file('avatar'),
                'audio'          => $request->file('audio'),
                'key_facts'      => $data['key_facts'] ?? [],
                'content_blocks' => $data['content_blocks'] ?? [],
            ]),
            categoryIds: $data['category_ids'] ?? [],
        );

        return redirect()->route('admin.figures.index')
            ->with('success', 'Nhân vật đã được cập nhật thành công.');
    }

    /**
     * Remove the specified figure.
     */
    public function destroy(int $figure): RedirectResponse
    {
        try {
            $this->figureService->delete($figure);
        } catch (\Exception $e) {
            return redirect()->route('admin.figures.index')
                ->with('error', 'Không thể xóa nhân vật: ' . $e->getMessage());
        }

        return redirect()->route('admin.figures.index')
            ->with('success', 'Nhân vật đã được xóa thành công.');
    }
}
