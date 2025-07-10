# Dictionary of Subscribers to certain events
subscribers = {} #empty, will be added to when needed

# adds a subscriber to an event
def subscribe(event_name: str, func) -> None:
    #if an event doesn't exist and someone wants to subscribe to it, the event is created
    if event_name not in subscribers :
        subscribers[event_name] = []
    subscribers[event_name].append(func)

# posts an event (alerts all subscribers)
def post(event_name: str, data) :
    #if an event doesn't exist and someone wants to post it, nothing is done.
    #ensures our subscribers dict isn't full of unused events
    if event_name not in subscribers :
        return

    for func in subscribers[event_name] :
        func(data)