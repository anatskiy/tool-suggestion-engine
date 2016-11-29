
# coding: utf-8

# In[1]:




# In[7]:

import pandas as pd
import sqlite3
import re


# In[2]:

cd ../galaxy


# In[3]:

with open('./config/galaxy.ini') as file:
    # default
    db_path = 'database/universe.sqlite'

    # if different value in config file
    for line in file:
        if re.match('^database_connection\ =.*', line):
            db_path = re.sub('database_connection\ = sqlite:///./', '', line)
            # without the index the string finishes with a space
            db_path = re.sub('\?.*', '', db_path)[:-1]


# In[4]:

conn = sqlite3.connect(db_path)


# In[5]:

download_history_query = """
SELECT * FROM history
"""

download_workflows_steps_query = """
SELECT * FROM workflow_steps
"""

download_workflows_steps_connections_query = """
SELECT * workflow_steps_connections
"""

histo = pd.read_sql(download_history_query, con=conn)
w_steps = pd.read_sql(download_workflows_steps_query, con=conn)
w_steps_connexions = pd.read_sql(download_workflows_steps_connections_query, con=conn)


# In[6]:

histo.to_csv('histories.csv')
w_steps.to_csv('workflow_steps.csv')
w_steps_connexions.to_csv('workflow_steps_connexions.csv')


# In[ ]:



