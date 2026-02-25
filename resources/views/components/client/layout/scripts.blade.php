<script>
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (mobileMenuBtn && mobileMenu && menuIcon) {
        mobileMenuBtn.addEventListener('click', () => {
            const isOpen = !mobileMenu.classList.contains('hidden');
            if (isOpen) {
                mobileMenu.classList.add('hidden');
                menuIcon.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
                mobileMenuBtn.setAttribute('aria-label', 'Mở menu');
            } else {
                mobileMenu.classList.remove('hidden');
                menuIcon.setAttribute('d', 'M6 18L18 6M6 6l12 12');
                mobileMenuBtn.setAttribute('aria-expanded', 'true');
                mobileMenuBtn.setAttribute('aria-label', 'Đóng menu');
            }
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                mobileMenu.classList.add('hidden');
                menuIcon.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
                mobileMenuBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    let lastScrollY = 0;
    const navbar = document.getElementById('main-navbar');

    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;

        // Back to top visibility
        if (backToTopBtn) {
            if (currentScrollY > 600) {
                backToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
                backToTopBtn.classList.add('opacity-100', 'pointer-events-auto');
            } else {
                backToTopBtn.classList.add('opacity-0', 'pointer-events-none');
                backToTopBtn.classList.remove('opacity-100', 'pointer-events-auto');
            }
        }

        // Navbar hide on scroll down, show on scroll up
        var progressBar = document.getElementById('reading-progress');
        if (navbar && currentScrollY > 80) {
            if (currentScrollY > lastScrollY && currentScrollY > 200) {
                navbar.style.transform = 'translateY(-100%)';
                if (progressBar) progressBar.style.transform = 'translateY(-48px)';
            } else {
                navbar.style.transform = 'translateY(0)';
                if (progressBar) progressBar.style.transform = 'translateY(0)';
            }
        } else if (navbar) {
            navbar.style.transform = 'translateY(0)';
            if (progressBar) progressBar.style.transform = 'translateY(0)';
        }

        lastScrollY = currentScrollY;
    }, { passive: true });
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });


    // Reading progress bar
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = progress + '%';
        }, { passive: true });
    }

    // Audio Player functions
    // Web Audio API context & gain nodes for volume boost beyond 100%
    var audioContext = null;
    var gainNodeMap = new WeakMap();

    // Copy article link with feedback
    function copyArticleLink(btn, url) {
        var copyIcon = btn.querySelector('.copy-icon');
        var checkIcon = btn.querySelector('.check-icon');
        var label = btn.querySelector('.copy-label');

        function showCopiedState(success) {
            if (success) {
                if (copyIcon) copyIcon.classList.add('hidden');
                if (checkIcon) checkIcon.classList.remove('hidden');
                if (label) label.textContent = 'Đã sao chép!';
            } else {
                if (copyIcon) copyIcon.classList.remove('hidden');
                if (checkIcon) checkIcon.classList.add('hidden');
                if (label) label.textContent = 'Không thể sao chép';
            }

            setTimeout(function() {
                if (copyIcon) copyIcon.classList.remove('hidden');
                if (checkIcon) checkIcon.classList.add('hidden');
                if (label) label.textContent = 'Sao chép liên kết';
            }, 2000);
        }

        if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
            navigator.clipboard.writeText(url)
                .then(function() { showCopiedState(true); })
                .catch(function() {
                    // fallback when Clipboard API is blocked
                    var textArea = document.createElement('textarea');
                    textArea.value = url;
                    textArea.setAttribute('readonly', '');
                    textArea.style.position = 'absolute';
                    textArea.style.left = '-9999px';
                    document.body.appendChild(textArea);
                    textArea.select();
                    var success = false;
                    try {
                        success = document.execCommand('copy');
                    } catch (e) {
                        success = false;
                    }
                    document.body.removeChild(textArea);
                    showCopiedState(success);
                });
            return;
        }

        // fallback for browsers/environments without navigator.clipboard (e.g. http/local network)
        var textArea = document.createElement('textarea');
        textArea.value = url;
        textArea.setAttribute('readonly', '');
        textArea.style.position = 'absolute';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.select();
        var success = false;
        try {
            success = document.execCommand('copy');
        } catch (e) {
            success = false;
        }
        document.body.removeChild(textArea);
        showCopiedState(success);
    }

    function getAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioContext;
    }

    function ensureGainNode(audio) {
        if (gainNodeMap.has(audio)) return gainNodeMap.get(audio);
        var ctx = getAudioContext();
        var source = ctx.createMediaElementSource(audio);
        var gainNode = ctx.createGain();
        source.connect(gainNode);
        gainNode.connect(ctx.destination);
        gainNodeMap.set(audio, gainNode);
        return gainNode;
    }

    function formatTime(seconds) {
        if (isNaN(seconds) || !isFinite(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return mins + ':' + (secs < 10 ? '0' : '') + secs;
    }

    function toggleAudio(btn) {
        const container = btn.closest('[data-audio-player]');
        const audio = container.querySelector('.audio-element');
        const playIcon = btn.querySelector('.play-icon');
        const pauseIcon = btn.querySelector('.pause-icon');
        if (!audio) return;

        // Pause all other audio players
        document.querySelectorAll('.audio-element').forEach(function (el) {
            if (el !== audio && !el.paused) {
                el.pause();
                const otherBtn = el.closest('[data-audio-player]').querySelector('.audio-play-btn');
                if (otherBtn) {
                    otherBtn.querySelector('.play-icon').classList.remove('hidden');
                    otherBtn.querySelector('.pause-icon').classList.add('hidden');
                }
            }
        });

        if (audio.paused) {
            // Resume AudioContext if suspended (Chrome autoplay policy)
            if (audioContext && audioContext.state === 'suspended') {
                audioContext.resume();
            }
            audio.play();
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
        } else {
            audio.pause();
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        }

        // Update time display
        audio.addEventListener('loadedmetadata', function () {
            container.querySelector('.audio-duration').textContent = formatTime(audio.duration);
        });
        audio.addEventListener('timeupdate', function () {
            container.querySelector('.audio-current-time').textContent = formatTime(audio.currentTime);
            const seek = container.querySelector('.audio-seek');
            if (audio.duration) {
                seek.value = (audio.currentTime / audio.duration) * 100;
            }
        });
        audio.addEventListener('ended', function () {
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        });
    }

    function seekAudio(input) {
        const container = input.closest('[data-audio-player]');
        const audio = container.querySelector('.audio-element');
        if (audio && audio.duration) {
            audio.currentTime = (input.value / 100) * audio.duration;
        }
    }

    function changeSpeed(select) {
        const container = select.closest('[data-audio-player]');
        const audio = container.querySelector('.audio-element');
        if (audio) {
            audio.playbackRate = parseFloat(select.value);
        }
    }

    function toggleVolumePopup(btn) {
        var popup = btn.closest('.relative').querySelector('.audio-volume-popup');
        var isHidden = popup.classList.contains('hidden');
        // Close all other volume popups first
        document.querySelectorAll('.audio-volume-popup').forEach(function (p) {
            p.classList.add('hidden');
        });
        if (isHidden) {
            popup.classList.remove('hidden');
        }
    }

    function changeVolume(slider) {
        var container = slider.closest('[data-audio-player]');
        var audio = container.querySelector('.audio-element');
        var volumePercent = parseInt(slider.value);
        var label = container.querySelector('.audio-volume-label');
        var valueLabel = slider.closest('.audio-volume-popup').querySelector('.audio-volume-value');

        if (label) label.textContent = volumePercent + '%';
        if (valueLabel) valueLabel.textContent = volumePercent + '%';

        if (audio) {
            if (volumePercent <= 100) {
                audio.volume = volumePercent / 100;
                // Reset gain to 1 if a gain node exists
                if (gainNodeMap.has(audio)) {
                    gainNodeMap.get(audio).gain.value = 1;
                }
            } else {
                // Use Web Audio API GainNode to boost beyond 100%
                audio.volume = 1;
                var gainNode = ensureGainNode(audio);
                gainNode.gain.value = volumePercent / 100;
            }
        }

        // Update volume icon
        updateVolumeIcon(container, volumePercent);
    }

    function updateVolumeIcon(container, percent) {
        var icon = container.querySelector('.volume-icon');
        if (!icon) return;
        if (percent === 0) {
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-3.707C10.923 4.663 12 5.109 12 6v12c0 .891-1.077 1.337-1.707.707L5.586 15z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />';
        } else if (percent <= 100) {
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M6.5 8.5H3a1 1 0 00-1 1v5a1 1 0 001 1h3.5l5 4V4.5l-5 4z" />';
        } else {
            icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M17.95 6.05a8 8 0 010 11.9M6.5 8.5H3a1 1 0 00-1 1v5a1 1 0 001 1h3.5l5 4V4.5l-5 4z" />';
        }
    }

    // Close volume popup when clicking outside
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.audio-volume-btn') && !e.target.closest('.audio-volume-popup')) {
            document.querySelectorAll('.audio-volume-popup').forEach(function (p) {
                p.classList.add('hidden');
            });
        }
    });

    // Init audio durations on page load
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.audio-element').forEach(function (audio) {
            audio.addEventListener('loadedmetadata', function () {
                const container = audio.closest('[data-audio-player]');
                if (container) {
                    container.querySelector('.audio-duration').textContent = formatTime(audio.duration);
                }
            });
        });

        // ─── Scroll-reveal observer ───
        const reveals = document.querySelectorAll('.reveal');
        if (reveals.length && 'IntersectionObserver' in window) {
            const revealObserver = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        revealObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
            reveals.forEach(function (el) { revealObserver.observe(el); });
        }

        // ─── Counter animation (stats numbers) ───
        document.querySelectorAll('[data-count-to]').forEach(function (el) {
            var target = parseInt(el.getAttribute('data-count-to'));
            var suffix = el.getAttribute('data-count-suffix') || '';
            var observed = false;
            var observer = new IntersectionObserver(function (entries) {
                if (entries[0].isIntersecting && !observed) {
                    observed = true;
                    var start = 0;
                    var duration = 1200;
                    var startTime = null;
                    function step(ts) {
                        if (!startTime) startTime = ts;
                        var progress = Math.min((ts - startTime) / duration, 1);
                        var eased = 1 - Math.pow(1 - progress, 3);
                        el.textContent = Math.floor(eased * target) + suffix;
                        if (progress < 1) requestAnimationFrame(step);
                    }
                    requestAnimationFrame(step);
                    observer.unobserve(el);
                }
            }, { threshold: 0.3 });
            observer.observe(el);
        });

        // ─── Typing effect ───
        document.querySelectorAll('[data-typing]').forEach(function (el) {
            var texts = JSON.parse(el.getAttribute('data-typing'));
            var speed = parseInt(el.getAttribute('data-typing-speed') || '80');
            var pause = parseInt(el.getAttribute('data-typing-pause') || '2000');
            var deleteSpeed = parseInt(el.getAttribute('data-typing-delete') || '40');
            var cursor = document.createElement('span');
            cursor.className = 'typing-cursor';
            el.parentNode.insertBefore(cursor, el.nextSibling);
            var idx = 0, charIdx = 0, deleting = false;
            function tick() {
                var current = texts[idx];
                if (!deleting) {
                    el.textContent = current.substring(0, charIdx + 1);
                    charIdx++;
                    if (charIdx >= current.length) {
                        setTimeout(function () { deleting = true; tick(); }, pause);
                        return;
                    }
                    setTimeout(tick, speed);
                } else {
                    el.textContent = current.substring(0, charIdx);
                    charIdx--;
                    if (charIdx < 0) {
                        deleting = false;
                        charIdx = 0;
                        idx = (idx + 1) % texts.length;
                        setTimeout(tick, speed * 2);
                        return;
                    }
                    setTimeout(tick, deleteSpeed);
                }
            }
            tick();
        });

        // ─── Client-side grid pagination ───
        document.querySelectorAll('[data-paginated-grid]').forEach(function (wrapper) {
            var perPage = parseInt(wrapper.getAttribute('data-paginated-grid')) || 6;
            // Responsive: on small screens show fewer per page
            function getPerPage() {
                if (window.innerWidth < 640) return Math.min(perPage, 2);
                if (window.innerWidth < 1024) return Math.min(perPage, 4);
                return perPage;
            }
            var items = wrapper.querySelectorAll('.paginated-item');
            var controls = wrapper.querySelector('.paginated-controls');
            var prevBtn = wrapper.querySelector('.paginated-prev');
            var nextBtn = wrapper.querySelector('.paginated-next');
            var info = wrapper.querySelector('.paginated-info');
            var currentPage = 0;

            if (items.length <= getPerPage()) {
                // No pagination needed
                return;
            }

            controls.classList.remove('hidden');

            function render() {
                var pp = getPerPage();
                var totalPages = Math.ceil(items.length / pp);
                if (currentPage >= totalPages) currentPage = totalPages - 1;
                var start = currentPage * pp;
                var end = start + pp;
                items.forEach(function (item, i) {
                    if (i >= start && i < end) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                });
                info.textContent = (currentPage + 1) + ' / ' + totalPages;
                prevBtn.disabled = currentPage === 0;
                nextBtn.disabled = currentPage >= totalPages - 1;
            }

            prevBtn.addEventListener('click', function () {
                if (currentPage > 0) { currentPage--; render(); }
            });
            nextBtn.addEventListener('click', function () {
                var pp = getPerPage();
                var totalPages = Math.ceil(items.length / pp);
                if (currentPage < totalPages - 1) { currentPage++; render(); }
            });

            window.addEventListener('resize', function () { render(); });
            render();
        });

        // ─── Horizontal scroll arrows ───
        document.querySelectorAll('[data-scroll-section]').forEach(function (section) {
            var container = section.querySelector('.scroll-container');
            var leftBtn = section.querySelector('.scroll-arrow-left');
            var rightBtn = section.querySelector('.scroll-arrow-right');
            if (!container || !leftBtn || !rightBtn) return;

            function updateArrows() {
                var scrollLeft = container.scrollLeft;
                var maxScroll = container.scrollWidth - container.clientWidth;
                if (scrollLeft > 20) {
                    leftBtn.classList.add('visible');
                } else {
                    leftBtn.classList.remove('visible');
                }
                if (scrollLeft < maxScroll - 20) {
                    rightBtn.classList.add('visible');
                } else {
                    rightBtn.classList.remove('visible');
                }
            }

            container.addEventListener('scroll', updateArrows, { passive: true });
            window.addEventListener('resize', updateArrows);
            setTimeout(updateArrows, 100);

            var scrollAmount = container.clientWidth * 0.75;
            leftBtn.addEventListener('click', function () {
                container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            });
            rightBtn.addEventListener('click', function () {
                container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            });
        });
    });
</script>