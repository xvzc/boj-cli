#include <bits/stdc++.h>

#define debug if constexpr (local) std::cout
#define endl '\n'
#define fi first
#define se second

#ifdef LOCAL
constexpr bool local = true;
#else
constexpr bool local = false;
#endif

typedef long long ll;
typedef unsigned long long ull;

using namespace std;

/* - GLOBAL VARIABLES ---------------------------- */
 
/* ----------------------------------------------- */

/* - FUNCTIONS ----------------------------------- */

/* ----------------------------------------------- */

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);

    if constexpr (local) 
        (void)!freopen("input.txt", "r", stdin);

    int N, L; cin >> N >> L;

    for (int i = L; i <= 100; ++i) {
        int top = 2*N - (i*(i - 1));
        int bottom = 2*i;

        if (top % bottom) {
            continue;
        }

        int x = top / bottom;

        if (x < 0) {
            continue;
        }

        for (int j = 0; j < i; ++j) {
            cout << x + j << ' ';
        }

        return 0;
    }

    cout << -1 << endl;

    return 0;
}


