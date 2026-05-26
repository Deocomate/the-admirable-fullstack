<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use RuntimeException;

class AzureTextToSpeechService
{
    public function synthesize(array $contentBlocks): string
    {
        $key = config('services.azure_tts.key');

        if (blank($key)) {
            throw new RuntimeException('Azure TTS key is not configured.');
        }

        $ssml = $this->buildSsml($contentBlocks);
        $endpoint = sprintf(
            'https://%s.tts.speech.microsoft.com/cognitiveservices/v1',
            config('services.azure_tts.region', 'eastus')
        );

        $response = Http::connectTimeout(10)
            ->timeout(120)
            ->retry(2, 500, null, false)
            ->withHeaders([
                'Ocp-Apim-Subscription-Key' => $key,
                'Content-Type' => 'application/ssml+xml',
                'X-Microsoft-OutputFormat' => config('services.azure_tts.output_format', 'audio-24khz-48kbitrate-mono-mp3'),
                'User-Agent' => config('app.name', 'Laravel'),
            ])
            ->send('POST', $endpoint, [
                'body' => $ssml,
            ]);

        if ($response->failed()) {
            throw new RuntimeException('Azure TTS API error: '.(string) str($response->body())->limit(500));
        }

        return $response->body();
    }

    public function buildSsml(array $contentBlocks): string
    {
        $text = $this->extractEscapedText($contentBlocks);

        if ($text === '') {
            throw new RuntimeException('No English content is available for audio generation.');
        }

        $voice = config('services.azure_tts.voice', 'en-US-AriaNeural');

        return <<<XML
<speak version="1.0" xml:lang="en-US">
    <voice xml:lang="en-US" name="{$voice}">
        <prosody rate="0%" pitch="0%">
            {$text}
        </prosody>
    </voice>
</speak>
XML;
    }

    public function extractEscapedText(array $contentBlocks): string
    {
        $parts = [];

        foreach ($contentBlocks as $block) {
            $type = $block['type'] ?? '';

            if ($type === 'heading') {
                $this->appendEscaped($parts, $block['text_en'] ?? null);
            }

            if ($type === 'paragraph') {
                $this->appendEscaped($parts, $block['heading_en'] ?? null);
                $this->appendEscaped($parts, $block['text_en'] ?? null);
            }

            if ($type === 'quote') {
                $this->appendEscaped($parts, $block['text_en'] ?? null);
            }
        }

        return implode("\n", $parts);
    }

    private function appendEscaped(array &$parts, ?string $value): void
    {
        $value = trim((string) $value);

        if ($value === '') {
            return;
        }

        $parts[] = htmlspecialchars($value, ENT_XML1 | ENT_QUOTES, 'UTF-8');
    }
}
