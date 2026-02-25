<?php

namespace App\Services;

use App\Models\FeaturedFigure;
use App\Models\Figure;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;

class FeaturedFigureService
{
    /**
     * Get featured list for admin screen.
     */
    public function getFeaturedForAdmin(): Collection
    {
        return FeaturedFigure::with('figure.categories')
            ->orderBy('priority')
            ->orderBy('id')
            ->get();
    }

    /**
     * Get figures that are not yet featured.
     */
    public function getAvailableFiguresForSelect(?string $search = null, int $limit = 120): Collection
    {
        return Figure::query()
            ->select(['id', 'name'])
            ->whereDoesntHave('featuredFigure')
            ->when($search, function ($query, $searchTerm) {
                $query->where('name', 'like', '%' . $searchTerm . '%');
            })
            ->orderBy('name')
            ->limit($limit)
            ->get();
    }

    /**
     * Add a figure to featured list.
     */
    public function add(int $figureId): FeaturedFigure
    {
        Figure::findOrFail($figureId);

        if (FeaturedFigure::where('figure_id', $figureId)->exists()) {
            throw new \InvalidArgumentException('Nhân vật này đã nằm trong danh sách tiêu biểu.');
        }

        $nextPriority = ((int) FeaturedFigure::max('priority')) + 1;

        return FeaturedFigure::create([
            'figure_id' => $figureId,
            'priority'  => $nextPriority,
        ]);
    }

    /**
     * Remove from featured list.
     */
    public function remove(int $id): void
    {
        $featuredFigure = FeaturedFigure::findOrFail($id);
        $featuredFigure->delete();
    }

    /**
     * Reorder featured list by given figure IDs.
     *
     * @param array<int, int|string> $figureIds
     */
    public function reorder(array $figureIds): void
    {
        DB::transaction(function () use ($figureIds) {
            foreach (array_values($figureIds) as $priority => $figureId) {
                FeaturedFigure::where('figure_id', (int) $figureId)->update([
                    'priority' => $priority,
                ]);
            }
        });
    }

    /**
     * Get ordered featured records with full figure relation.
     */
    public function getOrderedWithFigure(?int $limit = null): Collection
    {
        $query = FeaturedFigure::with([
            'figure' => fn ($q) => $q->with('categories')->withCount('storySnippets'),
        ])->orderBy('priority');

        if ($limit) {
            $query->limit($limit);
        }

        return $query->get();
    }
}
