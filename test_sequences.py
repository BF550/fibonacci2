from unittest import TestCase
import sequences as sq
import random

class TestSortedSequence(TestCase):

    def test_get_subsequence(self):
        self.fail()


class TestFibonacciSortedSequence(TestCase):
    def test_extend_sequence(self):
        fib_seq = sq.FibonacciSortedSequence()
        fib_seq.extend_sequence(random.randint(3,100))
        for i in range(2, len(fib_seq.sequence)):
            self.assertGreater(fib_seq.sequence[i], fib_seq.sequence[i-1])
            self.assertEqual(fib_seq.sequence[i], fib_seq.sequence[i-1]+fib_seq.sequence[i-2])

    def test_next_element(self):
        fib_seq = sq.FibonacciSortedSequence()
        for i in fib_seq.sequence:
            self.assertGreater(fib_seq.next_element(), i)

    def test_get_subsets(self):
        fib_seq = sq.FibonacciSortedSequence()
        target = random.randint(3, 100)
        fib_seq.get_subsequence(target)
        for subset in fib_seq.get_subsets(target):
            self.assertEqual(target, sum(subset))
