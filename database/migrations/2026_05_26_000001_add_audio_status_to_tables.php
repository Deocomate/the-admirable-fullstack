<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('figures', function (Blueprint $table) {
            $table->string('audio_status')->default('idle')->after('audio_path');
            $table->text('audio_error')->nullable()->after('audio_status');
        });

        Schema::table('story_snippets', function (Blueprint $table) {
            $table->string('audio_status')->default('idle')->after('audio_path');
            $table->text('audio_error')->nullable()->after('audio_status');
        });
    }

    public function down(): void
    {
        Schema::table('figures', function (Blueprint $table) {
            $table->dropColumn(['audio_status', 'audio_error']);
        });

        Schema::table('story_snippets', function (Blueprint $table) {
            $table->dropColumn(['audio_status', 'audio_error']);
        });
    }
};
