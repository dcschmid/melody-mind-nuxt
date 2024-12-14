export function useJokers() {
  const audienceHelp = ref<Record<string, number>>({})
  const phoneExpertOpinion = ref<ExpertOpinion | null>(null)
  const hiddenOptions = ref<string[]>([])
  const jokerUsedForCurrentQuestion = ref(false)

  const useFiftyFiftyJoker = (question: Question) => {
    const wrongOptions = question.options.filter(
      option => option !== question.correctAnswer
    )
    hiddenOptions.value = shuffle(wrongOptions).slice(0, 2)
    jokerUsedForCurrentQuestion.value = true
  }

  const useAudienceJoker = (question: Question) => {
    // Implementierung wie bisher...
  }

  const usePhoneJoker = (question: Question) => {
    // Implementierung wie bisher...
  }

  return {
    audienceHelp,
    phoneExpertOpinion,
    hiddenOptions,
    jokerUsedForCurrentQuestion,
    useFiftyFiftyJoker,
    useAudienceJoker,
    usePhoneJoker
  }
} 
