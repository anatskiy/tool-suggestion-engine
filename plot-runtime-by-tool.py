
# coding: utf-8

# In[9]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io import sql
import sqlite3
import h5py


# In[2]:

try:
    conn = sqlite3.connect('/home/u/abc/galaxy/database/universe.sqlite')
except:
    print """please enter where database is located.
    Hint: locate database/universe.sqlite returns:"""
    get_ipython().system(u'locate database/universe.sqlite')


# In[3]:

query = '''
    SELECT job.tool_id, job.id, job_metric_numeric.job_id, metric_value AS runtime_seconds
    FROM job_metric_numeric INNER JOIN job
    WHERE metric_name=\'runtime_seconds\' AND job.id=job_metric_numeric.job_id
'''
tools_runtime = sql.read_sql(query,con=conn)


# In[4]:

runtime_dict = {}
for index, tool in enumerate(tools_runtime['tool_id']):
    try:
        runtime_dict[str(tool)]
    except:
        runtime_dict[tool] = []
    runtime_dict[tool].append(tools_runtime.runtime_seconds[index])


# In[5]:

for tool in runtime_dict.keys():
    plt.plot(range(0, len(runtime_dict[tool])), runtime_dict[tool], label=tool)
    plt.savefig(tool + '-runtime.png')
    plt.close()


# In[13]:

hdf = pd.HDFStore('storage.h5')


# In[20]:

hdf.put('runtime_by_tool', tools_runtime)


# In[21]:

hdf.close()


# In[ ]:




# In[ ]:



