import json
from importlib import reload 
import pickle 

import glob 
json_files = glob.glob("v1.0/train/*.jsonl")
print(json_files)
#json_files=glob.glob("*.gz")

k=0
count=0
extracted_data=[]

for file in json_files:
	print(file)
	with open(file) as f:
	    
		for l in f:
			k=k+1
			if k%1000==0:
				print(k)
			data = json.loads(l)

			if data['annotations'][0]['yes_no_answer'] != 'NONE':
				continue 
			if data['annotations'][0]['long_answer']['candidate_index']== -1:
				continue 

			answer_start_byte = data['annotations'][0]['long_answer']['start_byte']
			answer_end_byte = data['annotations'][0]['long_answer']['end_byte']
			question = data['question_text']
			context = ""

			for i in data['document_tokens']:
				token=i['token']
				html_token = i['html_token']
				context_len = len(context)

				if i['start_byte']==answer_start_byte:
					answer_start = context_len
				if i['end_byte']==answer_end_byte:
					answer_end=context_len 

				if not html_token:
					context = context + " " + token 

			answer = context[answer_start+1:answer_end]

			extracted_data.append({"answer":answer,"answer_start":answer_start + 1, "context":context,
				"question":question})

with open('extracted_data_all.pickle','wb') as handle:
	pickle.dump(extracted_data,handle,protocol=pickle.HIGHEST_PROTOCOL)



