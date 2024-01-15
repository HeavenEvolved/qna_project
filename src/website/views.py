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

import os
import re
import pymongo
import hashlib
from datetime import datetime
from time import sleep
import random
from langchain.document_loaders import UnstructuredFileLoader
from unstructured.cleaners.core import clean, clean_non_ascii_chars

from glob import iglob

mongo_url = "mongodb://localhost:27017/"
User = get_user_model()

colors = [
    "bg-primary",
    "bg-secondary",
    "bg-yellow",
    "bg-green",
    "bg-purple",
    "bg-lightss",
    "bg-dark",
]
temp_colors = list(colors)


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


def data_manage(request):
    c = {}
    if request.user.is_authenticated:
        client = pymongo.MongoClient(mongo_url)
        folders_data = client["folders_data"]
        files_data = client["files_data"]
        folders_metadata_collection = folders_data["metadata"]
        request.session["dash"] = False
        request.session["data_manage"] = True
        request.session["business_case"] = False
        global temp_colors
        if request.method == "POST":
            if request.POST["type"] == "update_folder":
                desc_updated = False
                name_updated = False
                folder_web_id = request.POST["folder_web_id"]
                folder_name_error_msg = (
                    """The Folder name has to be 5-25 characters long. """
                    """The Folder name needs to contain atleast one alphabet or number. """
                    """The Folder name can only contain a-z, A-Z, _ (underscores) and spaces. """
                    """The Folder name needs to start with an alphabet."""
                )
                folder_exists_error_msg = (
                    """The Folder name you entered already exists!"""
                )
                folder_filters = [
                    lambda x: re.findall(r"^[a-zA-Z][a-zA-Z0-9_ ]{4,25}$", x) == [],
                    # Checks if these characters exist in the string
                    # and that the length is greater than 5.
                    lambda x: 5 > len(x) or len(x) > 25,
                    # Checks if the length of the folder name is between
                    # 5 and 25 including both ends.
                    lambda x: x.split() == [],
                    # Checks if the string is empty
                    lambda x: re.findall(r"[0-9]", x) == []
                    and re.findall(r"[a-zA-Z]", x) == [],
                    # Checks if the string contains atleast one integer.
                ]

                folder_name = request.POST["folder_name"]
                new_folder_web_id = "_".join(folder_name.split()).lower()
                description = request.POST["description"]
                folders_metadata_collection.update_one(
                    {"folder_web_id": folder_web_id},
                    {
                        "$set": {
                            "description": request.POST["description"],
                        }
                    },
                )
                desc_updated = True
                if any(map(lambda x: x(folder_name), folder_filters)):
                    response_to_page = {"status": 0, "msg": folder_name_error_msg}
                    return HttpResponse(
                        json.dumps(response_to_page), content_type="application/json"
                    )
                elif (
                    list(
                        folders_metadata_collection.find(
                            {"folder_id": calculate_hash(folder_name)}
                        )
                    )
                    != []
                ):
                    print(
                        list(
                            folders_metadata_collection.find(
                                {"folder_id": calculate_hash(folder_name)}
                            )
                        )
                    )
                    print("Name Error!")
                    response_to_page = {"status": 0, "msg": folder_exists_error_msg}
                elif (
                    list(
                        folders_metadata_collection.find(
                            {"folder_web_id": new_folder_web_id}
                        )
                    )
                    != []
                ):
                    print("Web ID Error!")
                    response_to_page = {"status": 0, "msg": folder_exists_error_msg}
                else:
                    folders_metadata_collection.update_one(
                        {"folder_web_id": folder_web_id},
                        {
                            "$set": {
                                "folder_id": calculate_hash(folder_name),
                                "folder_web_id": new_folder_web_id,
                                "folder_name": folder_name,
                            }
                        },
                    )
                    name_updated = True
                if desc_updated:
                    response_to_page = {
                        "status": 1,
                        "msg": "Description Updated Successfully!",
                    }
                    if name_updated:
                        response_to_page = {
                            "status": 1,
                            "msg": "Folder Name Updated Successfully!",
                        }
                if desc_updated and name_updated:
                    response_to_page = {
                        "status": 1,
                        "msg": "Folder Name and Description Updated Successfully!",
                    }
                return HttpResponse(
                    json.dumps(response_to_page), content_type="application/json"
                )
            if request.POST["type"] == "get_folder_update_data":
                folder_web_id = request.POST["folder_web_id"]
                if (
                    list(
                        folders_metadata_collection.find(
                            {"folder_web_id": folder_web_id}
                        )
                    )
                    != []
                ):
                    folder_data = folders_metadata_collection.find(
                        {"folder_web_id": folder_web_id}
                    )[0]
                    response_to_page = {
                        "status": 1,
                        "folder_name": folder_data["folder_name"],
                        "domain": folder_data["domain"],
                        "description": folder_data["description"],
                    }
                else:
                    response_to_page = {"status": 0, "msg": "Folder not found!"}
                return HttpResponse(
                    json.dumps(response_to_page), content_type="application/json"
                )
            if request.POST["type"] == "delete_folder":
                folder_web_id = request.POST["folder_web_id"]
                if (
                    list(
                        folders_metadata_collection.find(
                            {"folder_web_id": folder_web_id}
                        )
                    )
                    != []
                ):
                    folders_metadata_collection.delete_one(
                        {"folder_web_id": folder_web_id}
                    )
                    files_data.drop_collection(f"{folder_web_id}_metadata")
                    response_to_page = {
                        "status": 1,
                        "msg": "Folder Deleted Successfully!",
                    }
                else:
                    response_to_page = {"status": 0, "msg": "Folder does not exist!"}
                return HttpResponse(
                    json.dumps(response_to_page), content_type="application/json"
                )
            if request.POST["type"] == "open_folder":
                folder_web_id = request.POST["folder"]
                curr_folder = list(
                    folders_metadata_collection.find({"folder_web_id": folder_web_id})
                )[0]
                folder_files_metadata_collection = files_data[
                    f"{folder_web_id}_metadata"
                ]
                folder_files = list(
                    folder_files_metadata_collection.find(
                        {"folder_web_id": folder_web_id}
                    )
                )
                if curr_folder:
                    request.session["curr_folder"] = {
                        "folder_web_id": curr_folder["folder_web_id"],
                        "folder_name": curr_folder["folder_name"],
                        "description": curr_folder["description"],
                        "jd_count": curr_folder["jd_count"],
                        "resume_count": curr_folder["resume_count"],
                        "folder_dropdown": f"{curr_folder['folder_web_id']}_dropdown",
                        "folder_web_id": curr_folder["folder_web_id"],
                    }
                    if folder_files:
                        request.session["curr_files"] = [
                            {
                                "file_type": x["file_type"],
                                "file_name": x["file_name"],
                                "category": x["category"],
                                "uploaded_by": x["created_by"],
                                "uploaded_date": str(x["created_on"]),
                                "age": str(datetime.now() - x["created_on"]),
                                "embed_time": 1,
                                "size": os.path.getsize(x["file_path"]) / 8,
                            }
                            for x in folder_files
                        ]
                    else:
                        request.session["curr_files"] = []
                else:
                    request.session["curr_folder"] = {}

                response_to_page = {
                    "status": 1,
                    "url": reverse("file_manage"),
                }
                return HttpResponse(
                    json.dumps(response_to_page),
                    content_type="application/json",
                )
            if request.POST["type"] == "create_folder":
                curr_color = temp_colors.pop()
                if not temp_colors:
                    temp_colors = list(colors)
                folder_name_error_msg = (
                    """The Folder name has to be 5-25 characters long. """
                    """The Folder name needs to contain atleast one alphabet or number. """
                    """The Folder name can only contain a-z, A-Z, _ (underscores) and spaces. """
                    """The Folder name needs to start with an alphabet."""
                )
                folder_exists_error_msg = (
                    """The Folder name you entered already exists!"""
                )
                folder_filters = [
                    lambda x: re.findall(r"^[a-zA-Z][a-zA-Z0-9_ ]{4,25}$", x) == [],
                    # Checks if these characters exist in the string
                    # and that the length is greater than 5.
                    lambda x: 5 > len(x) or len(x) > 25,
                    # Checks if the length of the folder name is between
                    # 5 and 25 including both ends.
                    lambda x: x.split() == [],
                    # Checks if the string is empty
                    lambda x: re.findall(r"[0-9]", x) == []
                    and re.findall(r"[a-zA-Z]", x) == [],
                    # Checks if the string contains atleast one integer.
                ]

                folder_name = request.POST["folder_name"]
                if any(map(lambda x: x(folder_name), folder_filters)):
                    response_to_page = {"status": 0, "msg": folder_name_error_msg}
                    return HttpResponse(
                        json.dumps(response_to_page), content_type="application/json"
                    )
                elif (
                    list(
                        folders_metadata_collection.find(
                            {"folder_id": calculate_hash(folder_name)}
                        )
                    )
                    != []
                ):
                    response_to_page = {"status": 0, "msg": folder_exists_error_msg}
                    return HttpResponse(
                        json.dumps(response_to_page), content_type="application/json"
                    )

                folder_web_id = "_".join(folder_name.split()).lower()

                try:
                    domain = request.POST["domain"]
                except:
                    response_to_page = {"status": 0, "msg": "Please choose a domain!"}
                    return HttpResponse(
                        json.dumps(response_to_page), content_type="application/json"
                    )

                description = (
                    request.POST["description"]
                    if "description" in request.POST.keys()
                    and request.POST["description"]
                    else folder_name
                )

                metadata = {
                    "folder_id": calculate_hash(folder_name),
                    "folder_name": folder_name,
                    "folder_web_id": folder_web_id,
                    "folder_color": curr_color,
                    "folder_files_path": os.path.abspath(
                        f"src/media/{domain}/{folder_web_id}"
                    ),
                    "domain": domain,
                    "description": description,
                    "created_by": request.user.username,
                    "created_on": datetime.now(),
                    "modified_by": request.user.username,
                    "modified_on": datetime.now(),
                    "jd_count": 0,  # len(list(jd_collection.find())),
                    "resume_count": 0,  # len(list(resume_collection.find())),
                }
                try:
                    os.mkdir(metadata["folder_files_path"])
                except:
                    pass

                folders_metadata_collection.insert_one(metadata)
                messages.success(request, "Folder Successfully Created!")
                folders = folders_metadata_collection.find({})
                request.session["folders"] = [
                    {
                        "folder_name": x["folder_name"],
                        "description": x["description"],
                        "jd_count": x["jd_count"],
                        "resume_count": x["resume_count"],
                        "folder_dropdown": f"{folder_web_id}_dropdown",
                        "folder_color": x["folder_color"],
                        "folder_web_id": folder_web_id,
                        "text_color": "text-dark"
                        if x["folder_color"]
                        in ["bg-secondary", "bg-yellow", "bg-lightss"]
                        else "text-white",
                    }
                    for x in folders
                ]
                response_to_page = {
                    "status": 1,
                    "msg": "Successfully Created the Folder!",
                }
                return HttpResponse(
                    json.dumps(response_to_page), content_type="application/json"
                )
        elif request.method == "GET":
            folders = list(folders_metadata_collection.find({}))
            request.session["folders"] = [
                {
                    "folder_name": x["folder_name"],
                    "description": x["description"],
                    "jd_count": x["jd_count"],
                    "resume_count": x["resume_count"],
                    "folder_dropdown": f"{x['folder_web_id']}_dropdown",
                    "folder_color": x["folder_color"],
                    "folder_web_id": x["folder_web_id"],
                    "text_color": "text-dark"
                    if x["folder_color"] in ["bg-secondary", "bg-yellow", "bg-lightss"]
                    else "text-white",
                }
                for x in folders
            ]
            return render(request, "pages/data_manage.html", c)


def load_file(file_path):
    return (
        UnstructuredFileLoader(
            file_path,
            mode="single",
            post_processors=[
                clean_non_ascii_chars,
                lambda x: clean(
                    x,
                    extra_whitespace=True,
                ),
            ],
        )
        .load()[0]
        .page_content
    )


def file_manage(request):
    c = {}
    if request.user.is_authenticated:
        client = pymongo.MongoClient(mongo_url)
        folders_data = client["folders_data"]
        files_data = client["files_data"]
        folders_metadata_collection = folders_data["metadata"]
        request.session["dash"] = False
        request.session["data_manage"] = True
        request.session["business_case"] = False
        error_files = []
        if request.method == "POST":
            if request.POST["type"] == "file_upload":
                folder_web_id = request.POST["folder_web_id"]
                files = request.FILES
                for index in files.keys():
                    curr_folder = folders_metadata_collection.find(
                        {"folder_web_id": folder_web_id}
                    )[0]
                    folder_files_metadata_collection = files_data[
                        f"{folder_web_id}_metadata"
                    ]
                    folder_path = curr_folder["folder_files_path"]
                    temp_folder_path = os.path.abspath(f"src/media/temp")
                    file_name = "_".join(files[index].name.lower().split())
                    file_exists_error_msg = """The File you uploaded already exists!"""
                    if curr_folder:
                        if file_name.split(".")[1] not in ["pdf", "docx", "doc", "txt"]:
                            response_to_page = {
                                "status": 0,
                                "msg": "The File can only be of pdf, docx, doc and txt type.",
                            }
                            return HttpResponse(
                                json.dumps(response_to_page),
                                content_type="application/json",
                            )
                        temp_file_path = temp_folder_path + "/" + file_name
                        final_file_path = folder_path + "/" + file_name
                        with open(temp_file_path, "wb+") as fp:
                            for chunk in files[index].chunks():
                                fp.write(chunk)
                        file_content = load_file(temp_file_path)
                        if list(
                            folder_files_metadata_collection.find(
                                {"file_content_id": calculate_hash(file_content)}
                            )
                        ) or list(
                            folder_files_metadata_collection.find(
                                {"file_name_id": calculate_hash(file_name)}
                            )
                        ):
                            os.remove(temp_file_path)
                            response_to_page = {
                                "status": 0,
                                "msg": file_exists_error_msg,
                            }
                            return HttpResponse(
                                json.dumps(response_to_page),
                                content_type="application/json",
                            )
                        else:
                            os.remove(temp_file_path)
                            with open(final_file_path, "wb+") as fp:
                                for chunk in files[index].chunks():
                                    fp.write(chunk)
                        file_metadata = {
                            "file_content_id": calculate_hash(file_content),
                            "file_name_id": calculate_hash(file_name),
                            "file_name": file_name,
                            "file_path": final_file_path,
                            "folder_web_id": request.POST["folder_web_id"],
                            "category": request.POST["category"],
                            "description": request.POST["description"],
                            "file_type": "fa-file-pdf"
                            if file_name.endswith("pdf")
                            else "fa-file-word"
                            if file_name.endswith("docx") or file_name.endswith("doc")
                            else "fa-file-lines",
                            "created_by": request.user.username,
                            "created_on": datetime.now(),
                            "modified_by": request.user.username,
                            "modified_on": datetime.now(),
                            "uploaded": 1,
                            "processed": 0,
                        }
                        folders_metadata_collection.update_one(
                            {"folder_web_id": folder_web_id},
                            {"$inc": {f"{request.POST['category']}_count": 1}},
                        )
                        folder_files_metadata_collection.insert_one(file_metadata)
                        response_to_page = {
                            "status": 1,
                            "msg": "Successfully added Files",
                        }
                    else:
                        request.session["curr_folder"] = {}
                        request.session["curr_files"] = {}
                        response_to_page = {
                            "status": 0,
                            "url": reverse("data_manage"),
                        }
                return HttpResponse(
                    json.dumps(response_to_page), content_type="application/json"
                )
        if request.method == "GET":
            folder_web_id = request.session["curr_folder"]["folder_web_id"]

            curr_folder = list(
                folders_metadata_collection.find({"folder_web_id": folder_web_id})
            )[0]
            folder_files_metadata_collection = files_data[f"{folder_web_id}_metadata"]
            folder_files = list(
                folder_files_metadata_collection.find({"folder_web_id": folder_web_id})
            )
            if curr_folder:
                request.session["curr_folder"] = {
                    "folder_web_id": curr_folder["folder_web_id"],
                    "folder_name": curr_folder["folder_name"],
                    "description": curr_folder["description"],
                    "jd_count": curr_folder["jd_count"],
                    "resume_count": curr_folder["resume_count"],
                    "folder_dropdown": f"{curr_folder['folder_web_id']}_dropdown",
                    "folder_web_id": curr_folder["folder_web_id"],
                }
                if folder_files:
                    request.session["curr_files"] = [
                        {
                            "file_type": x["file_type"],
                            "file_name": x["file_name"],
                            "category": x["category"],
                            "uploaded_by": x["created_by"],
                            "uploaded_date": str(x["created_on"]),
                            "age": str(datetime.now() - x["created_on"]),
                            "embed_time": 1,
                            "size": os.path.getsize(x["file_path"]) / 8,
                        }
                        for x in folder_files
                    ]
                else:
                    request.session["curr_files"] = []
            return render(request, "pages/file_manage.html", c)


def resume(request):
    c = {}
    if request.user.is_authenticated:
        client = pymongo.MongoClient(mongo_url)
        folders_data = client["folders_data"]
        files_data = client["files_data"]
        folders_metadata_collection = folders_data["metadata"]
        request.session["dash"] = False
        request.session["data_manage"] = False
        request.session["business_case"] = True
        request.session["folders"] = [
            {
                "folder_name": x["folder_name"],
                "description": x["description"],
                "jd_count": x["jd_count"],
                "resume_count": x["resume_count"],
                "folder_dropdown": f"{x['folder_web_id']}_dropdown",
                "folder_color": x["folder_color"],
                "folder_web_id": x["folder_web_id"],
                "text_color": "text-dark"
                if x["folder_color"] in ["bg-secondary", "bg-yellow", "bg-lightss"]
                else "text-white",
            }
            for x in folders_metadata_collection.find({})
        ]
        request.session["choice_data"] = [
            {
                "folder_name": x["folder_name"],
                "description": x["description"],
                "jd_count": x["jd_count"],
                "resume_count": x["resume_count"],
                "folder_dropdown": f"{x['folder_web_id']}_dropdown",
                "folder_color": x["folder_color"],
                "folder_web_id": x["folder_web_id"],
                "text_color": "text-dark"
                if x["folder_color"] in ["bg-secondary", "bg-yellow", "bg-lightss"]
                else "text-white",
                "files": [
                    {
                        "file_name": f["file_name"],
                        "file_name_id": f["file_name_id"],
                        "category": f["category"],
                    }
                    for f in files_data[x["folder_web_id"] + "_metadata"].find({})
                ],
            }
            for x in request.session["folders"]
        ]
        if request.method == "GET":
            return render(request, "pages/resume.html", c)
