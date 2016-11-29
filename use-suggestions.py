
# coding: utf-8

# In[ ]:




# In[2]:

import pandas as pd


# In[5]:

cd ../galaxy


# In[6]:

suggestion = pd.read_hdf('recommendation_table.hdf')


# In[7]:

for index, tool in enumerate(suggestion.tool):
    print tool, "possibly connected to", suggestion.suggestion[index], "proof", suggestion.proof[index], """
    
    """


# In[ ]:



