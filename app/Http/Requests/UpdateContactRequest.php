<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateContactRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'type'       => ['required', 'string', 'max:50'],
            'label'      => ['required', 'string', 'max:255'],
            'value'      => ['required', 'string', 'max:500'],
            'icon'       => ['nullable', 'string', 'max:100'],
            'sort_order' => ['nullable', 'integer', 'min:0'],
            'is_active'  => ['nullable', 'boolean'],
        ];
    }

    public function messages(): array
    {
        return [
            'type.required'  => 'Loại liên hệ là bắt buộc.',
            'label.required' => 'Nhãn hiển thị là bắt buộc.',
            'value.required' => 'Giá trị liên hệ là bắt buộc.',
        ];
    }
}
