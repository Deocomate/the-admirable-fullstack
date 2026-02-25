@props([
    'title' => 'The Admirable — Những tấm gương đáng ngưỡng mộ',
    'description' => 'Khám phá những câu chuyện truyền cảm hứng từ các nhân vật nổi tiếng trên thế giới. Luyện IELTS qua bài đọc song ngữ, audio và video.',
    'activePage' => '',
    'canonicalUrl' => null,
    'ogType' => 'website',
    'ogImage' => null,
    'robots' => 'index,follow',
    'keywords' => null,
    'publishedTime' => null,
    'modifiedTime' => null,
    'articleSection' => null,
    'articleTags' => [],
    'jsonLd' => [],
])

@php
    $siteName = config('app.name', 'The Admirable');
    $seoCanonical = $canonicalUrl ?: url()->current();
    $seoImage = $ogImage ?: asset('assets/images/logo.png');
    $seoLocale = str_replace('_', '-', app()->getLocale());

    if (!filter_var($seoImage, FILTER_VALIDATE_URL)) {
        $seoImage = asset(ltrim($seoImage, '/'));
    }

    $defaultJsonLd = [
        '@context' => 'https://schema.org',
        '@type' => 'WebSite',
        'name' => $siteName,
        'url' => url('/'),
        'inLanguage' => 'vi',
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => route('client.search') . '?q={search_term_string}',
            'query-input' => 'required name=search_term_string',
        ],
    ];

    $jsonLdScripts = array_merge([$defaultJsonLd], is_array($jsonLd) ? $jsonLd : []);
@endphp

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ $title }}</title>
    <meta name="description" content="{{ $description }}" />
    <meta name="robots" content="{{ $robots }}" />
    @if($keywords)
        <meta name="keywords" content="{{ $keywords }}" />
    @endif
    <link rel="canonical" href="{{ $seoCanonical }}" />

    <meta property="og:locale" content="{{ $seoLocale }}" />
    <meta property="og:type" content="{{ $ogType }}" />
    <meta property="og:site_name" content="{{ $siteName }}" />
    <meta property="og:title" content="{{ $title }}" />
    <meta property="og:description" content="{{ $description }}" />
    <meta property="og:url" content="{{ $seoCanonical }}" />
    <meta property="og:image" content="{{ $seoImage }}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{{ $title }}" />
    <meta name="twitter:description" content="{{ $description }}" />
    <meta name="twitter:image" content="{{ $seoImage }}" />

    @if($ogType === 'article')
        @if($publishedTime)
            <meta property="article:published_time" content="{{ $publishedTime }}" />
        @endif
        @if($modifiedTime)
            <meta property="article:modified_time" content="{{ $modifiedTime }}" />
        @endif
        @if($articleSection)
            <meta property="article:section" content="{{ $articleSection }}" />
        @endif
        @foreach($articleTags as $tag)
            <meta property="article:tag" content="{{ $tag }}" />
        @endforeach
    @endif

    @foreach($jsonLdScripts as $schema)
        <script type="application/ld+json">{!! json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) !!}</script>
    @endforeach

    <link rel="icon" type="image/x-icon" href="{{ asset('assets/images/logo.ico') }}" />
    <link rel="shortcut icon" href="{{ asset('assets/images/logo.ico') }}" />
           <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Inter"', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
                    },
                    colors: {
                        apple: {
                            black: '#1D1D1F',
                            gray: '#86868B',
                            'gray-light': '#D2D2D7',
                            bg: '#F5F5F7',
                            white: '#FBFBFD',
                            blue: '#0071E3',
                            'blue-hover': '#0077ED',
                        },
                    },
                    letterSpacing: {
                        'apple-tight': '-0.003em',
                        'apple-headline': '-.015em',
                        'apple-display': '-0.04em',
                    },
                },
            },
        };
    </script>

    @include('components.client.layout.styles')
    @stack('styles')
</head>
<body class="bg-apple-white font-sans text-apple-black antialiased">

    <x-client.layout.navbar :activePage="$activePage" />

    @stack('after-navbar')

    <!-- Spacer for fixed navbar -->
    <div class="h-12"></div>

    {{ $slot }}

    <x-client.layout.footer />
    <x-client.layout.back-to-top />


    @include('components.client.layout.scripts')
    @stack('scripts')
</body>
</html>
