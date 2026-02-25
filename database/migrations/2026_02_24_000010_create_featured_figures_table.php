<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('featured_figures', function (Blueprint $table) {
            $table->id();
            $table->foreignId('figure_id')->unique()->constrained('figures')->cascadeOnDelete();
            $table->unsignedInteger('priority')->default(0)->index();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('featured_figures');
    }
};
