
# coding: utf-8

# In[145]:




# In[4]:

import pandas as pd
import sqlite3
import re
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.histories import HistoryClient


# In[5]:

cd ../galaxy


# ## config

# In[6]:

with open('./config/galaxy.ini') as file:
    # default
    db_path = 'database/universe.sqlite'

    # if different value in config file
    for line in file:
        if re.match('^database_connection\ =.*', line):
            db_path = re.sub('database_connection\ = sqlite:///./', '', line)
            # without the index the string finishes with a space
            db_path = re.sub('\?.*', '', db_path)[:-1]


# ## connect to database

# In[7]:

conn = sqlite3.connect(db_path)


# In[8]:

api_key = open('../galaxy_api_key').read()
galaxy_url = 'http://localhost:8080'
gi = GalaxyInstance(galaxy_url, api_key)


# ## alternative: load workflows from local files
local_workflow_folder = '../tool-suggestion-engine/shared-workflows'
list_of_wo = !ls $local_workflow_folder/*.gafor file in list_of_wo:
    gi.workflows.import_workflow_from_local_path(file)
# ## alternative: load histories from files and convert histories to workflows
hi = HistoryClient(gi)
# download histories to a binary file

# for id in [item['id'] for item in hi.get_histories()]:
#     hi.download_history(id, hi.export_history(id), open(str(id) + '.history', 'w'), chunk_size=4096)

# upload binary history to database
# 
print "not supported by the API"
# ## clear workflow table
for w in gi.workflows.get_workflows():
    gi.workflows.delete_workflow(w['id'])
# Display existing workflows
!scripts/api/./display.py $(cat ../galaxy_api_key) http://localhost:8080/api/workflows
# ## alternative: upload histories and workflows downloaded with SQL
histo_read = pd.read_csv('histories.csv')
w_steps_read = pd.read_csv('workflow_steps.csv')
w_steps_connexion_read = pd.read_csv('workflow_steps_connexions.csv')
# **ACHTUNG: the following _update_ query may break the versionning of the database**
histo_read.to_sql('history', con=conn, if_exists='replace')
w_steps_read.to_sql('workflow_steps', con=conn, if_exists='replace')
w_steps_connexion_read.to_sql('workflow_steps_connexions', con=conn, if_exists='replace')
# ## Extract workflows from histories

# Display existing histories
!scripts/api/./display.py $(cat ../galaxy_api_key) http://localhost:8080/api/historiesdef extract_workflow_from_history(wid):
    payload = "{'from_history_id': '" + wid + "', 'workflow_name': '" + wid + "'}"
    key = !cat ../galaxy_api_key
    print key[0]
    print requests.post("http://localhost:8080/api/workflows?key=" + str(key[0]),
                         headers={'Content-Type': 'application/json'}, data=payload).content
    
    #os.system("curl  http://localhost:8080/api/workflows?key=$(cat ../galaxy_api_key) \
   # -H 'Content-Type: application/json' --data \"" + payload + "\"" )
# The attempt to pass a string variable to the curl command in os.system fails (too many levels of \").
# 
# The following function stores the _payload_ in a file before passing the query.

# In[9]:

def extract_workflow_from_history(wid):
    payload = "{\"from_history_id\": \"" + wid + "\",  \"workflow_name\": \"" + "extracted-" +  wid + "\"}"
    open('payload.json', 'w').write(payload)
    get_ipython().system(u'curl http://localhost:8080/api/workflows?key=$(cat ../galaxy_api_key) -H "Content-Type: application/json"    --data @payload.json')
    get_ipython().system(u'rm -f payload.json')


# Extract history and display the extracted history

# In[10]:

for item in gi.histories.get_histories():
    extract_workflow_from_history(item['id'])
    print


# Display uploaded workflows and extracted workflows
!scripts/api/./display.py $(cat ../galaxy_api_key) http://localhost:8080/api/workflows
# ## get connections
# 
# 1. get connections (by id of workflow steps)
# 2. get tool id corresponding to each workflow step

# In[11]:

get_associations_query = '''
SELECT distinct w_s.workflow_id, w_s.id AS out_port, w_c.input_step_id AS in_port
FROM workflow_step AS w_s, workflow_step_connection AS w_c
WHERE w_s.id=w_c.output_step_id
'''
assoc = pd.read_sql(get_associations_query, con=conn)

print assoc[:10]


# In[12]:

get_tool_id_query = '''
SELECT distinct w_s.id, w_s.tool_id
FROM workflow_step AS w_s
'''

step_tool = pd.read_sql(get_tool_id_query, con=conn)
print step_tool[:10]


# ## replace degenerated step id by unique tool id

# In[13]:

out_tool_ids = [step_tool.tool_id[step_tool.id == item].values[0] for index, item in enumerate(assoc.out_port)]
in_tool_ids = [step_tool.tool_id[step_tool.id == item].values[0] for index, item in enumerate(assoc.in_port)]

assoc.insert(0, 'out_port_tool', pd.DataFrame(out_tool_ids))
assoc.insert(1, 'in_port_tool', pd.DataFrame(in_tool_ids))
print assoc[:10]


# ## association rule identification
# 
# dictionnary with tool as key and tool connected as output as values

# ## count associations

# In[14]:

d = {}

for item in assoc.out_port_tool.unique():
    d[item] = [{}]

for index, tool in enumerate(assoc.out_port_tool):
    #print index, tool, assoc.in_port_tool[index]
    if assoc.in_port_tool[index] not in d[tool][0].keys():
        d[tool][0][assoc.in_port_tool[index]] = 1
    else:
        d[tool][0][assoc.in_port_tool[index]] += 1


# ## sort associations by frequency

# In[15]:

recomm = {'tool': [], 'suggestion': [], 'proof': []}

for tool in d.keys():
    #d[tool].sort(key=lambda x: x[1])çç
    
    tool_max = max(d[None][0], key=d[None][0].get)
    
    recomm['tool'].append(tool)
    recomm['suggestion'].append(tool_max)
    recomm['proof'].append( sorted(d[tool][0].values())[-1]  )


# In[16]:

recommendation = pd.DataFrame(recomm)


# In[17]:

recommendation.to_hdf('recommendation_table.hdf', 'w')


# ## Use 

# see [use-suggestions.ipynb](use-suggestions.ipynb) and [use-suggestions.py](use-suggestions.py)
