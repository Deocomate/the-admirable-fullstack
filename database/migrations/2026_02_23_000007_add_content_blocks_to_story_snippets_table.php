<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('story_snippets', function (Blueprint $table) {
            $table->string('subtitle')->nullable()->after('title');
            $table->json('content_blocks')->nullable()->after('subtitle');
        });
    }

    public function down(): void
    {
        Schema::table('story_snippets', function (Blueprint $table) {
            $table->dropColumn(['subtitle', 'content_blocks']);
        });
    }
};
