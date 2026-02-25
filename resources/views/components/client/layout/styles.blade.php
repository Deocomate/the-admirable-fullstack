<style>
    html {
        scroll-behavior: smooth;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #D2D2D7; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #86868B; }

    /* ─── Card hover (Apple-style subtle lift) ─── */
    .card-hover {
        transition: transform 0.4s cubic-bezier(0.25, 0.1, 0.25, 1), box-shadow 0.4s cubic-bezier(0.25, 0.1, 0.25, 1);
    }
    .card-hover:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    }
    .img-zoom {
        transition: transform 0.7s cubic-bezier(0.25, 0.1, 0.25, 1);
    }
    .group:hover .img-zoom { transform: scale(1.06); }

    /* ─── Scroll-reveal animations ─── */
    .reveal {
        opacity: 0;
        transform: translateY(32px);
        transition: opacity 0.8s cubic-bezier(0.25, 0.1, 0.25, 1), transform 0.8s cubic-bezier(0.25, 0.1, 0.25, 1);
    }
    .reveal.revealed {
        opacity: 1;
        transform: translateY(0);
    }
    .reveal-delay-1 { transition-delay: 0.1s; }
    .reveal-delay-2 { transition-delay: 0.2s; }
    .reveal-delay-3 { transition-delay: 0.3s; }
    .reveal-delay-4 { transition-delay: 0.4s; }

    /* ─── Fade-in-up for hero sections ─── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in-up {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
        opacity: 0;
    }
    .animate-delay-1 { animation-delay: 0.15s; }
    .animate-delay-2 { animation-delay: 0.3s; }
    .animate-delay-3 { animation-delay: 0.45s; }
    .animate-delay-4 { animation-delay: 0.6s; }

    /* ─── Typing cursor blink ─── */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    .typing-cursor {
        display: inline-block;
        width: 2px;
        height: 1em;
        background: #0071E3;
        margin-left: 2px;
        animation: blink 0.8s step-end infinite;
        vertical-align: text-bottom;
    }

    /* ─── Counter animation ─── */
    @keyframes countUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .counter-animate {
        animation: countUp 0.6s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
        opacity: 0;
    }

    /* ─── Horizontal scroll container (for card sections) ─── */
    .scroll-container {
        overflow-x: auto;
        scroll-behavior: smooth;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    .scroll-container::-webkit-scrollbar { display: none; }

    /* ─── Scroll nav arrows ─── */
    .scroll-arrow {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        z-index: 10;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(12px);
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.06);
        color: #1D1D1F;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        opacity: 0;
        pointer-events: none;
    }
    .scroll-arrow:hover {
        background: #fff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transform: translateY(-50%) scale(1.05);
    }
    .scroll-arrow.visible {
        opacity: 1;
        pointer-events: auto;
    }
    .scroll-arrow-left  { left: -16px; }
    .scroll-arrow-right { right: -16px; }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
        .card-hover:hover { transform: none; }
        .group:hover .img-zoom { transform: none; }
        .reveal { opacity: 1; transform: none; }
    }

    .gradient-text {
        background: linear-gradient(135deg, #1D1D1F 0%, #515154 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Reading progress bar */
    #reading-progress {
        position: fixed;
        top: 48px;
        left: 0;
        height: 2px;
        background: #0071E3;
        z-index: 60;
        transition: width 0.1s linear, transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1);
    }

    /* Custom Audio Player Range Input */
    input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none; height: 12px; width: 12px; border-radius: 50%;
        background: #1D1D1F; cursor: pointer; margin-top: -4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    input[type=range]::-webkit-slider-runnable-track {
        width: 100%; height: 4px; cursor: pointer; background: #D2D2D7; border-radius: 2px;
    }
    input[type=range]:focus { outline: none; }

    /* Vertical volume slider */
    .audio-volume-slider {
        writing-mode: vertical-lr;
        direction: rtl;
        width: 28px;
        height: 100px;
        -webkit-appearance: none;
        appearance: none;
        background: transparent;
        cursor: pointer;
    }
    .audio-volume-slider::-webkit-slider-runnable-track {
        width: 4px; height: 100%; background: #D2D2D7; border-radius: 2px;
    }
    .audio-volume-slider::-webkit-slider-thumb {
        -webkit-appearance: none; height: 14px; width: 14px; border-radius: 50%;
        background: #0071E3; cursor: pointer; margin-left: -5px;
        box-shadow: 0 1px 4px rgba(0,113,227,0.4);
    }
    .audio-volume-slider::-moz-range-track {
        width: 4px; background: #D2D2D7; border-radius: 2px;
    }
    .audio-volume-slider::-moz-range-thumb {
        height: 14px; width: 14px; border-radius: 50%; border: none;
        background: #0071E3; cursor: pointer;
        box-shadow: 0 1px 4px rgba(0,113,227,0.4);
    }
</style>
