<?php

namespace Database\Factories;

use App\Models\Category;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Category>
 */
class CategoryFactory extends Factory
{
    protected $model = Category::class;

    public function definition(): array
    {
        $name = fake()->unique()->randomElement([
            'Chính trị', 'Khoa học', 'Nghệ thuật', 'Kinh tế',
            'Thể thao', 'Công nghệ', 'Văn hóa', 'Đời sống',
        ]);

        return [
            'name' => $name,
            'slug' => Str::slug($name),
        ];
    }
}
