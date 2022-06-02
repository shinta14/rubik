# rubik
import streamlit as st


#ルービックキューブの動かし方
#U:上面、F：手前面、R:右面
#アルファベットの右の数字は何回回すかを表す。添え字なしは1回、2なら2回、3なら3回
#1回で90°時計回り。Rのときは奥に90°
cube_move = ["U", "U2", "U3", "F", "F2", "F3", "R", "R2", "R3"] #cubeの動き方


class Cube():
    def __init__(self, cp, co):
        self.cp = cp
        self.co = co

    def apply_move(self, move):

        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]

        return Cube(new_cp, new_co)
    


# キューブの動きを定義する。2x2x2だから右、上、手前だけ定義すればよい。
moves = {
    "U": Cube([3, 0, 1, 2, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0]),
    "U2": Cube([2, 3, 0, 1, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0]),
    "U3": Cube([1, 2, 3, 0, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0]),
    "F": Cube([0, 1, 3, 7, 4, 5, 2, 6], [0, 0, 1, 2, 0, 0, 2, 1]),
    "F2": Cube([0, 1, 7, 6, 4, 5, 3, 2], [0, 0, 0, 0, 0, 0, 0, 0]),
    "F3": Cube([0, 1, 3, 7, 4, 5, 2, 6], [0, 0, 1, 2, 0, 0, 2, 1]),
    "R": Cube([0, 2, 6, 3, 4, 1, 5, 7], [0, 1, 2, 0, 0, 2, 1, 0]),
    "R2": Cube([0, 6, 5, 3, 4, 2, 1, 7], [0, 0, 0, 0, 0, 0, 0, 0]),
    "R3": Cube([0, 5, 1, 3, 4, 6, 2, 7], [0, 1, 2, 0, 0, 2, 1, 0]),
}

def is_solved(state):
    return (state.cp == [0, 1, 2, 3, 4, 5 ,6, 7] and state.co == [0, 0, 0, 0, 0, 0, 0, 0])

#解を探す#
class Search():
    def __init__(self):
        self.now_solution=[]#今探索している手順を入れる#
    
    #そろっているパーツを数える
    def count_solved_corners(self, state): 
        return sum([state.cp[i] == i and state.co[i] == 0 for i in range(8)])




    def depth_limited_search(self, state, depth):
        if depth == 0 and is_solved(state):
            return True
        elif depth == 0: #残りの手数がないのにそろっていないとき
            return False      
        if depth == 1 and self.count_solved_corners(state)< 4:          
            return False
        if depth == 2 and self.count_solved_corners(state)< 4:
             return False
        if depth == 3 and self.count_solved_corners(state)< 3:
             return False
         

        for move in cube_move:
            self.now_solution.append(move)
            if self.depth_limited_search(state.apply_move(moves[move]), depth-1):
                return True
            self.now_solution.pop()
    
    def start_search(self, state, max_search=20):
        for depth in range(0, max_search):
            if self.depth_limited_search(state, depth):
                return self.now_solution
        else:
            return None

st.title("ルービックキューブをそろえよう！（2×2）")
st.write("下の空欄にルービックキューブの配置を記入すると、6面そろえる手順が表示されるよ!!")
position_cp=list(st.text_input('状態CPを記入', "01234567"))
position_co=list(st.text_input('状態COを記入', "00000000"))

position_cp = list(map(int, position_cp))

position_co = list(map(int, position_co))  

st.button("実行")
if st.button:
    search = Search()
    x = Cube(position_cp,position_co)
    solution = search.start_search(x)
    if solution:
        st.write(f"Solution: {solution}.")
    else:
        st.write("Solution not found.")
