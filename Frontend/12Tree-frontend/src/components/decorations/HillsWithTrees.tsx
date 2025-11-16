import CartoonTree from './CartoonTree'

export default function HillsWithTrees() {
  return (
    <div className="absolute bottom-0 left-0 md:left-7 right-0 pointer-events-none" style={{ zIndex: 1 }}>
      
      {/* Decorative rolling hills on top */}
      <div 
        className="hill" 
        style={{ 
          transform: 'translateY(-10px) scale(1.1)', 
          opacity: 1.0,
          background: 'linear-gradient(180deg, #95D658 0%, #7BC950 100%)'
        }} 
      />
      
      {/* Forest of trees - ALL within green area (35vh from bottom) */}
      {/* Back row - small trees at 18-20vh from bottom (tops at ~30vh) */}
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18vh', left: '8%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '19vh', left: '15%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18vh', left: '22%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18.5vh', left: '32%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18vh', left: '42%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '19vh', left: '52%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18vh', left: '62%' }} />
      <CartoonTree variant={1} className="absolute w-11 h-13 opacity-100" style={{ bottom: '18.5vh', left: '72%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '18vh', left: '82%' }} />
      <CartoonTree variant={2} className="absolute w-11 h-13 opacity-100" style={{ bottom: '19vh', left: '92%' }} />
      
      {/* Middle row - medium trees at 10-11vh from bottom (tops at ~26vh) */}
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '10vh', left: '5%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '10vh', left: '18%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '11vh', left: '28%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '10vh', left: '40%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '11vh', left: '52%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '10vh', left: '62%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '11vh', left: '75%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '10vh', left: '88%' }} />
      
      {/* Front row - larger trees at 2-3vh from bottom (tops at ~22vh) */}
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '2vh', left: '3%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '2vh', left: '15%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '3vh', left: '28%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '2vh', left: '41%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '3vh', left: '54%' }} />
      <CartoonTree variant={1} className="absolute w-12 h-14 opacity-100" style={{ bottom: '2vh', left: '67%' }} />
      <CartoonTree variant={2} className="absolute w-12 h-14 opacity-100" style={{ bottom: '3vh', left: '80%' }} />
      <CartoonTree variant={3} className="absolute w-12 h-14 opacity-100" style={{ bottom: '2vh', left: '93%' }} />
    </div>
  )
}
