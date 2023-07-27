import re
import openai
import pandas as pd
openai.api_key = 'YOUR_API_KEY'
# openai.api_key = input('Please type your ChatGPT API key: ')
def get_synonyms(test_food, stop_words = []):
    def make_string():
        str = "List 10 synonyms for "+test_food+". Be concise and do not number the list."
        return str
    # Query ChatGPT
    yes_no=1
    req = make_string()
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": req}]
    )
    out = completion.choices[0].message.content
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
    out = out.split(', ')
    # make sure there isn't an "and" before the last ingredient
    if 'and ' == out[-1][0:4]:
        out[-1] = out[-1][4:]
    if yes_no == 1: # if they don't want to clarify, return the list as is
        return out
    return out

# Main:

# BEGIN USER CUSTOMIZE ZONE * type all words in lower case without punctuation *

test_foods = ['soup cream of asparagus canned condensed',
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

custom_stop_words = ['canned', 'condensed', 'baked', 'commercially', 'prepared', 'ready', 'to', 'eat', 'include', 'includes', 'with']

# END USER CUSTOMIZE ZONE
syn_list = [get_synonyms(f,stop_words = custom_stop_words) for f in test_foods]
df = pd.DataFrame()
df['foods'] = test_foods
df['synonyms']  = syn_list #[str(i) for i in syn_list]
print(syn_list)
save = input('Would you like to save this data as a csv? If so, type the file name (example - my foods). Otherwise, click enter:')
if len(save)>0:
    df.to_csv('./'+save+'.csv',index=False)
    print('Your data has been saved as '+save+'.csv in your current working directory.')
