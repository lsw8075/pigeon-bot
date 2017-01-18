
elements = '. H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og D T'
bonelem = elements.split(' ')
elemlist = elements.upper().split(' ')

def whichelem(x):
    try:
        return elemlist.index(x)
    except:
        return 0;
    
def tochemi(word):

    if word == '':
        return '불가능'

    word = str(word).upper()

    whatelem = [128]
    whatelem.append(whichelem(word[0]))
    whereelem = [3, 1]

    if len(word) == 1:
        if whatelem[1] == 0:
            return '불가능'
        else:
            return bonelem[whatelem[1]]

    # word[0:i] 가 되는지 확인
    for i in range(2, len(word)+1):
        x = whichelem(word[i-1])
        y = whichelem(word[i-2:i])
        if whatelem[i-2] != 0 and y != 0:
            whereelem.append(2)
            whatelem.append(y)
        elif whatelem[i-1] != 0 and x != 0:
            whereelem.append(1)
            whatelem.append(x)
        else:
            whereelem.append(0)
            whatelem.append(0)
    
    i = len(word)

    if whatelem[i] == 0:
        return '불가능'

    bonlist = []
    while whereelem[i] != 3:
        bonlist.append(whatelem[i])
        i = i - whereelem[i]

    bonlist.reverse()

    res = ''
    for i in bonlist:
        res = res + bonelem[i]

    return res

