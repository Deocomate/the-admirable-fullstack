<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreStorySnippetRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'figure_id'                    => ['required', 'integer', 'exists:figures,id'],
            'title'                        => ['required', 'string', 'max:255'],
            'subtitle'                     => ['nullable', 'string', 'max:500'],
            'content_blocks'               => ['required', 'array', 'min:1'],
            'content_blocks.*.type'        => ['required', 'string', 'in:paragraph,heading,quote'],
            'content_blocks.*.text_en'     => ['required', 'string'],
            'content_blocks.*.text_vi'     => ['nullable', 'string'],
            'content_blocks.*.heading_en'  => ['nullable', 'string', 'max:500'],
            'content_blocks.*.author'      => ['nullable', 'string', 'max:255'],
            'image'                        => ['nullable', 'image', 'mimes:jpg,jpeg,png,webp', 'max:5120'],
            'audio'                        => ['nullable', 'file', 'mimes:mp3,wav', 'max:20480'],
            'youtube_url'                  => ['nullable', 'url', 'max:500'],
        ];
    }

    public function messages(): array
    {
        return [
            'figure_id.required'         => 'Phải chọn nhân vật cho mẩu chuyện.',
            'figure_id.exists'           => 'Nhân vật không tồn tại.',
            'title.required'             => 'Tiêu đề mẩu chuyện là bắt buộc.',
            'content_blocks.required'    => 'Phải có ít nhất 1 đoạn văn nội dung.',
            'content_blocks.min'         => 'Phải có ít nhất 1 đoạn văn nội dung.',
            'content_blocks.*.text_en.required' => 'Nội dung tiếng Anh là bắt buộc cho mỗi đoạn văn.',
            'image.image'                => 'File phải là ảnh.',
            'image.mimes'                => 'Ảnh phải có định dạng: jpg, jpeg, png, webp.',
            'image.max'                  => 'Ảnh không được vượt quá 5MB.',
            'audio.mimes'                => 'File audio phải có định dạng: mp3, wav.',
            'audio.max'                  => 'File audio không được vượt quá 20MB.',
            'youtube_url.url'            => 'Link YouTube không hợp lệ.',
        ];
    }
}
