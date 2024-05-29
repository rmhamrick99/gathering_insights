# gathering_insights

This was used to take a block of transcripts between a client and financial advisor and accomplish a multitude of things with them:

- Identify the points in the conversation when the client vs the agent is speaking.
- Summarize the conversation

Using the transcripts to gather insights:

- Risk tolerance level assigned
- Products mentioned
- Purpose of the call
- Entities extracted
- Next steps/action items
- Account holdings
- Client relationships

Each notebook calls to a column of a csv file that contains the transcript and leverages that in the notebook to build out an insight using gen ai in either a 1 or 2 shot aproach then writes it to an output file based on the conversation id. You will need to create a .env for the notebooks or insert the credentials.

To run the ui you will need to build out an output csv using the gathering insights notebooks. Then in the streamlitUI folder you can edit main.py to call to the column names you created in that output file. Add a logo or delete that line. Then cd into streamlitUI and run the command in the terminal "streamlit run main.py".
