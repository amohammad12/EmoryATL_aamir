import { useState } from 'react'
import ModeTabSwitcher from '@components/ModeTabSwitcher'
import MusicMode from '@components/MusicMode'
import LessonCards from '@components/LessonCards'

export default function Learn() {
  const [activeMode, setActiveMode] = useState<'music' | 'cards'>('music')

  return (
    <div>
      <ModeTabSwitcher activeMode={activeMode} onModeChange={setActiveMode} />
      
      {activeMode === 'music' ? <MusicMode /> : <LessonCards />}
    </div>
  )
}
