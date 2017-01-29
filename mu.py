from collections import deque
from pprint import pprint
class MIU(object):

    def __init__(self, _input, target, rule=None, parent=None):
        self._input = _input
        self._rule_lookup = {
            1: self._rule_one,
            2: self._rule_two,
            3: self._rule_three,
            4: self._rule_four
        }
        self._target = target
        self.done_rule = rule
        self._parent = parent

    def _rule_one(self):
        if self._input[-1] == 'I':
            return [MIU(self._input + "U", self._target, 1, self)]
        return []

    def _rule_two(self):
        return [MIU(self._input + self._input[1:], self._target, 2, self)]

    def _rule_three(self):
        spawned = []
        groups = self._find_groups("III")
        for span in groups:
            spawned.append(MIU(self._input[0:span[0]] + "U" + self._input[span[1]:], self._target, 3, self))
        return spawned

    def _rule_four(self):
        spawned = []
        groups = self._find_groups("UU")
        for span in groups:
            spawned.append(MIU(self._input[0:span[0]] + self._input[span[1]:], self._target, 4, self))
        return spawned

    def _find_groups(self, grouping):
        groups = []
        for position, letter in enumerate(self._input):
            if letter == grouping[0]:
                end = position+len(grouping)
                if self._input[position:end] == grouping:
                    groups.append((position, end))
        return groups

    def generate(self):
        children = []
        for rule in [1, 2, 3, 4]:
            children += self._rule_lookup[rule]()
        return children

    def match(self):
        return self._input == self._target

    def history(self):
        status = [(self.done_rule, self._input)]
        if self._parent:
            status = self._parent.history() + status
        return status


def main():
    children = MIU("MI", "MU").generate()
    i = 0
    while i < len(children):
        child = children[i]
        generated = child.generate()
        for g in generated:
            if g.match():
                pprint(g.history())
                return
        children.extend(generated)
        print(i)
        i += 1

main()
