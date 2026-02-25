@props(['paginator'])

@if($paginator->hasPages())
<div class="mt-10 flex items-center justify-center gap-1">
    {{-- Previous --}}
    @if($paginator->onFirstPage())
        <span class="w-9 h-9 rounded-full flex items-center justify-center text-apple-gray/30 cursor-not-allowed">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </span>
    @else
        <a href="{{ $paginator->previousPageUrl() }}" class="w-9 h-9 rounded-full flex items-center justify-center text-apple-gray hover:bg-apple-gray-light/50 transition-colors cursor-pointer" aria-label="Trang trước">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
        </a>
    @endif

    {{-- Page Numbers --}}
    @foreach($paginator->getUrlRange(1, $paginator->lastPage()) as $page => $url)
        @if($page == $paginator->currentPage())
            <span class="w-9 h-9 rounded-full flex items-center justify-center text-sm font-medium bg-apple-black text-white">{{ $page }}</span>
        @else
            <a href="{{ $url }}" class="w-9 h-9 rounded-full flex items-center justify-center text-sm font-medium text-apple-gray hover:bg-apple-gray-light/50 transition-colors cursor-pointer">{{ $page }}</a>
        @endif
    @endforeach

    {{-- Next --}}
    @if($paginator->hasMorePages())
        <a href="{{ $paginator->nextPageUrl() }}" class="w-9 h-9 rounded-full flex items-center justify-center text-apple-gray hover:bg-apple-gray-light/50 transition-colors cursor-pointer" aria-label="Trang sau">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </a>
    @else
        <span class="w-9 h-9 rounded-full flex items-center justify-center text-apple-gray/30 cursor-not-allowed">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
        </span>
    @endif
</div>
@endif
