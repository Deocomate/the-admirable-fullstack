@props(['figure'])

<a href="{{ route('client.figures.show', $figure->slug) }}"
   class="group block bg-white rounded-2xl overflow-hidden card-hover cursor-pointer h-full flex flex-col">
    <div class="relative aspect-[3/2] overflow-hidden flex-shrink-0">
        <img src="{{ $figure->avatar_path ? asset('storage/' . $figure->avatar_path) : 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=600&h=400&fit=crop' }}"
             alt="{{ $figure->name }}"
             class="img-zoom w-full h-full object-cover" loading="lazy" />
    </div>
    <div class="p-5 flex flex-col flex-1">
        @if($figure->categories->isNotEmpty())
            <p class="text-apple-gray text-[11px] font-semibold uppercase tracking-wider mb-1.5">
                {{ $figure->categories->first()->name }}
            </p>
        @endif
        <h3 class="text-[17px] font-semibold text-apple-black tracking-apple-tight leading-snug mb-2 line-clamp-2">
            {{ $figure->name }}
        </h3>
        <p class="text-apple-gray text-sm leading-relaxed line-clamp-2 mb-3 flex-1">
            {{ $figure->short_description }}
        </p>
        <span class="text-apple-blue text-xs font-normal inline-flex items-center group-hover:underline mt-auto">
            Đọc thêm
            <svg class="w-3 h-3 ml-0.5 transition-transform duration-300 group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
            </svg>
        </span>
    </div>
</a>
