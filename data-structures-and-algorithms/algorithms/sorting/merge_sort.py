def merge(l1, l2):
    """
    Expects two sorted lists and combines the elements into a single sorted list.
    :param l1: the first sorted list
    :param l2: the second sorted list
    :return: a sorted list of the elements of the two list arguments
    """

    # popping and appending to the end of the list are the fastest operations
    merged_list = []
    while len(l1) > 0 or len(l2) > 0:
        if len(l2) == 0:
            merged_list.append(l1.pop())
        elif len(l1) == 0:
            merged_list.append(l2.pop())
        elif l1[-1] > l2[-1]:
            merged_list.append(l1.pop())
        else:
            merged_list.append(l2.pop())

    # reverse list since we have been appending smaller elements
    return merged_list.reverse()


def merge_sort(li):
    """
    Creates a sorted list containing the elements of the list argument.
    :param li: a list object
    :return: a sorted list
    """

    # list is already sorted if it has <2 elements
    if len(li) < 2:
        return li.copy()
    else:
        sorted_prefix = merge_sort(li[0:len(li) // 2])
        sorted_suffix = merge_sort(li[len(li) // 2: len(li)])
        return merge(sorted_prefix, sorted_suffix)
