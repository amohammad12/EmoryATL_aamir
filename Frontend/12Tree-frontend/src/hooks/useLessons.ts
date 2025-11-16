export type Lesson = {
  id: string
  label: string
  duration: string
}

export function useLessons() {
  // Placeholder. Replace with GET /lessons
  const lessons: Lesson[] = [
    { id: 'counting', label: 'Counting', duration: '2 minutes' },
    { id: 'letters', label: 'Letters', duration: '3 minutes' },
    { id: 'shapes', label: 'Shapes', duration: '6 minutes' },
  ]
  return { lessons }
}
