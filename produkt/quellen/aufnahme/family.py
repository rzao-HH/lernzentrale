def body(fill,mouth,extra=''):
    return ('<g stroke="%s" stroke-width="3" stroke-linecap="round" fill="none"><path d="M20 46 L8 54 M24 50 L14 60 M60 46 L72 54 M56 50 L66 60"></path></g>'
     '<ellipse cx="40" cy="42" rx="24" ry="16" fill="%s"></ellipse><path d="M32 28 L32 20 M48 28 L48 20" stroke="%s" stroke-width="3" stroke-linecap="round"></path>'
     '<circle cx="32" cy="16" r="6" fill="#fff"></circle><circle cx="48" cy="16" r="6" fill="#fff"></circle><circle cx="33" cy="16" r="2.6" fill="#0A1B27"></circle><circle cx="49" cy="16" r="2.6" fill="#0A1B27"></circle>'
     '%s%s')%(fill,fill,fill,mouth,extra)
def family(w=200,style=''):
    mom=('<g transform="translate(0,30) scale(1.25)">'
      '<path d="M22 36 Q8 34 8 22" stroke="#FF7A5C" stroke-width="3" stroke-linecap="round" fill="none"></path><circle cx="8" cy="17" r="9" fill="#FF7A5C"></circle>'
      +body('#FF7A5C','<path d="M33 46 Q40 52 47 46" stroke="#7A2A1A" stroke-width="2.4" fill="none" stroke-linecap="round"></path>',
       '<path d="M36 6 L40 10 L44 6 L44 14 L40 10 L36 14Z" fill="#e8559a"></path>')+'</g>')
    kid=('<g class="hop">'
      '<path d="M22 36 Q10 30 12 18" stroke="#ff9a80" stroke-width="3" stroke-linecap="round" fill="none"></path><circle cx="12" cy="14" r="7" fill="#ff9a80"></circle>'
      '<path d="M58 36 Q70 30 68 18" stroke="#ff9a80" stroke-width="3" stroke-linecap="round" fill="none"></path><circle cx="68" cy="14" r="7" fill="#ff9a80"></circle>'
      +body('#ff9a80','<path d="M32 44 Q40 55 48 44 Z" fill="#7A2A1A"></path>')+'</g>')
    hug=('<path d="M70 82 Q104 70 140 84" stroke="#FF7A5C" stroke-width="4.5" stroke-linecap="round" fill="none"></path>'
         '<circle cx="143" cy="88" r="9" fill="#FF7A5C"></circle><path d="M143 88 L149 82" stroke="#C94F36" stroke-width="2" stroke-linecap="round"></path>')
    hearts=''.join('<path class="heart" style="animation-delay:%ss" d="M%d 48 c-3 -4 -9 -1 -6 4 l6 6 l6 -6 c3 -5 -3 -8 -6 -4z" fill="#e8559a"></path>'%(d,x) for d,x in [(0,128),(-0.9,148),(-1.8,112)])
    bubble=('<g transform="translate(0,-14)"><g class="praise"><rect x="2" y="0" width="112" height="30" rx="15" fill="#ffffff" stroke="#FF7A5C" stroke-width="2"></rect>'
      '<path d="M40 30 L46 38 L52 30Z" fill="#ffffff" stroke="#FF7A5C" stroke-width="2"></path><path d="M41 29 L51 29" stroke="#ffffff" stroke-width="3"></path>'
      '<text x="58" y="20" text-anchor="middle" font-family="Fredoka, sans-serif" font-size="15" font-weight="600" fill="#1c2140">Toll gemacht!</text></g></g>')
    return ('<svg class="krabbi" viewBox="0 -16 180 161" width="%d" height="%d" aria-hidden="true" style="%s">'%(w,int(w*161/180),style)
      +hearts+mom+hug+kid+bubble+'</svg>')
CSS='''.hop{animation:hop 1.2s ease-in-out infinite}
@keyframes hop{0%,100%{transform:translate(80px,64px) scale(.82) translate(40px,42px) rotate(-6deg) translate(-40px,-42px)}50%{transform:translate(80px,62px) scale(.82) translate(40px,42px) rotate(6deg) translate(-40px,-42px)}}
.heart{opacity:0;transform-box:fill-box;animation:heart 2.7s ease-out infinite}
@keyframes heart{0%{opacity:0;transform:translateY(0) scale(.6)}20%{opacity:1}100%{opacity:0;transform:translateY(-46px) scale(1.1)}}
.praise{transform-box:fill-box;transform-origin:20% 100%;animation:praise 4s ease-in-out infinite}
@keyframes praise{0%,8%{opacity:0;transform:scale(.6)}18%,85%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.9)}}
'''
