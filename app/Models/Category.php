<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Category extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'slug',
    ];

    /**
     * Figures belonging to this category (many-to-many).
     */
    public function figures(): BelongsToMany
    {
        return $this->belongsToMany(Figure::class, 'category_figure');
    }
}
