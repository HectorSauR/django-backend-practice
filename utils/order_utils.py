
class QuickSort:
    def __init__(self, array: list, attr: str, order: str = "asc"):

        if order not in ["asc", "desc"]:
            raise ValueError("Order must be either 'asc' or 'desc'.")
        self.order = order
        self.array = array
        self.attr = attr

    def partition(self, low, high):
        pivot = self.array[high]

        i = low - 1

        for j in range(low, high):
            if self.ordering(self.array[j], pivot):
                i = i + 1

                self.array[i], self.array[j] = self.array[j], self.array[i]

        self.array[i + 1], self.array[high] = (
            self.array[high], self.array[i + 1])

        return i + 1

    def ordering(self, a: any, b: any):

        value1 = getattr(a, self.attr)
        value2 = getattr(b, self.attr)

        if (type(value1) is str and type(value2) is str):
            value1 = value1.lower()
            value2 = value2.lower()

        if self.order == "asc":
            return value1 <= value2
        return value1 >= value2

    def quickSort(self, low, high):
        if low < high:
            pi = self.partition(low, high)

            self.quickSort(low, pi - 1)

            self.quickSort(pi + 1, high)

    def sort(self) -> list:
        self.quickSort(0, len(self.array) - 1)
        return self.array
