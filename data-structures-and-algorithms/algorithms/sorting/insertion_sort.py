def insertion_sort(li):
    """
    Creates a sorted list containing the elements of the list argument.
    :param li: a list
    :return: a sorted list
    """

    li = li.copy()

    # proceed down the list to guarantee each element is sorted
    i = 1
    while i < len(li):

        # run insertion on the element
        j = i
        while (0 < j) and (li[j - 1] > li[j]):
            prev = li[j - 1]  # temp variable since prev element is overridden
            li[j - 1] = li[j]
            li[j] = prev
            j -= 1
