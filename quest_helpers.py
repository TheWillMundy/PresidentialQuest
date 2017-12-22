import random
import dynamo_connect as db_connect

# all_presidents = ['George Washington', 'John Adams', 'Thomas Jefferson', 'James Madison', 'James Monroe', 'John Quincy Adams', 'Andrew Jackson', 'Martin Van Buren', 'William Henry Harrison', 'John Tyler', 'James K. Polk', 'Zachary Taylor', 'Millard Fillmore', 'Franklin Pierce', 'James Buchanan', 'Abraham Lincoln', 'Andrew Johnson', 'Ulysses S. Grant', 'Rutherford B. Hayes', 'James A. Garfield', 'Chester A. Arthur', 'Grover Cleveland', 'Benjamin Harrison', 'William McKinley', 'Theodore Roosevelt', 'William H. Taft', 'Woodrow Wilson', 'Warren G. Harding', 'Calvin Coolidge', 'Herbert Hoover', 'Franklin Delano Roosevelt', 'Harry S. Truman', 'Dwight D. Eisenhower', 'John F. Kennedy', 'Lyndon B. Johnson', 'Richard Nixon', 'Gerald R. Ford', 'Jimmy Carter', 'Ronald Reagan', 'George Herbert Walker Bush', 'Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump']

# all_villains = {'Aaron Burr': "", 'Citizen Genet': "", 'King George III': ""}

def random_president():
    if len(db_connect.get_presidents()) > 0:
        return random.choice(db_connect.get_presidents())
    else:
        return ""

def random_villain():
    all_villains = db_connect.get_villains()
    if len(all_villains.keys()) > 0:
        chosen_villain = random.choice(all_villains.keys())
        villain_backstory = all_villains[chosen_villain]
        return chosen_villain, villain_backstory
    else:
        return "", ""
