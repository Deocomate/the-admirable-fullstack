<?php

use App\Jobs\GenerateAudioJob;
use App\Models\Figure;
use App\Models\StorySnippet;
use App\Models\User;
use App\Services\AzureTextToSpeechService;
use App\Services\FigureService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Client\Request;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;

uses(RefreshDatabase::class);

function actingAsAdmin(): User
{
    return User::factory()->create(['role' => 'admin']);
}

it('dispatches audio generation for a figure', function () {
    Bus::fake();
    config()->set('services.azure_tts.key', 'test-key');
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create([
        'content_blocks' => [
            ['type' => 'paragraph', 'text_en' => 'A short English paragraph.'],
        ],
    ]);

    $this->postJson(route('admin.audio.generate', ['figure', $figure->id]))
        ->assertSuccessful()
        ->assertJsonPath('message', 'Audio generation has been queued.');

    Bus::assertDispatched(GenerateAudioJob::class, fn (GenerateAudioJob $job) => $job->type === 'figure' && $job->id === $figure->id);
    expect($figure->fresh()->audio_status)->toBe('processing');
});

it('dispatches audio generation for a story', function () {
    Bus::fake();
    config()->set('services.azure_tts.key', 'test-key');
    $this->actingAs(actingAsAdmin());

    $story = StorySnippet::factory()->create([
        'content_blocks' => [
            ['type' => 'quote', 'text_en' => 'Stay hungry, stay foolish.'],
        ],
    ]);

    $this->postJson(route('admin.audio.generate', ['story', $story->id]))
        ->assertSuccessful();

    Bus::assertDispatched(GenerateAudioJob::class, fn (GenerateAudioJob $job) => $job->type === 'story' && $job->id === $story->id);
    expect($story->fresh()->audio_status)->toBe('processing');
});

it('rejects invalid audio model types', function () {
    Bus::fake();
    config()->set('services.azure_tts.key', 'test-key');
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create();

    $this->postJson(route('admin.audio.generate', ['invalid', $figure->id]))
        ->assertNotFound();

    Bus::assertNotDispatched(GenerateAudioJob::class);
});

it('returns conflict when audio generation is already processing', function () {
    Bus::fake();
    config()->set('services.azure_tts.key', 'test-key');
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create(['audio_status' => 'processing']);

    $this->postJson(route('admin.audio.generate', ['figure', $figure->id]))
        ->assertConflict();

    Bus::assertNotDispatched(GenerateAudioJob::class);
});

it('rejects generation when azure key is missing', function () {
    Bus::fake();
    config()->set('services.azure_tts.key', null);
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create();

    $this->postJson(route('admin.audio.generate', ['figure', $figure->id]))
        ->assertUnprocessable()
        ->assertJsonPath('message', 'Azure TTS key is not configured.');

    Bus::assertNotDispatched(GenerateAudioJob::class);
    expect($figure->fresh()->audio_status)->toBe('failed');
});

it('returns audio status payload', function () {
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create([
        'audio_path' => 'uploads/audio/example.mp3',
        'audio_status' => 'completed',
        'audio_error' => null,
    ]);

    $this->getJson(route('admin.audio.status', ['figure', $figure->id]))
        ->assertSuccessful()
        ->assertJsonPath('status', 'completed')
        ->assertJsonPath('error', null)
        ->assertJsonPath('audio_url', asset('storage/uploads/audio/example.mp3'));
});

it('marks processing status as failed when azure key is missing', function () {
    config()->set('services.azure_tts.key', null);
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create([
        'audio_status' => 'processing',
        'audio_error' => null,
    ]);

    $this->getJson(route('admin.audio.status', ['figure', $figure->id]))
        ->assertSuccessful()
        ->assertJsonPath('status', 'failed')
        ->assertJsonPath('error', 'Azure TTS key is not configured.');

    expect($figure->fresh()->audio_status)->toBe('failed');
});

it('cancels processing audio generation', function () {
    $this->actingAs(actingAsAdmin());

    $figure = Figure::factory()->create([
        'audio_status' => 'processing',
    ]);

    $this->postJson(route('admin.audio.cancel', ['figure', $figure->id]))
        ->assertSuccessful()
        ->assertJsonPath('message', 'Audio generation has been cancelled.');

    expect($figure->fresh()->audio_status)->toBe('cancelled')
        ->and($figure->fresh()->audio_error)->toBeNull();
});

it('blocks unauthenticated users from generating audio', function () {
    $figure = Figure::factory()->create();

    $this->postJson(route('admin.audio.generate', ['figure', $figure->id]))
        ->assertUnauthorized();
});

it('generates and stores audio with escaped ssml text', function () {
    Storage::fake('public');
    Http::preventStrayRequests();
    config()->set('services.azure_tts.key', 'test-key');

    Http::fake(function (Request $request) {
        expect($request->body())
            ->toContain('Chapter &amp; One')
            ->toContain('Tom &amp; &quot;A&quot; &lt;B&gt; &apos;C&apos;');

        return Http::response('mp3-bytes', 200);
    });

    $figure = Figure::factory()->create([
        'audio_path' => 'uploads/audio/old.mp3',
        'audio_status' => 'processing',
        'content_blocks' => [
            ['type' => 'heading', 'text_en' => 'Chapter & One'],
            ['type' => 'paragraph', 'heading_en' => 'Tom & "A" <B> \'C\'', 'text_en' => 'Body text.'],
        ],
    ]);

    Storage::disk('public')->put($figure->audio_path, 'old-bytes');

    (new GenerateAudioJob('figure', $figure->id))->handle(app(AzureTextToSpeechService::class));

    $figure->refresh();

    expect($figure->audio_status)->toBe('completed')
        ->and($figure->audio_error)->toBeNull()
        ->and($figure->audio_path)->toStartWith('uploads/audio/');

    Storage::disk('public')->assertExists($figure->audio_path);
    Storage::disk('public')->assertMissing('uploads/audio/old.mp3');
});

it('marks generation as failed when english content is empty', function () {
    Storage::fake('public');
    config()->set('services.azure_tts.key', 'test-key');

    $figure = Figure::factory()->create([
        'audio_status' => 'processing',
        'content_blocks' => [
            ['type' => 'paragraph', 'text_vi' => 'No English here.'],
        ],
    ]);

    (new GenerateAudioJob('figure', $figure->id))->handle(app(AzureTextToSpeechService::class));

    expect($figure->fresh()->audio_status)->toBe('failed')
        ->and($figure->fresh()->audio_error)->toContain('No English content');
});

it('marks generation as failed when azure key is missing', function () {
    Storage::fake('public');
    config()->set('services.azure_tts.key', null);

    $story = StorySnippet::factory()->create([
        'audio_status' => 'processing',
        'content_blocks' => [
            ['type' => 'paragraph', 'text_en' => 'Some English text.'],
        ],
    ]);

    (new GenerateAudioJob('story', $story->id))->handle(app(AzureTextToSpeechService::class));

    expect($story->fresh()->audio_status)->toBe('failed')
        ->and($story->fresh()->audio_error)->toContain('Azure TTS key');
});

it('marks generation as failed when azure returns an error', function () {
    Storage::fake('public');
    config()->set('services.azure_tts.key', 'test-key');
    Http::fake([
        '*' => Http::response('Invalid SSML', 400),
    ]);

    $figure = Figure::factory()->create([
        'audio_path' => 'uploads/audio/old.mp3',
        'audio_status' => 'processing',
        'content_blocks' => [
            ['type' => 'paragraph', 'text_en' => 'Some English text.'],
        ],
    ]);
    Storage::disk('public')->put($figure->audio_path, 'old-bytes');

    (new GenerateAudioJob('figure', $figure->id))->handle(app(AzureTextToSpeechService::class));

    $figure->refresh();

    expect($figure->audio_status)->toBe('failed')
        ->and($figure->audio_error)->toContain('Azure TTS API error')
        ->and($figure->audio_path)->toBe('uploads/audio/old.mp3');

    Storage::disk('public')->assertExists('uploads/audio/old.mp3');
});

it('does not store generated audio when the job has been cancelled', function () {
    Storage::fake('public');
    Http::preventStrayRequests();
    config()->set('services.azure_tts.key', 'test-key');

    Http::fake([
        '*' => Http::response('mp3-bytes', 200),
    ]);

    $figure = Figure::factory()->create([
        'audio_status' => 'cancelled',
        'audio_path' => 'uploads/audio/old.mp3',
        'content_blocks' => [
            ['type' => 'paragraph', 'text_en' => 'Some English text.'],
        ],
    ]);
    Storage::disk('public')->put($figure->audio_path, 'old-bytes');

    (new GenerateAudioJob('figure', $figure->id))->handle(app(AzureTextToSpeechService::class));

    $figure->refresh();

    expect($figure->audio_status)->toBe('cancelled')
        ->and($figure->audio_path)->toBe('uploads/audio/old.mp3');

    Storage::disk('public')->assertExists('uploads/audio/old.mp3');
});

it('marks manually uploaded figure audio as completed', function () {
    Storage::fake('public');

    $service = app(FigureService::class);
    $figure = $service->create([
        'name' => 'Ada Lovelace',
        'short_description' => 'Mathematician',
        'key_facts' => [],
        'content_blocks' => [
            ['type' => 'paragraph', 'text_en' => 'She wrote the first algorithm.'],
        ],
        'audio' => UploadedFile::fake()->create('audio.mp3', 10, 'audio/mpeg'),
    ]);

    expect($figure->audio_status)->toBe('completed')
        ->and($figure->audio_error)->toBeNull();
});
