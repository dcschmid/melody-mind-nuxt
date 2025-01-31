<template>
  <div class="game-over-screen">
    <h1 class="game-over-title">{{ $t('game.gameOver.title') }}</h1>

    <!-- Player Rankings -->
    <div class="player-rankings">
      <h2 class="rankings-title">{{ $t('game.gameOver.rankings') }}</h2>
      <div class="rankings-list">
        <div v-for="(player, index) in sortedPlayers" :key="player.name" 
          class="player-rank" 
          :class="{
            'gold': index === 0,
            'silver': index === 1,
            'bronze': index === 2
          }">
          <div class="rank-position">
            <Icon v-if="index === 0" name="material-symbols:trophy" size="32" class="trophy-icon" />
            <Icon v-else-if="index === 1" name="material-symbols:military-tech" size="32" class="trophy-icon" />
            <Icon v-else-if="index === 2" name="material-symbols:stars" size="32" class="trophy-icon" />
            <span v-else>{{ index + 1 }}</span>
          </div>
          <div class="player-info">
            <div class="player-name">{{ player.name }}</div>
            <div class="player-stats">
              <div class="stat-item">
                <div class="stat-label">{{ $t('game.score') }}</div>
                <div class="stat-value">
                  <Icon name="material-symbols:scoreboard" size="24" />
                  <span class="score">{{ player.score }}</span>
                </div>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <div class="stat-label">{{ $t('game.gameOver.correctAnswers') }}</div>
                <div class="stat-value">
                  <Icon name="material-symbols:check-circle" size="24" />
                  <span class="correct-answers">{{ player.correctAnswers }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <button class="play-again-button" @click="$emit('playAgain')">
        <Icon name="material-symbols:replay" size="24" />
        {{ $t('game.gameOver.playAgain') }}
      </button>
      <NuxtLink :to="localePath('/')" class="menu-button">
        <Icon name="material-symbols:home" size="24" />
        {{ $t('game.gameOver.backToMenu') }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Player {
  name: string;
  score: number;
  correctAnswers: number;
}

const props = defineProps<{
  players: Player[];
}>();

const localePath = useLocalePath();

// Sort players by score in descending order
const sortedPlayers = computed(() => {
  return [...props.players].sort((a, b) => b.score - a.score);
});

defineEmits(['playAgain']);
</script>

<style scoped lang="scss">
@use "sass:color";
@use "@/assets/scss/mixins" as *;

.game-over-screen {
    max-width: 800px;
    margin: 0 auto;
    padding: var(--padding-large);
    text-align: center;

    .game-over-title {
        font-size: var(--font-size-responsive-3xl);
        font-weight: var(--font-weight-bold);
        margin-bottom: var(--padding-large);
        color: var(--primary-color);
        text-align: center;
    }

    .rankings-title {
        font-size: var(--font-size-responsive-xl);
        font-weight: var(--font-weight-semibold);
        margin-bottom: var(--padding-medium);
        color: var(--text-secondary);
    }

    .rankings-list {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-large);

        .player-rank {
            display: flex;
            align-items: center;
            gap: var(--padding-medium);
            padding: var(--padding-medium);
            background: var(--surface-color);
            border-radius: var(--border-radius);
            transition: transform var(--transition-speed) var(--transition-bounce);

            &.gold {
                background: linear-gradient(45deg, #9B6B00, #FFD700); // Dunkleres Gold für besseren Kontrast
                transform: scale(1.05);

                .player-name, .stat-label, .stat-value {
                    color: #000000; // Schwarzer Text auf goldenem Hintergrund für maximalen Kontrast
                }

                .trophy-icon {
                    color: #000000; // Schwarzes Trophy-Icon für besseren Kontrast
                }
            }

            &.silver {
                .trophy-icon {
                    color: #757575; // Dunkleres Silber für besseren Kontrast
                }
            }

            &.bronze {
                .trophy-icon {
                    color: #8B4513; // Dunkleres Bronze für besseren Kontrast
                }
            }

            .rank-position {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 48px;
                height: 48px;
                background: var(--surface-color-light);
                border-radius: 50%;
                font-weight: var(--font-weight-bold);
                font-size: var(--font-size-responsive-md);
            }

            .player-info {
                flex: 1;
                text-align: left;

                .player-name {
                    font-size: var(--font-size-responsive-lg);
                    font-weight: var(--font-weight-bold);
                    margin-bottom: var(--padding-small);
                }

                .player-stats {
                    display: flex;
                    gap: var(--padding-large);
                    align-items: center;

                    .stat-item {
                        display: flex;
                        flex-direction: column;
                        gap: 4px;

                        .stat-label {
                            font-size: var(--font-size-responsive-sm);
                            color: #FFFFFF; // Weißer Text für maximalen Kontrast
                            font-weight: var(--font-weight-medium);
                        }

                        .stat-value {
                            display: flex;
                            align-items: center;
                            gap: 8px;
                            font-size: var(--font-size-responsive-md);
                            font-weight: var(--font-weight-semibold);
                            color: #FFFFFF; // Weißer Text für maximalen Kontrast

                            .score {
                                color: #E5B8FF; // Helleres Lila für besseren Kontrast
                            }

                            .correct-answers {
                                color: #40FFB3; // Helleres Grün für besseren Kontrast
                            }
                        }
                    }

                    .stat-divider {
                        width: 1px;
                        height: 24px;
                        background: var(--surface-color-light);
                    }
                }
            }
        }
    }

    .action-buttons {
        display: flex;
        justify-content: center;
        gap: var(--padding-medium);

        .play-again-button,
        .menu-button {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            padding: var(--padding-small) var(--padding-medium);
            border: none;
            border-radius: var(--border-radius);
            font-size: var(--font-size-responsive-md);
            font-weight: var(--font-weight-semibold);
            cursor: pointer;
            transition: all var(--transition-speed) var(--transition-bounce);
            text-decoration: none;

            &:hover {
                transform: translateY(-2px);
                box-shadow: var(--box-shadow-hover);
            }
        }

        .play-again-button {
            background: var(--primary-color);
            color: var(--surface-color);

            &:hover {
                background: var(--primary-color-dark);
            }
        }

        .menu-button {
            background: var(--surface-color-light);
            color: var(--text-color);

            &:hover {
                background: var(--surface-color-hover);
            }
        }
    }
}

@media (max-width: 640px) {
    .game-over-screen {
        padding: var(--padding-medium);

        .rankings-list .player-rank {
            flex-direction: column;
            text-align: center;
            padding: var(--padding-medium);

            .player-info {
                text-align: center;

                .player-stats {
                    justify-content: center;
                }
            }
        }

        .action-buttons {
            flex-direction: column;
            gap: var(--padding-small);
        }
    }
}

@media (max-width: 600px) {
  .action-buttons {
    flex-direction: column;
    gap: var(--padding-small);
  }
}

.play-again-button,
.menu-button {
  @include button-primary;
  min-width: 180px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--padding-small);
  font-size: var(--font-size-responsive-md);
  font-weight: var(--font-weight-semibold);
  text-decoration: none;
  transition: all 0.2s ease;
  color: var(--background-color); // Maximaler Kontrast mit dunklem Text auf hellem Hintergrund

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
}

.menu-button {
  @include button-secondary;
  background-color: #2d2d2d; // Dunklerer Hintergrund
  color: #ffffff; // Weißer Text für maximalen Kontrast
  border: 2px solid var(--primary-color);

  &:hover {
    background-color: var(--primary-color);
    color: var(--background-color);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>