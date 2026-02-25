<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('figures', function (Blueprint $table) {
            $table->json('key_facts')->nullable()->after('short_description');
            $table->json('content_blocks')->nullable()->after('key_facts');
        });
    }

    public function down(): void
    {
        Schema::table('figures', function (Blueprint $table) {
            $table->dropColumn(['key_facts', 'content_blocks']);
        });
    }
};
