from operator import itemgetter


def allocate_resources(resources, time_slots):
    """
    Assign resources to slots and create representations of any unassigned slots

    :param resources: list resources to be assigned
    :param time_slots: list of available time slots
    :return: allocated list of resources and time slots
    """
    if len(resources) > len(time_slots):
        raise ValueError("Can't allocate more resources than slots")

    resources_sorted = sorted(resources, key=itemgetter("priority"))
    allocated = []
    allocated_slot = 0
    for resource in resources_sorted:
        for hour in range(resource["hours"]):
            allocated.append([resource["name"],
                              time_slots[allocated_slot][0],
                              time_slots[allocated_slot][1]])
            allocated_slot += 1

    for remaining_slot in range(len(time_slots) - allocated_slot):
        allocated.append(["Nothing Scheduled",
                          time_slots[allocated_slot + remaining_slot][0],
                          time_slots[allocated_slot + remaining_slot][1]])

    return allocated


def allocate_resources_parallel(resources, time_slots):
    """
    Assign resources to time slots, assign as many
    resources to a single slot as its output value allows

    :param resources: list resources to be assigned
    :param time_slots: list of available time slots
    :return: allocated list of resources and time slots
    """
    # sort by priority asc
    resources_sorted = sorted(resources, key=itemgetter("priority"))
    allocated = []
    for window in time_slots:
        window_start_time = window[0]
        remaining_output = window[1]
        for resource in resources_sorted:
            if resource["hours"] == 0:
                continue
            if (remaining_output - resource["demand_per_hour"]) >= 0:
                allocated.append([resource["name"],
                                  window_start_time,
                                  resource["demand_per_hour"],
                                  resource["priority"]])
                resource["hours"] -= 1
                remaining_output -= resource["demand_per_hour"]

        if remaining_output > 0:
            allocated.append(["Nothing Scheduled",
                              window_start_time,
                              remaining_output,
                              float('inf')])
    return allocated
