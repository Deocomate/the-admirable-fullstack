<!DOCTYPE html>
<html lang="vi" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{{ $title ?? 'Admin' }} — The Admirable</title>

    {{-- TailwindCSS CDN --}}
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'Roboto', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            red:       '#A31D1D',
                            'red-dark':'#8A1818',
                        },
                    },
                },
            },
        };
    </script>

    {{-- Google Fonts: Inter --}}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        body { font-family: 'Inter', sans-serif; }

        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    </style>
</head>
<body class="h-full" style="background:#F3F6F9;">

    <div class="flex h-full min-h-screen">

        {{-- Sidebar --}}
        <x-admin.layout.sidebar />

        {{-- Main content --}}
        <div class="flex-1 flex flex-col min-h-screen" style="margin-left:16rem;">

            {{-- Top Header --}}
            <header class="sticky top-0 z-30 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                <div>
                    <h1 class="text-base font-semibold text-gray-800">{{ $title ?? 'Dashboard' }}</h1>
                    @isset($breadcrumb)
                        <p class="text-xs text-gray-400 mt-0.5">{{ $breadcrumb }}</p>
                    @endisset
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-xs text-gray-400">
                        {{ now()->format('d/m/Y') }}
                    </span>
                </div>
            </header>

            {{-- Flash messages --}}
            @if(session('success'))
                <div class="mx-6 mt-4 flex items-center gap-3 px-4 py-3 rounded text-sm text-green-800 bg-green-50 border border-green-200">
                    <svg class="w-4 h-4 flex-shrink-0 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                    {{ session('success') }}
                </div>
            @endif
            @if(session('error'))
                <div class="mx-6 mt-4 flex items-center gap-3 px-4 py-3 rounded text-sm text-red-800 bg-red-50 border border-red-200">
                    <svg class="w-4 h-4 flex-shrink-0 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                    {{ session('error') }}
                </div>
            @endif

            {{-- Page content --}}
            <main class="flex-1 p-6">
                {{ $slot }}
            </main>
        </div>
    </div>

</body>
</html>
