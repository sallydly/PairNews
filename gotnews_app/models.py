from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

class Event(models.Model):
	name = models.CharField(max_length=1000)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'EVENT'
        verbose_name_plural = 'EVENTS'

class Entity(models.Model):
	name = models.CharField(max_length=1000)
	occurrence_count = models.IntegerField(default=0)

	class Meta:
		verbose_name='ENTITY'
		verbose_name_plural='ENTITIES'

class Article(models.Model):
	date = models.DateField(null=True, blank=True)
	overall_sentiment = models.DecimalField()
	title = models.CharField(max_length=1000)
	url = models.CharField(max_length=1000) # see if there is a url field
	event = models.ForeignKey(Event, related_name='articles_related')
	news_source = models.ForeignKey(NewsSource, related_name='articles_related')
	
	class Meta:
		verbose_name='ARTICLE'
		verbose_name_plural='ARTICLES'

class NewsSource(models.Model):
	name = models.CharField(max_length=1000)

	class Meta:
		verbose_name='NEWSSOURCE'
		verbose_name_plural='NEWSSOURCES'

class NewsSourceEntityAssoc(models.Model):
	news_source = models.ForeignKey(NewsSource, related_name='entities_related')
	entity = models.ForeignKey(NewsSource, related_name='news_sources_related')
	sentiment = models.DecimalField()

	@receiver(post_save)
	def increment_entity_occurence_count(sender, instance, created, raw, using, update_fields):
		if created:
			instance.entity.occurrence_count += 1
			instance.entity.save()
	
	@receiver(pre_delete)
	def decrement_entity_occurrence_count(sender, instance, using, **kwargs):
		instance.entity.occurrence_count = instance.entity.occurrence_count - 1
		instance.entity.save()

	class Meta:
		verbose_name='NEWSSOURCEENTITYASSOC'
		verbose_name_plural='NEWSSOURCEENTITYASSOCS'

class ArticleEntityAssoc(models.Model):
	article = models.ForeignKey(Article, related_name='entities_related')
	entity = models.ForeignKey(Entity, related_name='articles_related')
	sentiment = models.DecimalField()

	@receiver(post_save)
	def increment_entity_occurence_count(sender, instance, created, raw,using, update_fields):
		if created:
			instance.entity.occurrence_count += 1
			instance.entity.save()

	@receiver(pre_delete)
	def decrement_entity_occurrence_count(sender, instance, using, **kwargs):
		instance.entity.occurrence_count = instance.entity.occurrence_count - 1
		instance.entity.save()

	class Meta:
		verbose_name='ARTICLEENTITYASSOC'
		verbose_name_plural = 'ARTICLEENTITYASSOCS'
