<x-client.layout.app title="Về chúng tôi — The Admirable"
                      description="The Admirable là nền tảng học tiếng Anh truyền cảm hứng qua những câu chuyện về các nhân vật vĩ đại."
                      :canonicalUrl="route('client.about-us')"
                      keywords="về chúng tôi, The Admirable, học tiếng anh truyền cảm hứng"
                      activePage="about-us">

    {{-- Hero --}}
    @include('client.about-us._hero')

    {{-- Stats --}}
    @include('client.about-us._stats')

    {{-- Problem & Solution --}}
    @include('client.about-us._problem-solution')

    {{-- Core Values --}}
    @include('client.about-us._core-values')

    {{-- Audience --}}
    @include('client.about-us._audience')

    {{-- CTA --}}
    @include('client.about-us._cta')

</x-client.layout.app>
