import { ref, onMounted, onUnmounted, computed } from "vue";

/**
 * Custom composable for audio player functionality
 * Provides state management and controls for HTML5 audio playback
 */
export function useAudioPlayer() {
  const UPDATE_INTERVAL = 250; // Throttle update interval in milliseconds

  // Core audio player state
  const audioPlayer = ref<HTMLAudioElement | null>(null);
  const isPlaying = ref(false);
  const currentTime = ref(0);
  const duration = ref(0);
  const audioLoaded = ref(false);
  const error = ref<string | null>(null);
  const isBuffering = ref(false);

  /**
   * Computed property for playback progress as percentage
   */
  const progress = computed(() => {
    if (!duration.value) return 0;
    return (currentTime.value / duration.value) * 100;
  });

  /**
   * Computed properties for formatted time display
   */
  const formattedTime = computed(() => formatTime(currentTime.value));
  const formattedDuration = computed(() => formatTime(duration.value));

  /**
   * Updates current time and duration using requestAnimationFrame for performance
   */
  let timeUpdateFrame: number;
  const updateProgress = () => {
    if (timeUpdateFrame) {
      cancelAnimationFrame(timeUpdateFrame);
    }

    timeUpdateFrame = requestAnimationFrame(() => {
      if (audioPlayer.value) {
        currentTime.value = audioPlayer.value.currentTime;
        duration.value = audioPlayer.value.duration;
      }
    });
  };

  /**
   * Formats time in seconds to MM:SS format
   */
  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  /**
   * Initializes audio player and sets up event listeners
   */
  const initAudioPlayer = () => {
    audioPlayer.value = new Audio();
    audioPlayer.value.preload = "metadata";
    error.value = null;

    // Buffer state handling
    audioPlayer.value.addEventListener("waiting", () => {
      isBuffering.value = true;
    });

    audioPlayer.value.addEventListener("canplay", () => {
      isBuffering.value = false;
    });

    // Throttled time updates
    let lastUpdate = 0;
    audioPlayer.value.addEventListener("timeupdate", () => {
      const now = Date.now();
      if (now - lastUpdate > UPDATE_INTERVAL) {
        updateProgress();
        lastUpdate = now;
      }
    });

    // Audio metadata and state handling
    audioPlayer.value.addEventListener("loadeddata", () => {
      audioLoaded.value = true;
      if (audioPlayer.value) {
        duration.value = audioPlayer.value.duration;
      }
    });

    audioPlayer.value.addEventListener("ended", () => {
      isPlaying.value = false;
      currentTime.value = 0;
    });

    audioPlayer.value.addEventListener("error", (e) => {
      isPlaying.value = false;
      audioLoaded.value = false;
      error.value = `Error loading audio: ${e.type}`;
    });
  };

  /**
   * Toggles play/pause state of audio
   */
  const togglePlay = async () => {
    if (!audioPlayer.value || !audioLoaded.value) return;

    try {
      if (isPlaying.value) {
        await audioPlayer.value.pause();
      } else {
        const playPromise = audioPlayer.value.play();
        if (playPromise !== undefined) {
          await playPromise;
        }
      }
      isPlaying.value = !isPlaying.value;
    } catch (err: unknown) {
      isPlaying.value = false;
      error.value = 'Error playing audio';
    }
  };

  /**
   * Loads new audio source with optimized preloading
   */
  const loadAudio = async (src: string) => {
    if (!audioPlayer.value) return;

    try {
      error.value = null;
      audioPlayer.value.pause();
      isPlaying.value = false;
      currentTime.value = 0;
      audioLoaded.value = false;

      // Check if audio is cached
      const response = await fetch(src, { method: 'HEAD' });
      const cachedResponse = response.headers.get('x-cache');

      audioPlayer.value.src = src;

      // Optimize preloading based on cache status
      if (!cachedResponse?.includes('HIT')) {
        audioPlayer.value.preload = "auto";
      }

      audioPlayer.value.load();
    } catch (err) {
      error.value = 'Error loading audio file';
    }
  };

  /**
   * Cleanup function to remove event listeners and reset state
   */
  const cleanup = () => {
    if (timeUpdateFrame) {
      cancelAnimationFrame(timeUpdateFrame);
    }
    if (audioPlayer.value) {
      audioPlayer.value.removeEventListener("timeupdate", updateProgress);
      audioPlayer.value.removeEventListener("loadeddata", () => {});
      audioPlayer.value.removeEventListener("ended", () => {});
      audioPlayer.value.removeEventListener("error", () => {});
      audioPlayer.value.pause();
      audioPlayer.value.src = "";
      audioPlayer.value.remove();
    }
  };

  /**
   * Seeks to specific time in audio
   */
  const seek = (time: number) => {
    if (!audioPlayer.value || !audioLoaded.value) return;
    audioPlayer.value.currentTime = Math.min(Math.max(0, time), duration.value);
  };

  // Lifecycle hooks
  onMounted(() => {
    initAudioPlayer();
  });

  onUnmounted(() => {
    cleanup();
  });

  // Exposed state and methods
  return {
    audioPlayer,
    isPlaying,
    currentTime,
    duration,
    audioLoaded,
    togglePlay,
    loadAudio,
    error,
    seek,
    progress,
    formattedTime,
    formattedDuration,
    isBuffering,
  };
}
