<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Figure extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'slug',
        'avatar_path',
        'short_description',
        'key_facts',
        'content_blocks',
        'content',
        'audio_path',
        'youtube_url',
    ];

    protected $casts = [
        'key_facts'      => 'array',
        'content_blocks' => 'array',
    ];

    /**
     * Categories this figure belongs to (many-to-many).
     */
    public function categories(): BelongsToMany
    {
        return $this->belongsToMany(Category::class, 'category_figure');
    }

    /**
     * Story snippets related to this figure (one-to-many).
     */
    public function storySnippets(): HasMany
    {
        return $this->hasMany(StorySnippet::class);
    }
}
