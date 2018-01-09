import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Presidential_Facts')
users = dynamodb.Table('Presidential_Users')
villains = dynamodb.Table('Presidential_Villains')

# all_presidents = ['George Washington', 'John Adams', 'Thomas Jefferson', 'James Madison', 'James Monroe', 'John Quincy Adams', 'Andrew Jackson', 'Martin Van Buren', 'William Henry Harrison', 'John Tyler', 'James K. Polk', 'Zachary Taylor', 'Millard Fillmore', 'Franklin Pierce', 'James Buchanan', 'Abraham Lincoln', 'Andrew Johnson', 'Ulysses S. Grant', 'Rutherford B. Hayes', 'James A. Garfield', 'Chester A. Arthur', 'Grover Cleveland', 'Benjamin Harrison', 'William McKinley', 'Theodore Roosevelt', 'William H. Taft', 'Woodrow Wilson', 'Warren G. Harding', 'Calvin Coolidge', 'Herbert Hoover', 'Franklin Delano Roosevelt', 'Harry S. Truman', 'Dwight D. Eisenhower', 'John F. Kennedy', 'Lyndon B. Johnson', 'Richard Nixon', 'Gerald R. Ford', 'Jimmy Carter', 'Ronald Reagan', 'George Herbert Walker Bush', 'Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump']

# President Methods
def get_presidents():
    all_presidents = []
    table_data = table.scan()
    for pres_obj in table_data['Items']:
        if pres_obj['President'] not in all_presidents:
            all_presidents.append(pres_obj['President'])
    return all_presidents

def get_facts(president):
    returned_facts = []
    president_facts = table.query(
        KeyConditionExpression=Key('President').eq(president)
    )
    for fact in president_facts['Items']:
        single_fact = str(fact['Fact'])
        returned_facts.append(single_fact)
    return returned_facts

def add_facts(president, fact):
    item = {
        'President': president,
        'Fact': fact
    }
    response = table.put_item(Item=item)
    return "Success!"

# Villain Methods
def get_villains():
    all_villains = {}
    table_data = villains.scan()
    for vil_obj in table_data['Items']:
        villain = vil_obj['Villain']
        if villain not in all_villains.keys():
            all_villains[villain] = (vil_obj['Backstories'][0], vil_obj['ArchEnemy'])
    return all_villains

# User Methods
def check_user(user_id):
    user_exists = users.query(
        KeyConditionExpression=Key('UserId').eq(user_id)
    )
    print "Found User: ", user_exists
    if len(user_exists['Items']) == 0:
        return "DNE"
    return str(user_exists['Items'][0]['Name'])

def add_user(user_id, name):
    if check_user(user_id) != "DNE":
        return "Already exists!"
    else:
        new_user = {
            'UserId': user_id,
            'Name': name
        }
        response = users.put_item(Item=new_user)
        # print dynamodb.get_item(Table="Users", Key=user_id)
        return "User successfully added!"
