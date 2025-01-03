import { useAudioPlayer } from './useAudioPlayer'

/**
 * A composable function that manages audio playback for the game
 * by wrapping the useAudioPlayer functionality with game-specific features
 * @returns {Object} An object containing audio control methods and state
 */
export function useGameAudio() {
  // Destructure all necessary methods and properties from useAudioPlayer
  const {
    isPlaying,      // Boolean ref indicating if audio is currently playing
    currentTime,    // Current playback position in seconds
    duration,       // Total duration of audio in seconds
    audioLoaded,    // Boolean ref indicating if audio file is loaded
    error,          // Error state if audio loading/playback fails
    progress,       // Playback progress as percentage (0-100)
    formattedTime,  // Current time formatted as MM:SS
    formattedDuration, // Total duration formatted as MM:SS
    isBuffering,    // Boolean ref indicating if audio is buffering
    togglePlay,     // Function to toggle play/pause
    loadAudio       // Function to load new audio file
  } = useAudioPlayer()

  /**
   * Handles changing the current artist and loads their preview audio
   * @param {Object} artist - The artist object containing preview_link
   * @returns {Promise<void>}
   */
  const handleArtistChange = async (artist: any) => {
    if (!artist?.preview_link) return
    await loadAudio(artist.preview_link)
  }

  /**
   * Cleanup function to stop audio playback
   * Typically used when component is unmounted
   */
  const cleanup = () => isPlaying.value && togglePlay()

  // Return all necessary methods and properties
  return {
    isPlaying,
    currentTime,
    duration,
    audioLoaded,
    error,
    isBuffering,
    progress,
    formattedTime,
    formattedDuration,
    togglePlay,
    handleArtistChange,
    cleanup
  }
}
