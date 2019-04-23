import pointClass
import plantClass
current_plant_id = 0;
spec = []
specLoop = True


def get_plant(name, plantList):
    for i in range(len(plantList)):
        if plantList[i].name == name:
            return i
            break
    return None;


def get_point(name, pointList):
    for i in range(len(pointList)):
        if pointList[i].name == name:
            return i
            break
    return None;

tempList = []

#set up idle plant


tempList.append(pointClass("Idle", True, [],[["Init_Start", "Init"], ["Start_Diagnostic", "Diagnostic"]]))
tempPlant = plantClass("Idle", tempList)
spec.append(tempPlant)
tempList.clear()
del tempPlant
# set up diagnostic plant

#tempList.append(pointClass("Diagnostic_Idle", False, [["Start_Diagnostic", "Docking_Station"]]))
tempList.append(pointClass("Docking_Station", False, [["Battery_Low", "Charging"], ["Tank_Full", "Tank_Emptying"],
                                                            ["Filter_Dirty", "Filter_Cleaning"],
                                                            ["Brush_Dirty", "Brush_Cleaning"]], [["Diagnostic_Done", "Idle"]]))
tempList.append(pointClass("Charging", False, [["Battery_Full", "Docking_Station"]]))
tempList.append(pointClass("Tank_Emptying", False, [["Tank_Empty", "Docking_Station"]]))
tempList.append(pointClass("Filter_Cleaning", False, [["Filter_Clean", "Docking_Station"]]))
tempList.append(pointClass("Brush_Cleaning", False, [["Brush_Clean", "Docking_Station"]]))
tempPlant = plantClass("Diagnostic",tempList)
spec.append(tempPlant)
tempList.clear()
del tempPlant
# set up init plant

#tempList.append(pointClass("Init_Idle", False, [["Init_Start", "Init_Start"]]))
tempList.append(pointClass("Init_Start", False, [["Check_Motor", "Motor_Check"]]))
tempList.append(pointClass(
    "Motor_Check", False, [["Check_Battery", "Battery_Check"]],[["Init_Failed", "Idle"]]))
tempList.append(pointClass("Battery_Check", False, [["Check_Tank", "Tank_Check"]],[["Init_Failed", "Idle"]]))
tempList.append(pointClass(
    "Tank_Check", False, [["Check_Brushes", "Brushes_Check"]], [["Init_Failed", "Idle"]]))
tempList.append(pointClass(
    "Brushes_Check", False, [["Check_Filter", "Filter_Check"]], [["Init_Failed", "Idle"]]))
tempList.append(pointClass("Filter_Check", False, [], [["Work_Start", "Work"], ["Init_Failed", "Idle"]]))
tempPlant = plantClass("Init", tempList)
spec.append(tempPlant)
tempList.clear()
del tempPlant
# set up error plant

#tempList.append(pointClass("Error_Idle", False, [["Error_Signal", "Error_Diagnose"]]))
tempList.append(pointClass("Error_Diagnose", False, [["Module_Failed", "Power_Off"], ["Motor_Failed", "Power_Off"],
                                                          ["Cleaner_Damaged", "Power_Off"],
                                                          ["Battery_Failed", "Battery_Error"],
                                                          ["Brushes_Failed", "Brushes_Error"],
                                                          ["Filter_Failed", "Filter_Error"]]))
tempList.append(pointClass("Power_Off", True, []))
tempList.append(pointClass("Battery_Error", False, [["Battery_Damaged", "Power_Off"], ["Battery_Low", "Batter_Empty"]]))
tempList.append(pointClass("Batter_Empty", False, [],[["Error_To_Diagnose", "Diagnostic"]]))
tempList.append(pointClass("Brushes_Error", False, [],[["Error_To_Diagnose", "Diagnostic"]]))
tempList.append(pointClass("Brushes_Error", False,[],[["Filter_Error", "Diagnostic"]]))
tempPlant = plantClass("Error",tempList)
spec.append(tempPlant)
tempList.clear()
del tempPlant
# set up work plant

#tempList.append(pointClass("WorkIdle", True, [["Work_Start", "Move"]]))
tempList.append(pointClass("Move", False,
                                [["No_Obstacle", "Move"],
                                 ["Obstacle_On_Front", "ChooseDirection"]],[["Work_Done", "Idle"], ["Error_Signal", "Error"]]))
tempList.append(pointClass(
    "ChooseDirection", False, [["Obstacle_On_Left", "TurnRight"], ["Obstacle_On_Right", "TurnLeft"]]))
tempList.append(pointClass("TurnLeft", False, [["Turn_Done", "Move"]]))
tempList.append(pointClass("TurnRight", False, [["Turn_Done", "Move"]]))
tempPlant = plantClass("Work", tempList)
spec.append(tempPlant)
tempList.clear()
del tempPlant

while specLoop:

    while True:
        current_plant_name = spec[current_plant_id].name
        current_plant = spec[current_plant_id]
        print("Obecny punkt specyfikacji: " + current_plant_name)
        print("Obecny stan: " + current_plant.get_point_name(current_plant.current_point_id) + "\nMożliwe zdarzenia:")
        iterator = 0
        for event in current_plant.point_list[current_plant.current_point_id].event_list:
            print(str(iterator) + " - " + event[0])
            iterator += 1

        exit_iterator_start = iterator   # to recognize is this exit event or event inside plant
        if len(current_plant.point_list[current_plant.current_point_id].exit_parameters) != 0:
            for exit_event in current_plant.point_list[current_plant.current_point_id].exit_parameters:
                print(str(iterator) + " - " + exit_event[0])
                iterator += 1
        if (current_plant.point_list[current_plant.current_point_id].is_end_possible):
            print("x - End Automata")
        print("Podaj nowy punkt specyfikacji")
        user_choice = input()
        if user_choice.isnumeric():
            if int(user_choice) < len(current_plant.point_list[current_plant.current_point_id].event_list)+len(current_plant.point_list[current_plant.current_point_id].exit_parameters):
                if int(user_choice)>=len(current_plant.point_list[current_plant.current_point_id].event_list):
                    last_plant_id = get_plant(current_plant.name, spec)
                    current_plant_id = get_plant(current_plant.point_list[current_plant.current_point_id].exit_parameters[int(user_choice)-exit_iterator_start][1],spec)
                    spec[last_plant_id].current_point_id = 0
                else:
                    current_plant.current_point_id = get_point(current_plant.point_list[current_plant.current_point_id].event_list[int(user_choice)][1], current_plant.point_list)
        elif user_choice == 'x':
            print("Zakonczono pracę");
            specLoop = False
            break