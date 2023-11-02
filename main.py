from connection import create_connection, execute_query, execute_modify

create_connection("postgres", "postgres", "postgres")

# query = """
# SELECT * from heroes
# """
# print(execute_query(query))

def view_hero():
    query = """
    SELECT name, id FROM heroes
    """
    data = execute_query(query)
    bad_hero_name = True
    hero_id = 0
    while bad_hero_name:
        who = input("What Hero would you like to view the profile of? ").lower()
        for item in data:
            if item[0].lower() == who:
                bad_hero_name = False
                hero_id = item[1]
        if bad_hero_name:
            print("No such hero, try again.")
    query = """
    SELECT * FROM heroes WHERE id = {}
    """.format(hero_id)
    hero_data = execute_query(query)
    hero_powers = convert_hero_id_to_powers(hero_id)
    hero_info = """
    Hero Name: {}
    Hero About Me: {}

    {}'s Power(s): {}

    Biography: {}
    """.format(hero_data[0][1], hero_data[0][2], hero_data[0][1], hero_powers, hero_data[0][3])
    print(hero_info)

def convert_hero_id_to_powers(hero_id):
    query = """
    SELECT ability_type_id FROM abilities WHERE hero_id = {}
    """.format(hero_id)
    ability_id_from_query = execute_query(query)
    ability_id = []
    for item in ability_id_from_query:
        ability_id.append(item[0])
    out = []
    for item in ability_id:
        query = """
        SELECT name FROM ability_types WHERE id = {}
        """.format(item)
        out.append(execute_query(query)[0][0])
    return ", ".join(out)



action = input("What would you like to do? ").lower()
match action:
    case "view hero":
        view_hero()



