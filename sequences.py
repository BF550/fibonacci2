from abc import ABCMeta, abstractmethod
import bisect


class SortedSequence(metaclass=ABCMeta):
    def __init__(self, ascending=True):
        self.sequence = []
        self.ascending = ascending

    @abstractmethod
    def next_element(self):
        pass

    def extend_sequence(self, num_of_elements=1):
        for i in range(num_of_elements):
            try:
                next_element = self.next_element()
                # if
                if self.ascending and next_element < self.sequence[-1]:
                    raise ValueError('%s > %s.', next_element, self.sequence[-1])
                elif not self.ascending and next_element > self.sequence[-1]:
                    raise ValueError('%s < %s.', next_element, self.sequence[-1])
                else:
                    self.sequence.append(self.next_element())
            except ValueError:
                print('Sequence order violated.')

    def get_subsequence(self, target, extend=True):
        """Gets the (sub-)sequence where the last element is less, greater or equal to target according to
        the sequence's order.

        If extend = True and the sequence's next element would contain more elements before the target this
        function will call :py:func:`REST_API.extend_sequence` as long as there are elements
        before target in it's order.
        """
        # get the index i of hypothetical position in sorted sequence
        i = bisect.bisect_left(self.sequence, target)
        if i:
            # i is max index but here might be more elements <= target
            if i == len(self.sequence) and extend:
                if self.ascending:
                    while self.next_element() < target:
                        self.extend_sequence()
                else:
                    while self.next_element() > target:
                        self.extend_sequence()
                return self.sequence
            # i is not max index
            else:
                return self.sequence[:i]
        raise ValueError('%s' % i)


class FibonacciSortedSequence(SortedSequence):

    def __init__(self):
        super().__init__()
        self.sequence = [2, 3]

    def next_element(self):
        return self.sequence[-1] + self.sequence[-2]

    def get_subsets(self, target):
        # We start with lists containing single elements of our sequence
        subsets = [[number] for number in self.sequence]
        new_subsets = []
        collected_subsets = []

        while subsets:
            for subset in subsets:
                s = sum(subset)
                for number in self.sequence:
                    if number >= subset[-1]:
                        if s + number < target:
                            new_subsets.append(subset + [number])
                        elif s + number == target:
                            collected_subsets.append(subset + [number])
            subsets = new_subsets
            new_subsets = []
        return collected_subsets



