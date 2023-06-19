from django.shortcuts import render
from users.models import User

# Create your views here.


def profile_edit(request):
    context = {}
    if request.method == "POST":
        data = User.objects.get(email=request.user.email)

        context["data"] = data
        print(request.POST)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        user = User.objects.get(email=request.user.email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        context["status"] = "Changes Saved successfully"
    return render(request, "users/profile_edit.html", context)
