<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class FeaturedFigure extends Model
{
    use HasFactory;

    protected $fillable = [
        'figure_id',
        'priority',
    ];

    /**
     * Figure that is marked as featured.
     */
    public function figure(): BelongsTo
    {
        return $this->belongsTo(Figure::class);
    }
}
