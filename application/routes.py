from application import app, dropzone
from flask import redirect, render_template, url_for, request, session
from application.forms import MyForm
from application import utils
import secrets
import os

# # OCR
import cv2
import pytesseract
import numpy as np
from gtts import gTTS

# # listen
import speech_recognition as sr
from googletrans import Translator



@app.route("/")
def index():
    return render_template("index.html", title = "Home Page")



@app.route("/upload", methods=["POST", "GET"])

def upload():
    if request.method == "POST":

        # set a session value
        sentence = ""

        f = request.files.get("file")
        #something.jpg >> ["something", "jpg"]
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".{extension}"


        file_location = os.path.join(app.config["UPLOADED_PATH"], generated_filename)

        f.save(file_location)

        # OCR here
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        img = cv2.imread(file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        boxes = pytesseract.image_to_data(img)
        # print (boxes)

        for i, box in enumerate(boxes.splitlines()):
            if i == 0:
                continue

            box = box.split()
            # print (box)

            #only deal with boxes with word in it.
            if len(box) == 12:
                sentence += box[11] + " "

       # print(sentence)
        session["sentence"] = sentence

        #delete file after you are done working with it
        os.remove(file_location)

        return redirect("/decoded/")

    else:
        return render_template("upload.html", title="Upload")
    


@app.route("/decoded", methods=["POST", "GET"])
def decoded():

    sentence = session.get("sentence")

    lang, _ = utils.detect_language(sentence)

    form = MyForm()

    if request.method == "POST":

        generated_audio_filename = secrets.token_hex(10) + ".mp4"

        text_data = form.text_field.data
        translate_to = form.language_field.data
       # print("Translate to: ", translate_to)


        translated_text = utils.translate_text(text_data, translate_to)
        print(translated_text)


        tts = gTTS(translated_text, lang=translate_to)

        file_location = os.path.join(
            app.config["AUDIO_FILE_UPLOAD"], 
            generated_audio_filename
        )

        # save file as audio
        tts.save(file_location)

        form.text_field.data = translated_text

        return render_template(
            "decoded.html", 
            title="Translations",
            form = form,
            lang=utils.languages.get(lang),
            audio = True, 
            file = generated_audio_filename
        )


    else:
        form.text_field.data = sentence
        session["sentence"] = ""
        return render_template(
                "decoded.html",
                title= "Translations",
                form = form,lang=utils.languages.get(lang), 
                audio = False
            )   


# @app.route("/text", methods=["POST", "GET"])
# def textdecoded():

#     sentence = session.get("sentence")

#     lang, _ = utils.detect_language(sentence)

#     form = MyForm()

#     if request.method == "POST":

#         generated_audio_filename = secrets.token_hex(10) + ".mp4"

#         text_data = form.text_field.data
#         translate_to = form.language_field.data
#        # print("Translate to: ", translate_to)


#         translated_text = utils.translate_text(text_data, translate_to)
#         print(translated_text)


#         tts = gTTS(translated_text, lang=translate_to)

#         file_location = os.path.join(
#             app.config["AUDIO_FILE_UPLOAD"], 
#             generated_audio_filename
#         )

#         # save file as audio
#         tts.save(file_location)

#         form.text_field.data = translated_text

#         return render_template(
#             "texttospeech.html", 
#             title="Translations",
#             form = form,
#             lang=utils.languages.get(lang),
#             audio = True, 
#             file = generated_audio_filename
#         )


#     else:
#         form.text_field.data = sentence
#         session["sentence"] = ""
#         return render_template(
#                 "texttospeech.html",
#                 title= "Translations",
#                 form = form,lang=utils.languages.get(lang), 
#                 audio = False
#             )   


@app.route("/speech", methods=["POST", "GET"])
def speech():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
    return render_template("speech.html", transcript=transcript)
    





# # for index J name in enumerate(sr.Kicrophone. list_nicrophone_names()):
# #print(f"name {name} at index {index}")
#     r=sr. Recognizer()
#     with sr.Microphone() as source:
#         print("say something")
#         audio=r. listen(source)
#         query=r.recognize_google(audio)
#         print(query)





#1 Listen : Hindi or English
# def Listen():
#     r= sr.Recognizer()

#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source,0,8)

#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio)

#     except:
#         return ""

#     query = str(query).lower()
#     return query

# #2 Translation
# def TranslationHinToEng(Text):
#     line = str(Text)
#     translate = Translator()
#     result = translate.translate(line)
#     data = result.text
#     print(f"You : {data}.")
#     return data

# #3 Connect
# def MicExecution():
#     query = Listen()
#     data = TranslationHinToEng(query)
#     return data
# MicExecution()

