@props([
    'categories',
    'activeSlug' => null,
])

<div class="flex flex-wrap justify-center gap-2" role="list" aria-label="Lĩnh vực">
    <a href="{{ route('client.categories.index') }}" role="listitem"
       class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-medium {{ !$activeSlug ? 'bg-apple-black text-white' : 'bg-apple-bg text-apple-gray hover:bg-apple-gray-light hover:text-apple-black' }} cursor-pointer transition-all duration-300">
        Tất cả
    </a>
    @foreach($categories as $category)
        <a href="{{ route('client.categories.show', $category->slug) }}" role="listitem"
           class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-medium {{ $activeSlug === $category->slug ? 'bg-apple-black text-white shadow-sm' : 'bg-apple-bg text-apple-gray hover:bg-apple-gray-light hover:text-apple-black' }} cursor-pointer transition-all duration-300">
            {{ $category->name }}
        </a>
    @endforeach
</div>
