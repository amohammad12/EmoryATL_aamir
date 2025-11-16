import { useState } from 'react'
import LessonCard from '@components/LessonCard'
import CardViewScreen from '@components/CardViewScreen'
import Toast from '@components/Toast'

// Mock card data for each lesson
const lessonCards: Record<string, Array<{ id: string; front: string; back: string; known: boolean }>> = {
  'Counting': [
    { id: '1', front: 'What comes after 1?', back: '2', known: false },
    { id: '2', front: 'What is 2 + 1?', back: '3', known: false },
    { id: '3', front: 'How many fingers on one hand?', back: '5', known: false },
    { id: '4', front: 'What is 5 + 5?', back: '10', known: false },
  ],
  'Letters': [
    { id: '1', front: 'First letter of the alphabet?', back: 'A', known: false },
    { id: '2', front: 'What comes after A?', back: 'B', known: false },
    { id: '3', front: 'Last letter of the alphabet?', back: 'Z', known: false },
    { id: '4', front: 'What letter makes the "sss" sound?', back: 'S', known: false },
  ],
  'Shapes': [
    { id: '1', front: 'Shape with 3 sides?', back: '△ Triangle', known: false },
    { id: '2', front: 'Shape with 4 equal sides?', back: '■ Square', known: false },
    { id: '3', front: 'Round shape?', back: '● Circle', known: false },
    { id: '4', front: 'Shape with 5 points?', back: '★ Star', known: false },
  ],
  'Sharing': [
    { id: '1', front: 'What does sharing mean?', back: 'Giving to others', known: false },
    { id: '2', front: 'Why do we share?', back: 'To be kind and helpful', known: false },
    { id: '3', front: 'What can we share?', back: 'Toys, food, time', known: false },
  ],
  'Helping': [
    { id: '1', front: 'What does helping mean?', back: 'Making things easier for others', known: false },
    { id: '2', front: 'Name a way to help at home?', back: 'Clean up, set table', known: false },
    { id: '3', front: 'How does helping make you feel?', back: 'Happy and proud', known: false },
  ],
  'Chores': [
    { id: '1', front: 'What is a chore?', back: 'A task or job to do', known: false },
    { id: '2', front: 'Name a chore you do?', back: 'Make bed, wash dishes', known: false },
    { id: '3', front: 'Why do chores?', back: 'To keep our space clean', known: false },
  ],
}

export default function LessonCards() {
  const [activeLesson, setActiveLesson] = useState<string | null>(null)
  const [customTopic, setCustomTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [customCards, setCustomCards] = useState<Array<{ id: string; front: string; back: string; known: boolean }>>([])
  const [showToast, setShowToast] = useState(false)
  const [toastMessage, setToastMessage] = useState('')

  const start = (label: string) => {
    setActiveLesson(label)
    setCustomCards([]) // Clear custom cards when opening preset lesson
  }

  const createCustomCards = async () => {
    if (!customTopic.trim()) return
    
    setLoading(true)
    
    // Generate custom cards based on topic
    // For now, create simple placeholder cards
    const newCards = [
      { id: '1', front: `What is ${customTopic}?`, back: 'Learn through practice!', known: false },
      { id: '2', front: `Key fact about ${customTopic}?`, back: 'Practice makes perfect', known: false },
      { id: '3', front: `Why learn ${customTopic}?`, back: 'To grow and improve!', known: false },
      { id: '4', front: `Fun fact about ${customTopic}?`, back: 'It\'s interesting!', known: false },
    ]
    
    setCustomCards(newCards)
    setActiveLesson(customTopic)
    setLoading(false)
  }
  
  const handleAddToLibrary = () => {
    setToastMessage(`"${activeLesson}" cards added to Your Cards!`)
    setShowToast(true)
  }

  // Show card view screen if a lesson is active
  if (activeLesson) {
    return (
      <div className="relative">
        <CardViewScreen
          songTitle={activeLesson}
          cards={customCards.length > 0 ? customCards : (lessonCards[activeLesson] || [])}
          onClose={() => {
            setActiveLesson(null)
            setCustomCards([])
            setCustomTopic('')
          }}
        />
        
        {/* Add to Library Button - Only for custom cards */}
        {customCards.length > 0 && (
          <button
            onClick={handleAddToLibrary}
            className="fixed bottom-8 right-8 bg-white text-gray-800 font-bold 
                       py-4 px-6 rounded-2xl shadow-2xl hover:shadow-xl 
                       tap focus-ring transition-all flex items-center gap-2 z-50
                       border-2 border-purple">
            <span className="text-2xl">➕</span>
            <span>Add to Library</span>
          </button>
        )}
        
        {/* Toast Notification */}
        {showToast && (
          <Toast
            message={toastMessage}
            icon="🎴"
            onClose={() => setShowToast(false)}
          />
        )}
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Custom Cards Input */}
      <div className="bg-white rounded-3xl p-8 shadow-md mb-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-700 flex items-center gap-2">
          <span className="text-3xl">✨</span> Create Custom Flashcards
        </h2>
        <div className="grid gap-4">
          <input
            id="customTopic"
            className="focus-ring rounded-3xl px-6 py-4 border-2 border-gray-200 outline-none 
                       text-lg bg-white text-center placeholder:text-gray-400
                       focus:border-purple transition-all"
            placeholder="What cards do you want to create?"
            value={customTopic}
            onChange={(e) => setCustomTopic(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                createCustomCards()
              }
            }}
          />
          <button 
            onClick={createCustomCards}
            disabled={loading || !customTopic.trim()}
            className="tap focus-ring bg-gradient-to-r from-purple to-pink text-white 
                       font-bold text-xl rounded-3xl py-4 px-12 shadow-lg mx-auto
                       hover:shadow-xl transition-all disabled:opacity-50 
                       disabled:cursor-not-allowed flex items-center gap-2">
            {loading ? (
              <>
                <span>🌱</span>
                <span>Creating Cards...</span>
              </>
            ) : (
              <>
                <span>🎴</span>
                <span>Create Cards</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Preset Lessons */}
      <div className="bg-white rounded-3xl p-8 shadow-md">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-6 text-gray-700 flex items-center gap-2">
            <span className="text-3xl">✏️</span> Hard skills
          </h2>
          <div className="grid sm:grid-cols-3 gap-6">
            <LessonCard bg="bg-lime" big="1 2 3" label="Counting" duration="2 minutes" onClick={() => start('Counting')} />
            <LessonCard bg="bg-orange" big="A B C" label="Letters" duration="3 minutes" onClick={() => start('Letters')} />
            <LessonCard bg="bg-yellow" big="★ ■" label="Shapes" duration="6 minutes" onClick={() => start('Shapes')} />
          </div>
        </section>
        <section>
          <h2 className="text-2xl font-bold mb-6 text-gray-700 flex items-center gap-2">
            <span className="text-3xl">❤️</span> Life skills
          </h2>
          <div className="grid sm:grid-cols-3 gap-6">
            <LessonCard bg="bg-purple" big="🤝" label="Sharing" duration="3 minutes" onClick={() => start('Sharing')} />
            <LessonCard bg="bg-orange" big="🫱" label="Helping" duration="2 minutes" onClick={() => start('Helping')} />
            <LessonCard bg="bg-pink" big="🧹" label="Chores" duration="4 minutes" onClick={() => start('Chores')} />
          </div>
        </section>
      </div>
    </div>
  )
}
