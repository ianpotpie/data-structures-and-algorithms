from collections.abc import MutableMapping
from singly_linked_list import SinglyLinkedList


class HashMap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buckets = [SinglyLinkedList([]) for _ in range(capacity)]

    def __repr__(self):
        s = "{ "
        for bucket in self.buckets:
            for (k, v) in bucket:
                s = s + str(k) + ":" + str(v) + " , "
        s = s[:len(s) - 2] + "}"
        return s

    def __contains__(self, key):
        """
        Checks the existence of a key in the hash map.
        :param key: the key to be found
        :return: true if the key is in the map, false otherwise
        """

        # use the hash of the key to determine the bucket
        hash_val = hash(key)
        n_buckets = len(self.buckets)
        bucket_index = hash_val % n_buckets
        bucket = self.buckets[bucket_index]

        # iterate through the bucket to find the key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                return True

        return False

    def insert(self, key: any, value: any) -> None:
        """
        Inserts a key-value pair into the hash-map.
        :param key: the key to be inserted
        :param value: the value to be inserted
        :return: None
        """

        # use the hash of the key to determine the insertion bucket
        hash_val = hash(key)
        n_buckets = len(self.buckets)
        bucket_index = hash_val % n_buckets
        bucket = self.buckets[bucket_index]

        # iterate through the bucket to find key duplicates
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.delete(i)

        bucket.push((key, value))

    def access(self, key: any) -> any:
        """
        Uses a key in order to access a value in the hash map
        :param key: the key of the key-value pair
        :return: the value of the key-value pair
        """

        # use the hash of the key to determine the insertion bucket
        hash_val = hash(key)
        n_buckets = len(self.buckets)
        bucket_index = hash_val % n_buckets
        bucket = self.buckets[bucket_index]

        # iterate through the bucket to find the key of interest
        for (k, v) in bucket:
            if k == key:
                return v

        # if the key was not found, return an error
        raise KeyError()

    def delete(self, key: any) -> None:
        """
        Delete the key-value pair with the given key from the hash-map.
        :param key: the key of the key-value pair
        :return: None
        """

        # use the hash of the key to determine the insertion bucket
        hash_val = hash(key)
        n_buckets = len(self.buckets)
        bucket_index = hash_val % n_buckets
        bucket = self.buckets[bucket_index]

        # iterate through the bucket to find the key of interest
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.delete(i)
                return

        # if the key was not found, return an error
        raise KeyError()