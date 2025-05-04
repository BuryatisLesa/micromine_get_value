import MMpy

path_hole_mark = MMpy.Project.path() + "Итоговое задание\Задание 1\Съемка устьев.DAT"
path_hole = MMpy.Project.path() + "Итоговое задание\Задание 1\Устья скважин.DAT"

def get_list_fields(path_file):
    file = MMpy.File()
    file.open(path_file)
    records_field = file.records_count
    fields_name = []
    for name_field in range(file.structure.fields_count):
        field_name = file.structure.get_field_name(name_field)
        fields_name.append(field_name)

    id_fields = []

    for i in fields_name:
        id_fields.append(file.get_field_id(i))

    list_file = []
    for id_field in id_fields:
        blank_list = []
        for rec in range(records_field):
            blank_list.append(file.get_str_field_value(id_field, rec+1))
        list_file.append(blank_list)
    dict_file = dict(zip(fields_name, list_file))
    print(dict_file)
    return dict_file

    file.close()


dict_1 = {'Hole': ['DH_1', 'DH_2', 'DH_3', 'DH_4', 'DH_5'], 'EAST': ['-2012.740', '-1094.724', '-22.145', '1556.280', '2558.603'], 'NORTH': ['851.694', '631.557', '551.933', '570.668', '547.250'], 'RL': ['10.000', '5.000', '10.000', '11.000', '8.000'], 'CODE': ['', '', '', '', ''], 'ЦВЕТ': ['', '', '', '', ''], 'Глубина': ['40.0', '30.0', '20.0', '50.0', '10.0']}
dict_2 = {'EAST': ['-2012.348634', '-1095.202021', '-22.939082', '1555.819952', '2558.240606'], 'NORTH': ['850.413450', '630.285690', '550.850280', '569.365051', '546.292907'], 'RL': ['10.000000', '5.000000', '10.000000', '11.000000', '8.000000'], 'CODE': ['', '', '', '', ''], 'ЦВЕТ': ['', '', '', '', '']}



def calculate_admission(project_data, mark_data):
    east_project = project_data['EAST']
    north_project = project_data['NORTH']
    rl_project = project_data['RL']
    east_mark_data = mark_data['EAST']
    north_mark_data = mark_data['NORTH']
    rl_mark_data = mark_data['RL']
    difference_east = []
    difference_north = []
    difference_rl = []

    for east_p, east_mark in zip(east_project,east_mark_data):
        res = float(east_p) - float(east_mark)
        difference_east.append(res)

    for north_p, north_mark in zip(north_project, north_mark_data):
        res = float(north_p) - float(north_mark)
        difference_north.append(res)

    for rl_p, rl_mark in zip(rl_project, rl_mark_data):
        res = float(rl_p) - float(rl_mark)
        difference_rl.append(res)

    admission = max(max(difference_north),max(difference_east))
    rl_admission = max(difference_rl)
    admission_list = []
    admission_list.append(admission)
    admission_list.append(rl_admission)
    return admission_list


admission = calculate_admission(dict_1, dict_2)

def comparison(admission, default, mark_data):
    name_project = default['Hole']
    east_project = default['EAST']
    north_project = default['NORTH']
    east_mark_data = mark_data['EAST']
    north_mark_data = mark_data['NORTH']
    valid_data_east = []
    valid_data_north = []
    dict_name_coord = {}

    for east_p, east_m, in zip(east_project, east_mark_data):
        res = float(east_p) - float(east_m)
        if res <= admission[0]:
            valid_data_east.append(east_m)

    for north_p, north_m in zip(north_project, north_mark_data):
        res = float(north_p) - float(north_m)
        if res <= admission[0]:
            valid_data_north.append(north_m)

    for name, east in zip(name_project, valid_data_east):
        dict_name_coord[name] = [east]

    for name, north in zip(name_project, valid_data_north):
        dict_name_coord[name].append(north)

    return dict_name_coord




valided_coord = comparison(admission, dict_1, dict_2)

def add_name(path, coord):
    x_name = "EAST"
    y_name = "NORTH"
    hole = 'Hole'
    file = MMpy.File()
    file.open(path)
    structure = file.structure
    if file.get_field_id(hole) ==  -1:
        structure.add_field(hole, MMpy.FieldType.character, 20)
    rec = file.records_count
    id_hole = file.get_field_id(hole)
    id_east = file.get_field_id(x_name)
    id_north = file.get_field_id(y_name)
    file.structure = structure
    for key, i in zip(coord.keys(), range(rec)):
        if round(file.get_num_field_value(id_east, i+1), 6) == round(float(coord[key][0]), 6) and round(file.get_num_field_value(id_north, i+1), 6) == round(float(coord[key][1]), 6):
            file.set_field_value(id_hole, i+1, key)
        else:
            file.set_field_value(id_hole, i+1, 'Error')
    file.close()
add_name(path_hole_mark, valided_coord)

