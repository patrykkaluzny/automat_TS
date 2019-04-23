class plantClass:
    point_list = []
    current_point_id = None
    name = ""
    plant_id = None

    def __init__(self, name, point_list):
        self.current_point_id = 0
        self.name = name
        self.point_list=point_list.copy()

    def get_point_id(self, name):
        for i in range(len(self.point_list)):
            if self.point_list[i].point_name == name:
                return i
                break

        return False

    def get_point_name(self, point_id):
        return self.point_list[point_id].name

    def add_point(self, point_name, is_end_possible, event_list, exit_parameters=None):
        if exit_parameters is None:
            exit_parameters = []
        self.point_list.append(pointClass(point_name, is_end_possible, event_list, exit_parameters))

