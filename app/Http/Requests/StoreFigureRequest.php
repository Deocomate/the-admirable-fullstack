<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreFigureRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name'                        => ['required', 'string', 'max:255'],
            'short_description'           => ['nullable', 'string', 'max:1000'],
            'key_facts'                   => ['nullable', 'array'],
            'key_facts.*.label'           => ['nullable', 'string', 'max:100'],
            'key_facts.*.value'           => ['nullable', 'string', 'max:255'],
            'content_blocks'              => ['required', 'array', 'min:1'],
            'content_blocks.*.type'       => ['required', 'string', 'in:paragraph,quote,heading'],
            'content_blocks.*.heading_en' => ['nullable', 'string', 'max:500'],
            'content_blocks.*.text_en'    => ['nullable', 'string'],
            'content_blocks.*.text_vi'    => ['nullable', 'string'],
            'content_blocks.*.author'     => ['nullable', 'string', 'max:255'],
            'avatar'                      => ['nullable', 'image', 'mimes:jpg,jpeg,png,webp', 'max:5120'],
            'audio'                       => ['nullable', 'file', 'mimes:mp3,wav', 'max:20480'],
            'youtube_url'                 => ['nullable', 'url', 'max:500'],
            'category_ids'                => ['nullable', 'array'],
            'category_ids.*'              => ['integer', 'exists:categories,id'],
        ];
    }

    public function messages(): array
    {
        return [
            'name.required'            => 'Tên nhân vật là bắt buộc.',
            'content_blocks.required'  => 'Vui lòng thêm ít nhất một block nội dung.',
            'content_blocks.min'       => 'Vui lòng thêm ít nhất một block nội dung.',
            'avatar.image'             => 'Ảnh đại diện phải là file ảnh.',
            'avatar.mimes'             => 'Ảnh đại diện phải có định dạng: jpg, jpeg, png, webp.',
            'avatar.max'               => 'Ảnh đại diện không được vượt quá 5MB.',
            'audio.mimes'              => 'File audio phải có định dạng: mp3, wav.',
            'audio.max'                => 'File audio không được vượt quá 20MB.',
            'youtube_url.url'          => 'Link YouTube không hợp lệ.',
        ];
    }
}
