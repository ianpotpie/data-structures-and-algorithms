
def quick_sort(li):
    """
    Creates a sorted list containing the elements of the list argument.
    :param li: a list
    :return: a sorted list
    """

    if len(li) < 2:
        return li.copy()

    else:
        pivot = li[0]
        greater = []
        lesser = []

        i = 1
        while i < len(li):
            if li[i] <= pivot:
                lesser.append(li[i])
            else:
                greater.append(li[i])

        return quick_sort(lesser) + [pivot] + quick_sort(greater)
