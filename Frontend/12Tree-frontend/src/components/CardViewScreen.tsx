import { useState } from 'react'

interface Card {
  id: string
  front: string
  back: string
  known: boolean
}

interface CardViewScreenProps {
  songTitle: string
  cards: Card[]
  onClose: () => void
  onMarkKnown?: (cardId: string) => void
}

export default function CardViewScreen({
  songTitle,
  cards,
  onClose,
  onMarkKnown
}: CardViewScreenProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [cardStates, setCardStates] = useState(cards)
  
  const currentCard = cardStates[currentIndex]
  const knownCount = cardStates.filter(c => c.known).length
  
  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % cardStates.length)
    setIsFlipped(false)
  }
  
  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + cardStates.length) % cardStates.length)
    setIsFlipped(false)
  }
  
  const handleMarkKnown = () => {
    setCardStates(prev => prev.map((card, idx) => 
      idx === currentIndex ? { ...card, known: !card.known } : card
    ))
    if (onMarkKnown) {
      onMarkKnown(currentCard.id)
    }
  }
  
  const handleShuffle = () => {
    const shuffled = [...cardStates].sort(() => Math.random() - 0.5)
    setCardStates(shuffled)
    setCurrentIndex(0)
    setIsFlipped(false)
  }
  
  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto">
      {/* Header */}
      <button 
        onClick={onClose}
        className="flex items-center gap-2 text-gray-700 font-bold mb-6 
                   hover:text-pink tap focus-ring">
        <span className="text-2xl">←</span>
        <span>Back</span>
      </button>
      
      {/* Title */}
      <div className="text-center mb-8">
        <h1 className="gradient-title text-4xl font-extrabold mb-2"
            data-text={`${songTitle} – Cards`}>
          {songTitle} – Cards
        </h1>
        <p className="text-gray-600 font-semibold text-lg">
          Learn with interactive flashcards
        </p>
      </div>
      
      {/* Progress */}
      <div className="bg-white rounded-3xl shadow-md p-4 mb-6 
                      flex items-center justify-between">
        <span className="font-bold text-gray-800">
          Card {currentIndex + 1} of {cardStates.length}
        </span>
        <div className="flex items-center gap-2">
          <span className="text-2xl">⭐</span>
          <span className="font-bold text-gray-800">
            {knownCount}/{cardStates.length} Known
          </span>
        </div>
      </div>
      
      {/* Card Display */}
      <div className="mb-8 flex justify-center">
        <div 
          className="relative w-full max-w-md aspect-[3/4]"
          style={{ perspective: '1000px' }}
          onClick={() => setIsFlipped(!isFlipped)}
        >
          <div 
            className="relative w-full h-full transition-transform duration-600"
            style={{
              transformStyle: 'preserve-3d',
              transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)'
            }}
          >
            {/* Front */}
            <div 
              className="absolute inset-0 bg-white rounded-3xl shadow-2xl 
                          p-12 flex flex-col items-center justify-center cursor-pointer 
                          border-4 border-pink"
              style={{ backfaceVisibility: 'hidden' }}
            >
              <div className="text-3xl font-bold text-gray-800 text-center mb-6">
                {currentCard.front}
              </div>
              <div className="text-gray-500 font-medium">
                Click to reveal ✨
              </div>
            </div>
            
            {/* Back */}
            <div 
              className="absolute inset-0 bg-gradient-to-br from-lime to-green-400 
                          rounded-3xl shadow-2xl p-12 flex flex-col items-center 
                          justify-center cursor-pointer"
              style={{ 
                backfaceVisibility: 'hidden',
                transform: 'rotateY(180deg)'
              }}
            >
              <div className="text-4xl font-extrabold text-white text-center 
                              drop-shadow-lg">
                {currentCard.back}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Navigation */}
      <div className="flex items-center justify-center gap-6 mb-6">
        <button 
          onClick={handlePrev}
          disabled={cardStates.length <= 1}
          className="w-14 h-14 rounded-2xl border-2 border-gray-200 
                     hover:bg-gray-50 hover:border-pink flex items-center 
                     justify-center tap focus-ring text-2xl
                     disabled:opacity-50 disabled:cursor-not-allowed">
          ⬅️
        </button>
        
        <div className="text-gray-600 font-bold">
          Swipe or use arrows
        </div>
        
        <button 
          onClick={handleNext}
          disabled={cardStates.length <= 1}
          className="w-14 h-14 rounded-2xl border-2 border-gray-200 
                     hover:bg-gray-50 hover:border-pink flex items-center 
                     justify-center tap focus-ring text-2xl
                     disabled:opacity-50 disabled:cursor-not-allowed">
          ➡️
        </button>
      </div>
      
      {/* Actions */}
      <div className="flex items-center justify-center gap-4 flex-wrap">
        <button 
          onClick={handleShuffle}
          className="px-6 py-3 rounded-2xl border-2 border-gray-200 
                     hover:bg-gray-50 hover:border-purple font-bold 
                     text-gray-700 tap focus-ring">
          🔀 Shuffle
        </button>
        
        <button 
          onClick={handleMarkKnown}
          className={`px-6 py-3 rounded-2xl font-bold tap focus-ring ${
            currentCard.known
              ? 'bg-lime text-white shadow-md'
              : 'border-2 border-gray-200 hover:bg-gray-50 hover:border-lime text-gray-700'
          }`}>
          {currentCard.known ? '✓ Known' : 'Mark as Known'}
        </button>
        
        <button className="px-6 py-3 rounded-2xl border-2 border-gray-200 
                           hover:bg-gray-50 hover:border-orange font-bold 
                           text-gray-700 tap focus-ring">
          🔊 Replay Audio
        </button>
      </div>
    </div>
  )
}
