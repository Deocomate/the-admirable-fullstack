<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class StorySnippet extends Model
{
    use HasFactory;

    protected $fillable = [
        'figure_id',
        'title',
        'subtitle',
        'content',
        'content_blocks',
        'image_path',
        'audio_path',
        'youtube_url',
    ];

    /**
     * Cast attributes to native types.
     */
    protected $casts = [
        'content_blocks' => 'array',
    ];

    /**
     * The figure this story snippet belongs to.
     */
    public function figure(): BelongsTo
    {
        return $this->belongsTo(Figure::class);
    }
}
