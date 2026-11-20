from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, StudentAttempt, StudentAnswer
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
   
    
    if request.method == 'POST':
     
        username = request.POST.get('username')  
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'index.html', {'error': 'Invalid username or password'})
            
    return render(request, 'index.html')
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard_view(request):
    attempts = StudentAttempt.objects.filter(user=request.user)
    completed_count = attempts.filter(status='Completed').count()
    active_count = Exam.objects.filter(is_active=True).count()
    
    context = {
        'attempts': attempts,
        'completed_count': completed_count,
        'active_count': active_count,
    }
    return render(request, 'question.html', context)  

@login_required
def exam_list_view(request):
    exams = Exam.objects.filter(is_active=True)
    user_attempts = {att.exam_id: att.status for att in StudentAttempt.objects.filter(user=request.user)}
    
    exam_data = []
    for exam in exams:
        status = user_attempts.get(exam.id, 'Not Started')
        exam_data.append({
            'exam': exam,
            'status': status
        })
        
    return render(request, 'exam.html', {'exam_data': exam_data})

@login_required
def exam_page_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    attempt, created = StudentAttempt.objects.get_or_create(
        user=request.user, 
        exam=exam,
        defaults={'status': 'In Progress'}
    )
    
    questions = exam.questions.all()
    return render(request, 'exam_page.html', {
        'exam': exam,
        'attempt': attempt,
        'questions': questions
    })


@login_required
def questions_list_view(request):
    questions = Question.objects.select_related('exam').all()
    return render(request, 'questions.html', {'questions': questions})

@login_required
def add_question_view(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam')
        question_text = request.POST.get('question_text')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_option = request.POST.get('correct_option')

        exam = Exam.objects.get(id=exam_id)

        Question.objects.create(
            exam=exam,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option
        )

        messages.success(request, 'Question added successfully!')
        return redirect('question_bank')

    exams = Exam.objects.all()
    return render(request, 'add_question.html', {
        'exams': exams
    })

@login_required
def submit_exam_view(request, attempt_id):
    if request.method == 'POST':
        attempt = get_object_or_404(StudentAttempt, id=attempt_id, user=request.user)
        questions = attempt.exam.questions.all()
        
        correct_count = 0
        total_q = questions.count()
        
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            is_correct = (selected == q.correct_option)
            if is_correct:
                correct_count += 1
            
      
            StudentAnswer.objects.update_or_create(
                attempt=attempt,
                question=q,
                defaults={
                    'selected_option': selected,
                    'is_correct': is_correct
                }
            )
            
        score = int((correct_count / total_q) * 100) if total_q > 0 else 0
        accuracy = round((correct_count / total_q) * 100, 1) if total_q > 0 else 0
        
        attempt.score = score
        attempt.accuracy = accuracy
        attempt.status = 'Completed'
        attempt.save()
        
        return redirect('result', attempt_id=attempt.id)
    
@login_required
def result_view(request, attempt_id):
    print("Logged-in User ID:", request.user.id)

    attempt = get_object_or_404(
        StudentAttempt,
        id=attempt_id,
        user=request.user
    )

    return render(request, 'result.html', {
        'attempt': attempt
    })


@login_required
def dashboard_view(request):
    attempts = StudentAttempt.objects.filter(user=request.user)
    completed_count = attempts.filter(status='Completed').count()
   
    exams = Exam.objects.filter(is_active=True)
    active_count = exams.count()
    
    context = {
        'attempts': attempts,
        'completed_count': completed_count,
        'active_count': active_count,
        'exams': exams,  
    }
    return render(request, 'dashboard.html', context)


@login_required
def admin_dashboard_view(request):
    total_exams = Exam.objects.count()
    total_students = User.objects.filter(is_staff=False).count()
    total_attempts = StudentAttempt.objects.count()
    recent_attempts = StudentAttempt.objects.select_related('user', 'exam').order_by('-start_time')[:5]

    # Subject counts for Chart.js
    subject_data = Exam.objects.values('subject').annotate(total=Count('id'))
    subjects = [item['subject'] if item['subject'] else 'General' for item in subject_data]
    subject_counts = [item['total'] for item in subject_data]

    context = {
        'total_exams': total_exams,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'recent_attempts': recent_attempts,
        'subjects': subjects,
        'subject_counts': subject_counts,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def certificate_list_view(request):
   
    completed_attempts = StudentAttempt.objects.filter(status='Completed').select_related('user', 'exam')
    return render(request, 'certificates.html', {'attempts': completed_attempts})




@login_required
def view_certificate(request, attempt_id):
    attempt = get_object_or_404(
        StudentAttempt.objects.select_related('user', 'exam'),
        id=attempt_id
    )

    return render(request, 'view_certificate.html', {
        'attempt': attempt
    })
