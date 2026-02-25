<?php

namespace App\Services;

use App\Helpers\FileUploadHelper;
use App\Models\Figure;
use Illuminate\Http\UploadedFile;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Str;

class FigureService
{
    /**
     * Get paginated list of figures with eager-loaded categories.
     *
     * @param string|null $search      Search query.
     * @param int|null    $categoryId  Filter by category.
     */
    public function getAll(?string $search = null, ?int $categoryId = null, int $perPage = 15): LengthAwarePaginator
    {
        $query = Figure::with('categories')->withCount('storySnippets');

        if ($search) {
            $query->where('name', 'like', "%{$search}%");
        }

        if ($categoryId) {
            $query->whereHas('categories', function ($q) use ($categoryId) {
                $q->where('categories.id', $categoryId);
            });
        }

        return $query->latest()->paginate($perPage);
    }

    /**
     * Find a figure by ID with relationships.
     */
    public function findById(int $id): Figure
    {
        return Figure::with(['categories', 'storySnippets'])->findOrFail($id);
    }

    /**
     * Create a new figure.
     *
     * @param array  $data          Form data.
     * @param array  $categoryIds   Array of category IDs.
     */
    public function create(array $data, array $categoryIds = []): Figure
    {
        $slug = Str::slug($data['name']);

        $figureData = [
            'name'              => $data['name'],
            'slug'              => $this->uniqueSlug($slug),
            'short_description' => $data['short_description'] ?? null,
            'key_facts'         => $this->normalizeKeyFacts($data['key_facts'] ?? []),
            'content_blocks'    => $this->normalizeContentBlocks($data['content_blocks'] ?? []),
            'content'           => $this->buildPlainContent($data['content_blocks'] ?? []),
            'youtube_url'       => $data['youtube_url'] ?? null,
            'avatar_path'       => null,
            'audio_path'        => null,
        ];

        // Handle avatar upload
        if (isset($data['avatar']) && $data['avatar'] instanceof UploadedFile) {
            $figureData['avatar_path'] = FileUploadHelper::upload(
                $data['avatar'], 'uploads/avatars', $slug
            );
        }

        // Handle audio upload
        if (isset($data['audio']) && $data['audio'] instanceof UploadedFile) {
            $figureData['audio_path'] = FileUploadHelper::upload(
                $data['audio'], 'uploads/audio', $slug
            );
        }

        $figure = Figure::create($figureData);

        // Sync categories
        if (!empty($categoryIds)) {
            $figure->categories()->sync($categoryIds);
        }

        return $figure;
    }

    /**
     * Update an existing figure.
     *
     * @param array  $data          Form data.
     * @param array  $categoryIds   Array of category IDs.
     */
    public function update(int $id, array $data, array $categoryIds = []): Figure
    {
        $figure = $this->findById($id);
        $slug   = Str::slug($data['name']);

        $figureData = [
            'name'              => $data['name'],
            'slug'              => $figure->slug !== $slug ? $this->uniqueSlug($slug, $id) : $figure->slug,
            'short_description' => $data['short_description'] ?? null,
            'key_facts'         => $this->normalizeKeyFacts($data['key_facts'] ?? []),
            'content_blocks'    => $this->normalizeContentBlocks($data['content_blocks'] ?? []),
            'content'           => $this->buildPlainContent($data['content_blocks'] ?? []),
            'youtube_url'       => $data['youtube_url'] ?? null,
        ];

        // Handle avatar upload (replace old)
        if (isset($data['avatar']) && $data['avatar'] instanceof UploadedFile) {
            $figureData['avatar_path'] = FileUploadHelper::replace(
                $data['avatar'], $figure->avatar_path, 'uploads/avatars', $slug
            );
        }

        // Handle audio upload (replace old)
        if (isset($data['audio']) && $data['audio'] instanceof UploadedFile) {
            $figureData['audio_path'] = FileUploadHelper::replace(
                $data['audio'], $figure->audio_path, 'uploads/audio', $slug
            );
        }

        $figure->update($figureData);

        // Sync categories
        $figure->categories()->sync($categoryIds);

        return $figure->fresh(['categories']);
    }

    /**
     * Delete a figure and its related files.
     */
    public function delete(int $id): void
    {
        $figure = $this->findById($id);

        // Delete physical files
        FileUploadHelper::delete($figure->avatar_path);
        FileUploadHelper::delete($figure->audio_path);

        // Delete story snippets files
        foreach ($figure->storySnippets as $snippet) {
            FileUploadHelper::delete($snippet->image_path);
            FileUploadHelper::delete($snippet->audio_path);
        }

        // Detach categories & cascade delete snippets via FK
        $figure->categories()->detach();
        $figure->delete();
    }

    /**
     * Generate a unique slug.
     */
    private function uniqueSlug(string $slug, ?int $excludeId = null): string
    {
        $original = $slug;
        $counter  = 1;

        while (Figure::where('slug', $slug)->when($excludeId, fn ($q) => $q->where('id', '!=', $excludeId))->exists()) {
            $slug = $original . '-' . $counter++;
        }

        return $slug;
    }

    /**
     * Normalize key_facts array: filter out empty entries.
     */
    private function normalizeKeyFacts(array $facts): array
    {
        return array_values(
            array_filter($facts, fn ($f) => !empty(trim($f['label'] ?? '')) && !empty(trim($f['value'] ?? '')))
        );
    }

    /**
     * Normalize content_blocks array: filter out empty blocks, keep order.
     */
    private function normalizeContentBlocks(array $blocks): array
    {
        return array_values(
            array_filter($blocks, function ($block) {
                $type = $block['type'] ?? '';

                return match ($type) {
                    'paragraph' => !empty(trim($block['text_en'] ?? '')),
                    'quote'     => !empty(trim($block['text_en'] ?? '')),
                    'heading'   => !empty(trim($block['text_en'] ?? '')),
                    default     => false,
                };
            })
        );
    }

    /**
     * Build plain-text content from blocks (for backward compatibility & search).
     */
    private function buildPlainContent(array $blocks): string
    {
        $parts = [];

        foreach ($blocks as $block) {
            $type = $block['type'] ?? '';

            if ($type === 'heading' && !empty($block['text_en'])) {
                $parts[] = $block['text_en'];
            }

            if ($type === 'paragraph') {
                if (!empty($block['heading_en'])) {
                    $parts[] = $block['heading_en'];
                }
                if (!empty($block['text_en'])) {
                    $parts[] = $block['text_en'];
                }
                if (!empty($block['text_vi'])) {
                    $parts[] = $block['text_vi'];
                }
            }

            if ($type === 'quote' && !empty($block['text_en'])) {
                $author = $block['author'] ?? '';
                $parts[] = '"' . $block['text_en'] . '"' . ($author ? " — {$author}" : '');
            }
        }

        return implode("\n\n", $parts);
    }
}
