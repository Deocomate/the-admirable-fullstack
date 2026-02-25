<x-admin.layout.app
    title="{{ isset($story) ? 'Chỉnh sửa mẩu chuyện' : 'Thêm mẩu chuyện' }}"
    breadcrumb="Admin › Mẩu chuyện › {{ isset($story) ? 'Chỉnh sửa' : 'Thêm mới' }}">

    <form method="POST"
          action="{{ isset($story) ? route('admin.stories.update', $story->id) : route('admin.stories.store') }}"
          enctype="multipart/form-data"
          id="story-form">
        @csrf
        @if(isset($story)) @method('PUT') @endif

        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">

            {{-- ═══════════════════════════════════════════════════════════ --}}
            {{-- LEFT COLUMN: Main content                                  --}}
            {{-- ═══════════════════════════════════════════════════════════ --}}
            <div class="xl:col-span-2 space-y-6">

                @include('admin.stories.partials.basic-info-card')
                @include('admin.stories.partials.content-blocks-card')

            </div>

            {{-- ═══════════════════════════════════════════════════════════ --}}
            {{-- RIGHT COLUMN: Media & actions                              --}}
            {{-- ═══════════════════════════════════════════════════════════ --}}
            <div class="space-y-6">

                @include('admin.stories.partials.media-card')
                @include('admin.stories.partials.actions-card')

            </div>
        </div>
    </form>

    @include('admin.stories.partials.content-blocks-script')

</x-admin.layout.app>
