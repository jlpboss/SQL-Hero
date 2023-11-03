from connection import create_connection, execute_query, execute_modify

create_connection("postgres", "postgres", "postgres")

class Input_Controller:

    def __init__(self, Creater, Reader, Updater, Deleter):
        # Create
        # Read (Y)
        # Update
        # Delete
        done = False
        while not done:
            self.action = input("What would you like to do? ").lower()
            match self.action:
                case "view hero":
                    Reader.view_hero()
                case "create hero":
                    Creater.create_hero()
                case "update hero":
                    Updater.update_hero()
                case "remove hero":
                    Deleter.delete_hero()
                case "done":
                    done = True
                    print("Thank you for useing the Hero Database")

class Creater:
    def create_hero(self):
        hero_done = False
        hero_name = ""
        hero_about_me = ""
        hero_powers = []
        hero_friends = []
        hero_enemies = []
        hero_bio = ""

        while not hero_done:
            query = """
            SELECT name FROM heroes
            """
            result = execute_query(query)
            query2 = """
            SELECT id FROM heroes
            """
            result2 = execute_query(query2)
            all_hero_names = [result[0], result2[0]]
            
            hero_name = input("New Hero Name: ")
            hero_about_me = input("New Hero About Me: ")
            
            done_with_powers = False
            hero_powers = []
            while not done_with_powers:
                power = input("New Hero's Power(Enter 'done' to finish): ")
                if power != "done":
                    hero_powers.append(power)
                else:
                    done_with_powers = True

            done_with_friends = False
            hero_friends = [[], []]
            while not done_with_friends:
                friend = input("New Hero's Friend(Enter 'done' to finish): ")
                if friend == "done":
                    done_with_friends = True
                elif friend in all_hero_names[0]:
                    hero_friends[0].append(friend)
                    hero_friends[1].append(all_hero_names.index(friend))
                else:
                    print("Not a valid hero name")
            
            done_with_enemies = False
            hero_enemies = [[],[]]
            while not done_with_enemies:
                enemy = input("New Hero's Enemy(Enter 'done' to finish): ")
                if enemy == "done":
                    done_with_enemies = True
                elif enemy in all_hero_names[0]:
                    hero_enemies[0].append(enemy)
                    hero_enemies[1].append(all_hero_names.index(enemy))

            hero_bio = input("New Hero Biography: ")

            hero_info_responce = False
            while not hero_info_responce:
                hero_info = """Is this corect? (y/n):
                Hero Name: {}
                Hero About Me: {}

                {}'s Power(s): {}

                Friends: {}
                Enemies: {}

                Biography: {} 
                    """.format(hero_name, hero_about_me, hero_name, ", ".join(hero_powers), ", ".join(hero_friends[0]), ", ".join(hero_enemies[0]), hero_bio)
                correct = input(hero_info)
                match correct:
                    case "y":
                        hero_done = True
                        hero_info_responce = True
                    case "n":
                        hero_done = False
                        hero_info_responce = True

        query = """
        INSERT INTO
            heroes (name, about_me, biography)
        VALUES
            (
                %s,
                %s,
                %s
        );
        """
        data = (hero_name, hero_about_me, hero_bio)

        execute_modify(query, data)

        query = """
        SELECT id FROM heroes WHERE name = %s AND about_me = %s;
        """
        data = (hero_name, hero_about_me)

        hero_id = execute_query(query, data)

        for item in hero_friends[1]:
            query = """
            INSERT INTO
                relationships (hero1_id, hero2_id, relationship_type_id)
            VALUES
                (%s, %s, 1);
            INSERT INTO
                relationships (hero1_id, hero2_id, relationship_type_id)
            VALUES
                (%s, %s, 1);
            """
            data = (hero_id, item, item, hero_id)

            execute_modify(query, data)

        query = """
        SELECT name FROM ability_types
        """
        query2 = """
        SELECT id FROM ability_types
        """
        list_of_powers = [execute_query(query)[0], execute_query(query)[1]]

        for item in hero_powers:
            if item in list_of_powers[0]:
                query = """
                INSERT INTO
                    abilities (hero_id, ability_type_id)
                VALUES
                    (%s, %s);
                """
                data = (hero_id[0], list_of_powers[1][list_of_powers[0].index(item)])
                execute_modify(query, data)
            else:
                list_of_powers[0] = list_of_powers[0] + (item, )
                query = """
                INSERT INTO
                    ability_types (name)
                VALUES
                    (%s);
                """
                data = (item, )
                execute_modify(query, data)
                query = """
                SELECT id FROM ability_types WHERE name = %s;
                """
                data = (item,)
                new_power_id = execute_query(query, data)
                query = """
                INSERT INTO
                    abilities (hero_id, ability_type_id)
                VALUES
                    (%s, %s);
                """
                data = (hero_id[0], new_power_id[0])
                execute_modify(query, data)

class Reader:
    def view_hero(self):
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
        hero_powers = self.convert_hero_id_to_powers(hero_id)
        [hero_friends, hero_enemies] = self.convert_hero_id_to_relationships(hero_id)
        hero_info = """
        Hero Name: {}
        Hero About Me: {}

        {}'s Power(s): {}

        Friends: {}
        Enemies: {}

        Biography: {}
        """.format(hero_data[0][1], hero_data[0][2], hero_data[0][1], hero_powers, hero_friends, hero_enemies, hero_data[0][3])
        print(hero_info)

    def convert_hero_id_to_powers(self, hero_id):
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
    
    def convert_hero_id_to_relationships(self, hero_id):
        query = """
        SELECT hero2_id, relationship_type_id FROM relationships WHERE hero1_id = {}
        """.format(hero_id)
        hero_relationships = execute_query(query)

        friends = []
        enemies = []
        
        for item in hero_relationships:
            query = """
            SELECT name FROM heroes WHERE id = {}
            """.format(item[0])
            hero2_name = execute_query(query)[0][0]
            query = """
            SELECT name FROM relationship_types WHERE id = {}
            """.format(item[1])
            relationship_type = execute_query(query)[0][0]
            match relationship_type:
                case "Friend":
                    friends.append(hero2_name)
                case "Enemy":
                    enemies.append(hero2_name)
        
        return [", ".join(friends), ", ".join(enemies)]

class Updater:
    pass

class Deleter:
    pass

c___ = Creater()
_r__ = Reader()
__u_ = Updater()
___d = Deleter()

db_controller = Input_Controller(c___, _r__, __u_, ___d)

