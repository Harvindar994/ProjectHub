from django.shortcuts import render, redirect
from .models import Project
from django.contrib import messages
from django.contrib.auth.models import User, auth
import re

# Create your views here.
def home(request):
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})

def Singup(request):
    if request.method == 'POST':
        frist_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, "username already used.")
            return redirect('Singup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "email already exits.")
            return redirect('Singup')
        else:
            user = User.objects.create_user(username=username, password=password, email=email,
                                            first_name=frist_name,
                                            last_name=last_name)
            user.save()
            return redirect('Login')
    else:
        return render(request, 'singUp.html')

def forgetPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        new_password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.filter(email=email)
        if len(user) > 0:
            user = user[0]
        else:
            user = None
        if user is not None:
            if user.username == username:
                if name.lower() == str(user.first_name).lower() + " " + str(user.last_name).lower():
                    if new_password == confirm_password:
                        if len(new_password) > 0:
                            user.set_password(new_password)
                            user.save()
                            messages.info(request, "Password Successfully Changed")
                            return render(request, 'forgetPassword.html', {'msg_color': '#28a745'})
                        else:
                            messages.info(request, "Invalid Password")
                            return render(request, 'forgetPassword.html', {'msg_color': '#dc3545'})
                    else:
                        messages.info(request, "Password is not matching")
                        return render(request, 'forgetPassword.html', {'msg_color': '#dc3545'})
                else:
                    messages.info(request, "Invalid Name")
                    return render(request, 'forgetPassword.html', {'msg_color': '#dc3545'})
            else:
                messages.info(request, "Invalid Username " + user.username)
                return render(request, 'forgetPassword.html', {'msg_color': '#dc3545'})
        else:
            messages.info(request, "Account doesn't exist")
            return render(request, 'forgetPassword.html', {'msg_color': '#dc3545'})
    else:
        return render(request, 'forgetPassword.html')

def Login(request):
    # u = User.objects.get(username='admin')
    # u.set_password('1234')
    # u.save()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username or password is invalid')
            return redirect('Login')
    else:
        if str(request.user) == "AnonymousUser":
            return render(request, 'Login.html')
        else:
            return redirect('/')

def viewHomeProject(request, pk=None):
    project = Project.objects.get(id=pk)
    return render(request, 'viewHomeProject.html', {'project': project})

def Search(request):
    if request.method == "POST":
        string = request.POST['Search']
        projects = Project.objects.all()
        result = []
        for project in projects:
            name = project.name
            email = project.email
            developerName = project.developerName
            description = project.description
            code = project.code

            for findData in [name, email, developerName]:
                find = re.compile(findData)
                matches = list(find.finditer(string))
                if len(matches) > 0:
                    result.append(project)
                    break
                find = re.compile(string)
                matches = list(find.finditer(findData))
                if len(matches) > 0:
                    result.append(project)
                    break
            else:
                find = re.compile(string)
                matches = list(find.finditer(description))
                if len(matches) > 0:
                    result.append(project)
                    continue
                find = re.compile(description)
                matches = list(find.finditer(string))
                if len(matches) > 0:
                    result.append(project)
                    continue

                try:
                    string.index(code)
                    result.append(project)
                except ValueError:
                    try:
                        code.index(string)
                        result.append(project)
                    except ValueError:
                        pass

        return render(request, 'index.html', {'projects': result})

    return redirect('/')

def Logout(request):
    auth.logout(request)
    return redirect('/')

def Dashboard(request):
    return render(request, "editProfile.html")

def EditProfile(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        new_password = request.POST['new_password']
        old_password = request.POST['password']
        new_username = request.POST['username']

        if first_name == "" or last_name == "" or new_username == "":
            messages.info(request, "You can't leave any field blank except new password")
            return render(request, "editProfile.html", {'msg_color': '#dc3545'})
        else:
            username = request.user.username
            user = auth.authenticate(username=username, password=old_password)
            if user is not None:
                user.first_name = first_name
                user.last_name = last_name
                if not new_password == "":
                    user.set_password(new_password)
                if not username == new_username:
                    if User.objects.filter(username=new_username).exists():
                        messages.info(request, "username already used")
                        return render(request, "editProfile.html", {'msg_color': '#dc3545'})
                user.username = new_username
                auth.logout(request)
                user.save()
                auth.login(request, user)
                messages.info(request, "profile updated")
                return render(request, "editProfile.html", {'msg_color': '#28a745'})
            else:
                messages.info(request, "incorrect password")
                return render(request, "editProfile.html", {'msg_color': '#dc3545'})
    else:
        return render(request, "editProfile.html")

def deleteAccount(request):
    user = User.objects.get(email=request.user.email)
    if not str(request.user) == "AnonymousUser":
        projects = Project.objects.filter(email=request.user.email)
        for project in projects:
            project.delete()
        auth.logout(request)
        user.delete()
    return redirect('/')

def bashboardViewProject(request, pk=None):
    project = Project.objects.get(id=pk)
    return render(request, 'viewProject.html', {'project': project})

def Projects(request):
    projects = Project.objects.filter(email=request.user.email)
    if len(projects) == 0:
        return render(request, "NoData.html", {'message': 'No Project'})
    else:
        return render(request, "dasProjects.html", {'projects': projects})

def AddProject(request):
    if request.method == "POST":
        name = request.POST['name']
        image = request.FILES['image']
        Description = request.POST['description']
        code = request.POST['code']
        developerName = str(request.user.first_name).capitalize()+" "+str(request.user.last_name).capitalize()
        project = Project(name=name, image=image, developerName=developerName,
                          email=request.user.email, description=Description, code=code)
        project.save()
        messages.info(request, "Project Added")
        return render(request, "addProject.html", {'msg_color': '#28a745'})
    else:
        return render(request, "addProject.html")

def DeleteProject(request, pk=None):
    project = Project.objects.get(id=pk)
    project.delete()
    return redirect("Projects")

def EditProject(request, pk=None):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST['name']
        try:
            image = request.FILES['image']
        except:
            image = None

        Description = request.POST['description']
        code = request.POST['code']

        if name == "" or Description == "" or code == "":
            messages.info(request, "You can't leave any field blank except Preview")
            return render(request, "editProject.html", {"project": project, 'msg_color': '#dc3545'})
        else:
            project.name = name
            project.description = Description
            project.code = code
            if image is not None:
                project.image = image
            project.save()
            messages.info(request, "Project Updated")
        return render(request, "editProject.html", {"project": project, 'msg_color': '#28a745'})
    else:
        return render(request, "editProject.html", {"project": project})