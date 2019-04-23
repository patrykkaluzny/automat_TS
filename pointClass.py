class pointClass:
    name = ""
    event_list = []             # event_list[0] - event name, event_list[1] - where it leads (name of point)
    is_end_possible = None
    exit_parameters = None      # exit_parameters[0] - name of event, exit_parameters[1] - where it leads (name of plant)

    def __init__(self, point_name, is_end_possible, event_list, exit_parameters=None):
        self.event_list = []
        self.name = point_name
        self.is_end_possible = is_end_possible
        self.event_list = event_list.copy()
        if exit_parameters is None:
            self.exit_parameters = []
        else:
            self.exit_parameters = exit_parameters.copy()