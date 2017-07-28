import Queue
import sys
import time
from copy import deepcopy

class csp:
    def __init__(self, domains, arcs, constraints):
        self.domains = domains
        self.arcs = arcs
        self.constraints = constraints

    def check_allconstraints(self, x, y):
        arcs = self.arcs[x]
        #print arcs
        #print self.domains
        for arc in arcs:
            d = self.domains[arc]
            #print d
            if len(d) == 1 and y in d:
                return False
        return True
    
    def is_complete(self, assignment):
        #print assignment
        #print self.domains
        for d in self.domains:
            if len(self.domains[d]) != 1:
                return False
        for var in assignment.keys():
            arcs = self.arcs[var]
            intersection = [val for val in arcs if val in assignment]
            for arc in intersection:
                if len([assignment[var]]) == 1 and len([assignment[arc]]) == 1:
                    if assignment[var] == assignment[arc]:
                        return False
        #for key in assignment.keys():
         #   if self.check_allconstraints(key, assignment[key]) == False:
          #      return False
        return True        

# reference: https://github.com/LewisJEllis/Various/blob/master/sudoku/sudoku.py - readSudoku()
def get_sudoku(target):
    def boxRange(x): return range((x/3)*3, (x/3)*3+3)
    def constraints(i, j): return (i != j)
    def to_tuple(input_list):
        j = 0
        data = []
        for num in ['0','1','2','3','4','5','6','7','8']:
            for i in range(0,9):
                data.append((num+str(i), input_list[i+j]))
            j += 9
        return data
    
    def arcgen(x,y):
        return [str(i)+str(j) for i in range(0,9) for j in range(0,9) if
                (i != x or y != j) and (i == x or j == y or (i in boxRange(x) and j in boxRange(y)))]

    #data0 = tuple(open(filename, 'r'))
    #for i in range(0, len(data0)):
        #list0 = data0[i]
        #target = list0.rstrip()
        #print target
    data1 = list(target)
    data2 = to_tuple(data1)
    #print data2
    domains = {key: (range(1,10) if c == '0' else [int(c)]) for (key, c) in data2}
        #print domains 
    arcs = {key: arcgen(int(key[0]), int(key[1])) for (key, c) in data2}
        #print arcs
    return csp(domains, arcs, constraints)

def AC_3(csp):
    queue = []
    for d in csp.domains:
        for a in csp.arcs[d]:
            queue.append((d, a))

    while len(queue)>0:
        Xi, Xj = queue.pop()
        if revise(csp, Xi, Xj):
            #if len(csp.domains[Xi]) == 0:
                #return False
            for Xk in csp.arcs[Xi]:
                if Xi != Xk:
                    queue.append((Xk, Xi))

def revise(csp, Xi, Xj):
    revised = False
    #print csp.domains[i][:]
    for x in csp.domains[Xi][:]:
        need_revise = True
        for y in csp.domains[Xj]:
            if csp.constraints(x, y):
                need_revise = False
        if need_revise == True:
            csp.domains[Xi].remove(x)
            revised = True
    return revised

def backtrack(assignment, csp):
    #print assignment
    if csp.is_complete(assignment):
        print_sudoku(csp)
        #print csp.domains['16']
        return assignment
    var = mrv(assignment, csp)
    #print var
    #print csp.arcs[var]
    new_copy = deepcopy(csp)
    for d in csp.domains[var]:
        #print d
        #new_copy = deepcopy(csp)
        #print "var=%s, [%s]"%(var,d)
        #inference = {}
        if csp.check_allconstraints(var, d):
            #if check_constraint({var:d}, assignment, csp):
            #print "getthrough_var=%s"%var
            assignment[var] = d
            csp.domains[var] = [d]
            for arc in csp.arcs[var]:
                if d in csp.domains[arc]:
                    csp.domains[arc].remove(d)
            #print assignment
            inference = forward_checking(csp, var, d)
            if inference != False:
                #print inference
            #if inference != False:
                #if check_constraint(inference, assignment, csp):
                    #print 'inference:%s'%inference
                #assignment.update(inference)
                #for key in inference.keys():
                #csp.domains[key] = [inference[key]]
                result = backtrack(assignment, csp)
                #if result != False:
                if result != False:
                    csp = deepcopy(new_copy)
                    return result
        #print assignment
        #print var
                del assignment[var]
            #if inference != False:
                #print 'inference: %s'%inference
                #if inference != False:
                 #   for value in inference:
                  #      del assignment[value]
        #print csp.domains
            csp = deepcopy(new_copy)
    return False


def mrv(assignment, csp):
    domain_len = {}
    for d in csp.domains:
        if len(csp.domains[d]) > 1:
            domain_len[d] = len(csp.domains[d])
    #sorted_var = sorted(domain_len, key=domain_len.get)
    #print sorted_var
    for var in sorted(domain_len, key=domain_len.get):
        if var not in assignment:
            return var
    return False

def check_constraint(inference, assignment, csp):
    checking_keys = inference.keys()
    if len(checking_keys) == 0:
        return True
    #print "checking_key: %s"%checking_key
    checking_values = inference.values()
    #print "checking_values: %s"%checking_values
    checked_keys = assignment.keys()
    for checking_key in checking_keys:
        arcs = csp.arcs[checking_key]
        #print arcs
        intersection = [val for val in arcs if val in checked_keys]
        #print "intersection: %s"%intersection
        for key in intersection:
            if assignment[key] == inference[checking_key]:
                return False
    return True
        
        
#{'56': 1}, csp, '56', [1]
def forward_checking(csp, var, d):
    #inference = {}
    #print "var=%s, [%s]"%(var,d)
    arcs = csp.arcs[var]
    #print arcs
    for arc in arcs:
        dm = csp.domains[arc]
        #print d
        #print "arc%s:%s"%(arc,dm)
        #print dm
        if len(dm) < 1:# and d in dm:
            return False
        '''
            #dm = [num for num in dm if num not in [d]]
            #csp.domains[arc] = dm
            #print "newarc%s:%s"%(arc,csp.domains[arc])
            #if inference(dm) == 1 and arc not in assignment:
             #       inference[arc] = dm[0]
        #print "inference: %s"%inference
        #for value in inference.values():
         #   if inference.values().count(value) > 1:
          #      return False
        '''

    return True

def print_sudoku(csp):
    out = [range(0,9) for i in range(0,9)]
    for x in csp.domains:
        if (len(csp.domains[x]) == 1):
            out[int(x[0])][int(x[1])] = str(csp.domains[x][0])
        else:
            out[int(x[0])][int(x[1])] = '0'
    flat_list = [item for sublist in out for item in sublist]
    print ''.join(flat_list)
    result = ''.join(flat_list)
    f = open('output.txt','w')
    f.write(result)
    f.close()


def print_assignment(assignment, csp):
    out = [range(0,9) for i in range(0,9)]
    for x in csp.domains:
        if (len(csp.domains[x]) == 1):
            out[int(x[0])][int(x[1])] = str(csp.domains[x][0])
        elif len(csp.domains[x]) != 1 and x in assignment:
            out[int(x[0])][int(x[1])] = str(assignment[x])
        else:
            out[int(x[0])][int(x[1])] = '0'
    flat_list = [item for sublist in out for item in sublist]
    #print len(flat_list)
    result = ''.join(flat_list)
    f = open('output.txt','w')
    f.write(result)
    f.close()
    return result

def main():
        #data0 = tuple(open(sys.argv[1], 'r'))
        data0 = str(sys.argv[1])
    #print len(data0)
    #for i in range(0, len(data0)):
        start_time = time.time() 
        list0 = data0
        target = list0.rstrip()
        node = get_sudoku(target)
        AC_3(node)
        start_time = time.time()
        assignment = backtrack({},node)
        #if assignment != False:
        #    print True
        #else:
        #print assignment
        #result = print_assignment(assignment, node)
        #print result
        #for d in node.domains:
        #    print "%s: %s"%(d, node.domains[d])
        #print node.domains
        #solved = True
        #if '0' in result:
        #    solved = False
        #solved = True
        #for key in node.domains:
        #    if len(node.domains[key]) != 1:
        #        solved = False
        #print solved
        #spend_time = time.time() - start_time
        #print ("index%d: "+str(solved) + ". Time spent: %s seconds")%(i+1, spend_time)    
        #print_sudoku(node)
        

if __name__ == "__main__":
    main()
