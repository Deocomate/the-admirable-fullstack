@php
    $audioModel = $audioModel ?? null;
    $audioType = $audioType ?? null;
    $canGenerateAudio = $audioModel && $audioType && $audioModel->exists;
    $audioComponentId = 'audio-generator-' . ($audioType ?? 'new') . '-' . ($audioModel->id ?? 'new');
    $audioStatus = $audioModel->audio_status ?? 'idle';
    $audioError = $audioModel->audio_error ?? null;
@endphp

<div id="{{ $audioComponentId }}"
     data-audio-generator
     @if($canGenerateAudio)
         data-generate-url="{{ route('admin.audio.generate', [$audioType, $audioModel->id]) }}"
         data-cancel-url="{{ route('admin.audio.cancel', [$audioType, $audioModel->id]) }}"
         data-status-url="{{ route('admin.audio.status', [$audioType, $audioModel->id]) }}"
         data-initial-status="{{ $audioStatus }}"
     @endif>
    <div class="flex items-center justify-between gap-3 mb-1.5">
        <label for="audio" class="block text-xs font-medium text-gray-600">
            File Audio (Bài đọc)
        </label>

        @if($canGenerateAudio)
            <button type="button"
                    data-audio-generate-btn
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200 rounded hover:bg-indigo-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                </svg>
                Tạo bằng AI
            </button>
            <button type="button"
                    data-audio-cancel-btn
                    class="{{ $audioStatus === 'processing' ? '' : 'hidden' }} inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-gray-50 text-gray-700 border border-gray-200 rounded hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                Hủy
            </button>
        @endif
    </div>

    <div data-audio-loading class="{{ $audioStatus === 'processing' ? '' : 'hidden' }} mb-3 p-3 bg-blue-50 border border-blue-100 rounded flex items-center gap-3">
        <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <div>
            <p class="text-xs font-semibold text-blue-800">Đang tạo audio...</p>
            <p class="text-[11px] text-blue-600">Bạn có thể tiếp tục làm việc, hệ thống sẽ cập nhật khi xong.</p>
        </div>
    </div>

    <div data-audio-error class="{{ $audioStatus === 'failed' && $audioError ? '' : 'hidden' }} mb-3 p-3 bg-red-50 border border-red-100 rounded">
        <p class="text-xs font-semibold text-red-800 mb-1">Lỗi khi tạo audio:</p>
        <p class="text-[11px] text-red-600" data-audio-error-text>{{ $audioError }}</p>
    </div>

    <div data-audio-cancelled class="{{ $audioStatus === 'cancelled' ? '' : 'hidden' }} mb-3 p-3 bg-gray-50 border border-gray-100 rounded">
        <p class="text-xs font-semibold text-gray-700">Đã hủy tạo audio.</p>
    </div>

    @if($audioModel && $audioModel->audio_path)
        <div class="mb-2" data-audio-player-container>
            <audio controls class="w-full h-9" style="border-radius:6px;" data-audio-player>
                <source src="{{ asset('storage/' . $audioModel->audio_path) }}" type="audio/mpeg" data-audio-source>
            </audio>
            <span class="text-xs text-gray-400 mt-1 block" data-audio-helper>Audio hiện tại. Chọn file mới để thay thế.</span>
        </div>
    @endif

    <input type="file" id="audio" name="audio" accept="audio/mpeg,audio/wav"
           class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-3 file:rounded file:border-0
                  file:text-xs file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
    <p class="mt-1 text-xs text-gray-400">MP3, WAV. Max 20MB.</p>
    @error('audio')
        <p class="mt-1 text-xs text-red-600">{{ $message }}</p>
    @enderror
</div>

@if($canGenerateAudio)
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const root = document.getElementById(@json($audioComponentId));
            if (!root) return;

            const button = root.querySelector('[data-audio-generate-btn]');
            const cancelButton = root.querySelector('[data-audio-cancel-btn]');
            const loading = root.querySelector('[data-audio-loading]');
            const errorBox = root.querySelector('[data-audio-error]');
            const errorText = root.querySelector('[data-audio-error-text]');
            const cancelledBox = root.querySelector('[data-audio-cancelled]');
            const input = root.querySelector('input[type="file"]');
            let pollingInterval = null;

            const setProcessing = (isProcessing) => {
                loading.classList.toggle('hidden', !isProcessing);
                if (button) button.disabled = isProcessing;
                if (cancelButton) {
                    cancelButton.classList.toggle('hidden', !isProcessing);
                    cancelButton.disabled = false;
                }
            };

            const showError = (message) => {
                setProcessing(false);
                errorText.textContent = message || 'Unknown error.';
                errorBox.classList.remove('hidden');
                cancelledBox.classList.add('hidden');
            };

            const showCancelled = () => {
                setProcessing(false);
                errorBox.classList.add('hidden');
                cancelledBox.classList.remove('hidden');
            };

            const updatePlayer = (audioUrl) => {
                if (!audioUrl) return;

                let container = root.querySelector('[data-audio-player-container]');
                let player = root.querySelector('[data-audio-player]');
                let source = root.querySelector('[data-audio-source]');

                if (!container) {
                    container = document.createElement('div');
                    container.className = 'mb-2';
                    container.setAttribute('data-audio-player-container', '');
                    container.innerHTML = `
                        <audio controls class="w-full h-9" style="border-radius:6px;" data-audio-player>
                            <source type="audio/mpeg" data-audio-source>
                        </audio>
                        <span class="text-xs text-green-600 font-medium mt-1 block" data-audio-helper>Audio AI đã tạo thành công.</span>
                    `;
                    root.insertBefore(container, input);
                    player = container.querySelector('[data-audio-player]');
                    source = container.querySelector('[data-audio-source]');
                }

                source.src = audioUrl;
                player.load();

                const helper = container.querySelector('[data-audio-helper]');
                if (helper) {
                    helper.textContent = 'Audio AI đã tạo thành công.';
                    helper.className = 'text-xs text-green-600 font-medium mt-1 block';
                }
            };

            const stopPolling = () => {
                if (pollingInterval) {
                    clearInterval(pollingInterval);
                    pollingInterval = null;
                }
            };

            const checkStatus = async () => {
                try {
                    const response = await fetch(root.dataset.statusUrl, {
                        headers: { 'Accept': 'application/json' },
                    });

                    if (!response.ok) throw new Error('Unable to check audio status.');

                    const data = await response.json();

                    if (data.status === 'processing') {
                        errorBox.classList.add('hidden');
                        cancelledBox.classList.add('hidden');
                        setProcessing(true);
                        return;
                    }

                    if (data.status === 'completed') {
                        stopPolling();
                        setProcessing(false);
                        errorBox.classList.add('hidden');
                        cancelledBox.classList.add('hidden');
                        updatePlayer(data.audio_url);
                        return;
                    }

                    if (data.status === 'failed') {
                        stopPolling();
                        showError(data.error || 'Audio generation failed.');
                        return;
                    }

                    if (data.status === 'cancelled') {
                        stopPolling();
                        showCancelled();
                    }
                } catch (error) {
                    console.error(error);
                }
            };

            const startPolling = () => {
                stopPolling();
                pollingInterval = setInterval(checkStatus, 3000);
            };

            if (button) {
                button.addEventListener('click', async () => {
                    if (!confirm('Hệ thống sẽ tạo audio mới từ nội dung tiếng Anh. Bạn muốn tiếp tục?')) {
                        return;
                    }

                    setProcessing(true);
                    errorBox.classList.add('hidden');
                    cancelledBox.classList.add('hidden');

                    try {
                        const response = await fetch(root.dataset.generateUrl, {
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
                            },
                        });

                        if (response.status === 409) {
                            startPolling();
                            return;
                        }

                        if (!response.ok) {
                            const data = await response.json().catch(() => ({}));
                            throw new Error(data.message || 'Unable to queue audio generation.');
                        }

                        startPolling();
                    } catch (error) {
                        showError(error.message);
                    }
                });
            }

            if (cancelButton) {
                cancelButton.addEventListener('click', async () => {
                    cancelButton.disabled = true;

                    try {
                        const response = await fetch(root.dataset.cancelUrl, {
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
                            },
                        });

                        if (!response.ok && response.status !== 409) {
                            const data = await response.json().catch(() => ({}));
                            throw new Error(data.message || 'Unable to cancel audio generation.');
                        }

                        stopPolling();
                        showCancelled();
                    } catch (error) {
                        showError(error.message);
                    }
                });
            }

            if (root.dataset.initialStatus === 'processing') {
                setProcessing(true);
                startPolling();
            }
        });
    </script>
@endif
