<?php

namespace Database\Factories;

use App\Models\Figure;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Figure>
 */
class FigureFactory extends Factory
{
    protected $model = Figure::class;

    public function definition(): array
    {
        $name = fake()->name();

        return [
            'name'              => $name,
            'slug'              => Str::slug($name) . '-' . fake()->unique()->randomNumber(4),
            'avatar_path'       => null,
            'short_description' => fake()->sentence(10),
            'content'           => fake()->paragraphs(5, true),
            'audio_path'        => null,
            'youtube_url'       => 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        ];
    }
}
