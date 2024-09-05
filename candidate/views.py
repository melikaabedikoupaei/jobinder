
from django.shortcuts import render ,get_object_or_404,redirect
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.contrib.sites.requests import RequestSite
from .models import *
from employer.models import Position
from .forms import *
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
import torch
import tensorflow as tf
from tensorflow import keras
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from pdfreader import SimplePDFViewer
#nltk.download('stopwords')
#nltk.download('punkt')



def cleaning(text):
    text = str(text)
    # Define stop words
    stop_words = set(stopwords.words('english'))
    
    # Remove user mentions, URLs, hashtags
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"#\w+", "", text)
    
    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    
    # Remove specific escape sequences
    text = re.sub(r"\\r", " ", text)
    
    # Remove special characters and punctuations
    text = re.sub(r"[()]", "", text)
    text = re.sub(r"/", " ", text)
    text = re.sub(r"[,;:]", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"-", " ", text)
    text = re.sub(r"\+", "", text)
    text = re.sub(r"\*", "", text)
    text = re.sub(r"\"", "", text)
    text = re.sub(r"&", "", text)
    text = re.sub(r"=", "", text)
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    
    # Remove digits
    text = re.sub(r"\b\d+\b", "", text)
    
    # Remove extra whitespace, newlines, and tabs
    text = re.sub(r"\s+", " ", text).strip()
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stopwords
    filtered_words = [word for word in words if word not in stop_words]
    
    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

def cos_sim(job, candidate):
    return np.sum(job * candidate) / (np.sqrt(np.sum(job**2)) * np.sqrt(np.sum(candidate**2)))

def get_similar_cvs(jobs_and_embeddings: pd.DataFrame, resume: str, number_of_jobs = 10):
    # jobs_and_embeddings dataframe should have a column embeddings and a column with the job name embeddings and a column that points to 
    #resume = cleaning(resume)

    # Initialize the DistilBERT tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('distilbert-base-uncased')

    tokens = tokenizer(resume, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        output = model(**tokens)
    resume_embedding = output.last_hidden_state.mean(dim=1).numpy()

    sims = np.zeros((jobs_and_embeddings.shape[0]))
    for i,job in enumerate(jobs_and_embeddings["Combined"]):
        sims[i]=cos_sim(job,resume_embedding)

    jobs_and_embeddings["similarity"] = sims

    jobs_and_embeddings.sort_values(by="similarity",axis=0,ascending=False,inplace=True)

    return jobs_and_embeddings.head(number_of_jobs)

def browsejobs (request):
    return render (request,"candidate/browsejobs.html") 

def candidates (request):
    candidates = Candidate.objects.all()
    context={'candidates': candidates}
    return render (request,"candidate/candidates.html",context)
 
def candidate_single (request,pid):
    candidate = get_object_or_404(Candidate,pk=pid)
    context={'candidate': candidate}
    return render (request,"candidate/candidate-single.html",context) 

def createresume(request):
    candidateform = CandidateForm()
    degreeformset = modelformset_factory(Degree, form=DegreeForm, extra=0)
    workexperienceformset = modelformset_factory(WorkExperience, form=WorkExperienceForm, extra=0)

    if request.method == 'POST':
        candidateform = CandidateForm(request.POST)
        degreeformset = degreeformset(request.POST)
        workexperienceformset = workexperienceformset(request.POST)

        if candidateform.is_valid() and degreeformset.is_valid() and workexperienceformset.is_valid():
            parent = candidateform.save(commit=True)
            for degreeform in degreeformset:
                degreechild = degreeform.save(commit=False)
                degreechild.candidate = parent
                degreechild.save()
                
            for workexperienceform in workexperienceformset:
                workexperiencechild = workexperienceform.save(commit=False)
                workexperiencechild.candidate = parent
                workexperiencechild.save()
            
            return redirect('candidate:result')  # Redirect to a success page after saving
    else:
        degreeformset = degreeformset(queryset=Degree.objects.none())  # Initialize an empty formset for GET request
        workexperienceformset = workexperienceformset(queryset=WorkExperience.objects.none())  # Initialize an empty formset for GET request
    return render(request, 'candidate/create_resume.html', {
        'candidateform': candidateform,
        'degreeformset': degreeformset,
    })


def result(request):
    latest_candidate = Candidate.objects.latest('id')
    candidate_resume = latest_candidate.about_me
    jobs = Position.objects.all()
    jobs_and_embeddings = pd.DataFrame(list(jobs.values("JobID", "Combined")))

    # Convert 'Combined' column from string to NumPy array
    def convert_to_array(combined_str):
        try:
            return np.array([float(x) for x in combined_str.split(',')])
        except ValueError:
            return np.array([])  # Return an empty array if conversion fails

    jobs_and_embeddings['Combined'] = jobs_and_embeddings['Combined'].apply(convert_to_array)
    # Filter out rows where conversion failed
    jobs_and_embeddings = jobs_and_embeddings[jobs_and_embeddings['Combined'].apply(lambda x: x.size > 0)]
    print(jobs_and_embeddings)

    similar_jobs = get_similar_cvs(jobs_and_embeddings, candidate_resume)
    print(similar_jobs)
    similar_job_ids = similar_jobs['JobID'].tolist()
    
    # Fetch the positions from the database
    similar_positions = Position.objects.filter(JobID__in=similar_job_ids)

    return render(request, 'candidate/result.html', {
        'latest_candidate': latest_candidate,
        'similar_positions': similar_positions,
    })

def wantajob(request):
    return render (request,"candidate/want-a-job.html")



def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            
            # Redirect to the result page with resume text as query parameter
            return redirect('candidate:upload_resume_result')
    else:
        form = ResumeForm()

    return render(request, 'candidate/upload_resume.html', {'form': form})

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as fd:
        viewer = SimplePDFViewer(fd)
        viewer.render()
        text = "".join(viewer.canvas.strings)
    return text

def upload_resume_result(request):
    resume=Resume.objects.latest("id")
    resume_text=extract_text_from_pdf(resume.file.path)



    jobs = Position.objects.all()
    jobs_and_embeddings = pd.DataFrame(list(jobs.values("JobID", "Combined")))

    # Convert 'Combined' column from string to NumPy array
    def convert_to_array(combined_str):
        try:
            return np.array([float(x) for x in combined_str.split(',')])
        except ValueError:
            return np.array([])  # Return an empty array if conversion fails

    jobs_and_embeddings['Combined'] = jobs_and_embeddings['Combined'].apply(convert_to_array)
    # Filter out rows where conversion failed
    jobs_and_embeddings = jobs_and_embeddings[jobs_and_embeddings['Combined'].apply(lambda x: x.size > 0)]
    print(jobs_and_embeddings)

    similar_jobs = get_similar_cvs(jobs_and_embeddings, resume_text)
    print(similar_jobs)
    similar_job_ids = similar_jobs['JobID'].tolist()
    
    # Fetch the positions from the database
    similar_positions = Position.objects.filter(JobID__in=similar_job_ids)

    return render(request, 'candidate/upload_resume_result.html', {
        'similar_positions': similar_positions,
    })


