from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import json
import re

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.views.decorators.csrf import csrf_exempt

import re
import pymongo
import hashlib
from datetime import datetime
from time import sleep
import random

from glob import iglob

mongo_url = "mongodb://localhost:27017/"
User = get_user_model()

colors = [
    "bg-primary",
    "bg-secondary",
    "bg-success",
    "bg-pink",
    "bg-yellow",
    "bg-aqua",
    "bg-lightss",
    "bg-dark",
]
# def delete(request):
#     User.objects.all().delete()


def calculate_hash(content):
    md5 = hashlib.md5()
    md5.update(content.encode())
    return md5.hexdigest()


def login(request):
    c = {}
    if request.POST:
        success = False
        try:
            email = request.POST["u_email"]
            if not email:
                raise ValueError()
        except:
            messages.error(request, "Please enter an email!")

        try:
            password = request.POST["u_pass"]
            if not password:
                raise ValueError()
        except:
            messages.error(request, "Please enter a password!")
        if email and re.match(r"[^@]+@[^@]+\.[^@]+", email):
            user = User.objects.get(email=email)
            if user:
                if user.check_password(password):
                    auth_login(request, User.objects.get(email=email))
                    messages.success(request, "Successfully Logged in!")
                    success = True
                else:
                    messages.error(request, "Incorrect Password!")
            else:
                messages.error(request, "Email does not Exist!")
        else:
            messages.error(request, "Invalid Email")
        return redirect(reverse("dash" if success else "login"))
    return render(request, "pages/login.html", c)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect(reverse("login"))


def dashboard(request):
    c = {}
    if request.user.is_authenticated:
        request.session["dash"] = True
        request.session["data_manage"] = False
        return render(request, "pages/dash.html", c)


@csrf_exempt
def update_folder(request):
    c = {}
    if request.user.is_authenticated:
        if request.POST:
            folder_id = request.POST["folder"]
            folders_data = pymongo.MongoClient(mongo_url)["folders_data"]
            folders_metadata_collection = folders_data["metadata"]
            folder_info = list(
                folders_metadata_collection.find({"folder_web_id": folder_id})
            )
            if folder_info:
                print(folder_info)

        return redirect(reverse("data_manage"))


@csrf_exempt
def delete_folder(request):
    pass


def update_file(request):
    pass


def data_manage(request):
    c = {}
    if request.user.is_authenticated:
        folders_data = pymongo.MongoClient(mongo_url)["folders_data"]
        folders_metadata_collection = folders_data["metadata"]
        request.session["dash"] = False
        request.session["data_manage"] = True
        if request.POST:
            try:
                folder_name = request.POST["u_folder_name"]
                if len(folder_name) == 0:
                    raise ValueError()
            except:
                messages.error(request, "Please enter Folder Name!")
                return redirect(reverse("data_manage"))

            if len(re.findall(r"[a-zA-Z0-9_ ]", folder_name)) == len(folder_name):
                if len(re.findall(r"[a-zA-Z0-9]", folder_name)) == 0:
                    messages.error(
                        request, "You need to have atleast one alphabet or number!"
                    )
                elif len(re.findall(r"^[0-9_ ]", folder_name)) > 0:
                    messages.error(
                        request, "The folder name needs to start with an alphabet!"
                    )
                else:
                    folder_web_id = "_".join(folder_name.split()).lower()
            else:
                messages.error(
                    request,
                    "Invalid Folder Name! Only use alphabets, numbers and underscores",
                )
                return redirect(reverse("data_manage"))

            try:
                domain = request.POST["u_domain"]
            except:
                messages.error(request, "Please choose a Domain!")
                return redirect(reverse("data_manage"))

            try:
                description = request.POST["u_desc"]
            except:
                description = folder_name

            # db = pymongo.MongoClient(mongo_url)[folder_name + "_" + category]
            # jd_collection = db["jd_collection"]
            # resume_collection = db["resume_collection"]
            if list(
                folders_metadata_collection.find(
                    {"folder_id": calculate_hash(folder_name)}
                )
            ):
                messages.error(request, "Folder already exists!")
                return redirect(reverse("data_manage"))
            else:
                metadata = {
                    "folder_id": calculate_hash(folder_name),
                    "folder_name": folder_name,
                    "folder_web_id": folder_web_id,
                    "domain": domain,
                    "description": description,
                    "created_by": request.user.username,
                    "created_on": datetime.now(),
                    "modified_by": request.user.username,
                    "modified_on": datetime.now(),
                    "jd_count": 0,  # len(list(jd_collection.find())),
                    "resume_count": 0,  # len(list(resume_collection.find())),
                }

                folders_metadata_collection.insert_one(metadata)
                messages.success(request, "Folder Successfully Created!")
                folders = list(folders_metadata_collection.find({}))
                request.session["folders"] = [
                    {
                        "folder_name": x[1]["folder_name"],
                        "description": x[1]["description"],
                        "jd_count": x[1]["jd_count"],
                        "resume_count": x[1]["resume_count"],
                        "folder_dropdown": f"{folder_web_id}_dropdown",
                        "folder_color": x[0],
                        "folder_id": folder_web_id,
                        "text_color": "text-dark"
                        if x[0] == "bg-lightss"
                        else "text-white",
                    }
                    for x in zip(
                        [random.choice(colors) for _ in range(len(folders))],
                        folders,
                    )
                ]
                return redirect(reverse("data_manage"))
        folders = list(folders_metadata_collection.find({}))
        request.session["folders"] = [
            {
                "folder_name": x[1]["folder_name"],
                "description": x[1]["description"],
                "jd_count": x[1]["jd_count"],
                "resume_count": x[1]["resume_count"],
                "folder_dropdown": f"{x[1]['folder_web_id']}_dropdown",
                "folder_color": x[0],
                "folder_id": x[1]["folder_web_id"],
                "text_color": "text-dark" if x[0] == "bg-lightss" else "text-white",
            }
            for x in zip(
                [random.choice(colors) for _ in range(len(folders))],
                folders,
            )
        ]

        return render(request, "pages/data_manage.html", c)


@csrf_exempt
def file_manage(request):
    c = {}
    if request.user.is_authenticated:
        folders_data = pymongo.MongoClient(mongo_url)["folders_data"]
        folders_metadata_collection = folders_data["metadata"]
        request.session["dash"] = False
        request.session["data_manage"] = True
        if request.POST:
            folder_web_id = request.POST["folder"]
            print(folder_web_id)
            curr_folder = folders_metadata_collection.find(
                {"folder_web_id": folder_web_id}
            )
            print([x for x in curr_folder])
        return render(request, "pages/file_manage.html", c)
