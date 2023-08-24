from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter
from .models import Post, User

class PostFilter(FilterSet):
    author = ModelMultipleChoiceFilter(
        field_name="author__user",
        queryset=User.objects.filter(author__isnull=False),
        label="Автор",
        conjoined=False,
    )

    creation_datetime = DateFilter(
        field_name="creation_datetime",
        widget=forms.DateInput(attrs={"type": "date"}),
        lookup_expr="gt",
        label="Опубликовано после",
    )

    heading=CharFilter(field_name="heading", lookup_expr="icontains", label="Заголовок")
    
    class Meta:
        model = Post
        fields = ["author", "creation_datetime", "heading"]
        # fields = {
        #     'heading': ['icontains'],
        #     'author__user': ['exact'],
        #     'creation_datetime': ['gt']
        # }