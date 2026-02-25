{{-- ── Categories Card ─────────────────────────────────────────────────── --}}
<div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
        </svg>
        Lĩnh vực
    </h2>

    <div class="space-y-2">
        @foreach($categories as $cat)
            <label class="flex items-center gap-2.5 px-3 py-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                <input type="checkbox" name="category_ids[]" value="{{ $cat->id }}"
                       {{ in_array($cat->id, old('category_ids', isset($figure) ? $figure->categories->pluck('id')->toArray() : [])) ? 'checked' : '' }}
                       class="rounded border-gray-300 text-red-600 focus:ring-red-500 w-4 h-4">
                <span class="text-sm text-gray-700">{{ $cat->name }}</span>
            </label>
        @endforeach
    </div>

    @error('category_ids')
        <p class="mt-2 text-xs text-red-600">{{ $message }}</p>
    @enderror
</div>
