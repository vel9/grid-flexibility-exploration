import math
import pandas as pd
from operator import attrgetter


class Resource:
    def __init__(self, name: str, priority: int, hours: int, demand_per_hour: float):
        """
        Object representing a home resource consuming energy

        :param name: name of resource
        :param priority: priority of resource
        :param hours: number of hours resource needs to be 'turned on'
        :param demand_per_hour: amount of energy resource will consume per hour
        """
        self.name = name
        self.priority = priority
        self.hours = hours
        self.demand_per_hour = demand_per_hour


def allocate_resources_by_min_rolling_average(resources: list,
                                              data_by_location: pd.DataFrame,
                                              num_minutes_in_interval: int):
    """
    Find optimal window for each resource by calculating a minimum rolling
    average across 5-minute intervals. Window size is the number of hours
    a given resource was assigned.

    :param resources: list resources to be assigned
    :param data_by_location: price data in 5 minute intervals
    :param num_minutes_in_interval: sample size
    :return: list of data points representing start and end time of optimal windows for each resource
    """
    col_name: str = "Rolling Average"
    allocated = []
    for resource in resources:
        data_by_location_copy = data_by_location.copy()
        window_size = get_window_size(resource.hours, num_minutes_in_interval)
        # add a column representing rolling average ending at given column
        data_by_location_copy[col_name] = data_by_location_copy.rolling(window=window_size).mean(numeric_only=True)

        min_df = data_by_location_copy.min()
        rows_with_min_rolling_avg = data_by_location_copy[data_by_location_copy[col_name] == min_df[col_name].min()]

        # only get end time from first matching window
        end_time = rows_with_min_rolling_avg["Time"].iloc[0]
        start_time = end_time - pd.Timedelta(hours=(resource.hours - 1))
        rolling_avg_value = rows_with_min_rolling_avg[col_name].iloc[0]

        allocated.append([resource.name, start_time, rolling_avg_value])
        allocated.append([resource.name, end_time, rolling_avg_value])

    return allocated


def get_window_size(num_hours: int, num_minutes_in_interval: int):
    """
    Break hours down into intervals

    :param num_hours: number of hours
    :param num_minutes_in_interval: sample size
    :return: number of 5 minute intervals in num_hours
    """
    if num_hours <= 0:
        raise ValueError("num_hours must be greater than 0")
    if num_minutes_in_interval <= 0:
        raise ValueError("num_minutes_in_interval must be greater than 0")
    return math.ceil((num_hours * 60) / num_minutes_in_interval)


def allocate_resources_parallel(resources: list[Resource], time_slots: list):
    """
    Assign resources to time slots, assign as many
    resources to a single slot as its output value allows

    :param resources: list resources to be assigned
    :param time_slots: list of available time slots
    :return: allocated list of resources and time slots
    """
    # sort by priority asc
    resources_sorted = sorted(resources, key=attrgetter("priority"))
    allocated = []
    for window in time_slots:
        window_start_time = window[0]
        remaining_output = window[1]
        resources_to_remove = []
        for index, resource in enumerate(resources_sorted):
            if (remaining_output - resource.demand_per_hour) >= 0:
                allocated.append([resource.name,
                                  window_start_time,
                                  resource.demand_per_hour,
                                  resource.priority])
                resource.hours -= 1
                if resource.hours == 0:
                    resources_to_remove.append(index)
                remaining_output -= resource.demand_per_hour

        # once all of resource's hours have been satisfied, remove from list
        for index_to_remove in reversed(resources_to_remove):
            resources_sorted.pop(index_to_remove)

        if remaining_output > 0:
            allocated.append(["Nothing Scheduled",
                              window_start_time,
                              remaining_output,
                              float('inf')])
    return allocated


def to_resources(resources_data: list[dict]):
    """
    covert each dict to a Resource object and return list

    :param resources_data: dict of resource values
    :return: list of Resource objects
    """
    resources = []
    for resource in resources_data:
        resources.append(Resource(resource["name"],
                                  resource["priority"],
                                  resource["hours"],
                                  resource.get("demand_per_hour", float("inf"))))
    return resources
