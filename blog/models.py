from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django.contrib.auth import get_user_model


from seo.const import (
    INDEX_CHOICES,
    FOLLOW_CHOICES,
    DEFAULT_OBJECT_TYPES
)
from seo.settings import (
    SEO_OG_TYPES,
    SEO_IMAGE_WIDTH,
    SEO_IMAGE_HEIGHT
)
User = get_user_model()


class SEO(models.Model):
    seo_object_type = models.CharField(
        pgettext_lazy('ok:seo', 'Open graph type'),
        max_length=40,
        blank=True,
        choices=SEO_OG_TYPES,
        default=DEFAULT_OBJECT_TYPES[0][0]
    )
    seo_index = models.CharField(
        pgettext_lazy('ok:seo', 'Index robots value'),
        max_length=15,
        blank=True,
        choices=INDEX_CHOICES,
        default=INDEX_CHOICES[0][0]
    )
    seo_follow = models.CharField(
        pgettext_lazy('ok:seo', 'Follow robots value'),
        max_length=15,
        blank=True,
        choices=FOLLOW_CHOICES,
        default=FOLLOW_CHOICES[0][0]
    )
    seo_canonical = models.CharField(
        pgettext_lazy('ok:seo', 'Canonical'),
        max_length=255,
        blank=True
    )
    seo_title = models.CharField(
        pgettext_lazy('ok:seo', 'Title'),
        max_length=255,
        blank=True
    )
    seo_og_title = models.CharField(
        pgettext_lazy('ok:seo', 'OpenGraph Title'),
        max_length=255,
        blank=True
    )
    seo_keywords = models.TextField(
        pgettext_lazy('ok:seo', 'Keywords'),
        blank=True,
    )
    seo_description = models.TextField(
        pgettext_lazy('ok:seo', 'Description'),
        blank=True,
    )
    seo_h1 = models.CharField(
        pgettext_lazy('ok:seo', 'H1 title'),
        max_length=255,
        blank=True
    )
    seo_h2 = models.CharField(
        pgettext_lazy('ok:seo', 'H2 title'),
        max_length=255,
        blank=True
    )
    seo_h3 = models.CharField(
        pgettext_lazy('ok:seo', 'H3 title'),
        max_length=255,
        blank=True
    )
    seo_text = models.TextField(
        pgettext_lazy('ok:seo', 'Seo text'),
        blank=True,
        help_text=pgettext_lazy(
            'ok:seo',
            'Can be useful for some static pages '
            'or some objects (like product category).'
        ),
    )
    seo_img_width = models.PositiveIntegerField(
        pgettext_lazy('ok:seo', 'Image width'),
        default=SEO_IMAGE_WIDTH
    )
    seo_img_height = models.PositiveIntegerField(
        pgettext_lazy('ok:seo', 'Image height'),
        default=SEO_IMAGE_HEIGHT
    )
    seo_img_alt = models.CharField(
        pgettext_lazy('ok:seo', 'Image alt text'),
        max_length=255,
        blank=True
    )

    @property
    def meta(self):
        return {
            "object_type": self.seo_object_type,
            "index": self.seo_index,
            "canonical": self.seo_canonical,
            "title": self.seo_title,
            "og_title": self.seo_og_title,
            "keywords": self.seo_keywords,
            "description": self.seo_description,
            "h1": self.seo_h1,
            "h2": self.seo_h2,
            "h3": self.seo_h3,
            "seo_text": self.seo_text,
            "img_width": self.seo_img_width,
            "img_height": self.seo_img_height,
            "img_alt": self.seo_img_alt
        }

    class Meta:
        abstract = True


class Post(SEO, models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Post`s creator', related_name="posts")
    title = models.CharField(max_length=200, verbose_name='The title')
    content = RichTextField(verbose_name='Post content')
    created_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created time')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    slug = models.SlugField(blank=True, verbose_name='Name of post in URL', allow_unicode=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_time",)

    def save(self, *args, **kwargs):
        if not self.content_uk:
            self.content_uk = self.content_en
        if not self.title_uk:
            self.title_uk = self.title_en
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Liked post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Like`s owner')
    time = models.DateTimeField(auto_now_add=True)
