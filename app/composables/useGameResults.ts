import { ref, computed, markRaw } from "vue";
import { useI18n } from "vue-i18n";
import { goldMessages } from "../constants/messages/goldMessages";
import { silverMessages } from "../constants/messages/silverMessages";
import { bronzeMessages } from "../constants/messages/bronzeMessages";
import { participationMessages } from "../constants/messages/participationMessages";
import { useGameScore } from "~/composables/useGameScore";

/**
 * Message mapping for different reward levels.
 * Using markRaw to prevent Vue from making this reactive unnecessarily.
 */
const messageMap = markRaw({
  gold: goldMessages,
  silver: silverMessages,
  bronze: bronzeMessages,
  none: participationMessages,
});

/** Possible reward types that can be earned */
type RewardType = "gold" | "silver" | "bronze" | "none";

/**
 * Cache for threshold calculations to avoid recalculating same results
 * Key format: `${correctAnswers}-${maxQuestions}-${allQuestionsCorrect}`
 */
const thresholdChecks = new Map<string, RewardType>();

/**
 * Composable for handling game results and rewards
 * @param config Configuration object with threshold values for different reward levels
 * @returns Object containing result message, earned record, and save function
 */
export const useGameResults = (
  config = {
    thresholds: {
      gold: 1,
      silver: 0.75,
      bronze: 0.5,
    },
  }
) => {
  const { locale } = useI18n();
  const { saveGameScore } = useGameScore();
  const resultMessage = ref("");
  const earnedRecord = ref<RewardType>("none");

  /**
   * Memoized message lengths for each reward type in current locale
   * Prevents recalculating lengths on every access
   */
  const messageLengths = computed(() => ({
    gold: messageMap.gold[locale.value]?.length ?? 0,
    silver: messageMap.silver[locale.value]?.length ?? 0,
    bronze: messageMap.bronze[locale.value]?.length ?? 0,
    none: messageMap.none[locale.value]?.length ?? 0,
  }));

  /**
   * Gets a random message from the provided message array
   * @param messages Message array for specific reward type
   * @returns Random message string
   */
  const getRandomMessage = (messages: typeof messageMap[RewardType]) => {
    const length =
      messageLengths.value[
        messages === goldMessages
          ? "gold"
          : messages === silverMessages
          ? "silver"
          : messages === bronzeMessages
          ? "bronze"
          : "none"
      ];
    return messages[locale.value][Math.floor(Math.random() * length)];
  };

  /**
   * Calculates the reward type based on game performance
   * Uses caching to avoid recalculating same scenarios
   */
  const calculateReward = (correctAnswers: number, maxQuestions: number, allQuestionsCorrect: boolean): RewardType => {
    const key = `${correctAnswers}-${maxQuestions}-${allQuestionsCorrect}`;

    if (thresholdChecks.has(key)) {
      return thresholdChecks.get(key)!;
    }

    let reward: RewardType = "none";
    const ratio = correctAnswers / maxQuestions;

    if (allQuestionsCorrect || ratio >= config.thresholds.gold) reward = "gold";
    else if (ratio >= config.thresholds.silver) reward = "silver";
    else if (ratio >= config.thresholds.bronze) reward = "bronze";

    thresholdChecks.set(key, reward);
    return reward;
  };

  /**
   * Saves game results and sets appropriate reward message
   */
  const saveGameResults = async (
    category: string,
    totalPoints: number,
    correctAnswers: number,
    maxQuestions: number,
    allQuestionsCorrect: boolean,
    difficulty: string,
  ) => {
    try {
      const reward = calculateReward(correctAnswers, maxQuestions, allQuestionsCorrect);
      resultMessage.value = getRandomMessage(messageMap[reward]);
      earnedRecord.value = reward;

      if (reward !== "none") {
        await saveGameScore(category, totalPoints, reward, locale.value, difficulty);
      }
    } catch (error) {
      console.error("Error saving game results:", error);
    }
  };

  const getResultMessage = (reward: RewardType) => {
    return getRandomMessage(messageMap[reward]);
  };

  return {
    resultMessage,
    earnedRecord,
    saveGameResults,
    calculateReward,
    getResultMessage,
  };
};
