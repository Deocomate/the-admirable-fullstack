<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Services\FeaturedFigureService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class FeaturedFigureController extends Controller
{
    public function __construct(
        private readonly FeaturedFigureService $featuredFigureService,
    ) {}

    /**
     * Display featured figures management page.
     */
    public function index(Request $request): View
    {
        $featuredFigures = $this->featuredFigureService->getFeaturedForAdmin();
        $availableFigures = $this->featuredFigureService->getAvailableFiguresForSelect(
            search: $request->input('search'),
        );

        return view('admin.featured-figures.index', compact('featuredFigures', 'availableFigures'));
    }

    /**
     * Add figure to featured list.
     */
    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'figure_id' => ['required', 'integer', 'exists:figures,id'],
        ]);

        try {
            $this->featuredFigureService->add((int) $validated['figure_id']);
        } catch (\Throwable $exception) {
            return redirect()->route('admin.featured-figures.index')
                ->with('error', $exception->getMessage());
        }

        return redirect()->route('admin.featured-figures.index')
            ->with('success', 'Đã thêm nhân vật vào danh sách tiêu biểu.');
    }

    /**
     * Remove from featured list.
     */
    public function destroy(int $id): RedirectResponse
    {
        $this->featuredFigureService->remove($id);

        return redirect()->route('admin.featured-figures.index')
            ->with('success', 'Đã gỡ nhân vật khỏi danh sách tiêu biểu.');
    }

    /**
     * Reorder featured list after drag & drop.
     */
    public function reorder(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'figure_ids'   => ['required', 'array'],
            'figure_ids.*' => ['required', 'integer', 'exists:figures,id'],
        ]);

        $this->featuredFigureService->reorder($validated['figure_ids']);

        return response()->json([
            'message' => 'Cập nhật vị trí thành công.',
        ]);
    }
}
