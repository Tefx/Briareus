IN = 0
OUT = 1


class RoutineDependence(object):
    def __init__(self):
        self.varOperators = {}
        self.routineDeps = {}

    def add_routine(self, routine, ins, outs):
        r_deps = set()
        for v in ins:
            if v not in self.varOperators:
                self.varOperators[v] = [(IN, routine)]
            else:
                head = self.varOperators[v][-1]
                if isinstance(head, set):
                    for t, r in head:
                        r_deps.update(self.routineDeps[r])
                    head.add((IN, routine))
                elif head[0] == OUT:
                    r_deps.add(head[1])
                    self.varOperators[v].append((IN, routine))
                else:
                    r_deps.update(self.routineDeps[head[1]])
                    self.varOperators[v][-1] = set([(IN, routine), head])
        for v in outs:
            if v not in self.varOperators:
                self.varOperators[v] = [(OUT, routine)]
            else:
                head = self.varOperators[v][-1]
                if isinstance(head, set):
                    for t, r in head:
                        r_deps.add(r)
                else:
                    r_deps.add(head[1])
                self.varOperators[v].append((OUT, routine))
        self.routineDeps[routine] = r_deps

    def query_deps_by_routine(self, routine):
        return self.routineDeps[routine]

    def query_deps_by_vars(self, v, t):
        if v not in self.varOperators:
            return []
        head = self.varOperators[v][-1]
        if t == IN:
            if isinstance(head, set) or head[0] == IN:
                if len(self.varOperators[v]) > 1:
                    return [self.varOperators[v][-2][1]]
            else:
                return [head[1]]
        else:
            if isinstance(head, set):
                return [r0 for _, r0 in head]
            else:
                return [head[1]]
        return r

    def query_deps(self, routine, var, t):
        pass


if __name__ == '__main__':
    r = RoutineDependence()
    r.add_routine(1, [], ["a", "b"])
    r.add_routine(2, [], ["c", "d"])
    r.add_routine(3, ["a"], ["e", "f"])
    r.add_routine(4, ["a", "c"], ["f"])
    print r.routineDeps
    print r.varOperators
    print r.query_deps_by_routine(4)
    print r.query_deps_by_vars("f", OUT)




