from flask import Flask, render_template, request, jsonify, redirect, Response,session,flash,url_for
import urllib.parse
# from LLM import get_answer, give_keywords
from LLM import  LLM_ANSWER
import pandas as pd
from sqlalchemy import create_engine
#import mysql.connector
from flask_cors import CORS
import json
import sqlite3
import os
import re
import openai
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from datetime import timedelta



app = Flask(__name__)

LLM_MODEL= LLM_ANSWER()

CORS(app)
## Configure OpenAI API Key
openai.api_key = os.environ.get('OPENAI_API_KEY')
app.secret_key = 'secret_key'

# Database configuration
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create a users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            totalQuestion TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            edited DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT

        )
    ''')

    conn.commit()
    conn.close()

    # Create Question Table
    conn2 = sqlite3.connect(DATABASE)
    cursor2 = conn2.cursor()

    # Create a users table if it doesn't exist
    cursor2.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            ans_by_gpt TEXT NOT NULL,
            ans_by_pdf TEXT NOT NULL,
            ans_by_db TEXT NOT NULL,
            useremail TEXT NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            edited DATETIME DEFAULT CURRENT_TIMESTAMP
            
        )
    ''')

    conn2.commit()
    conn2.close()

# Create the users table
create_table()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
@app.route("/")
def dashboard():
    return render_template("home.html")

@app.route("/chatbotsignup")
def chatbotsignup():
    return render_template("signin.html")



# @app.route("/login")
# def login():
#     return render_template("login.html")
@app.route("/dashboard")
def register():
    if session.get('logged_in'):
        username = session.get('username')
        return render_template('index.html', username=username)
    else:
        return redirect('/chatbotsignup')


@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    email = request.form.get('email')
    password = request.form.get('password')
  
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where email = ?" ,(email,))
    result = cursor.fetchall()
    
    #print("Result: ", result) 

    if not result[0]:
        error_msg = 'Username is required.'
        return render_template('signin.html', error_msg=error_msg)
        
    else:
        if result[0][2] == password:
            username=result[0][1]
            email=result[0][1]
            cursor.execute("SELECT * FROM users ")
            usersdata = cursor.fetchall()
          
            cursor.execute("SELECT COUNT(*) FROM questions")
            totalquestion = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM questions")
            tquestion = cursor.fetchall()
           
            cursor.execute("SELECT COUNT(*) FROM questions where ans_by_gpt = ? " ,("YES",))
            gptans = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM questions where ans_by_pdf = ?" ,("YES",))
            pdfans = cursor.fetchone()[0]
           
            
            #print(totalquestion)
            connection.commit()

            #Closing the cursor
            cursor.close()
            session['logged_in'] = True
            session['username'] = username
            session['totalquestion'] = totalquestion
            session['result'] = result
            session['email'] = email
            session['usersdata'] = usersdata
            session['gptans'] = gptans
            session['pdfans'] = pdfans
            


            return redirect('/dashboard')
        else:
            
            error_msg = 'Password is Incorrect'
            return render_template('signin.html', error_msg=error_msg)
    


@app.route('/logout')
def logout():
    # Clear the session data
    
    session.clear()
    return redirect('/chatbotsignup')

@app.route('/userlogout')
def userlogout():
    # Clear the session data
    
    session.clear()
    return redirect('/chatbotsignup')

@app.route("/anser",methods=['POST'])

def answer():
    ques = request.form.get('question')
    # similar_docs = give_keywords(ques)
    email= request.form.get('email')
    usersquestions= request.form.get('usersquestions')
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions where useremail = ? " ,(email,))
    usersquestions = int(cursor.fetchone()[0])+1
    connection.commit()

    #Closing the cursor
    cursor.close()
    
    
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET totalQuestion = ? WHERE email = ?", (usersquestions, email))
    
    connection.commit()

    #Closing the cursor
    cursor.close()
    
    #print(email)
    # data = json.loads(json_string)
    #print(ques)
    healthcare_words = ["medications","drugs", "pills", "DNA", "RNA", "Sequence", "Sequencing", "tablets", "prescriptions", 
                        "dosages","diabetes", "Genome Sequencing","cancer", "heart disease","covid-19","covid", "asthma","genomics", 
                        "arthritis","disease", "Alzheimer's disease", "Parkinson's disease", "mental health conditions",
                        "infectious diseases","doctors", "nurses", "pharmacists", "surgeons", 'therapists', 'chiropractors', 
                        "acupuncturists", 'midwives',"hospitals", "clinics", "urgent care centers","rehabilitation centers", 
                        "nursing homes", "hospices", "home health agencies", "policies", "premiums", "deductibles", "copays", 
                        "coverage", "claims", "network","providers","fitness", "nutrition", "weight loss", "smoking cessation",
                        "stress management", "sleep", "mental health", "addiction treatment","blood pressure monitors",
                        "glucose meters", "prosthetics", "hearing aids", "wheelchairs", "crutches", "braces", "inhalers",
                        "surgeries", "diagnostic tests", "imaging studies", "biopsies", "vaccinations","screenings", "check-ups",
                        "disease prevention", "vaccination campaigns", "epidemiology", "health promotion", "health policy",
                        "disaster preparedness","electronic health records", "telemedicine", "health apps", "wearable devices",
                        "AI in healthcare","double helix", "nucleotide", "gene","genetic","genetics", "chromosome", "base pair","genome sequence",
                        "mutation", "genetic code", "genetic variation","gene expression", "genetic mapping", "epigenetics",
                        "transcriptomics", "proteomics", "metabolomics","cystic fibrosis", "sickle cell anemia",
                        "Huntington's disease", "muscular dystrophy", "Down syndrome", "hemophilia", "thalassemia","CRISPR",
                        "gene therapy","genome engineering", "targeted gene editing","pharmacogenomics", "genetic testing",
                        "genetic counseling", "precision medicine", "gene-based diagnosis","gene-based therapy",
                        "population genetics", "evolutionary genetics", "molecular genetics", "comparative genomics",
                        "functional genomics","genetic engineering","synthetic biology", "gene synthesis", "gene cloning",
                        "genetic modification", "recombinant DNA technology","genetic discrimination", "privacy concerns",
                        "informed consent", "gene patenting", "intellectual property rights", "genetically modified organisms",
                        "whole genome sequencing", "targeted sequencing","high-throughput sequencing","nanopore sequencing",
                        "agriculture and livestock breeding", "forensic science", "paleogenomics","next-generation sequencing",
                        "conservation biology", "ancestry testing", "evolutionary biology", "Tay-Sachs disease", "bioinformatics",
                        "side effects", "interactions", "diseases", "providers","facilities", "insurance", "wellness", "equipment",
                        "procedures", "public health", "technology","radiology","ophthalmology", "oncology", "cardiology",
                        "orthopedics","gynecology", "pediatrics", "endocrinology", "dermatology", "immunology","urology",
                        "neurosurgery", "Reproductive Health", "Primary Care","gastroenterology","pathology", "bioethics",
                        "performance indicators", "psychiatry", "pain management", "health outcomes", "medical ethics",
                        "patient education", "healthcare financing", "home care","iot in healthcare", "healthcare administration",
                        "ambulance services", "medical laboratory", "disease management", "allergies and immunotherapy",
                        "cosmetic medicine", "robotic surgery", "healthcare startups", "intensive care units","health equity",
                        "artificial intelligence diagnosis", "data privacy in healthcare","medical billing","preventive care",
                        "healthcare delivery models", "nanotechnology in medicine", "blockchain in healthcare","ambulatory care",
                        "3D printing in healthcare", "healthcare supply chain","immunizations", "mental health counseling",
                        "dental care", "eye care", "audiology", "occupational therapy", "physical therapy", "speech therapy",
                        "holistic medicine", "alternative medicine", "medical research", "medical education", "clinical trials",
                        "healthcare regulation", "patient safety", "informed consent","patient satisfaction","aging population",
                        "chronic illnesses", "global health", "health disparities", "managed care", "medical devices",
                        "accountable care organizations","pharmacy benefits","palliative care","telehealth","healthcare analytics", 
                        "remote monitoring", "point of care testing", "health informatics","population health management",
                        "symptoms","more","additional","fever","Extra","Further","Added","Excess","Plus","Augmented","Extended",
                        "Advanced","Enhanced","hello","hi", "stakeholder", "heart attack", "healthcare", "medicine",
                        "market expansion", "WHO","PRC", "Pfizer", "Novartis AG", "Roche Holding AG", "Merck &amp Co", 
                        "GlaxoSmithKline", "Johnson &amp; Johnson", "Sanofi", "AbbVie", "AstraZeneca", "Bayer AG", 
                        "Eli Lilly and Company", "Bristol-Myers Squibb", "Amgen", "Gilead Sciences", "Teva Pharmaceutical",
                        "Novo Nordisk", "Takeda Pharmaceutical", "Boehringer Ingelheim", "Allergan", "Astellas",
                        "Good Morning", "morning", "Good afternoon", "Good night", "night", "afternoon", "noon", "AAV", 
                        "rAAV", "viral vectors", "adenoviruses", "lentiviruses", "adeno-associated virus",
                        "lipid-based nanoparticles", "electroporation", "therapeutic genes", "CRISPR-Cas9", "TALENs",
                        "Transcription Activator-Like Effector Nucleases", "ZFNs", "Zinc Finger Nucleases",
                        "forge biologics", "Catalent", "WuXi Advanced Therapies", "Lonza", "Vigene Biosciences",
                        "bluebird bio", "Oxford Biomedica", "Thermo Fisher Scientific", "Genezen", "ABL",
                        "DiNAMIQS", "KRIYA", "Jaguar Gene Therapy", "Elevatebio", "AGC Biologics", "Aldevron",
                        "Batavia Biosciences", "BioNTech IMFS", "CEVEC Pharmaceuticals", "Cobra Biologics", "Cytiva",
                        "FUJIFILM Diosynth Biotechnologies", "Genethon", "MolMed", "Paragon Bioservices",
                        "SIRION Biotech", "Yposkesi", "AveXis (now a part of Novartis)", "AskBio", "Eurofins Scientific",
                        "FinVector", "Généthon", "Homology Medicines", "MassBiologics", "MaxCyte", "MeiraGTx",
                        "Mustang Bio", "Orchard Therapeutics", "Orgenesis", "Polyplus-transfection", "REGENXBIO",
                        "Spark Therapeutics", "uniQure", "Adverum Biotechnologies", "Amicus Therapeutics",
                        "Anova Gene", "Benitec Biopharma", "Dimension Therapeutics (acquired by Ultragenyx)",
                        "Editas Medicine", "Freeline Therapeutics", "GenSight Biologics", "Gyroscope Therapeutics",
                        "LogicBio Therapeutics", "Nightstar Therapeutics (acquired by Biogen)", "Passage Bio",
                        "Precision BioSciences", "Rocket Pharmaceuticals", "Sangamo Therapeutics",
                        "Solid Biosciences", "Valerion Therapeutics", "Voyager Therapeutics", "Zinc Finger Therapeutics",
                        "HEK293", "adeno-associated viral vectors", "Luxturna", "rAAV2", "RPE65", "Zolgensma", "rAAV9",
                        "retinal dystrophy", "Spinal Muscular Atrophy", "haemophilia", "ASPIRO",
                        "X-linked myotubular myopathy", "rAAV8", "Duchenne muscular dystrophy", "Pfizer", "HeLa", "HeLaS3",
                        "Stable producer cell lines (PCL)", "ELEVECTA", "HEK", "CAP cells", "CHO cells", "insect cells",
                        "KCNN2", "antibodies", "serotypes", "Capsid engineering", "Apellis Pharmaceuticals",
                        "Catalent Pharma Solutions", "Cytiva", "World Courier", "Covance", "Beam Therapeutics", "Novartis",
                        "Cell and Gene Therapy Catapult", "Asklepios BioPharmaceutical, Inc. (AskBio)",
                        "Affinia Therapeutics", "Resilience", "Precision BioSciences, Inc.", "Sangamo Therapeutics, Inc.",
                        "Astellas Gene Therapies", "WuXi AppTec", "Labcorp Drug Development", "Spark Therapeutics, Inc.",
                        "Kriya Therapeutics, Inc.", "Homology Medicines, Inc.", "REGENXBIO Inc.", "Iveric Bio",
                        "GenScript Europe", "Shape Therapeutics Inc.", "Akouos", "Poseida Therapeutics, Inc.",
                        "Graphite Bio", "enGene", "Dyno Therapeutics", "MaxCyte, Inc.", "Andelyn Biosciences",
                        "Tune Therapeutics", "SwanBio Therapeutics", "AveXis, Inc.", "Taysha Gene Therapies",
                        "CYTENA", "Excelya", "Allucent", "Gene Therapy Program | University of Pennsylvania",
                        "BioAgilytix", "Ori Biotech", "TaqMan RT-PCR", "ferret", "T cell responses", "IFNg-ELISpot assay",
                        "AAV2.5T capsid", "epitope mapping", "synthetic peptides", "amino acid sequence", "VP1",
                        "liver enzymes", "prednisone", "factor IX coagulant activity", "AAV gene therapy",
                        "Leber's hereditary optic neuropathy", "corticosteroids", "ocular inflammation",
                        "intravitreal administration", "rAAV2/2-ND4", "methylprednisolone", "azathioprine", "cyclosporine",
                        "orthotopic lung transplantation", "plasma gLuc activity", "repeat dosing", "HEK293 cells",
                        "AAV capsid", "pAV2.5-Trepcap", "adenovirus helper", "pAd4.1", "AAV pro-viral vector",
                        "AAV2 ITR sequences", "rAAV vectors", "iodixanol cushion", "cesium chloride", "titers",
                        "DNase-I-resistant particles", "SRA", "Spirovant Sciences", "lung-resident T cells",
                        "lymph nodes", "gLuc expression", "resident T cell suppression", "cytokines", "splenocyte",
                        "pro-inflammatory cytokines", "TaqMan qPCR", "transgenes", "SDS-PAGE", "animal dosing",
                        "juvenile wild-type ferrets", "ketamine", "xylazine", "mutated capsids", "apical transduction",
                        "HAE", "air-liquid interphase", "CFTR minigene", "CFTRDR", "synthetic promoter/enhancer", "SP183",
                        "Baytril", "bacterial infection", "gLuc activity", "plasma", "BALF", "jugular vein",
                        "heparinized tubes", "euthanized", "Euthasol", "ANOVA", "IC50", "AAV2.5T", "immunosuppression",
                        "TriIS", "capsidbinding", "Gene therapy", "Genetic modification", "Genetic engineering",
                        "CRISPR", "Cas9", "Viral vector", "Adeno-associated virus (AAV)", "Lentivirus", "Retrovirus",
                        "Ex vivo gene therapy", "In vivo gene therapy", "Antisense oligonucleotides",
                        "RNA interference (RNAi)", "Small interfering RNA (siRNA)", "Gene editing", "Gene silencing",
                        "Gene knockdown", "Gene knockout", "Gene knockin", "Gen", "AveXis"]

    def is_healthcare_question(question):
        question = question.lower()
        for word in healthcare_words:
            pattern = r'\b{}\b'.format(re.escape(word.lower()))
            if re.search(pattern, question):
                return True
        return False

    user_input = ques


    def check_pdf_ans(answer, lst):
        for n in lst:
            if n in answer:
                return False
        return True 
    

    lst = ["don't know.", "don't know the answer.", "information does not provide","not in the context",
           "The information provided does not specify the number","According to the given context",
           "it does not provide information", "Based on the given context","apologies","sorry"]
    
    if is_healthcare_question(user_input):
            # Process the question with the chatbot
       
        query = ques
        answer = LLM_MODEL.get_answer(query)
        
        #print(ques)
        
        # if ("context" not in answer) or ("don't know" not in answer) or ("apologize" not in answer):
        if check_pdf_ans(answer, lst):
            session["prev_question"] = ques
            session["prev_answer"] = answer
            #print("PDF")
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
                    
            cursor.execute("INSERT INTO questions (question, answer,useremail,ans_by_gpt,ans_by_pdf,ans_by_db) VALUES (?, ?, ?,?,?,?)", (ques, answer,email,'NO','YES','NO'))
            connection.commit()
                
            cursor.close()
                    ## Returning new answer as response
            return answer       
        
        else :
            
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            
            cursor.execute("SELECT answer FROM questions where question =?", (ques,))
            result = cursor.fetchall()
            #print("Result: ", result) 
            if result:
            ## If a match is found, return the answer 
            #print(result[0][0])
                session["prev_question"] = ques
                session["prev_answer"] = result[0][0]
                # connection = sqlite3.connect(DATABASE)
                # cursor = connection.cursor()
                # connection = sqlite3.connect(DATABASE)
                # cursor = connection.cursor()
                        
                # cursor.execute("INSERT INTO questions (question, answer,useremail,ans_by_gpt,ans_by_pdf,ans_by_db) VALUES (?, ?, ?,?,?,?)", (ques, result[0][0],email,'NO','NO','YES'))
                # connection.commit()
                    
                # cursor.close()
                return result[0][0]
         
            else:
                ## If no match is found, ask chatGPT and return the answers1 = 'Hello'
                s2 = ''
                s1 = ques
                s4="?"
                #print(ques)
                s3 = "{} {} {}".format(s2, s1,s4)
                response = openai.Completion.create(
                    engine = "text-davinci-003",
                    prompt = s3,                
                    max_tokens = 1500,
                    n = 1,
                    stop = None,
                    temperature=0.5,
                    timeout = 15,
                )
            
                answer = response.choices[0].text.strip()
                
                ## Store the new question and their answer in the database
                
                connection = sqlite3.connect(DATABASE)
                cursor = connection.cursor()
                #print("GPT")
                cursor.execute("INSERT INTO questions (question, answer,useremail,ans_by_gpt,ans_by_pdf,ans_by_db) VALUES (?, ?, ?,?,?,?)", (ques, answer,email,'YES','NO','NO'))
                ## Returning new answer as response
                connection.commit()
        
                #Closing the cursor
                cursor.close()
                #print(answer)
                session["prev_question"] = ques
                session["prev_answer"] = answer
                return answer
                # pass

    else:
        return "I apologize, but I don't have sufficient information or training on that particular topic. Is there something else I can assist you with?"
    



@app.route('/saveCustomer', methods=['POST'])
def saveCustomer():
   
    name = request.form.get('name')
    email = request.form.get('email')
    #print(email)
    password = request.form.get('password')
    # phone = request.form.get('phone')
    # Orgnization = request.form.get('Orgnization')
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where email = ?", (email,))
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    #print("Result: ", result) 
       
    if result:
        
        return render_template('signin.html', error_msg='User already exits. Please login')
    else:

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        #cursor.execute("INSERT INTO users (name, password,email,phone,organisation) VALUES (?,?,?,?,?)", (name, password,email,phone,Orgnization))
        cursor.execute("INSERT INTO users (password,email) VALUES (?,?)", (password,email))
        ## Returning new answer as response
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        
        session['logged_in'] = True
        session['user_id'] = email
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM questions where useremail = ?" ,(email,))
        tquestion = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM questions where useremail = ?" ,(email,))
        totalquestionnew = cursor.fetchone()[0]
        session['totalquestionnew'] = totalquestionnew
        
        connection.commit()
        cursor.close()
        return redirect('/rdgpt')
        


#SignIn Form

@app.route('/signin', methods=['POST'])
def signIn():
   

    email = request.form.get('email')
    password = request.form.get('password')
  
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where email = ?" ,(email,))
    result = cursor.fetchall()
    # print("Result: ", result[0][2]) 

    if result:
        if result[0][2] == password and result[0][6] == "admin":
            username=result[0][1]
            email=result[0][1]
            cursor.execute("SELECT * FROM users ")
            usersdata = cursor.fetchall()
          
            cursor.execute("SELECT COUNT(*) FROM questions")
            totalquestion = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM questions")
            tquestion = cursor.fetchall()
           
            cursor.execute("SELECT COUNT(*) FROM questions where ans_by_gpt = ? " ,("YES",))
            gptans = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM questions where ans_by_pdf = ?" ,("YES",))
            pdfans = cursor.fetchone()[0]
           
            
            #print(totalquestion)
            connection.commit()

            #Closing the cursor
            cursor.close()
            session['logged_in'] = True
            session['username'] = username
            session['totalquestion'] = totalquestion
            session['result'] = result
            session['email'] = email
            session['usersdata'] = usersdata
            session['gptans'] = gptans
            session['pdfans'] = pdfans
            


            return redirect('/dashboard')
        elif result[0][2] == password:
            ## If a match is found, return the answer 
            #print("Result: ", result)
           
            session['logged_in'] = True
            session['user_id'] = email
            cursor.execute("SELECT COUNT(*) FROM questions where useremail = ?" ,(email,))
            totalquestionnew = cursor.fetchone()[0]
            session['totalquestionnew'] = totalquestionnew
            
            return redirect('/rdgpt')
            
        else:
            
            return render_template('signin.html', error_msg='Password is incorrect') 
            
        
            
    else:
        return render_template('signin.html', error_msg='User Does not exist. Please signup')
        
        
    
@app.route('/fetchhistory', methods=['POST'])
def fetchhistory():
   
    
    email = request.form.get('email')
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM questions where useremail = ?", (email,))
    result = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM questions where useremail = ? " ,(email,))
    gptanscount = cursor.fetchone()[0]
    session["gptanscount"]=gptanscount
    #print("Result: ", result) 

    
    if result:
        ## If a match is found, return the answer 
        #print("Result: ", result)
        cursor.execute("SELECT * FROM questions where useremail = ?", (email,))
        result = cursor.fetchall()
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        return jsonify(result)
    else:
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        return "No Search History"



@app.route('/more', methods=['GET','POST'])

def more():
    ## If no match is found, ask chatGPT and return the answers1 = 'Hello'
    prev_question = session.get("prev_question")
    prev_answer = session.get("prev_answer")
    if prev_question is None or len(prev_question) == 0:
        return "I'm sorry, I don't have any previous question and answer to show you."
    else:
      
        response = openai.Completion.create(
            engine = "text-davinci-002",
            prompt=prev_question + '\nMore information:',
            
            max_tokens = 50,
            n = 1,
            stop = None,
            temperature=0.5,
            timeout = 10,
        )
        
        answer = response.choices[0].text.strip()
        session["prev_question"] = prev_question + '\nMore information:'
        session["prev_answer"] = answer
        
        ## Store the new question and their answer in the database
        
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("UPDATE questions SET answer = ? WHERE question = ?", (answer, prev_question))
        
        connection.commit()

        #Closing the cursor
        cursor.close()
        return answer

@app.route('/train_model', methods=['POST'])

def train_model():
    
    #print("Kuchh ni aya")
    json_string = request.get_json()
    #data = json.loads(json_string)
    #print(json_string)
    ques = json_string['subject']
    #print(ques)
    answer = json_string['request_message']
   
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT question, answer FROM questions where question = ?", (ques,))
    result = cursor.fetchall()
    #print("Result: ", result) 
       
    if result:
        ## If a match is found, return the answer 
        #print("Result: ", result)
        response = Response(json.dumps({'success':True}))
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    else:

        ## Store the new question and their answer in the database
        
        cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (ques, answer))
        ## Returning new answer as response
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    


#Send All Customer

@app.route('/alluser', methods=['GET'])

def alluser():
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    #print("Result: ", result) 
    
       
    if result:
        ## If a match is found, return the answer 
        #print("Result: ", result)
        resp=jsonify(result)
        
        response = Response(resp)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    else:
        resp=jsonify({'sucess':False})
        
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

@app.route('/allquestion', methods=['GET'])

def allquestion():
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM questions")
    result = cursor.fetchall()
    
    
       
    if result:
        ## If a match is found, return the answer 
        #print("Result: ", result)
        resp=jsonify(result)
        
        # response = Response(resp)
        # response.headers['Access-Control-Allow-Origin'] = '*'
       
        return resp
    else:
        
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
# def is_logged_in():
#     if 'user_id' in session:
#         # User is logged in
#         return True
#     else:
#         # User is not logged in
#         return False

# # Middleware
# @app.before_request
# def check_login():
#     if request.path == '/rdgpt':
#         if not is_logged_in():
#             return render_template('signin.html', error_msg='Please Login to access this route')

# Example route with middleware
@app.route('/rdgpt')
def protected_route():
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM questions where useremail = ? " ,(session.get('user_id'),))
    tquestion = cursor.fetchall()
    
    connection.commit()
    cursor.close()
    return render_template('chatGPT.html', sucess_msg=tquestion)

@app.route('/adminregister')
def adminregister():   
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    #cursor.execute("INSERT INTO users (name, password,email,phone,organisation) VALUES (?,?,?,?,?)", (name, password,email,phone,Orgnization))
    cursor.execute("INSERT INTO users (password,email,role) VALUES (?,?,?)", ("Admin@123","reportdesk.admin@gmail.com","admin"))
    ## Returning new answer as response
    connection.commit()

    #Closing the cursor
    cursor.close()


@app.route('/questiondelete')
def questiondelete():   
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    #cursor.execute("INSERT INTO users (name, password,email,phone,organisation) VALUES (?,?,?,?,?)", (name, password,email,phone,Orgnization))
    cursor.execute("DELETE FROM users WHERE id = ? " ,(2,))
    ## Returning new answer as response
    connection.commit()

    #Closing the cursor
    cursor.close()
    return "sussess"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="8000",debug=True)
