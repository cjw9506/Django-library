from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="enter the book's natural language")

    def __str__(self):
        return self.name

#class book(models.Model):
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='저자')
    summary = models.CharField(max_length=1000, help_text='Enter a brief description of the book', verbose_name='요약')
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book', verbose_name='장르')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name='언어')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
        
import uuid #Required for unique book instances

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status  = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = 'Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)   
    def __str__(self):
        return f'{self.id}({self.book.title})'
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name' , 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name},{self.first_name}'