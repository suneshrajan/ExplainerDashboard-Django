from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache
from base64 import b64encode, b64decode
import PyPDF2
import csv
import pandas as pd
import shutil
import os

# Haystack NLP Package
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def load_chat_document(request):
    file_data = request.data
    file_name_list:list = file_data['file_names']
    encoded_string_list:list = file_data['base_64s']

    # file_name_list = []
    # encoded_string_list = []
    # file_name_list.append("eng12.pdf")
    # with open("/home/suensh/Software/App/NLP-QA-MODEL/eng12.pdf", "rb") as file:
    #     pdf_data = file.read()
    #     encoded_data = b64encode(pdf_data)
    #     encoded_string_list.append('file base64,' + encoded_data.decode("utf-8"))
    cache.delete('trained_pipline_cache')
    for index,encoded_string in enumerate(encoded_string_list):
        decoded_file = decode_image(encoded_string = encoded_string)

        destination_path = 'static/uploaded_file/' + str(file_name_list[index])

        with open(destination_path, 'wb') as destination_file:
            destination_file.write(decoded_file)
        destination_file.close()

        training_file_path = 'static/training_file/' + str(file_name_list[index]).split('.')[0] + '.txt'

        upload_doc(destination_path, training_file_path)
    trained_pipeline = create_new_pipeline()
    return HttpResponse('got image')


def decode_image(encoded_string=None):
    print('Convert string to image file(Decode)')
    head, splited_image = encoded_string.split('base64,')
    decoded_file = b64decode(splited_image)
    return decoded_file


def upload_doc(input_file_path, output_file_path):
    
    # Loads a single document from a file path
    if input_file_path.endswith(".txt"):
        shutil.copy2(input_file_path, output_file_path)

    elif input_file_path.endswith(".pdf"):
        text = ''
        with open(input_file_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page_idx in range(len(pdf.pages)):
                page_obj = pdf.pages[page_idx]
                text += page_obj.extract_text()
        with open(output_file_path, 'w') as txt_file:
            txt_file.write(text)

    elif input_file_path.endswith(".csv"):
        with open(input_file_path, "r") as csv_file:
            with open(output_file_path, "w") as text_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    line = " ".join(row)  # Join the row elements with spaces
                    text_file.write(line + "\n")  # Write the line to the text file

    elif input_file_path.endswith(".xlsx"):
        df = pd.read_excel(input_file_path)  # Read Excel file into a DataFrame
        df.to_csv(output_file_path, sep=" ", index=False, header=False)  # Write DataFrame to a text file


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def train_doc_chat_model(request):
#     pipeline_status = create_new_pipeline()
#     return HttpResponse('Model Trained ...')


def create_new_pipeline():
    document_store = InMemoryDocumentStore(use_bm25=True)
    doc_dir = "static/training_file"
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run_batch(file_paths=files_to_index)

    retriever = BM25Retriever(document_store=document_store)

    reader = FARMReader(model_name_or_path="distilbert-base-uncased-distilled-squad", use_gpu=True)

    pipe = ExtractiveQAPipeline(reader, retriever)

    cache.set('trained_pipline_cache', pipe)
    return True


@api_view(['GET'])
@permission_classes([AllowAny])
def retrive_data_from_pipeline(request):
    query = "What is your weakness?" #request.data['query']
    tirained_pipleine = cache.get('trained_pipline_cache')
    if tirained_pipleine is None:
        create_new_pipeline()
        tirained_pipleine = cache.get('trained_pipline_cache')
    else:
        tirained_pipleine = cache.get('trained_pipline_cache')

    prediction = tirained_pipleine.run(
        query = query,
        params = { 
            "Retriever": {"top_k": 2},
            "Reader": {"top_k": 1}
        }
    )

    return HttpResponse(str(prediction['answers'][0].answer))