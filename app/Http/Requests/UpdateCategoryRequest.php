<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateCategoryRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $categoryId = $this->route('category');

        return [
            'name' => ['required', 'string', 'max:255', 'unique:categories,name,' . $categoryId],
        ];
    }

    public function messages(): array
    {
        return [
            'name.required' => 'Tên lĩnh vực là bắt buộc.',
            'name.unique'   => 'Lĩnh vực này đã tồn tại.',
        ];
    }
}
