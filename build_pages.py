import os
import django
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Examination_system.settings')
django.setup()

from Portal.models import Exam, Question

exams = list(Exam.objects.all())
all_questions = list(Question.objects.all())

url_map = {
    "{% url 'index' %}": "index.html",
    "{% url 'logout' %}": "index.html",
    "{% url 'dashboard' %}": "dashboard.html",
    "{% url 'questions_list' %}": "questions.html",
    "{% url 'question_bank' %}": "questions.html",
    "{% url 'add_question' %}": "add_question.html",
    "{% url 'exam_list' %}": "exam.html",
    "{% url 'admin_dashboard' %}": "admin_dashboard.html",
    "{% url 'certificates' %}": "certificates.html",
}

def clean_django_tags(txt):
    for old, new in url_map.items():
        txt = txt.replace(old, new)
    txt = txt.replace('{{ request.user.username }}', 'Student')
    txt = txt.replace('{{ user.username }}', 'Student')
    txt = txt.replace('method="POST"', 'method="GET"')
    while '{%' in txt:
        s = txt.find('{%')
        e = txt.find('%}', s)
        if e == -1:
            break
        txt = txt[:s] + txt[e+2:]
    while '{{' in txt:
        s = txt.find('{{')
        e = txt.find('}}', s)
        if e == -1:
            break
        txt = txt[:s] + txt[e+2:]
    return txt

# 1. index.html (Login -> goes directly to dashboard.html)
idx_txt = open('templates/index.html', encoding='utf-8').read()
idx_txt = idx_txt.replace('<form method="POST">', '<form action="dashboard.html" method="GET">')
open('index.html', 'w', encoding='utf-8').write(clean_django_tags(idx_txt))

# 2. dashboard.html (All 9 Exams from DB)
dash_txt = open('templates/dashboard.html', encoding='utf-8').read()
colors = ['bg-blue-600', 'bg-purple-600', 'bg-emerald-600', 'bg-amber-500', 'bg-indigo-600']
cards_html = ""
for i, ex in enumerate(exams):
    q_count = Question.objects.filter(exam=ex).count()
    cards_html += f"""
    <div class="bg-white border border-slate-200 rounded-2xl p-6 relative overflow-hidden shadow-sm hover:shadow-md transition flex flex-col justify-between">
        <div class="absolute top-0 left-0 w-full h-1 {colors[i % len(colors)]}"></div>
        <div>
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-bold text-slate-900 text-base">{ex.title}</h3>
                <span class="text-xs px-2.5 py-1 bg-slate-100 text-slate-600 font-medium rounded-md">{ex.subject}</span>
            </div>
            <p class="text-xs text-slate-500 mb-4 leading-relaxed">
                Duration: {ex.duration_minutes} mins <br>
                Total Questions: {q_count}
            </p>
        </div>
        <div class="flex items-center justify-between pt-4 border-t border-slate-100">
            <span class="text-xs px-3 py-1 bg-blue-50 text-blue-700 font-semibold rounded-full">Ready to Take</span>
            <a href="exam_{ex.id}.html" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-xl shadow-sm transition flex items-center gap-2">
                <span>Start Exam</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
            </a>
        </div>
    </div>"""

s = dash_txt.find('{% if exams %}')
e = dash_txt.find('{% endif %}', s) + 11
dash_txt = dash_txt[:s] + cards_html + dash_txt[e:]
open('dashboard.html', 'w', encoding='utf-8').write(clean_django_tags(dash_txt))

# 3. exam.html (All 9 Exams list)
exam_txt = open('templates/exam.html', encoding='utf-8').read()
exam_cards = ""
for ex in exams:
    q_count = Question.objects.filter(exam=ex).count()
    exam_cards += f"""
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition flex flex-col justify-between">
        <div>
            <div class="h-2 bg-blue-500"></div>
            <div class="p-5">
                <h3 class="font-bold text-gray-800 text-lg mb-2">{ex.title}</h3>
                <p class="text-xs text-gray-400">Subject & Questions:</p>
                <p class="text-xs font-semibold text-gray-600 mb-4">{ex.subject} - {q_count} Questions ({ex.duration_minutes} mins)</p>
            </div>
        </div>
        <div class="p-5 pt-0 flex items-center justify-between">
            <span class="text-xs px-3 py-1 rounded-full font-medium bg-blue-100 text-blue-700">Available</span>
            <a href="exam_{ex.id}.html" class="w-8 h-8 rounded-full bg-gray-100 hover:bg-blue-600 hover:text-white flex items-center justify-center text-gray-600 transition">
                <i class="fa-solid fa-chevron-right text-xs"></i>
            </a>
        </div>
    </div>"""

s = exam_txt.find('{% for item in exam_data %}')
e = exam_txt.find('{% endfor %}', s) + 12
exam_txt = exam_txt[:s] + exam_cards + exam_txt[e:]
open('exam.html', 'w', encoding='utf-8').write(clean_django_tags(exam_txt))

# 4. Separate Pure HTML Page for EACH Exam (exam_1.html, exam_2.html, etc.)
ep_tpl = open('templates/exam_page.html', encoding='utf-8').read()
for ex in exams:
    qs = list(Question.objects.filter(exam=ex))
    nav_html = "".join(f'<a href="#q_{i}" class="w-10 h-10 rounded-xl bg-white border border-gray-200 hover:bg-teal-500 hover:text-white flex items-center justify-center text-xs font-bold shadow-sm transition">{i}</a>' for i in range(1, len(qs)+1))
    q_html = ""
    for i, q in enumerate(qs, 1):
        q_html += f"""
        <div id="q_{i}" class="p-4 bg-gray-50 rounded-2xl border border-gray-200">
            <p class="font-semibold text-gray-800 text-sm mb-4">{i}. {q.question_text}</p>
            <div class="space-y-2 text-sm">
                <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_{i}" value="A"><span>A. {q.option_a}</span></label>
                <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_{i}" value="B"><span>B. {q.option_b}</span></label>
                <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_{i}" value="C"><span>C. {q.option_c}</span></label>
                <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_{i}" value="D"><span>D. {q.option_d}</span></label>
            </div>
        </div>"""

    t = ep_tpl.replace('{{ exam.title }}', ex.title).replace('Interactive Test Session', ex.title)
    t = t.replace('{% url \'submit_exam\' attempt.id %}', 'result.html')
    s1 = t.find('{% for q in questions %}')
    e1 = t.find('{% endfor %}', s1) + 12
    t = t[:s1] + nav_html + t[e1:]
    s2 = t.find('{% for q in questions %}')
    e2 = t.find('{% endfor %}', s2) + 12
    t = t[:s2] + q_html + t[e2:]
    clean_out = clean_django_tags(t)
    open(f'exam_{ex.id}.html', 'w', encoding='utf-8').write(clean_out)
    if ex == exams[0]:
        open('exam_page.html', 'w', encoding='utf-8').write(clean_out)

# 5. questions.html (All 65 Questions)
q_txt = open('templates/questions.html', encoding='utf-8').read()
q_rows = ""
for i, q in enumerate(all_questions, 1):
    q_rows += f"""
    <tr class="hover:bg-purple-50/50">
        <td class="p-3 font-semibold text-slate-900">{i}</td>
        <td class="p-3"><span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-lg font-medium">{q.exam.title}</span></td>
        <td class="p-3 font-medium text-slate-800">{q.question_text}</td>
        <td class="p-3 font-bold text-emerald-600 uppercase">{q.correct_option}</td>
        <td class="p-3"><a href="add_question.html" class="px-3 py-1 bg-purple-50 text-purple-600 rounded-lg text-xs font-semibold hover:bg-purple-100"><i class="fa-solid fa-pen-to-square"></i> Edit</a></td>
    </tr>"""

s = q_txt.find('{% for q in questions %}')
e = q_txt.find('{% endfor %}', s) + 12
q_txt = q_txt[:s] + q_rows + q_txt[e:]
open('questions.html', 'w', encoding='utf-8').write(clean_django_tags(q_txt))

# 6. result.html, certificates.html, view_certificate.html, admin_dashboard.html, add_question.html
res_txt = open('templates/result.html', encoding='utf-8').read()
res_txt = res_txt.replace('{{ attempt.score }}', '80').replace('{{ attempt.accuracy }}', '80').replace('{{ attempt.status }}', 'Passed')
res_txt = res_txt.replace('{% if attempt.score >= 50 %}Excellent{% else %}Needs Improvement{% endif %}', 'Excellent')
res_txt = res_txt.replace('Back to Exams</a>', 'Back to Exams</a><a href="view_certificate.html" class="bg-purple-600 text-white text-xs font-semibold px-4 py-2 rounded-xl ml-2">View Certificate</a>')
open('result.html', 'w', encoding='utf-8').write(clean_django_tags(res_txt))

vc_txt = open('templates/view_certificate.html', encoding='utf-8').read()
vc_txt = vc_txt.replace('{{ attempt.user.username }}', 'Student').replace('{{ attempt.exam.title }}', exams[0].title if exams else 'Examination').replace('{{ attempt.score }}', '80').replace('{{ attempt.status }}', 'Passed')
open('view_certificate.html', 'w', encoding='utf-8').write(clean_django_tags(vc_txt))

for extra in ['certificates.html', 'admin_dashboard.html', 'add_question.html']:
    et = open(f'templates/{extra}', encoding='utf-8').read()
    open(extra, 'w', encoding='utf-8').write(clean_django_tags(et))

print(f"SUCCESS! Pure HTML built for {len(exams)} exams & {len(all_questions)} questions (NO JS)!")
