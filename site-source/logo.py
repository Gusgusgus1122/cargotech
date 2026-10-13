L={ 'C':(70,"M12 0H70V22H26V78H70V100H12L0 88V12Z"),
 'A':(72,"M0 100L22 0H50L72 100H48L45 82H27L24 100ZM31 62H41L36 30Z"),
 'R':(70,"M0 0H56L70 14V46L58 58L72 100H47L36 62H24V100H0ZM24 20V42H46V20Z"),
 'G':(70,"M12 0H70V22H26V78H46V62H34V44H70V100H12L0 88V12Z"),
 'O':(70,"M12 0H58L70 12V88L58 100H12L0 88V12ZM24 22V78H46V22Z"),
 'T':(72,"M0 0H72V22H48V100H24V22H0Z"),
 'E':(66,"M0 0H66V22H24V38H58V58H24V78H66V100H0Z"),
 'H':(72,"M0 0H24V38H48V0H72V100H48V62H24V100H0Z")}
def word(s,x=0,gap=8):
    out=[];
    for ch in s:
        w,d=L[ch]; out.append('<path transform="translate(%d 0)" fill-rule="evenodd" d="%s"/>'%(x,d)); x+=w+gap
    return "".join(out),x
def logo(c1,c2,slit_bg=None):
    a,x=word("CARGO"); b,x2=word("TECH",x+0)
    W=x2-8+25
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 100" role="img" aria-label="CargoTech">'
     '<defs><mask id="s"><rect x="-10" y="-5" width="%d" height="110" fill="#fff"/><rect x="%d" y="46" width="150" height="6" fill="#000"/></mask></defs>'
     '<g transform="translate(25 0) skewX(-14)"><g fill="%s">%s</g><g fill="%s" mask="url(#s)">%s</g></g></svg>')%(W,W+20,x+70,c1,a,c2,b)
def icon(bg,fg,ac):
    c=L['C'][1]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="CargoTech">'
     '<rect width="120" height="120" rx="22" fill="%s"/><g transform="translate(22 16) scale(.88) translate(21 0) skewX(-14)"><path fill="%s" d="%s"/><rect x="40" y="40" width="22" height="20" fill="%s"/></g></svg>')%(bg,fg,c,ac)
open('logo/cargotech-logo-light.svg','w').write(logo('#104772','#5A6F7E'))
open('logo/cargotech-logo-dark.svg','w').write(logo('#FFFFFF','#4FC3EC'))
open('logo/cargotech-logo-navy-cyan.svg','w').write(logo('#104772','#4FC3EC'))
open('logo/cargotech-icon.svg','w').write(icon('#104772','#FFFFFF','#4FC3EC'))
open('logo/_dark_inline.txt','w').write(logo('#FFFFFF','#4FC3EC').replace('id="s"','id="sh"').replace('url(#s)','url(#sh)'))
