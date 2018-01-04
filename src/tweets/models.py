import re

from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from .validators import validate_content
from hashtags.signals import parsed_hashtags

class TweetManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj

		qs = self.get_queryset().filter(user=user, parent=og_parent).filter(
			timestamp__year=timezone.now().year,
			timestamp__month=timezone.now().month,
			timestamp__day=timezone.now().day,
			reply=False,
			)
		if qs.exists():
			return None

		qs = self.get_queryset().filter(user=user, parent=parent_obj)
		if qs.exists():
			return None;
		
		obj = self.model(
			parent = parent_obj,
			user = user,
			content = parent_obj.content,
			)
		obj.save()
		return obj

	def like_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			not_liked = True
			tweet_obj.liked.remove(user)
		else:
			not_liked = False
			tweet_obj.liked.add(user)
		return not_liked

class Tweet(models.Model):
	parent    = models.ForeignKey("self", blank=True, null=True)
	user      = models.ForeignKey(settings.AUTH_USER_MODEL)
	content   = models.CharField(max_length=140, validators=[validate_content])
	liked     = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	reply     = models.BooleanField(verbose_name='Is a reply?',default=False)
	updated   = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = TweetManager()

	def __str__(self):
	     return str(self.content)

	def get_absolute_url(self):
		return reverse("tweet:detail", kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp', 'content']

	def get_parent(self):
		the_parent = self
		if self.parent:
			the_parent = self.parent
		return the_parent

	def get_children(self):
		parent = self.get_parent()
		qs = Tweet.objects.filter(parent=parent)
		qs_parent = Tweet.objects.filter(pk=parent.pk)
		return (qs | qs_parent)
	# def clean(self, *args, **kwargs):         //Validation for Content
	# 	content = self.content
	# 	if content == "abc":
	# 		raise ValidationError("Cannot be ABC")
	# 	return super(Tweet, self).clean(*args, **kwargs)

def tweet_save_receiver(sender, instance, created, *args, **kwargs):
  if created and not instance.parent:
  	user_regex = r'@(?P<username>[\w.@+-]+)'
  	username = re.findall(user_regex, instance.content)
  	# if m:
  	# 	username = m.group("username")
  	# 	print(username)
  	# 	#alert();

  	hash_regex = r'#(?P<hashtag>[\w.\d-]+)'
  	hashtags = re.findall(hash_regex, instance.content)
  	parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
  	# if h_m:
  	# 	hashtag = h_m.group("hashtag")
  	# 	print(hashtag)




post_save.connect(tweet_save_receiver, sender = Tweet)