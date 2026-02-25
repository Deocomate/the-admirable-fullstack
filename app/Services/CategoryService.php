<?php

namespace App\Services;

use App\Models\Category;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Str;

class CategoryService
{
    /**
     * Get paginated list of all categories.
     */
    public function getAll(int $perPage = 15): LengthAwarePaginator
    {
        return Category::withCount('figures')
            ->latest()
            ->paginate($perPage);
    }

    /**
     * Get all categories (no pagination) for dropdowns.
     */
    public function getAllForSelect(): \Illuminate\Database\Eloquent\Collection
    {
        return Category::orderBy('name')->get();
    }

    /**
     * Find a category by ID.
     */
    public function findById(int $id): Category
    {
        return Category::findOrFail($id);
    }

    /**
     * Create a new category.
     *
     * @param array{name: string} $data
     */
    public function create(array $data): Category
    {
        return Category::create([
            'name' => $data['name'],
            'slug' => Str::slug($data['name']),
        ]);
    }

    /**
     * Update an existing category.
     *
     * @param array{name: string} $data
     */
    public function update(int $id, array $data): Category
    {
        $category = $this->findById($id);

        $category->update([
            'name' => $data['name'],
            'slug' => Str::slug($data['name']),
        ]);

        return $category->fresh();
    }

    /**
     * Delete a category.
     */
    public function delete(int $id): void
    {
        $category = $this->findById($id);
        $category->figures()->detach();
        $category->delete();
    }
}
