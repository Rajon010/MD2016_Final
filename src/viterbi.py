from types import FunctionType

INF = float('inf')

#TODO: log prob (* -> +)
def viterbi(N1, N2, L1, L2, f11, f12, f22):
    '''
        L1 has values in [0, N1)
        L2 has values in [0, N2)
        fij: Li x Lj -> R
        (
            f11: L1 x L1 -> R
            f12: L1 x L2 -> R
            f22: L2 x L2 -> R
        )
        
        L1  O - O - O - O - O - O ...
            |   |   |   |   |   |
        L2  O - O - O - O - O - O ...
    '''
    
    assert len(L1) == len(L2), 'Lengths of two lists differ.'
    for fs in ['f11', 'f12', 'f22']:
        assert isinstance(eval(fs), FunctionType), '%s should be a function.' % fs
    
    for idx, (l1, l2) in enumerate(zip(L1, L2)):
        cand1 = [l1] if l1 else range(N1)
        cand2 = [l2] if l2 else range(N2)
        cand = [(i, j) for i in cand1 for j in cand2]
        
        if idx == 0:
            old_cand = list(cand)
            old_prob = {}
            old_path = {}
            for i, j in cand:
                old_prob[i, j] = f12(i, j)
                old_path[i, j] = [(i, j)]
            continue
        
        new_prob = {}
        new_path = {}
        for i, j in cand:
            max_prob = -INF
            for i0, j0 in old_cand:
                prob = old_prob[i0, j0] * f11(i0, i) * f22(j0, j) * f12(i, j)
                if prob > max_prob:
                    max_prob = prob
                    max_prev = (i0, j0)
                
            new_prob[i, j] = max_prob
            new_path[i, j] = old_path[max_prev] + [(i, j)]
        
        old_prob = dict(new_prob)
        old_path = dict(new_path)
        old_cand = list(cand)
    
    max_prob = 0
    for cand in old_prob:
        if old_prob[cand] > max_prob:
            max_prob = old_prob[cand]
            max_path = old_path[cand]
    
    return max_path


if __name__ == '__main__':
    print(viterbi(2, 4, [None, 2, 1], [None, 3, None], lambda x,y:(x+y), lambda x,y:x*y, lambda x,y:1))
