import asyncio
import random
import time


async def bubble_sort(arr: list):
    swapped = False

    start = time.time()

    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if swapped:
            swapped = False
        else:
            break

    return (time.time() - start), arr


async def selection_sort(arr: list):
    start = time.time()

    for i in range(len(arr) - 1):
        min_i = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_i]:
                min_i = j

        arr[i], arr[min_i] = arr[min_i], arr[i]

    return (time.time() - start), arr



async def my_sort(arr):
    print(f"unsorted: {arr.__str__()} (len: {len(arr)})")

    for i in range(len(arr)):
        try:
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]

        except IndexError:
            pass

    print(f"sorted: {arr.__str__()} (len: {len(arr)})")


async def sorter():
    rand_l = [random.randint(0, 100) for _ in range(20)]
    sorted = await my_sort(rand_l)


def main():
    asyncio.run(sorter())


if __name__ == "__main__":
    main()
