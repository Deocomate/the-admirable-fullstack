{{-- Search Category Pills --}}
<div class="flex flex-wrap justify-center gap-2" role="list" aria-label="Lọc theo lĩnh vực">
    <a href="{{ route('client.search', $query ? ['q' => $query] : []) }}" role="listitem"
       class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-medium {{ !$categorySlug ? 'bg-apple-black text-white' : 'bg-apple-bg text-apple-gray hover:bg-apple-gray-light hover:text-apple-black' }} cursor-pointer transition-all duration-300">
        Tất cả
    </a>
    @foreach($categories as $category)
        @php
            $params = ['category' => $category->slug];
            if ($query) $params['q'] = $query;
        @endphp
        <a href="{{ route('client.search', $params) }}" role="listitem"
           class="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-medium {{ ($categorySlug ?? '') === $category->slug ? 'bg-apple-black text-white shadow-sm' : 'bg-apple-bg text-apple-gray hover:bg-apple-gray-light hover:text-apple-black' }} cursor-pointer transition-all duration-300">
            {{ $category->name }}
        </a>
    @endforeach
</div>
