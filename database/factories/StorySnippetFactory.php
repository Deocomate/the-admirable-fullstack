<?php

namespace Database\Factories;

use App\Models\Figure;
use App\Models\StorySnippet;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\StorySnippet>
 */
class StorySnippetFactory extends Factory
{
    protected $model = StorySnippet::class;

    public function definition(): array
    {
        return [
            'figure_id'   => Figure::factory(),
            'title'       => fake()->sentence(6),
            'content'     => fake()->paragraphs(3, true),
            'image_path'  => null,
            'audio_path'  => null,
            'youtube_url' => 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        ];
    }
}
