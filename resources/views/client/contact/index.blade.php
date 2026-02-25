<x-client.layout.app title="Liên hệ — The Admirable"
                      description="Liên hệ với The Admirable — Chúng tôi luôn sẵn sàng lắng nghe và hợp tác cùng bạn."
                      :canonicalUrl="route('client.contact')"
                      keywords="liên hệ, contact, The Admirable, xây dựng website, hợp tác"
                      activePage="contact">

    {{-- Hero --}}
    @include('client.contact._hero')

    {{-- Contact Info --}}
    @include('client.contact._contact-info')

    {{-- Services --}}
    @include('client.contact._services')

    {{-- Buy Me a Coffee --}}
    @include('client.contact._buy-me-a-coffee')

    {{-- CTA --}}
    @include('client.contact._cta')

</x-client.layout.app>
