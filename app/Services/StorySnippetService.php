<?php

namespace App\Services;

use App\Helpers\FileUploadHelper;
use App\Models\StorySnippet;
use Illuminate\Http\UploadedFile;
use Illuminate\Pagination\LengthAwarePaginator;

class StorySnippetService
{
    /**
     * Get paginated list of story snippets with eager-loaded figure.
     *
     * @param int|null    $figureId  Filter by figure.
     * @param string|null $search    Search query.
     */
    public function getAll(?int $figureId = null, ?string $search = null, int $perPage = 15): LengthAwarePaginator
    {
        $query = StorySnippet::with('figure');

        if ($figureId) {
            $query->where('figure_id', $figureId);
        }

        if ($search) {
            $query->where('title', 'like', "%{$search}%");
        }

        return $query->latest()->paginate($perPage);
    }

    /**
     * Find a story snippet by ID.
     */
    public function findById(int $id): StorySnippet
    {
        return StorySnippet::with('figure')->findOrFail($id);
    }

    /**
     * Create a new story snippet.
     *
     * @param array $data  Form data including figure_id.
     */
    public function create(array $data): StorySnippet
    {
        $contentBlocks = $this->normalizeContentBlocks($data['content_blocks'] ?? []);

        $snippetData = [
            'figure_id'      => $data['figure_id'],
            'title'          => $data['title'],
            'subtitle'       => $data['subtitle'] ?? null,
            'content_blocks' => $contentBlocks,
            'content'        => $this->buildPlainContent($contentBlocks),
            'youtube_url'    => $data['youtube_url'] ?? null,
            'image_path'     => null,
            'audio_path'     => null,
        ];

        // Handle image upload
        if (isset($data['image']) && $data['image'] instanceof UploadedFile) {
            $snippetData['image_path'] = FileUploadHelper::upload(
                $data['image'], 'uploads/stories/images'
            );
        }

        // Handle audio upload
        if (isset($data['audio']) && $data['audio'] instanceof UploadedFile) {
            $snippetData['audio_path'] = FileUploadHelper::upload(
                $data['audio'], 'uploads/stories/audio'
            );
        }

        return StorySnippet::create($snippetData);
    }

    /**
     * Update an existing story snippet.
     *
     * @param array $data  Form data.
     */
    public function update(int $id, array $data): StorySnippet
    {
        $snippet = $this->findById($id);
        $contentBlocks = $this->normalizeContentBlocks($data['content_blocks'] ?? []);

        $snippetData = [
            'figure_id'      => $data['figure_id'],
            'title'          => $data['title'],
            'subtitle'       => $data['subtitle'] ?? null,
            'content_blocks' => $contentBlocks,
            'content'        => $this->buildPlainContent($contentBlocks),
            'youtube_url'    => $data['youtube_url'] ?? null,
        ];

        // Handle image upload (replace old)
        if (isset($data['image']) && $data['image'] instanceof UploadedFile) {
            $snippetData['image_path'] = FileUploadHelper::replace(
                $data['image'], $snippet->image_path, 'uploads/stories/images'
            );
        }

        // Handle audio upload (replace old)
        if (isset($data['audio']) && $data['audio'] instanceof UploadedFile) {
            $snippetData['audio_path'] = FileUploadHelper::replace(
                $data['audio'], $snippet->audio_path, 'uploads/stories/audio'
            );
        }

        $snippet->update($snippetData);

        return $snippet->fresh(['figure']);
    }

    /**
     * Delete a story snippet and its physical files.
     */
    public function delete(int $id): void
    {
        $snippet = $this->findById($id);

        FileUploadHelper::delete($snippet->image_path);
        FileUploadHelper::delete($snippet->audio_path);

        $snippet->delete();
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
                    'heading'   => !empty(trim($block['text_en'] ?? '')),
                    'quote'     => !empty(trim($block['text_en'] ?? '')),
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
            } elseif ($type === 'heading') {
                if (!empty($block['text_en'])) {
                    $parts[] = $block['text_en'];
                }
            } elseif ($type === 'quote') {
                if (!empty($block['text_en'])) {
                    $parts[] = $block['text_en'];
                }
                if (!empty($block['author'])) {
                    $parts[] = '— ' . $block['author'];
                }
            }
        }

        return implode("\n\n", $parts);
    }
}
