# Global Modules
from random import shuffle
# Custom Modules


class IntUtils(object):

    @staticmethod
    def random_list(length: int, num_of_shuffles: int = 1) -> list:
        if length == 0:
            return []

        rand_ints = []

        for num in range(length):
            rand_ints.append(num)

        for x in range(num_of_shuffles):
            shuffle(rand_ints)

        return rand_ints
