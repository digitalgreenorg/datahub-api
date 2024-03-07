# from langchain.document_loaders import PdfLoader
import argparse
import concurrent.futures
import csv
import json
import logging
import os
import re
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from urllib.parse import quote_plus
from uuid import UUID

import certifi
import openai
import pytz
import requests
from bs4 import BeautifulSoup
from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Cast

# from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# from langchain import PromptTemplate
# from langchain.docstore.document import Document
from langchain.document_loaders import (
    BSHTMLLoader,
    CSVLoader,
    JSONLoader,
    PyMuPDFLoader,
    UnstructuredHTMLLoader,
)

# from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.vectorstores.pgvector import DistanceStrategy
from pgvector.django import CosineDistance, L2Distance
from psycopg.conninfo import make_conninfo


# import fitz
from requests import Request, Session
from requests.adapters import HTTPAdapter
from sqlalchemy.dialects.postgresql import dialect
from urllib3.util import Retry

from celery import shared_task
from core import settings
from core.constants import Constants
from datahub.models import LangchainPgCollection, LangchainPgEmbedding, ResourceFile
from utils.chain_builder import ChainBuilder
from langchain.prompts import PromptTemplate
from utils.pgvector import PGVector
from langchain.retrievers.merger_retriever import MergerRetriever

# from openai import OpenAI
LOGGING = logging.getLogger(__name__)
load_dotenv()
open_ai=openai.Audio()
os.environ[Constants.OPENAI_API_KEY] = settings.OPENAI_API_KEY

openai.api_key = settings.OPENAI_API_KEY

embedding_model = Constants.TEXT_EMBEDDING_ADA_002
embeddings = OpenAIEmbeddings(model=embedding_model)
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

db_settings = settings.DATABASES[Constants.DEFAULT]
encoded_user = quote_plus(db_settings[Constants.USER.upper()])
encoded_password = quote_plus(db_settings[Constants.PASSWORD])
retriever = ''


# Construct the connection string
connectionString = f"postgresql://{encoded_user}:{encoded_password}@{db_settings[Constants.HOST]}:{db_settings[Constants.PORT]}/{db_settings[Constants.NAME.upper()]}"
embeddings = OpenAIEmbeddings()


def get_embeddings(self, docs, collection_name, resource):
    for document in docs:
        document.metadata[Constants.URL] = resource.get(Constants.URL)
    retriever = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name=collection_name,
    connection_string=connectionString,
)

def transcribe_audio(self, audio_bytes, language="en-US"):
    try:
        transcript = openai.Audio.translate(file=audio_bytes, model=Constants.WISHPER_1)
        return transcript
    except Exception as e:
        print("Transcription error:", str(e))
        return str(e)
    

def generate_response(self, prompt, tokens=2000):
    response = openai.Completion.create(
        engine=Constants.GPT_TURBO_INSTRUCT,  # Use an appropriate engine
        prompt=prompt,
        temperature=0.1,
        max_tokens=tokens  # Adjust as necessary
    )
    return response.choices[0].text.strip(), response.get(Constants.USAGE)


def load_vector_db(resource_id):
    embeddings = OpenAIEmbeddings(model=embedding_model)

    LOGGING.info("Looking into resource: {resource_id} embeddings")
    collection_ids = LangchainPgCollection.objects.filter(
        name__in=Subquery(
            ResourceFile.objects.filter(resource=resource_id)
            .annotate(string_id=Cast('id', output_field=models.CharField()))
            .values('string_id')
        )
    ).values_list('uuid', flat=True)
    retrievals = []
    
    def setup_retriever(collection_id):
        vector_db = PGVector(
            collection_name=str(collection_id),
            connection_string=connectionString,
            embedding_function=embeddings,
        )
        retriever = vector_db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5, "k": 5})
        return retriever

    # Use ThreadPoolExecutor to run setup_retriever concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Create a future for each setup_retriever call
        future_to_collection_id = {executor.submit(setup_retriever, collection_id): collection_id for collection_id in collection_ids}
        
        for future in as_completed(future_to_collection_id):
            collection_id = future_to_collection_id[future]
            try:
                retriever = future.result()  # Retrieve the result from the future
                retrievals.append(retriever)  # Add the successfully created retriever to the list
            except Exception as exc:
                print(f'{collection_id} generated an exception: {exc}')

    lotr = MergerRetriever(retrievers=retrievals)
    return lotr


def genrate_embeddings_from_text(self, text):
    response = openai.Embedding.create(input=text, model=embedding_model)
    embedding = response['data'][0]['embedding']
    return embedding

def find_similar_chunks(self, input_embedding, resource_id,  top_n=5):
    # Assuming you have a similarity function or custom SQL to handle vector comparison
    if resource_id:
        LOGGING.info("Looking into resource: {resource_id} embeddings")
        collection_ids = LangchainPgCollection.objects.filter(
            name__in=Subquery(
                ResourceFile.objects.filter(resource=resource_id)
                .annotate(string_id=Cast('id', output_field=models.CharField()))
                .values('string_id')
            )
        ).values_list('uuid', flat=True)
        # Use these IDs to filter LangchainPgEmbedding objects
        similar_chunks = LangchainPgEmbedding.objects.annotate(
            similarity=CosineSimilarity("embedding", input_embedding)
        ).order_by("similarity").filter(similarity__lt=0.17, collection_id__in=collection_ids).defer("cmetadata").all()[:top_n]
        return similar_chunks
    else:
        LOGGING.info("Looking into all embeddings")
        similar_chunks = LangchainPgEmbedding.objects.annotate(
            similarity=CosineSimilarity("embedding", input_embedding)
        ).order_by("similarity").filter(similarity__lt=0.17).defer('cmetadata').all()[:top_n]
        return similar_chunks
