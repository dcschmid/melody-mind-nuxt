import { ref, computed, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";

// Type definitions for the quiz structure
interface Question {
  question: string;
  options: string[];
  correctAnswer: string;
}

interface Artist {
  questions: {
    [key: string]: Question[]; // Dictionary of difficulty levels to question arrays
  };
}

// Memoized function to shuffle options for better performance
const memoizedShuffleOptions = memoize((options: string[]): string[] => {
  return [...options].sort(() => Math.random() - 0.5);
});

export const useQuestions = (category: string, difficulty: string) => {
  const { locale } = useI18n();

  // Improved typing
  const currentQuestion = ref<Question | null>(null);
  const questions = ref<Question[]>([]);
  const usedQuestions = ref<number[]>([]);
  const currentOptions = ref<string[]>([]);

  // Computed property to determine max questions based on difficulty level
  const maxQuestions = computed(() => {
    switch (difficulty) {
      case "easy":
        return 10;
      case "medium":
        return 15;
      case "hard":
        return 20;
      default:
        return 10;
    }
  });

  // Cache system to store loaded questions and prevent unnecessary API calls
  const questionsCache = new Map<string, Question[]>();
  const cacheKey = `${category}-${difficulty}-${locale.value}`;

  // Improved typing and null check
  const shuffleOptions = (question: Question): string[] => {
    if (!question?.options?.length) return [];
    return memoizedShuffleOptions(question.options);
  };

  /**
   * Loads questions from JSON files based on category and difficulty
   * Uses caching to improve performance on subsequent loads
   */
  const loadQuestions = async () => {
    try {
      // Check cache
      if (questionsCache.has(cacheKey)) {
        questions.value = questionsCache.get(cacheKey)!;
        selectRandomQuestion();
        return;
      }

      const response = await import(
        /* webpackChunkName: "questions-[request]" */
        `~/json/genres/${locale.value}/${category}.json`
      );

      const allQuestions = response.default.reduce((acc: Question[], artist: Artist) => {
        const difficultyQuestions = artist.questions[difficulty] || [];
        return [...acc, ...difficultyQuestions];
      }, []);

      if (allQuestions.length === 0) {
        throw new Error(`No questions found for category ${category} and difficulty ${difficulty}`);
      }

      // Set cache
      questionsCache.set(cacheKey, allQuestions);
      questions.value = allQuestions;
      selectRandomQuestion();
    } catch (error) {
      console.error("Error loading questions:", error);
      throw error;
    }
  };

  /**
   * Selects a random question that hasn't been used yet
   * Resets used questions when all questions have been shown
   * Updates currentQuestion and shuffles its options
   */
  const selectRandomQuestion = async () => {
    if (questions.value.length === 0) return;

    const availableIndices = Array.from({ length: questions.value.length }, (_, i) => i).filter(
      (i) => !usedQuestions.value.includes(i)
    );

    if (availableIndices.length === 0) {
      usedQuestions.value = [];
      return selectRandomQuestion();
    }

    const randomIndex = availableIndices[Math.floor(Math.random() * availableIndices.length)];

    usedQuestions.value.push(randomIndex);
    currentQuestion.value = {
      ...questions.value[randomIndex],
      correctAnswer: questions.value[randomIndex].correctAnswer
    };
    currentOptions.value = shuffleOptions(currentQuestion.value);
  };

  // Cleanup cache when component is unmounted
  onUnmounted(() => {
    questionsCache.clear();
  });

  return {
    currentQuestion,
    questions,
    usedQuestions,
    currentOptions,
    maxQuestions,
    loadQuestions,
    selectRandomQuestion,
  };
};

/**
 * Simple memoization function to cache results of pure functions
 * @param fn The function to memoize
 * @returns Memoized version of the function
 */
function memoize<T extends (...args: any[]) => any>(fn: T) {
  const cache = new Map();
  return (...args: Parameters<T>): ReturnType<T> => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
