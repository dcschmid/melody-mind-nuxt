export interface Question {
  id: string | number
  question: string
  options: string[]
  correctAnswer: string
  category: string
  difficulty: string
  // Zusätzliche musik-spezifische Eigenschaften
  audioUrl?: string
  imageUrl?: string
  points?: number
  explanation?: string
}
