import _illion
from illion import setset

def constructors():
    ss = setset()
#    print ss
    assert ss.dumps() == '{}'

    ss = setset(set())
    assert ss.dumps() == '{{}}'

    ss = setset(frozenset([1, 2]))
    assert ss.dumps() == '{{1,2}}'

    ss = setset([set(), set([1, 2]), set([1, 3])])
    assert ss.dumps() == '{{1,2},{1,3},{}}'

    ss = setset({'include': set([1, 2]), 'exclude': set([4])})
    assert ss.dumps() == '{{1,2,3},{1,2}}'

    # TODO:
    #ss = setset([{'include': set([1, 2]), 'exclude': set([4])},
    #             {'include': set([1, 3, 4])},
    #             {'exclude': set([2, 3])}])
    #assert ss.dumps() == e0 + e1 + e1*e2 + e1*e2*e3 + e1*e2*e3*e4 + e1*e3*e4 + e1*e4 + e4

    # copy constructor
    ss = setset([set(), set([1, 2]), set([1, 3])])
    assert ss.dumps() == '{{1,2},{1,3},{}}'

    ss1 = setset([set(), set([1, 2]), set([1, 3])])
    ss2 = ss1.copy()
    ss1.clear()
    assert ss1.dumps() == '{}'
    assert ss2.dumps() == '{{1,2},{1,3},{}}'

def comparison():
    ss = setset(set([1, 2]))
    assert ss == setset(set([1, 2]))
    assert ss != setset(set([1, 3]))

    v = [set(), set([1, 2]), set([1, 3])]
    ss = setset(v)
    assert ss.isdisjoint(setset([set([1]), set([1, 2, 3])]))
    assert not ss.isdisjoint(setset([set([1]), set([1, 2])]))

    assert ss.issubset(setset(v))
    assert not ss.issubset(setset([set(), set([1, 2])]))
    assert ss <= setset(v)
    assert not (ss <= setset([set(), set([1, 2])]))
    assert ss < setset([set(), set([1]), set([1, 2]), set([1, 3])])
    assert not (ss < setset(v))

    assert ss.issuperset(setset(v))
    assert not ss.issuperset(setset([set([1]), set([1, 2])]))
    assert ss >= setset(v)
    assert not (ss >= setset([set([1]), set([1, 2])]))
    assert ss > setset([set(), set([1, 2])])
    assert not (ss > setset(v))

def unary_operators():
    ss = setset([set(), set([1]), set([1, 2]), set([1, 2, 3]), set([1, 2, 3, 4]),
                 set([1, 3, 4]), set([1, 4]), set([4])])
    assert ~ss == setset([set([1, 2, 4]), set([1, 3]), set([2]), set([2, 3]),
                          set([2, 3, 4]), set([2, 4]), set([3]), set([3, 4])])
    assert ss.complement() == setset([set([1, 2, 4]), set([1, 3]), set([2]),
                                      set([2, 3]), set([2, 3, 4]), set([2, 4]),
                                      set([3]), set([3, 4])])
    assert ss.smaller(2) == setset([set(), set([1]), set([1, 2]), set([1, 4]),
                                    set([4])])

    ss = setset([set([1, 2]), set([1, 4]), set([2, 3]), set([3, 4])])
    assert ss.hitting() == setset([set([1, 2, 3]), set([1, 2, 3, 4]),
                                   set([1, 2, 4]), set([1, 3]), set([1, 3, 4]),
                                   set([2, 3, 4]), set([2, 4])])

    ss = setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 3, 4]), set([2, 4, 5])])
    assert ss.minimal() == setset([set([1, 2]), set([2, 4, 5])])
    assert ss.maximal() == setset([set([1, 2, 3, 4]), set([2, 4, 5])])

def binary_operators():
    u = [set(), set([1]), set([1, 2]), set([1, 2, 3]), set([1, 2, 3, 4]),
         set([1, 3, 4]), set([1, 4]), set([4])]
    v = [set([1, 2]), set([1, 4]), set([2, 3]), set([3, 4])]
    ss = setset(u) & setset(v)
    assert ss == setset([set([1, 2]), set([1, 4])])
    ss = setset(u).intersection(setset(v))
    assert ss == setset([set([1, 2]), set([1, 4])])

    ss = setset(u)
    ss &= setset(v)
    assert ss == setset([set([1, 2]), set([1, 4])])
    ss = setset(u)
    ss.intersection_update(setset(v))
    assert ss == setset([set([1, 2]), set([1, 4])])

    ss = setset(u) | setset(v)
    assert ss == setset([set(), set([1]), set([1, 2]), set([1, 2, 3]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([3, 4]), set([4])])
    ss = setset(u).union(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2]), set([1, 2, 3]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([3, 4]), set([4])])

    ss = setset(u)
    ss |= setset(v)
    assert ss == setset([set(), set([1]), set([1, 2]), set([1, 2, 3]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([3, 4]), set([4])])
    ss = setset(u)
    ss.update(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2]), set([1, 2, 3]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([3, 4]), set([4])])

    ss = setset(u) - setset(v)
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([4])])
    ss = setset(u).difference(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([4])])

    ss = setset(u)
    ss -= setset(v)
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([4])])
    ss = setset(u)
    ss.difference_update(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([4])])

    ss = setset(u) * setset(v)
    assert ss == setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 4]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([2, 3, 4]), set([3, 4])])
    ss = setset(u).product(setset(v))
    assert ss == setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 4]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([2, 3, 4]), set([3, 4])])

    ss = setset(u)
    ss *= setset(v)
    assert ss == setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 4]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([2, 3, 4]), set([3, 4])])
    ss = setset(u)
    ss.product_update(setset(v))
    assert ss == setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 4]),
                         set([1, 2, 3, 4]), set([1, 3, 4]), set([1, 4]),
                         set([2, 3]), set([2, 3, 4]), set([3, 4])])

    ss = setset(u) ^ setset(v)
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([2, 3]), set([3, 4]), set([4])])
    ss = setset(u).symmetric_difference(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([2, 3]), set([3, 4]), set([4])])

    ss = setset(u)
    ss ^= setset(v)
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([2, 3]), set([3, 4]), set([4])])
    ss = setset(u)
    ss.symmetric_difference_update(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([2, 3]), set([3, 4]), set([4])])

    v = [set([1, 2])]
    ss = setset(u) / setset(v)
    assert ss == setset([set(), set([3]), set([3, 4])])
    ss = setset(u).divide(setset(v))
    assert ss == setset([set(), set([3]), set([3, 4])])

    ss = setset(u)
    ss /= setset(v)
    assert ss == setset([set(), set([3]), set([3, 4])])
    ss = setset(u)
    ss.divide_update(setset(v))
    assert ss == setset([set(), set([3]), set([3, 4])])

    ss = setset(u) % setset(v)
    assert ss == setset([set(), set([1]), set([1, 3, 4]), set([1, 4]), set([4])])
    ss = setset(u).remainder(setset(v))
    assert ss == setset([set(), set([1]), set([1, 3, 4]), set([1, 4]), set([4])])

    ss = setset(u)
    ss %= setset(v)
    assert ss == setset([set(), set([1]), set([1, 3, 4]), set([1, 4]), set([4])])
    ss = setset(u)
    ss.remainder_update(setset(v))
    assert ss == setset([set(), set([1]), set([1, 3, 4]), set([1, 4]), set([4])])

    v = [set([1, 2]), set([1, 4]), set([2, 3]), set([3, 4])]
    ss = setset(u).subsets(setset(v))
    assert ss == setset([set(), set([1]), set([1, 2]), set([1, 4]), set([4])])

    ss = setset(u).supersets(setset(v))
    assert ss == setset([set([1, 2]), set([1, 2, 3]), set([1, 2, 3, 4]),
                         set([1, 3, 4]), set([1, 4])])

    ss = setset(u).nonsubsets(setset(v))
    assert ss == setset([set([1, 2, 3]), set([1, 2, 3, 4]), set([1, 3, 4])])

    ss = setset(u).nonsupersets(setset(v))
    assert ss == setset([set(), set([1]), set([4])])

def capacity():
    ss = setset()
    assert not ss

    ss = setset([set(), set([1, 2]), set([1, 3])])
    assert not not ss

    assert len(ss) == 3
    assert ss.len() == 3

def iterators():
    ss1 = setset([set(), set([1, 2]), set([1, 3])])
    ss2 = setset()
    for s in ss1:
        ss2 = ss2 | setset(s)
    assert ss1 == ss2

def lookup():
    pass

def modifiers():
    v = [set(), set([1, 2]), set([1, 3])]
    ss = setset(v)
    ss.clear()
    assert ss == setset()  # TODO: use empty()

def stream():
    pass

if __name__ == '__main__':
    ss1 = setset([set(), set([1, 2]), set([1, 3])])
    ss2 = setset()
    for s in ss1:
        ss2 = ss2 | setset(s)
    assert ss1 == ss2
    import sys
    sys.exit()

    constructors()
    comparison()
    unary_operators()
    binary_operators()
    capacity()
    iterators()
    lookup()
    modifiers()
    stream()
    print 'ok'
