def sort_by_datetime(event_list):
    event_list.sort(reverse=True, key=lambda x: x.timestamp)
