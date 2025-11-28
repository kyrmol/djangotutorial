from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
import datetime
from .models import Question, Choice

def index(request): 
      return HttpResponse("Hello, world. You're at the polls index.")

def dashboard(request):
    # Statistics
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(total=Sum('votes'))['total'] or 0
    
    # Recent questions (last 7 days)
    week_ago = timezone.now() - datetime.timedelta(days=7)
    recent_questions = Question.objects.filter(pub_date__gte=week_ago).count()
    
    # Questions with vote data
    questions_with_stats = []
    for question in Question.objects.all().order_by('-pub_date')[:10]:
        choices = Choice.objects.filter(question=question)
        question_votes = choices.aggregate(total=Sum('votes'))['total'] or 0
        choice_count = choices.count()
        
        questions_with_stats.append({
            'question': question,
            'total_votes': question_votes,
            'choice_count': choice_count,
            'choices': choices,
        })
    
    # Top questions by votes
    top_questions = []
    for question in Question.objects.all():
        question_votes = Choice.objects.filter(question=question).aggregate(total=Sum('votes'))['total'] or 0
        if question_votes > 0:
            top_questions.append({
                'question': question,
                'total_votes': question_votes,
            })
    top_questions = sorted(top_questions, key=lambda x: x['total_votes'], reverse=True)[:5]
    
    # Chart data - votes per question
    chart_labels = []
    chart_data = []
    for item in questions_with_stats[:5]:
        chart_labels.append(item['question'].question_text[:30])
        chart_data.append(item['total_votes'])
    
    context = {
        'total_questions': total_questions,
        'total_choices': total_choices,
        'total_votes': total_votes,
        'recent_questions': recent_questions,
        'questions_with_stats': questions_with_stats,
        'top_questions': top_questions,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    
    return render(request, 'polls/dashboard.html', context)

