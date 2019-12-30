import sys
import re

#pos=<-39857152,26545464,51505035>, r=86328482

p = re.compile("pos=\<([\-0-9]*),([\-0-9]*),([\-0-9]*)\>, r=([0-9]*)")

bots = []
most=0
for line in sys.stdin.readlines():
    m = p.match(line.strip())
    data = map(lambda x:int(x), list(m.groups()))
    if data[3]>most:
        most = data[3]
        largest=len(bots)
    bots.append(data)




#print bots[largest]
best=0
maxb=0
minx=bots[0][0]
maxx=bots[0][0]
miny=bots[0][1]
maxy=bots[0][1]
minz=bots[0][2]
maxz=bots[0][2]

for bot in bots:
    minx=min(minx,bot[0])
    maxx=max(maxx,bot[0])
    miny=min(miny,bot[1])
    maxy=max(maxy,bot[1])
    minz=min(minz,bot[2])
    maxz=max(maxz,bot[2])

def check(x,y,z):
    global bots
    cnt = 0
    for bot in bots:
        dx = abs(bot[0]-x)
        dy = abs(bot[1]-y)
        dz = abs(bot[2]-z)
        if dx+dy+dz <= bot[3]:
            cnt += 1
            #print bot
    return cnt

# prev submitted: 82010378 (865)

best_score = 1e99
most = 0
bc = None

for bot in bots:
    #break
    for x in range(bot[0]-bot[3],bot[0]+bot[3]+1,bot[3]):
        for y in range(bot[1]-bot[3],bot[1]+bot[3]+1,bot[3]):
            for z in range(bot[2]-bot[3],bot[2]+bot[3]+1,bot[3]):
                t = (1 if x == bot[0] else 0) + (1 if y == bot[1] else 0) + (1 if z == bot[2] else 0)
                if t != 2:
                    continue
                cnt=check(x,y,z)
                score=abs(x)+abs(y)+abs(z)
                if cnt > most or (cnt == most and score<best_score):
                    bc = (x,y,z)
                    best_score=score
                    most = cnt

                if cnt == 865:
                    print 'cand', bc


#bc = (8390571, 42244765, 31375060)
#most = check(bc[0],bc[1],bc[2])
#best_score = abs(bc[0]+bc[1]+bc[2])

print most
print bc
print best_score

#bc =


STEP = 100000

while STEP >= 1:
    print 'STEP = %d' % STEP
    seen = {}

    q = [bc]
    seen[bc] = True
    p = 0
    while p < len(q):
        bc = q[p]
        p += 1

        score = abs(bc[0])+abs(bc[1])+abs(bc[2])
        if score < best_score:
            best_score = score
            print bc, best_score

        #print 'at %s, score %d' % (str(bc), score)

        for x in range(-STEP,STEP*2,STEP):
            for y in range(-STEP,STEP*2,STEP):
                for z in range(-STEP,STEP*2,STEP):
                    chk = check(bc[0]+x,bc[1]+y,bc[2]+z)
                    if chk > most:
                        altc=(bc[0]+x,bc[1]+y,bc[2]+z)
                        print 'oops %d %s' % (chk, str(altc))
                        most = chk
                        q = [altc]
                        best_score = abs(altc[0])+abs(altc[1])+abs(altc[2])
                        seen = {}
                        p = 0

                    if x+y+z <= 0  and chk == most:
                        altc=(bc[0]+x,bc[1]+y,bc[2]+z)
                        if not altc in seen:
                            q.append(altc)
                            seen[altc] = True

    STEP /= 10
