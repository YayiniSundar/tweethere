from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views import View
from django.views.generic import (
	CreateView,
	DetailView,
	DeleteView,
	ListView,
	UpdateView
	)
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet


#Retweet
class RetweetView(View):
 def get(self, request, pk, *args, **kwargs):
 	tweet = get_object_or_404(Tweet, pk=pk)
 	if request.user.is_authenticated():
 		new_tweet = Tweet.objects.retweet(request.user, tweet)
 		return HttpResponseRedirect("/")
 	return HttpResponseRedirect(tweet.get_absolute_url())


# Create your views here.
class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	# success_url = "/tweet/create/"
	# login_url = '/admin/'

	# def form_valid(self, form):   //Added this to Mixins.py file
	# 	if self.request.user.is_authenticated():
	# 		form.instance.user = self.request.user
	# 		return super(TweetCreateView, self).form_valid(form)
	# 	else:
	# 		return self.form_invalid(form)


# def tweet_create_view(request):
# 	form = TweetModelForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.user = request.user
# 		instance.save()
# 	context = {
# 	"form":form
# 	}
# 	return render(request, 'tweets/create_view.html', context)

#Update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/update_view.html'
	#success_url = "/tweet/"

#Delete
class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	template_name = 'tweets/delete_confirm.html'
	success_url = reverse_lazy("tweet:list")

#Retrieve 
class TweetDetailView(DetailView):
	# template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	def get_object(self):
		pk= self.kwargs.get("pk")
		obj = get_object_or_404(Tweet, pk=pk)
		return obj

class TweetListView(LoginRequiredMixin, ListView):
	# template_name = "tweets/list_view.html"
	#queryset = Tweet.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		# print(self.request.GET)
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm
		context['create_url'] = reverse_lazy("tweet:create")
		return context




# def tweet_detail_view(request, id=8):
# 	obj = Tweet.objects.get(id=id)
# 	print(obj)
# 	context = {
# 	    "object": obj
# 	}
# 	return render(request, "tweets/detail_view.html", context)

# def tweet_list_view(request):
# 	queryset = Tweet.objects.all()
# 	print(queryset)
# 	for obj in queryset:
# 		print(obj.content)
# 	context = {
# 	    "object_list": queryset
# 	}
# 	return render(request, "tweets/list_view.html", context)
