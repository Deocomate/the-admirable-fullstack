<?php

namespace App\Http\Controllers\Client;

use App\Http\Controllers\Controller;
use App\Models\StorySnippet;

class StorySnippetController extends Controller
{
    /**
     * Display a single story snippet detail page.
     */
    public function show(int $id)
    {
        $snippet = StorySnippet::with(['figure.categories'])->findOrFail($id);

        // Get other stories from the same figure, excluding current
        $otherStories = StorySnippet::where('figure_id', $snippet->figure_id)
            ->where('id', '!=', $snippet->id)
            ->limit(3)
            ->get();

        return view('client.story.show', compact('snippet', 'otherStories'));
    }
}
