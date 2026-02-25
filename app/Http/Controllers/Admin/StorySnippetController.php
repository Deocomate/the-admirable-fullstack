<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreStorySnippetRequest;
use App\Http\Requests\UpdateStorySnippetRequest;
use App\Services\FigureService;
use App\Services\StorySnippetService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class StorySnippetController extends Controller
{
    public function __construct(
        private readonly StorySnippetService $storySnippetService,
        private readonly FigureService $figureService,
    ) {}

    /**
     * Display a listing of story snippets.
     */
    public function index(Request $request): View
    {
        $stories = $this->storySnippetService->getAll(
            figureId: $request->input('figure_id') ? (int) $request->input('figure_id') : null,
            search: $request->input('search'),
        );
        $figures = \App\Models\Figure::orderBy('name')->get(['id', 'name']);

        return view('admin.stories.index', compact('stories', 'figures'));
    }

    /**
     * Show the form for creating a new story snippet.
     */
    public function create(Request $request): View
    {
        $figures = \App\Models\Figure::orderBy('name')->get(['id', 'name']);
        $selectedFigureId = $request->input('figure_id');

        return view('admin.stories.form', compact('figures', 'selectedFigureId'));
    }

    /**
     * Store a newly created story snippet.
     */
    public function store(StoreStorySnippetRequest $request): RedirectResponse
    {
        $data = $request->validated();

        $this->storySnippetService->create(array_merge($data, [
            'image'          => $request->file('image'),
            'audio'          => $request->file('audio'),
            'content_blocks' => $data['content_blocks'] ?? [],
        ]));

        return redirect()->route('admin.stories.index')
            ->with('success', 'Mẩu chuyện đã được tạo thành công.');
    }

    /**
     * Show the form for editing a story snippet.
     */
    public function edit(int $story): View
    {
        $story   = $this->storySnippetService->findById($story);
        $figures = \App\Models\Figure::orderBy('name')->get(['id', 'name']);

        return view('admin.stories.form', compact('story', 'figures'));
    }

    /**
     * Update the specified story snippet.
     */
    public function update(UpdateStorySnippetRequest $request, int $story): RedirectResponse
    {
        $data = $request->validated();

        $this->storySnippetService->update($story, array_merge($data, [
            'image'          => $request->file('image'),
            'audio'          => $request->file('audio'),
            'content_blocks' => $data['content_blocks'] ?? [],
        ]));

        return redirect()->route('admin.stories.index')
            ->with('success', 'Mẩu chuyện đã được cập nhật thành công.');
    }

    /**
     * Remove the specified story snippet.
     */
    public function destroy(int $story): RedirectResponse
    {
        try {
            $this->storySnippetService->delete($story);
        } catch (\Exception $e) {
            return redirect()->route('admin.stories.index')
                ->with('error', 'Không thể xóa mẩu chuyện: ' . $e->getMessage());
        }

        return redirect()->route('admin.stories.index')
            ->with('success', 'Mẩu chuyện đã được xóa thành công.');
    }
}
