# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:36:45 2021

@author: lor
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. 
But -- oh no! -- one of the escape pods has flown into a nearby nebula, causing you to lose track of it. 
You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. 
However, you do find that the gas of the steadily expanding nebula follows a simple pattern, 
meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. 
You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, 
specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. 
If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  
Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, 
so in the next state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell 
(the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  
For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) 
as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, 
and the height of the grid will be between 3 and 9 inclusive.  The solution will always be less than one billion (10^9).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{true, true, false, true, false, true, false, true, true, false}, {true, true, false, false, false, false, true, true, true, false}, {true, true, false, false, false, false, false, false, false, true}, {false, true, false, false, false, false, true, true, false, false}})
Output:
    11567

Input:
Solution.solution({{true, false, true}, {false, true, false}, {true, false, true}})
Output:
    4

Input:
Solution.solution({{true, false, true, false, false, true, true, true}, {true, false, true, false, false, false, true, false}, {true, true, true, false, false, false, true, false}, {true, false, true, false, false, false, true, false}, {true, false, true, false, false, true, true, true}}
Output:
    254

-- Python cases --
Input:
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254


"""

def solution(g):
    from collections import defaultdict

    def convert_to_numbers(g):
        result = []
        for row in g:
            line = ''
            for element in row:
                if element:
                    line += ('1')
                else:
                    line += ('0')
            result.append(int((line), base = 2))
        return result
    


    
    def get_next_step2(row1, row2, length):
        new_row = []
        for i in range(length - 1):
            tmp1, tmp2 = row1 % 4, row2 % 4 

            
            if (tmp1 in [1,2] and tmp2 == 0) or (tmp1 == 0 and tmp2 in [1,2]):
                new_row.append(1)
            else:
                new_row.append(0)
            row1 = row1 >> 1
            row2 = row2 >> 1
        new_row.reverse()
        new_num = 0
        for i in new_row:
            new_num += i
            new_num = new_num << 1
        new_num = new_num >> 1
        return int(new_num)
    


    def get_all_combos(numbers, length):
        answer = dict()
        for i in numbers:
            answer.update({i:[]})
        for i in range(2 ** (length + 1)):
            for j in range(i+1):
                next_step = get_next_step2(i,j, length + 1)
                if next_step in numbers:
                    if [i,j] not in answer[next_step]:
                        answer[next_step].append([i,j])
                    if [j,i] not in answer[next_step]:
                        answer[next_step].append([j,i])

                    
        return answer

    def get_all_combos2(numbers, length):
        answer = dict()
        nums = sorted(numbers)
        for i in numbers:
            answer.update({i:set()})
        for i in range(2 ** (length + 1)):
            for j in range(i+1):
                next_step = get_next_step2(i,j, length + 1)
                if next_step in nums:                   
                    answer[next_step].add((i,j))
                    answer[next_step].add((j,i))
        return answer

    def get_prev_steps(numbers, combos, no_of_rows):           
        def other_steps(numbers, combos, answer, i):
            new_answer = []
            for last_answer in answer:
                for step in combos[numbers[i]]:
                    if step[0] == last_answer[-1]:
                        tmp = last_answer[:]                   
                        tmp.append(step[1])
                        new_answer.append(tmp)
            
            answer = new_answer[:]
            return answer
        
        answer = []
        for element in combos[numbers[0]]:
            answer.append(list(element))
        for i in range(1, no_of_rows):
            answer = other_steps(numbers, combos, answer, i) 
        
        return answer

    def transfer_matrix(combos, numbers):
        nums = set(numbers)
        result = defaultdict(set)
        
        for i in nums:
            for element in combos[i]:
                # print(element)
                
                result.update({(i, element[0]): set()})      
        for i in nums:
            for element in combos[i]:
                result[(i, element[0])].add(element[1])
     
        return result


    def count(numbers, tr_ma, length):
        result = {i: 1 for i in range(2**(length + 1))}
        for row in numbers:
            next_row = defaultdict(int)
            for i in result:
                for j in tr_ma[(row, i)]:
                    next_row[j] += result[i]

            result = next_row
        return sum(result.values())


    g = list(zip(*g))
    length = len(g[0])
    no_of_rows = len(g)
    numbers = convert_to_numbers(g)
   
    combos = get_all_combos2(numbers, length)    
    tr_ma = transfer_matrix(combos, numbers)

    answer = count(numbers, tr_ma, length)

    return answer



from time import time
from random import choice
start = time()    
# result = solution([[True, False, True], [False, True, False], [True, False, True]])
# result = solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
# result = solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])


tc7 = [
        [False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, True, False, False, True],
        [True, True, False, False, True, False, False, False, False, False, True, True, False, True, True, False, True, False, False, False],
        [False, False, False, True, False, True, False, True, False, False, False, True, False, True, False, False, False, False, True, True],
        [False, False, False, False, False, False, True, False, True, False, True, False, True, False, False, False, False, False, False, True],
        [False, False, False, False, False, False, True, False, True, False, True, False, True, False, False, False, False, False, False, True],
        [False, False, True, False, True, False, False, False, False, False, False, True, False, False, True, False, False, False, True, False]
        ]

tc4 = [
       [True, True, True, True, True],
       [True, False, False, False, True],
       [True, False, False, False, True],
       [True, False, False, False, True],
       [True, True, True, True, True]
       
       ]



# base = [True, False]
# test = []
# for i in range(9):
#     newline = []
#     for j in range(50):
#         newline.append(choice(base))
#     test.append(newline)

# for line in test:
#     print(line)

result = solution(tc7)
print(result)
print("timing: ", time()-start)

