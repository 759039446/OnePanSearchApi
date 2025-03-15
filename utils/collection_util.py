def sort_results_by_key(results,sort_key,sort_order_array):
    # 对结果进行排序
    if results:
        def custom_sort(sublist):
            if sublist and sublist[0][sort_key]:  # 检查sublist是否为空以及sublist[0]中是否存在'driver'键
                return sort_order_array.index(sublist[0][sort_key])
            else:
                return len(sort_order_array) + 1

        results = sorted(results, key=lambda sublist: custom_sort(sublist))
    return results
