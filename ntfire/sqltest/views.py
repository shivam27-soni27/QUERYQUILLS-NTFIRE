from django.shortcuts import render
file=""
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import os
import csv
import csv
import pandas as pd
import mysql.connector
from django.http import JsonResponse

def upload_file(request):
    if request.method == 'POST' and request.FILES['file_upload']:
        uploaded_file = request.FILES['file_upload']
        
        df = pd.read_csv(uploaded_file)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shivam1shivam",
            database="queryquill"
        )

        cursor = conn.cursor()

        # Extract column names from the first row of the CSV file
        first_row = df.columns.tolist()

        # Generate table name from the file name
        table_name = str(uploaded_file).replace(" ","_").replace(".csv","")
        table_name = table_name[::-1]
        try:
            table_name = table_name[:table_name.index('/')]
        except:
            pass
        table_name = table_name[::-1]

        # Create table if not exists with the columns from the first row of CSV
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} VARCHAR(255)' for col in first_row])})"
        cursor.execute(create_table_query)

        # Insert data into the table
        for index, row in df.iterrows():
            sql = f"INSERT INTO {table_name} ({', '.join(first_row)}) VALUES ({', '.join(['%s' for _ in first_row])})"
            values = tuple(row)
            cursor.execute(sql, values)

        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse({'data': 'File uploaded successfully.'})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

def index(request):
    return render(request, 'index.html')
    
def login(request):
    return render(request, 'popup.html')

import re

def extract_sql_queries(query_string):
    # Regular expression pattern to match various types of SQL queries
    sql_pattern = r'\b(INSERT\s.*?;\s*|SELECT\s.*?;\s*|DELETE\s.*?;\s*|DROP\s.*?;\s*|UPDATE\s.*?;\s*|ALTER\s.*?;\s*)'

    # Find all matches of SQL queries in the string
    sql_queries = re.findall(sql_pattern, query_string, re.IGNORECASE | re.DOTALL)

    return sql_queries
def datafetch():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shivam1shivam",
        database="queryquill"
    )
    cursor=conn.cursor()

    cursor.execute("show tables")
    tables=cursor.fetchall()
    for i in range(len(tables)):
        cursor.execute(f"desc {tables[i][0]}")
        tables[i]=cursor.fetchall()
    return tables
    cursor.close()
    conn.close()
def process_form(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        print(input_data)
        
        # Predefined list of SQL keywords and commands
        sql_keywords = ['select', 'insert', 'delete', 'update', 'drop', 'alter', 'create', 'show', 'desc', 'schema', 'table', 'sql', 'database', 'databases', 'use', 'desc', 'show', 'tables', 'describe', 'show', 'tables', 'show', 'databases', 'create', 'alter', 'drop', 'update', 'delete', 'insert', 'make', 'change', 'modify', 'rename', 'replace', 'rename', 'rename', 'rename to', 'rename as', 'rename table', 'rename column', 'rename database', 'rename schema', 'rename index', 'rename key', 'rename constraint', 'rename column', 'rename column to', 'rename column as', 'rename column in', 'rename column from', 'rename column of', 'rename column on', 'rename column with', 'rename column by', 'rename column for', 'rename column as', 'rename column is', 'rename column are', 'rename column not', 'rename column null', 'rename column not null', 'rename column primary key', 'rename column foreign key', 'rename column unique', 'rename column index', 'rename column key', 'rename column constraint', 'rename column default', 'rename column auto_increment', 'rename column auto increment', 'rename column autoincrement', 'rename column auto increment', 'rename column autoincrement', 'rename column auto increment by', 'rename column auto increment to', 'rename column autoincrement to', 'rename column auto increment as', 'rename column autoincrement as', 'rename column auto increment in', 'rename column autoincrement in', 'rename column auto increment from', 'rename column autoincrement from']

        # Split input data into words and check if any word is not in the SQL keywords list
        input_words = input_data.split()
        num=0
        for i in range(len(input_words)):
            input_words[i] = input_words[i].lower() 
            if input_words[i] in sql_keywords:
                pass
            else:
                num=num+1
        if num==len(input_words):
            return JsonResponse({'output': 'Invalid SQL Query'})
        else:
            # Valid SQL query
            # Your further processing logic goes here
            pass
        from huggingface_hub import hf_hub_download

#model_name = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
#model_file = "tinyllama-1.1b-chat-v1.0.Q8_0.gguf"
#model_path1 = hf_hub_download(model_name, filename=model_file)
#print(f"Model downloaded to: {model_path1}")

        from llama_cpp import Llama

        llm = Llama(model_path=r"C:\Users\SHIVAM\.cache\huggingface\hub\models--TheBloke--TinyLlama-1.1B-Chat-v1.0-GGUF\snapshots\52e7645ba7c309695bec7ac98f4f005b139cf465\tinyllama-1.1b-chat-v1.0.Q8_0.gguf",n_ctx=512,n_threads=8,n_gpu_layers=40)

        #output = llm("<|im_start|>user\nAre you a robot?<|im_end|>\n<|im_start|>assistant\n",max_tokens=512, stop=["</s>"],)

        def chat_template(question, context):
            """
            Creates a chat template for the Llama model.

            Args:
                question: The question to be answered.
                context: The context information to be used for generating the answer.

            Returns:
                A string containing the chat template.
            """

            template = f"""\
            <|im_start|>user
            Given the context, generate an SQL query for the following question
            PLEASE GIVE ONLY SQL QUERY AS OUTPUT NOTHING ELSE
            do not give output
            context:{context}
            question:{question}
            <|im_end|>
            <|im_start|>assistant 
            """
            template1 = "\n".join([line.lstrip() for line in template.splitlines()])
            return template1
        
        question = input_data
        context = ""
        #print(chat_template(question,context))
        output = llm(
            chat_template(input_data, context),
            max_tokens=512,
            stop=["</s>"],
        )
        processed_data=output['choices'][0]['text']
        
        return JsonResponse({'output':processed_data})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def execute_query(request):
    global file
    if request.method == 'POST'     :
        if file=="":
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
        else:
            pass
        return JsonResponse({'message': 'Query executed successfully.'})
    else:
        # Return an error response if the request is not valid
        return JsonResponse({'error': 'Invalid request.'}, status=400)
