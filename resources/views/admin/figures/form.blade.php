<x-admin.layout.app
    title="{{ isset($figure) ? 'Chỉnh sửa nhân vật' : 'Thêm nhân vật' }}"
    breadcrumb="Admin › Nhân vật › {{ isset($figure) ? 'Chỉnh sửa' : 'Thêm mới' }}">

    <form method="POST"
          action="{{ isset($figure) ? route('admin.figures.update', $figure->id) : route('admin.figures.store') }}"
          enctype="multipart/form-data"
          id="figure-form">
        @csrf
        @if(isset($figure)) @method('PUT') @endif

        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">

            {{-- ═══════════════════════════════════════════════════════════ --}}
            {{-- LEFT COLUMN: Main content                                  --}}
            {{-- ═══════════════════════════════════════════════════════════ --}}
            <div class="xl:col-span-2 space-y-6">

                @include('admin.figures.partials.basic-info-card')
                @include('admin.figures.partials.key-facts-card')
                @include('admin.figures.partials.content-blocks-card')

            </div>

            {{-- ═══════════════════════════════════════════════════════════ --}}
            {{-- RIGHT COLUMN: Media & metadata                             --}}
            {{-- ═══════════════════════════════════════════════════════════ --}}
            <div class="space-y-6">

                @include('admin.figures.partials.media-card')
                @include('admin.figures.partials.categories-card')
                @include('admin.figures.partials.actions-card')

            </div>
        </div>
    </form>

    @include('admin.figures.partials.content-blocks-script')

</x-admin.layout.app>
