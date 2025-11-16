import FlashcardViewer from '@components/FlashcardViewer'

const sample = [
  { id: '1', symbol: '1', hint: 'One sun' },
  { id: '2', symbol: '2', hint: 'Two birds' },
  { id: '3', symbol: '3', hint: 'Three apples' },
]

export default function Cards() {
  return (
    <div>
      <div className="mb-4 flex gap-2 flex-wrap">
        {['Counting','Letters','Shapes','Sharing','Helping','Chores'].map((t: string) => (
          <button key={t} className="pill bg-white tap focus-ring" aria-label={`Filter ${t}`}>{t}</button>
        ))}
      </div>
      <FlashcardViewer cards={sample} />
    </div>
  )
}
