from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('show_category', args=(self.slug,))

    def add_like(self):
        self.likes += 1

    @classmethod
    def get_most_viewed(cls):
        return cls.objects.order_by('-views')[:5]

    class Meta:
        verbose_name_plural = 'categories'


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_url(self):
        return self.url

    @classmethod
    def get_most_viewed(cls):
        return cls.objects.order_by('-views')[:5]


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    # class MyPhoto(models.Model):
    #     image = ImageField()
    #
    #     def save(self, *args, **kwargs):
    #         if self.image:
    #             self.image = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
    #         super(MyPhoto, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     try:
    #         this = UserProfile.objects.get(id=self.id)
    #         if this.picture:
    #             this.picture.delete()
    #         print('Success OMG!')
    #     except UserProfile.DoesNotExist:
    #         pass
    #     super(UserProfile, self).save(*args, **kwargs)
