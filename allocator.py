from operator import itemgetter


def allocate_resources(resources, data_averaged_by_hour_sorted):
    if len(resources) > len(data_averaged_by_hour_sorted):
        raise ValueError("Can't allocate more resources than slots")

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
        allocated.append(["Nothing Scheduled",
                          data_averaged_by_hour_sorted[i + rem_i][0],
                          data_averaged_by_hour_sorted[i + rem_i][1]])

    return allocated


def allocate_resources_parallel(resources, data_averaged_by_hour_sorted):
    # sort by priority asc
    resources_sorted = sorted(resources, key=itemgetter("priority"))
    allocated = []
    max_priority = 100
    for window in data_averaged_by_hour_sorted:
        window_start_time = window[0]
        remaining_output = window[1]
        for resource in resources_sorted:
            if resource["hours"] == 0:
                continue
            if (remaining_output - resource["demand"]) >= 0:
                allocated.append([resource["name"],
                                  window_start_time,
                                  resource["demand"],
                                  resource["priority"]])
                resource["hours"] -= 1
                remaining_output -= resource["demand"]

        if remaining_output > 0:
            allocated.append(["Nothing Scheduled",
                              window_start_time,
                              remaining_output,
                              max_priority])
    return allocated
