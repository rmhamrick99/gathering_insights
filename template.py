
import os
import pandas as pd
from ibm_watson_machine_learning.foundation_models import Model
from dotenv import load_dotenv
load_dotenv()

# below are connection details of watsonx account
apikey = os.getenv("GENAI_API")
project_id = os.getenv("GENAI_PRO_ID")
url = "https://us-south.ml.cloud.ibm.com"
creds= {
		"url" : url,
        "apikey": apikey
	}
params = {
        "decoding_method" : "greedy",
        "max_new_tokens" : 400,
        "min_new_tokens" : 0,
        "temperature" : 0.0,
        "repetition_penalty" :1.0 
    }
def send_to_watsonxai(data, prompt_template, parameters, model_name):
    
    prompt_data = prompt_template + "\n\n Input: " + data + "\n Output: "

    model = Model(
    model_id=str(model_name),
    params = parameters,
    credentials = creds,
    project_id = project_id,)
    response = model.generate(prompt_data)
    result = response['results'][0]['generated_text']
    return (result) 


def remove_not_mentioned(data):
    substring = "not mentioned"
    if substring in data.lower():
        data = data.lower().replace(substring, "")
        return data
    else:
        return data

#  read file
df = pd.read_csv('clean_smaller_chunks_20.csv')

#  prompt variable level 1
LEVEL1_PROMPT = """
your level 1 prompt goes here
"""

#  df['risks_data'] = (lambda command for prompting)
df['<insert col name>'] = df['<insert code col name>'].map(lambda x:send_to_watsonxai(data=x, prompt_template=LEVEL1_PROMPT, parameters=params, model_name="google/flan-ul2"))
#commmand to view in your terminal the first 5 
df.head()
# backup: save chunked file (temporary) by running df.to_csv('backup.csv', index=False)

# OPTIONAL: if you want to remove "not mentioned" run below
# df['<insert col name>'] = df_clean['<insert col name>'](lambda x:remove_not_mentioned(x)).reset_index()


df_og = pd.read_csv('file.csv')
# [OPTIONAL] If column name already in file.csv
#  you can either rename or delete those using one of these:
# df_output = df_output.drop([['<insert col name>']], axis=1)
# df_output = df_output.rename({'<insert col name>': '<insert col name>_v2'}, axis=1)

df_og.head()

df_join = pd.merge(df, df_og, on='<insert index for code>', how='left')
# the result should be all the original columns (in file.csv) + <insert col name>
df_join.head()
df_join.to_csv('file.csv')
