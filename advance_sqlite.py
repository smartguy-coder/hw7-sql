import os
from support_module_advance_sqlite import *


def hw7_workflow():
    create_table_professions()
    add_new_profession('manager')
    add_new_profession('judge')
    add_new_profession('driver')
    create_table_genders()
    add_new_gender("Male")
    add_new_gender("Female")
    
    create_table_people()
    records_generator_people(100)
    add_new_gender("new gender")
    
    add_new_person("Bill", "Gates", 20, 50000, 1, None, 25)
    add_new_person("Jeff", "Benny", 50, 50000, 80, None, 60)
    
    add_new_person("Nik", "BUSH", 1, 80000, 1, 'N.BUCH@ukr.net', 60)
    amend_gender_by_surname("BUSH", 3)
    choose_people_by_gender(3)
    delete_records_from_table("genders", 3)
    choose_people_by_gender(3)

    select_all_with_gender_and_profession_with_filter_salary_more_than()
    select_all_with_gender_profession_not_required_with_filter_salary_more_than()
    delete_records_from_table("professions", 3)
    select_all_with_gender_profession_not_required_with_filter_salary_more_than()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    hw7_workflow()