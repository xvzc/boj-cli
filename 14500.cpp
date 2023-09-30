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
int paper[500][500], N, M;
vector<vector<pair<int, int>>> I = {
    {{0, 0}, {0, 1}, {0, 2}, {0, 3}}, 
    {{0, 0}, {1, 0}, {2, 0}, {3, 0}}
};
vector<vector<pair<int, int>>> L1 = {
    {{0, 0}, {1, 0}, {2, 0}, {2, 1}}, // 0
    {{0, 0}, {0, 1}, {0, 2}, {1, 0}}, // 90
    {{0, 0}, {0, 1}, {1, 0}, {2, 0}}, // 180
    {{1, 0}, {1, 1}, {1, 2}, {0, 2}}  // 270
};

vector<vector<pair<int, int>>> L2 = {
    {{0, 0}, {1, 0}, {1, 1}, {1, 2}}, // 0
    {{0, 0}, {0, 1}, {1, 1}, {2, 1}}, // 90
    {{0, 0}, {0, 1}, {0, 2}, {1, 2}}, // 180
    {{2, 0}, {2, 1}, {1, 1}, {0, 1}}  // 270
};

vector<vector<pair<int, int>>> O = {
    {{0, 0}, {1, 0}, {1, 1}, {0, 1}} // 0 
};
vector<vector<pair<int, int>>> S1 = {
    {{1, 0}, {1, 1}, {0, 1}, {0, 2}}, // 0 
    {{0, 0}, {1, 0}, {1, 1}, {2, 1}} // 0 
};

vector<vector<pair<int, int>>> S2 = {
    {{1, 0}, {2, 0}, {0, 1}, {1, 1}}, // 0 
    {{0, 0}, {0, 1}, {1, 1}, {1, 2}} // 0 
};
vector<vector<pair<int, int>>> T = {
    {{0, 0}, {0, 1}, {0, 2}, {1, 1}}, // 0 
    {{0, 1}, {1, 1}, {2, 1}, {1, 0}}, // 0 
    {{1, 0}, {1, 1}, {1, 2}, {0, 1}}, // 0 
    {{0, 0}, {1, 0}, {2, 0}, {1, 1}}, // 0 
};
/* ----------------------------------------------- */
/* - FUNCTIONS ----------------------------------- */
bool is_out_of_index(int ny, int nx) {
    if(ny < 0 || N <= ny || nx < 0 || M <= nx)
        return true;

    return false;
}
int get_max_sum(vector<vector<pair<int, int>>> &filter) {
    int ret = 0;
    for(int i = 0; i < filter.size(); i++) {
        for(int y = 0; y < N; ++y) {
            for(int x = 0; x < M; ++x) {
                int sum = 0;
                for(int j = 0; j < filter[i].size(); ++j) {
                    int ny = y + filter[i][j].fi;
                    int nx = x + filter[i][j].se;

                    if(is_out_of_index(ny, nx)) {
                        sum = 0;
                        break;
                    }
                    sum += paper[ny][nx];
                }

                ret = max(sum, ret);
            }
        }
    }
    return ret;
}
/* ----------------------------------------------- */
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    if constexpr (local) 
        (void)!freopen("input.txt", "r", stdin);
    cin >> N >> M;
    for(int i = 0; i < N; ++i) {
        for(int j = 0; j < M; ++j) {
            cin >> paper[i][j];
        }
    }
    int answer = 0;

    answer = max(answer, get_max_sum(I));
    answer = max(answer, get_max_sum(L1));
    answer = max(answer, get_max_sum(L2));
    answer = max(answer, get_max_sum(O));
    answer = max(answer, get_max_sum(S1));
    answer = max(answer, get_max_sum(S2));
    answer = max(answer, get_max_sum(T));

    cout << answer << endl;

    return 0;
}
