"""USER: to input your descired foods, see the list at the bottom called test_foods.
To run, open your terminal and type 'python get_ingredients.py, then follow the prompts.'"""

import re
import openai
import pandas as pd
openai.api_key = 'YOUR_API_KEY'
# openai.api_key = input('Please type your ChatGPT API key: ')
import time

def get_ingredients(test_food,yes_no, stop_words = [], simplify=False):
    def make_string():
        str = "List the recipe ingredients of "+test_food+" without listing ingredient quantities. Be concise and do not number the list."
        return str
    def check_descrip(uncleaned_list, choice = 0):
        ls = uncleaned_list
        modified_list = []
        for ingredient in ls:
            if ')' in ingredient:
                start = ingredient.index('(')
                end = ingredient.index(')')
                base = ingredient[:start-1]
                detail = ingredient[start+1:end]
                choices = [detail, base, base+' ('+detail+')',ingredient]
                ingredient = detail
                if choice == 0:
                    if choices[2] == choices[3]:
                        pick = input('Which ingredient would you like? Type a number: 1 (specific)- '+choices[0]+', 2 (generalized)- '+choices[1]+', 3 (original)- '+choices[2]+': ')
                        ingredient = choices[int(pick)-1]
                    else:
                        pick = input('Which ingredient would you like? Type a number: 1 (specific)- '+choices[0]+', 2 (generalized)- '+choices[1]+', 3 (detailed)- '+choices[2]+', 4 (original)- '+choices[3]+': ')
                        ingredient = choices[int(pick)-1]
            if (' and ' in ingredient) or (' or ' in ingredient) or ('and/or' in ingredient) or ('contain' in ingredient) or (len(ingredient)>30):
                ings = input('Does this token "'+ingredient+'" represent more than one ingredient? If so, please type the ingredients separated by a comma WITH NO SPACE (example - vitamin A,zinc). Otherwise, type nothing and hit enter: ')
                if len(ings)>0:
                    ings=ings.split(',')
                    for ing in ings:
                        modified_list.append(ing)
            elif ingredient not in stop_words: # make sure it's an ingredient we want to include
                modified_list.append(ingredient)
        return modified_list

    # Query ChatGPT
    req = make_string()
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": req}]
    )
    out = completion.choices[0].message.content
    # out = 'chicken (a bird), this and that, them. their'
    print('Chat GPT output: ',out)

    # preliminary cleaning (lower case and remove periods)
    out = out.lower()
    p1 = True
    while p1 == True:
        if ('. ' in out) and (out.index('. ')<len(out)-2): # check if there are multiple sentences (such as an allergy statement)
            loc = out.index('. ')
            out = [o for o in out]
            out[loc] = ','
            out = ''.join(out)
        else:
            p1 = False
    # otherwise, remove the periods
    p2 = True
    while p2 == True:
        if '.' in out:
            loc = out.index('.')
            out = [o for o in out]
            out[loc] = ''
            out = ''.join(out)
        else:
            p2 = False
        # out = re.sub(r".", "", out)
    out = out.split(', ')
    # make sure there isn't an "and" before the last ingredient
    if 'and ' == out[-1][0:4]:
        out[-1] = out[-1][4:]
    if yes_no == 1: # if they don't want to clarify, return the list as is
        return out
    return check_descrip(out,simplify)

# Main:
# let the user choose how they want their ingredients
a = True
b = True
yes_no = input('Would you like to clarify ingredient names? Type a number: 0 - Yes, 1 - No')
# if int(yes_no)==1: # 1 = No, don't want to clarify
#     a = False
simplify = 1
if int(yes_no) ==0:
    simplify= input('Great, would you like to select the level of detail of ingredient names or default to greater detail? Type a number: 0 - I want to make selections, 1 - add detail for me')

# BEGIN USER CUSTOMIZE ZONE * type all words in lower case without punctuation *


original_test_foods = ['soup cream of asparagus canned condensed',
 'soup bean with pork canned condensed',
 'soup beef broth or bouillon canned ready to serve',
 'soup beef noodle canned condensed',
 'soup cream of celery canned condensed',
 'soup cheese canned condensed',
 'soup chicken broth canned condensed',
 'soup chicken canned chunky ready to serve',
 'soup cream of chicken canned condensed',
 'soup chunky chicken noodle canned ready to serve',
 'soup chicken noodle canned condensed',
 'soup clam chowder new england canned prepared with equal volume water',
 'soup cream of mushroom canned prepared with equal volume water',
 'soup pea green canned prepared with equal volume water',
 'soup cream of shrimp canned prepared with equal volume water',
 'soup tomato beef with noodle canned prepared with equal volume water']

# start_idx = input('Enter start index of list for this terminal')
# end_idx = input('Enter end index of list for this terminal. If end of list, type !')
start_idx = 0
end_idx = '!'

if end_idx == '!':
    original_test_foods = original_test_foods[int(start_idx):]
else:
    original_test_foods = original_test_foods[int(start_idx):int(end_idx)+1]
test_foods = original_test_foods.copy()
custom_stop_words = ['canned', 'condensed', 'baked', 'commercially', 'prepared', 'ready', 'to', 'eat', 'include', 'includes', 'with']

# END USER CUSTOMIZE ZONE
big_list = []
start = time.perf_counter()
time2 = start
count = 0
while len(test_foods)>0:
    time_diff = time2 - start
    if (time_diff >= 61) or (count == 0):
        count = 1
        print('time diff', time_diff)
        if len(test_foods)>=3:
            to_test = test_foods[0:3]
            test_foods = test_foods[4:]
            ingredients_list = [get_ingredients(f,int(yes_no),stop_words = custom_stop_words, simplify = int(simplify)) for f in to_test]
            big_list = big_list + ingredients_list
        else:
            ingredients_list = [get_ingredients(f,int(yes_no),stop_words = custom_stop_words, simplify = int(simplify)) for f in test_foods]
            big_list = big_list + ingredients_list
        start = time.perf_counter()
    else:
        time2 = time.perf_counter()



df = pd.DataFrame()
df['foods'] = original_test_foods
df['ingredients']  = big_list #[str(i) for i in ingredients_list]
# print(ingredients_list)
save = input('Would you like to save this data as a csv? If so, type the file name (example - my foods). Otherwise, click enter:')
if len(save)>0:
    df.to_csv('./'+save+'.csv',index=False)
    print('Your data has been saved as '+save+'.csv in your current working directory.')
