from operator import itemgetter


def allocate_resources(resources, data_averaged_by_hour_sorted):
    # sort by priority asc
    resources_sorted = sorted(resources, key=itemgetter("priority"))
    allocated = []
    i = 0
    for resource in resources_sorted:
        for hour in range(resource["hours"]):
            allocated.append([resource["name"],
                              data_averaged_by_hour_sorted[i][0],
                              data_averaged_by_hour_sorted[i][1]])
            i += 1

    for rem_i in range(len(data_averaged_by_hour_sorted) - i):
        allocated.append(["Unallocated",
                          data_averaged_by_hour_sorted[i + rem_i][0],
                          data_averaged_by_hour_sorted[i + rem_i][1]])
    return allocated
