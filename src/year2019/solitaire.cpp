#include <iostream>
#include <vector>
#include <map>
#include <unordered_set>
#include <queue>

using namespace std;

typedef long long LL;
typedef pair<int,int> Coord;

vector<Coord> indexToCoord;
map<Coord,int> coordToIndex;
vector<vector<int> > symmetry;

int bitcnt(LL x) {
    return x ? (1 + bitcnt(x&(x-1))) : 0;
}

void show(LL state) {
    int x = 0, y = 0;
    for(int i=0;i<indexToCoord.size();i++) {
        char c = ((1LL<<i) & state) ? 'o' : '.';
        Coord coord = indexToCoord[i];
        while (coord.second > y) {
            cout << endl;
            y++;
            x = 0;
        }
        while (coord.first > x) {
            cout << " ";
            x++;
        }
        cout << c;
        x++;
    }
    cout << endl;
}

void setupSymmetries() {
    const int FLIP_AXIS = 3;
    for(int i=0;i<indexToCoord.size();i++) {
        Coord coord = indexToCoord[i];
        vector<int> symBits;
        for(int sym=0;sym<8;sym++) {
            int x = (sym&1) ? 2*FLIP_AXIS-coord.first : coord.first;
            int y = (sym&2) ? 2*FLIP_AXIS-coord.second : coord.second;
            if (sym & 4) {
                x-=FLIP_AXIS;
                y-=FLIP_AXIS;
                int ny = -x;
                int nx = y;
                x = nx+FLIP_AXIS;
                y = ny+FLIP_AXIS;
            }
            symBits.push_back(coordToIndex[make_pair(x, y)]);
        }
        symmetry.push_back(symBits);
    }
}

LL flip(LL state, int sym) {
    LL newState = 0;
    for(int i=0;i<indexToCoord.size();i++) {
        if ((1LL<<i) & state) {
            newState += (1LL<<symmetry[i][sym]);
        }
    }
    return newState;
}

int main() {
    string s;
    getline(cin, s);

    int y = 0;
    LL start = 0;
    while (!cin.eof()) {
        for(int x=0;x<s.size();x++) {
            if (s[x] == '.' || s[x] == 'o') {
                if (s[x] == 'o') start += 1LL<<indexToCoord.size();
                coordToIndex[make_pair(x,y)] = indexToCoord.size();
                indexToCoord.push_back(make_pair(x,y));
            }
        }
        y += 1;
        getline(cin, s);
    }

    vector<Coord> directions;
    directions.push_back(make_pair(0,1));
    directions.push_back(make_pair(0,-1));
    directions.push_back(make_pair(1,0));
    directions.push_back(make_pair(-1,0));

    vector<pair<LL, LL> > moves;
    for(map<Coord,int>::iterator it=coordToIndex.begin(); it!=coordToIndex.end(); it++) {
        for(int d=0;d<4;d++) {
            Coord p = it->first;
            Coord np = make_pair(p.first+directions[d].first,p.second+directions[d].second);
            Coord npp = make_pair(np.first+directions[d].first,np.second+directions[d].second);
            if (coordToIndex.count(np) && coordToIndex.count(npp)) {
                int i0 = it->second, i1 = coordToIndex[np], i2 = coordToIndex[npp];
                LL mask = (1LL<<i0)+(1LL<<i1)+(1LL<<i2);
                LL eq = (1LL<<i0)+(1LL<<i1);
                moves.push_back(make_pair(mask, eq));
            }
        }
    }
    cout << moves.size() << " moves available" << endl;

    setupSymmetries();

    int numStates = 0, pegsLeft = -1;
    queue<LL> q;
    unordered_set<LL> seen;
    q.push(start);
    seen.insert(start);
    LL cur;
    while (!q.empty()) {
        numStates += 1;
        if (numStates % 100000 == 0) {
            cout << numStates << " states visited" << endl;
        }

        cur = q.front();
        q.pop();

        if (bitcnt(cur) != pegsLeft) {
            pegsLeft = bitcnt(cur);
            cout << pegsLeft << " pegs left (" << (q.size() + 1) << " states to visit)" << endl;
            seen.clear();
        }
        bool hasMoves = false;
        for(vector<pair<LL, LL> >::iterator it = moves.begin(); it != moves.end(); it++) {
            LL mask = it->first, eq = it->second;
            if ((cur & mask) == eq) {
                hasMoves = true;
                LL pos = cur - eq + (mask-eq);
                for(int sym=1;sym<8;sym++) {
                    LL p = flip(pos, sym);
                    if (p < pos) pos=p;
                }
                if (!seen.count(pos)) {
                    seen.insert(pos);
                    q.push(pos);
                }
            }
        }
        if (pegsLeft == 1) {
            show(cur);
            cout << endl;
        }
        /*
        if (!hasMoves) {
            cout << "Done; the following position with " << pegsLeft << " pegs left has no moves:" << endl;
            show(cur);
            break;
        }
        */
    }

    cout << "Last position:" << endl;
    show(cur);

    return 0;
}
