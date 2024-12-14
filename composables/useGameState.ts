interface Question {
  question: string;
  options: string[];
  correctAnswer: string;
  trivia: string;
}

interface GameState {
  currentQuestion: Question | null;
  questions: Question[];
  usedQuestions: number[];
  gameFinished: boolean;
  correctAnswers: number;
  totalPoints: number;
  remainingJokers: number;
}

export function useGameState(difficulty: string) {
  const getTotalJokers = (difficulty: string): number => {
    switch (difficulty) {
      case 'easy': return 3
      case 'medium': return 5
      case 'hard': return 7
      default: return 3
    }
  }

  const state = reactive<GameState>({
    currentQuestion: null,
    questions: [],
    usedQuestions: [],
    gameFinished: false,
    correctAnswers: 0,
    totalPoints: 0,
    remainingJokers: getTotalJokers(difficulty)
  })

  // Computed Properties
  const maxQuestions = computed(() => {
    switch (difficulty) {
      case 'easy': return 10
      case 'medium': return 15
      case 'hard': return 20
      default: return 10
    }
  })

  // Methoden
  const selectRandomQuestion = () => {
    if (state.usedQuestions.length === state.questions.length) {
      state.usedQuestions = []
    }

    let randomIndex
    do {
      randomIndex = Math.floor(Math.random() * state.questions.length)
    } while (state.usedQuestions.includes(randomIndex))

    state.usedQuestions.push(randomIndex)
    state.currentQuestion = state.questions[randomIndex]
  }

  return {
    ...toRefs(state),
    maxQuestions,
    selectRandomQuestion
  }
}
