<?php

namespace App\Jobs;

use App\Helpers\FileUploadHelper;
use App\Models\Figure;
use App\Models\StorySnippet;
use App\Services\AzureTextToSpeechService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use RuntimeException;
use Throwable;

class GenerateAudioJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 1;

    public int $timeout = 120;

    public function __construct(
        public readonly string $type,
        public readonly int $id,
    ) {}

    public function handle(AzureTextToSpeechService $textToSpeech): void
    {
        $model = $this->findModel();

        if (! $model) {
            return;
        }

        try {
            if ($model->audio_status !== 'processing') {
                return;
            }

            $audio = $textToSpeech->synthesize($model->content_blocks ?? []);

            $model->refresh();

            if ($model->audio_status !== 'processing') {
                return;
            }

            $oldPath = $model->audio_path;
            $newPath = $this->storeAudio($model, $audio);

            $model->refresh();

            if ($model->audio_status !== 'processing') {
                FileUploadHelper::delete($newPath);

                return;
            }

            $model->update([
                'audio_path' => $newPath,
                'audio_status' => 'completed',
                'audio_error' => null,
            ]);

            if ($oldPath !== $newPath) {
                FileUploadHelper::delete($oldPath);
            }
        } catch (Throwable $e) {
            $model->update([
                'audio_status' => 'failed',
                'audio_error' => (string) str($e->getMessage())->limit(500),
            ]);
        }
    }

    public function failed(Throwable $exception): void
    {
        $model = $this->findModel();

        if (! $model) {
            return;
        }

        $model->update([
            'audio_status' => 'failed',
            'audio_error' => (string) str($exception->getMessage())->limit(500),
        ]);
    }

    private function findModel(): ?Model
    {
        return match ($this->type) {
            'figure' => Figure::find($this->id),
            'story' => StorySnippet::find($this->id),
            default => throw new RuntimeException('Unsupported audio model type.'),
        };
    }

    private function storeAudio(Model $model, string $audio): string
    {
        $slug = Str::slug($model->name ?? $model->title ?? 'audio') ?: 'audio';
        $directory = $this->type === 'figure' ? 'uploads/audio' : 'uploads/stories/audio';
        $path = sprintf('%s/%s_%s.mp3', $directory, $slug, time());

        if (! Storage::disk('public')->put($path, $audio)) {
            throw new RuntimeException('Unable to store generated audio.');
        }

        return $path;
    }
}
