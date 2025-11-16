type Props = { label: string; icon?: string }
export default function ModeSwitcher({ label, icon }: Props) {
  return (
    <div className="inline-flex items-center gap-2 px-5 py-2.5 bg-white rounded-full shadow-lg text-base border border-gray-100">
      <span className="w-6 h-6 bg-pink rounded-lg grid place-items-center text-sm">✨</span>
      <span className="font-semibold text-gray-700">{label}</span>
      <span className="text-gray-400 text-sm">▴</span>
    </div>
  )
}
