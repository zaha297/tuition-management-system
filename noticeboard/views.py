from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.decorators import admin_or_teacher
from .models import Notice
from .forms import NoticeForm


@login_required
def notice_list(request):

    notices = Notice.objects.order_by("-created_at")

    return render(
        request,
        "noticeboard/notice_list.html",
        {
            "notices": notices
        }
    )


@login_required
@admin_or_teacher
def add_notice(request):

    if request.method == "POST":

        form = NoticeForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("notice_list")

    else:

        form = NoticeForm()

    return render(
        request,
        "noticeboard/add_notice.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_notice(request, id):

    notice = get_object_or_404(
        Notice,
        id=id
    )

    if request.method == "POST":

        form = NoticeForm(
            request.POST,
            instance=notice
        )

        if form.is_valid():

            form.save()

            return redirect("notice_list")

    else:

        form = NoticeForm(
            instance=notice
        )

    return render(
        request,
        "noticeboard/add_notice.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_notice(request, id):

    notice = get_object_or_404(
        Notice,
        id=id
    )

    notice.delete()

    return redirect("notice_list")