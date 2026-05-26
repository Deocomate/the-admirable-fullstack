<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Jobs\GenerateAudioJob;
use App\Models\Figure;
use App\Models\StorySnippet;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Http\JsonResponse;

class AudioController extends Controller
{
    public function generate(string $type, int $id): JsonResponse
    {
        $model = $this->findModel($type, $id);

        if (blank(config('services.azure_tts.key'))) {
            $model->update([
                'audio_status' => 'failed',
                'audio_error' => 'Azure TTS key is not configured.',
            ]);

            return response()->json([
                'message' => 'Azure TTS key is not configured.',
            ], 422);
        }

        if ($model->audio_status === 'processing') {
            return response()->json([
                'message' => 'Audio is already being generated.',
            ], 409);
        }

        $model->update([
            'audio_status' => 'processing',
            'audio_error' => null,
        ]);

        GenerateAudioJob::dispatch($type, $id);

        return response()->json([
            'message' => 'Audio generation has been queued.',
        ]);
    }

    public function cancel(string $type, int $id): JsonResponse
    {
        $model = $this->findModel($type, $id);

        if ($model->audio_status !== 'processing') {
            return response()->json([
                'message' => 'No audio generation is currently running.',
            ], 409);
        }

        $model->update([
            'audio_status' => 'cancelled',
            'audio_error' => null,
        ]);

        return response()->json([
            'message' => 'Audio generation has been cancelled.',
        ]);
    }

    public function status(string $type, int $id): JsonResponse
    {
        $model = $this->findModel($type, $id);

        if ($model->audio_status === 'processing' && blank(config('services.azure_tts.key'))) {
            $model->update([
                'audio_status' => 'failed',
                'audio_error' => 'Azure TTS key is not configured.',
            ]);
        }

        return response()->json([
            'status' => $model->audio_status,
            'error' => $model->audio_error,
            'audio_url' => $model->audio_path ? asset('storage/'.$model->audio_path) : null,
        ]);
    }

    private function findModel(string $type, int $id): Model
    {
        return match ($type) {
            'figure' => Figure::findOrFail($id),
            'story' => StorySnippet::findOrFail($id),
            default => abort(404),
        };
    }
}
