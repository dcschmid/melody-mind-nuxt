/**
 * Represents an expert's response to a music question
 * @interface ExpertResponse
 */
export interface ExpertResponse {
  /** Name of the expert */
  expert: string
  /** Response message from the expert */
  message: string
  /** Confidence level of the expert (0-100) */
  confidence: number
}

/**
 * Structure for responses by confidence level
 */
interface ExpertResponses {
  high: string[]
  medium: string[]
  low: string[]
}

/**
 * Type for localized responses
 */
export type LocaleResponses = Record<string, ExpertResponses>

/**
 * Defines the different confidence levels for expert responses
 */
export type ConfidenceLevel = 'high' | 'medium' | 'low'

/**
 * Predefined confidence ranges for different levels
 */
const CONFIDENCE_RANGES: Record<ConfidenceLevel, { min: number; max: number }> = {
  high: { min: 85, max: 100 },
  medium: { min: 60, max: 80 },
  low: { min: 35, max: 60 },
}

export const expertTitles = [
  'Dr. Schmidt',
  'Thomas',
  'Sarah',
  'Michael',
  'Lisa',
  'Mark',
  'Alex',
  'Julia',
  'Chris',
  'Max',
  'Emma',
  'David',
  'Sophie',
  'Felix',
  'Laura',
] as const

export const expertResponsesByLocale: LocaleResponses = {
  de: {
    high: [
      'Ohne jeden Zweifel - es ist \'{answer}\'. Ich habe die Original-Aufnahme-Session dokumentiert.',
      'Als langjähriger Produzent des Labels kann ich dir garantieren: Das ist \'{answer}\'.',
      'Oh, das kenne ich in- und auswendig! \'{answer}\' - darauf verwette ich meinen Plattenspieler.',
      'Diese Frage ist ein Heimspiel für mich. Eindeutig \'{answer}\', ich war beim Recording dabei.',
      'Das ist mein absolutes Lieblingsalbum! Natürlich ist es \'{answer}\'.',
      'Diese Aufnahme hat Geschichte geschrieben - definitiv \'{answer}\'.',
      'Ich habe den Song hunderte Male aufgelegt. Ohne Frage \'{answer}\'.',
      'Diese Produktion ist legendär! Kann nur \'{answer}\' sein.',
      'Da muss ich nicht mal nachdenken - \'{answer}\', zu 100%!',
      'Diese Aufnahme hat mein Leben verändert. Es ist \'{answer}\'.',
    ],
    medium: [
      'Moment... ja, ich glaube das müsste \'{answer}\' sein. Die Produktion kommt mir sehr bekannt vor.',
      'Wenn mich mein Gehör nicht täuscht, würde ich auf \'{answer}\' tippen.',
      'Hmm, der Sound erinnert mich stark an \'{answer}\', aber lass mich kurz nachdenken...',
      'Das klingt sehr nach \'{answer}\', aber es gab damals einige ähnliche Produktionen.',
      'Ich würde zu 70% sagen \'{answer}\', aber nagel mich nicht darauf fest.',
      'Kenne ich aus dem Club - sollte \'{answer}\' sein, wenn ich mich recht erinnere.',
      'Hatte ich mal in meiner Sammlung... \'{answer}\', oder?',
      'Das läuft öfter im Radio - müsste \'{answer}\' sein.',
      'Ziemlich sicher \'{answer}\', aber keine Garantie.',
      'Erinnert mich stark an \'{answer}\', bin aber nicht ganz sicher.',
    ],
    low: [
      'Puh, schwierige Frage... spontan würde ich \'{answer}\' raten, aber das ist echt nur geraten.',
      'Oh Mann, das ist nicht meine Ära... vielleicht \'{answer}\'?',
      'Musik ist normalerweise mein Ding, aber hier... \'{answer}\' maybe?',
      '*kratzt sich am Kopf* \'{answer}\'? Aber das ist wirklich nur eine Vermutung!',
      'Wenn ich jetzt raten müsste... \'{answer}\'? Aber ich bin mir echt unsicher.',
      'Das ist nicht meine Expertise, aber könnte \'{answer}\' sein?',
      'Uff, da fragst du den Falschen... \'{answer}\' vielleicht?',
      'Keine Ahnung, aber \'{answer}\' klingt plausibel?',
      'Schwer zu sagen... \'{answer}\'? Aber das ist echt nur geraten!',
      'Da bin ich überfragt... \'{answer}\' würde ich mal tippen.',
    ],
  },
  en: {
    high: [
      'Without any doubt - it\'s \'{answer}\'. I documented the original recording session.',
      'As a long-time producer of the label, I can guarantee you: This is \'{answer}\'.',
      'Oh, I know this inside out! \'{answer}\' - I\'d bet my turntable on it.',
      'This question is home turf for me. Clearly \'{answer}\', I was there during the recording.',
      'This is my absolute favorite album! Of course it\'s \'{answer}\'.',
      'This recording made history - definitely \'{answer}\'.',
      'I\'ve played this song hundreds of times. No question \'{answer}\'.',
      'This production is legendary! Can only be \'{answer}\'.',
      'I don\'t even need to think about it - \'{answer}\', 100%!',
      'This recording changed my life. It\'s \'{answer}\'.',
    ],
    medium: [
      'Hold on... yes, I think it must be \'{answer}\'. The production sounds very familiar.',
      'If my ears don\'t deceive me, I\'d say \'{answer}\'.',
      'Hmm, the sound strongly reminds me of \'{answer}\', but let me think for a moment...',
      'This sounds a lot like \'{answer}\', but there were several similar productions back then.',
      'I\'d say 70% it\'s \'{answer}\', but don\'t hold me to that.',
      'I know it from the club - should be \'{answer}\', if I remember correctly.',
      'Used to have it in my collection... \'{answer}\', right?',
      'It plays often on the radio - must be \'{answer}\'.',
      'Pretty sure it\'s \'{answer}\', but no guarantee.',
      'Strongly reminds me of \'{answer}\', but I\'m not entirely sure.',
    ],
    low: [
      'Phew, tough question... spontaneously I\'d guess \'{answer}\', but that\'s really just a guess.',
      'Oh man, this isn\'t my era... maybe \'{answer}\'?',
      'Music is usually my thing, but here... \'{answer}\' maybe?',
      '*scratches head* \'{answer}\'? But that\'s really just a guess!',
      'If I had to guess now... \'{answer}\'? But I\'m really not sure.',
      'This isn\'t my expertise, but could be \'{answer}\'?',
      'Ugh, you\'re asking the wrong person... \'{answer}\' perhaps?',
      'No idea, but \'{answer}\' sounds plausible?',
      'Hard to say... \'{answer}\'? But that\'s really just guessing!',
      'I\'m stumped here... I\'d guess \'{answer}\'.',
    ],
  },
  es: {
    high: [
      '¡Increíble! ¡Has ganado un LP de Oro! 🏆\n¡Eres un campeón absoluto de la música! Todas las preguntas perfectamente respondidas - ¡solo los mejores de los mejores lo logran!',
      '¡Sensacional! ¡El LP de Oro es tuyo! 🏆\n¡Tu conocimiento musical es verdaderamente extraordinario - una actuación impecable!',
      '¡Asombroso! ¡El LP de Oro te pertenece! 🏆\n¡Eres una enciclopedia musical andante! Una ronda perfecta - ¡simplemente magnífico!',
      '¡Fantástico! ¡Te has ganado más que merecidamente el LP de Oro! 🏆\n¡Tu actuación fue simplemente impecable - eres un verdadero virtuoso de la música!',
      '¡Magistral! ¡El LP de Oro es tuyo! 🏆\n¡Una ronda perfecta - definitivamente eres un genio de la música!',
      '¡Brillante! ¡Un LP de Oro para ti! 🏆\n¡Tu experiencia musical es verdaderamente impresionante - todas las preguntas correctas!',
      '¡Fenomenal! ¡El LP de Oro te pertenece! 🏆\n¡Eres un verdadero conocedor de la música - una actuación impeccable!',
      '¡Magnífico! ¡Te has ganado el LP de Oro! 🏆\n¡Una ronda perfecta - tu conocimiento musical es imbatible!',
      '¡Sobresaliente! ¡El LP de Oro es tuyo! 🏆\n¡Eres un profesional absoluto de la música - todas las preguntas respondidas perfectamente!',
      '¡Legendario! ¡Has ganado el LP de Oro! 🏆\n¡Una actuación perfecta - eres un verdadero maestro de la música!',
    ],
    medium: [
      'Espera... sí, creo que debe ser \'{answer}\'. La producción me suena muy familiar.',
      'Si mis oídos no me engañan, diría \'{answer}\'.',
      'Hmm, el sonido me recuerda mucho a \'{answer}\', pero déjame pensar un momento...',
      'Esto suena mucho a \'{answer}\', pero hubo varias producciones similares en ese entonces.',
      'Diría con un 70% de seguridad que es \'{answer}\', pero no me hagas caso del todo.',
      'Lo conozco del club - debería ser \'{answer}\', si mal no recuerdo.',
      'Lo tenía en mi colección... \'{answer}\', ¿verdad?',
      'Suena a menudo en la radio - debe ser \'{answer}\'.',
      'Bastante seguro de que es \'{answer}\', pero sin garantías.',
      'Me recuerda mucho a \'{answer}\', pero no estoy completamente seguro.',
    ],
    low: [
      'Uf, pregunta difícil... espontáneamente diría \'{answer}\', pero es solo una suposición.',
      'Oh vaya, esta no es mi época... ¿tal vez \'{answer}\'?',
      'La música suele ser lo mío, pero aquí... ¿\'{answer}\' quizás?',
      '*se rasca la cabeza* ¿\'{answer}\'? ¡Pero es realmente solo una suposición!',
      'Si tuviera que adivinar... ¿\'{answer}\'? Pero realmente no estoy seguro.',
      'Esta no es mi especialidad, pero ¿podría ser \'{answer}\'?',
      'Uf, le preguntas a la persona equivocada... ¿\'{answer}\' tal vez?',
      'Ni idea, pero ¿\'{answer}\' suena plausible?',
      'Difícil de decir... ¿\'{answer}\'? ¡Pero esto es solo una suposición!',
      'Estoy perdido aquí... Yo diría \'{answer}\'.',
    ],
  },
  fr: {
    high: [
      'Incroyable ! Tu as gagné un LP d\'Or ! 🏆\nTu es un champion absolu de la musique ! Toutes les questions parfaitement répondues - seuls les meilleurs y parviennent !',
      'Sensationnel ! Le LP d\'Or est à toi ! 🏆\nTes connaissances musicales sont vraiment extraordinaires - une performance impeccable !',
      'Fantastique ! Le LP d\'Or t\'appartient ! 🏆\nTu es une encyclopédie musicale vivante ! Une manche parfaite - simplement grandiose !',
      'Fantastique ! Tu as plus que mérité le LP d\'Or ! 🏆\nTa performance était simplement impeccable - tu es un véritable virtuose de la musique !',
      'Magistral ! Le LP d\'Or est à toi ! 🏆\nUne manche parfaite - tu es définitivement un génie de la musique !',
      'Brillant ! Un LP d\'Or pour toi ! 🏆\nTon expertise musicale est vraiment impressionnante - toutes les réponses correctes !',
      'Phénoménal ! Le LP d\'Or t\'appartient ! 🏆\nTu es un véritable connaisseur de musique - une performance impeccable !',
      'Magnifique ! Tu as gagné le LP d\'Or ! 🏆\nUne manche parfaite - tes connaissances musicales sont imbattables !',
      'Exceptionnel ! Le LP d\'Or est à toi ! 🏆\nTu es un pro absolu de la musique - toutes les questions parfaitement répondues !',
      'Légendaire ! Tu as gagné le LP d\'Or ! 🏆\nUne performance parfaite - tu es un véritable maestro de la musique !',
    ],
    medium: [
      'Attends... oui, je pense que ça doit être \'{answer}\'. La production me semble très familière.',
      'Si mes oreilles ne me trompent pas, je dirais \'{answer}\'.',
      'Hmm, le son me rappelle fortement \'{answer}\', mais laisse-moi réfléchir un moment...',
      'Ça ressemble beaucoup à \'{answer}\', mais il y avait plusieurs productions similaires à l\'époque.',
      'Je dirais à 70% que c\'est \'{answer}\', mais ne me prends pas au mot.',
      'Je le connais du club - ça devrait être \'{answer}\', si je me souviens bien.',
      'Je l\'avais dans ma collection... \'{answer}\', non ?',
      'Ça passe souvent à la radio - ça doit être \'{answer}\'.',
      'Assez sûr que c\'est \'{answer}\', mais pas de garantie.',
      'Ça me rappelle beaucoup \'{answer}\', mais je ne suis pas totalement sûr.',
    ],
    low: [
      'Ouf, question difficile... spontanément je dirais \'{answer}\', mais c\'est vraiment juste une supposition.',
      'Oh là là, ce n\'est pas mon époque... peut-être \'{answer}\' ?',
      'La musique c\'est généralement mon truc, mais là... \'{answer}\' peut-être ?',
      '*se gratte la tête* \'{answer}\' ? Mais c\'est vraiment juste une supposition !',
      'Si je devais deviner... \'{answer}\' ? Mais je ne suis vraiment pas sûr.',
      'Ce n\'est pas mon domaine d\'expertise, mais ça pourrait être \'{answer}\' ?',
      'Aïe, tu demandes à la mauvaise personne... \'{answer}\' peut-être ?',
      'Aucune idée, mais \'{answer}\' semble plausible ?',
      'Difficile à dire... \'{answer}\' ? Mais c\'est vraiment juste une supposition !',
      'Je sèche là... Je dirais \'{answer}\'.',
    ],
  },
  it: {
    high: [
      'Incredibile! Hai vinto un LP d\'Oro! 🏆\nSei un campione assoluto della musica! Tutte le domande perfettamente risposte - solo i migliori dei migliori ci riescono!',
      'Sensazionale! L\'LP d\'Oro è tuo! 🏆\nLa tua conoscenza musicale è davvero straordinaria - una performance impeccabile!',
      'Fantastico! L\'LP d\'Oro è tuo! 🏆\nSei un\'enciclopedia musicale ambulante! Un round perfetto - semplicemente grandioso!',
      'Fantastico! Ti sei più che meritato l\'LP d\'Oro! 🏆\nLa tua performance è stata semplicemente impeccabile - sei un vero virtuoso della musica!',
      'Magistrale! L\'LP d\'Oro è tuo! 🏆\nUn round perfetto - sei decisamente un genio della musica!',
      'Brillante! Un LP d\'Oro per te! 🏆\nLa tua competenza musicale è davvero impressionante - tutte le risposte corrette!',
      'Fenomenale! L\'LP d\'Oro è tuo! 🏆\nSei un vero intenditore di musica - una performance impeccabile!',
      'Magnifico! Ti sei guadagnato l\'LP d\'Oro! 🏆\nUn round perfetto - la tua conoscenza musicale è imbattibile!',
      'Eccezionale! L\'LP d\'Oro è tuo! 🏆\nSei un professionista assoluto della musica - tutte le domande risposte perfettamente!',
      'Leggendario! Hai vinto l\'LP d\'Oro! 🏆\nUna performance perfetta - sei un vero maestro della musica!',
    ],
    medium: [
      'Aspetta... sì, penso che debba essere \'{answer}\'. La produzione mi suona molto familiare.',
      'Se le mie orecchie non mi ingannano, direi \'{answer}\'.',
      'Hmm, il suono mi ricorda molto \'{answer}\', ma fammi pensare un momento...',
      'Suona molto come \'{answer}\', ma c\'erano diverse produzioni similari all\'epoca.',
      'Direi al 70% che è \'{answer}\', ma non prenderlo per certo.',
      'Lo conosco dal club - dovrebbe essere \'{answer}\', se ricordo bene.',
      'Lo avevo nella mia collezione... \'{answer}\', giusto?',
      'Passa spesso alla radio - deve essere \'{answer}\'.',
      'Abbastanza sicuro che sia \'{answer}\', ma nessuna garanzia.',
      'Mi ricorda molto \'{answer}\', ma non sono del tutto sicuro.',
    ],
    low: [
      'Uff, domanda difficile... spontaneamente direi \'{answer}\', ma è davvero solo un\'ipotesi.',
      'Oh cavolo, questa non è la mia epoca... forse \'{answer}\'?',
      'La musica di solito è il mio forte, ma qui... \'{answer}\' forse?',
      '*si gratta la testa* \'{answer}\'? Ma è davvero solo un\'ipotesi!',
      'Se dovessi indovinare... \'{answer}\'? Ma non sono proprio sicuro.',
      'Questa non è la mia specialità, ma potrebbe essere \'{answer}\'?',
      'Uff, stai chiedendo alla persona sbagliata... \'{answer}\' forse?',
      'Non ne ho idea, ma \'{answer}\' suona plausibile?',
      'Difficile da dire... \'{answer}\'? Ma è solo un\'ipotesi!',
      'Sono in difficoltà qui... Direi \'{answer}\'.',
    ],
  },
}

/**
 * Generates a random number between min and max (inclusive)
 */
const getRandomNumber = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

/**
 * Returns a random expert name from the predefined list
 */
const EXPERT_TITLES_LENGTH = expertTitles.length
export const getRandomExpertTitle = (): string =>
  expertTitles[Math.floor(Math.random() * EXPERT_TITLES_LENGTH)]

/**
 * Cache for localized expert responses
 */
const responseCache = new Map<string, string[]>()

/**
 * Retrieves a localized expert response for a specific confidence level
 */
export const getExpertResponse = (confidenceLevel: ConfidenceLevel, locale: string): string => {
  const cacheKey = `${locale}-${confidenceLevel}`

  if (!responseCache.has(cacheKey)) {
    const responses =
      expertResponsesByLocale[locale]?.[confidenceLevel] ??
      expertResponsesByLocale.en[confidenceLevel]
    responseCache.set(cacheKey, responses)
  }

  const responses = responseCache.get(cacheKey)!
  return responses[Math.floor(Math.random() * responses.length)]
}

/**
 * Predefined probabilities for different confidence levels and correctness
 */
const CONFIDENCE_PROBABILITIES = {
  HIGH_THRESHOLD: 0.6,
  MEDIUM_THRESHOLD: 0.8,
  MEDIUM_CORRECT_PROBABILITY: 0.8,
  LOW_CORRECT_PROBABILITY: 0.5,
} as const

/**
 * Generates a complete expert opinion for an answer
 * @param correctAnswer - The correct answer
 * @param options - All possible answer options
 * @param locale - Desired language
 * @returns ExpertResponse object containing expert, message, and confidence
 */
export const generateExpertOpinion = (
  correctAnswer: string,
  options: string[],
  locale: string
): ExpertResponse => {
  const random = Math.random()
  const confidenceLevel: ConfidenceLevel =
    random < CONFIDENCE_PROBABILITIES.HIGH_THRESHOLD
      ? 'high'
      : random < CONFIDENCE_PROBABILITIES.MEDIUM_THRESHOLD
        ? 'medium'
        : 'low'

  const isCorrectAnswer =
    confidenceLevel === 'high'
      ? true
      : confidenceLevel === 'medium'
        ? Math.random() < CONFIDENCE_PROBABILITIES.MEDIUM_CORRECT_PROBABILITY
        : Math.random() < CONFIDENCE_PROBABILITIES.LOW_CORRECT_PROBABILITY

  const { min, max } = CONFIDENCE_RANGES[confidenceLevel]
  const confidence = getRandomNumber(min, max)

  const incorrectOptions = options.filter((o) => o !== correctAnswer)
  const answer = isCorrectAnswer
    ? correctAnswer
    : (incorrectOptions[Math.floor(Math.random() * incorrectOptions.length)] ?? correctAnswer)

  return {
    expert: getRandomExpertTitle(),
    message: getExpertResponse(confidenceLevel, locale).replace('{answer}', answer),
    confidence,
  }
}
