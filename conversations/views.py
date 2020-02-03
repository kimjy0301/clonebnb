from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, View
from django.http import Http404
from users import models as user_models
from . import models as conversation_models
from . import forms
from django.db.models import Q

# Create your views here.


def go_conversations(request, host_pk, guest_pk):
    user_host = user_models.User.objects.get_or_none(pk=host_pk)
    user_guest = user_models.User.objects.get_or_none(pk=guest_pk)
    if user_host is not None and user_guest is not None:
        try:
            conversation = conversation_models.Conversation.objects.get(
                (Q(participants=user_host) & Q(participants=user_guest))
            )
        except conversation_models.Conversation.DoesNotExist:
            conversation = conversation_models.Conversation.objects.create()
            conversation.participants.add(user_host)
            conversation.participants.add(user_guest)

    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = conversation_models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm
        return render(
            self.request,
            "conversations/detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        form = forms.AddCommentForm(self.request.POST)
        pk = kwargs.get("pk")
        conversation = conversation_models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if form.is_valid():
            message = form.cleaned_data.get("message")
            conversation_models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
            return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
