import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__)))))
from index import *



# path_hole_mark = MMpy.Project.path() + "Итоговое задание\Задание 1\Съемка устьев.DAT"
path_hole = MMpy.Project.path() + "Итоговое задание\Задание 1\Устья скважин.DAT"
get_list_fields(path_hole)
#
#
# project_data = get_list_fields(path_hole)
# mark_data = get_list_fields(path_hole_mark)
#
# admission = calculate_admission(project_data, mark_data)
# print(admission)