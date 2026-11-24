import os
import django
import json
import glob
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Examination_system.settings')
django.setup()

from Portal.models import Exam, Question

exams_data = []
all_questions = []

for ex in Exam.objects.all():
    qs = []
    for q in Question.objects.filter(exam=ex):
        q_dict = {
            'id': q.id,
            'exam_title': ex.title,
            'question_text': getattr(q, 'question_text', getattr(q, 'text', '')),
            'option_a': getattr(q, 'option_a', ''),
            'option_b': getattr(q, 'option_b', ''),
            'option_c': getattr(q, 'option_c', ''),
            'option_d': getattr(q, 'option_d', ''),
            'correct_option': getattr(q, 'correct_option', 'A')
        }
        qs.append(q_dict)
        all_questions.append(q_dict)
    exams_data.append({
        'id': ex.id,
        'title': ex.title,
        'subject': getattr(ex, 'subject', 'General'),
        'duration': getattr(ex, 'duration_minutes', 30),
        'questions': qs
    })

print("Found Exams in DB:", len(exams_data), "Questions:", len(all_questions))

# Fallback if DB is empty
if not exams_data:
    exams_data = [
        {'id': 1, 'title': 'Physics Mechanics Test', 'subject': 'Physics', 'duration': 30, 'questions': [
            {'question_text': 'What is the SI unit of Force?', 'option_a': 'Newton (N)', 'option_b': 'Joule (J)', 'option_c': 'Watt (W)', 'option_d': 'Pascal (Pa)', 'correct_option': 'A'},
            {'question_text': 'Which quantity is a vector?', 'option_a': 'Speed', 'option_b': 'Velocity', 'option_c': 'Mass', 'option_d': 'Time', 'correct_option': 'B'},
            {'question_text': 'Value of g on Earth?', 'option_a': '9.8 m/s²', 'option_b': '8.9 m/s²', 'option_c': '10.8 m/s²', 'option_d': '7.8 m/s²', 'correct_option': 'A'}
        ]},
        {'id': 2, 'title': 'Chemistry Basics Test', 'subject': 'Chemistry', 'duration': 30, 'questions': [
            {'question_text': 'Chemical symbol for Gold?', 'option_a': 'Au', 'option_b': 'Ag', 'option_c': 'Fe', 'option_d': 'Pb', 'correct_option': 'A'},
            {'question_text': 'pH value of pure water?', 'option_a': '5', 'option_b': '7', 'option_c': '9', 'option_d': '14', 'correct_option': 'B'}
        ]},
        {'id': 3, 'title': 'Biology Life Science Test', 'subject': 'Biology', 'duration': 30, 'questions': [
            {'question_text': 'Powerhouse of the cell?', 'option_a': 'Mitochondria', 'option_b': 'Nucleus', 'option_c': 'Ribosome', 'option_d': 'Vacuole', 'correct_option': 'A'}
        ]},
        {'id': 4, 'title': 'Computer Science Python Test', 'subject': 'Computer Science', 'duration': 30, 'questions': [
            {'question_text': 'Which data structure uses LIFO?', 'option_a': 'Queue', 'option_b': 'Stack', 'option_c': 'Array', 'option_d': 'Tree', 'correct_option': 'B'}
        ]},
        {'id': 5, 'title': 'Mathematics Advanced Test', 'subject': 'Mathematics', 'duration': 30, 'questions': [
            {'question_text': 'Derivative of x² is?', 'option_a': '2x', 'option_b': 'x', 'option_c': '2', 'option_d': 'x²', 'correct_option': 'A'}
        ]},
        {'id': 6, 'title': 'Social-Science', 'subject': 'General', 'duration': 30, 'questions': [
            {'question_text': 'Capital of India?', 'option_a': 'Mumbai', 'option_b': 'New Delhi', 'option_c': 'Chennai', 'option_d': 'Kolkata', 'correct_option': 'B'}
        ]}
    ]
    for ex in exams_data:
        for q in ex['questions']:
            all_questions.append({**q, 'exam_title': ex['title']})

url_map = {
    'index': 'index.html', 'logout': 'index.html', 'dashboard': 'dashboard.html',
    'questions_list': 'questions.html', 'question_bank': 'questions.html',
    'add_question': 'add_question.html', 'exam_list': 'exam.html',
    'exam_page': 'exam_page.html', 'submit_exam': 'result.html',
    'result': 'result.html', 'admin_dashboard': 'admin_dashboard.html',
    'certificates': 'certificates.html', 'view_certificate': 'view_certificate.html',
}

def fix_urls(m):
    return url_map.get(m.group(1), m.group(1) + '.html')

db_json = json.dumps(exams_data)

runtime_js = f'''
<script>
const DB_EXAMS = {db_json};
document.addEventListener("DOMContentLoaded", function() {{
    const user = localStorage.getItem("demo_user") || "Student";
    const selId = Number(localStorage.getItem("demo_exam_id")) || (DB_EXAMS.length ? DB_EXAMS.id : 1);
    const currentExam = DB_EXAMS.find(e => e.id === selId) || DB_EXAMS;
    const score = localStorage.getItem("demo_score") || "80";
    const accuracy = localStorage.getItem("demo_acc") || "80";

    document.querySelectorAll(".js-username").forEach(el => el.innerText = user);
    document.querySelectorAll(".js-initials").forEach(el => el.innerText = user.slice(0, 2).toUpperCase());

    const path = window.location.pathname;

    if (path.endsWith("/") || path.endsWith("index.html")) {{
        const form = document.querySelector("form");
        if (form) {{
            form.addEventListener("submit", function(e) {{
                e.preventDefault();
                const u = form.querySelector("input[name='username']").value.trim() || "Student";
                localStorage.setItem("demo_user", u);
                window.location.href = u.toLowerCase() === "admin" ? "admin_dashboard.html" : "dashboard.html";
            }});
        }}
    }}

    if (path.includes("exam_page.html") && currentExam) {{
        const titleEl = document.querySelector("title");
        if (titleEl) titleEl.innerText = "Exam - " + currentExam.title;
        const h2 = document.querySelector("h2");
        if (h2) h2.innerText = currentExam.title;

        const navGrid = document.getElementById("q-nav-grid");
        const qList = document.getElementById("q-list-container");
        if (navGrid && qList && currentExam.questions.length > 0) {{
            navGrid.innerHTML = currentExam.questions.map((q, i) =>
                `<a href="#q_${{i+1}}" class="w-10 h-10 rounded-xl bg-white border border-gray-200 hover:bg-teal-500 hover:text-white flex items-center justify-center text-xs font-bold shadow-sm transition">${{i+1}}</a>`
            ).join("");

            qList.innerHTML = currentExam.questions.map((q, i) => `
                <div id="q_${{i+1}}" class="p-4 bg-gray-50 rounded-2xl border border-gray-200">
                    <p class="font-semibold text-gray-800 text-sm mb-4">${{i+1}}. ${{q.question_text}}</p>
                    <div class="space-y-2 text-sm">
                        <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_${{i}}" value="A"><span>A. ${{q.option_a}}</span></label>
                        <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_${{i}}" value="B"><span>B. ${{q.option_b}}</span></label>
                        <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_${{i}}" value="C"><span>C. ${{q.option_c}}</span></label>
                        <label class="flex items-center space-x-3 p-3 bg-white rounded-xl border border-gray-200 cursor-pointer hover:border-teal-500 transition"><input type="radio" name="q_${{i}}" value="D"><span>D. ${{q.option_d}}</span></label>
                    </div>
                </div>
            `).join("");
        }}

        let secs = (currentExam.duration || 30) * 60;
        const timerEl = document.getElementById("timer");
        if (timerEl) {{
            setInterval(() => {{
                if (secs > 0) secs--;
                timerEl.innerText = String(Math.floor(secs/60)).padStart(2,"0") + ":" + String(secs%60).padStart(2,"0");
            }}, 1000);
        }}

        const form = document.querySelector("form");
        if (form) {{
            form.addEventListener("submit", function(e) {{
                e.preventDefault();
                let correct = 0;
                const total = currentExam.questions.length || 1;
                currentExam.questions.forEach((q, i) => {{
                    const sel = form.querySelector(`input[name="q_${{i}}"]:checked`);
                    if (sel && sel.value.toUpperCase() === (q.correct_option || "").toUpperCase()) correct++;
                }});
                const pct = Math.round((correct / total) * 100);
                localStorage.setItem("demo_score", String(pct));
                localStorage.setItem("demo_acc", String(pct));
                window.location.href = "result.html";
            }});
        }}
    }}

    if (path.includes("result.html")) {{
        document.querySelectorAll(".js-score").forEach(el => el.innerText = score);
        document.querySelectorAll(".js-acc").forEach(el => el.innerText = accuracy);
        const bar = document.getElementById("js-score-bar");
        if (bar) bar.style.width = score + "%";
        const perf = document.getElementById("js-perf");
        if (perf) perf.innerText = Number(score) >= 50 ? "Excellent" : "Needs Improvement";
        const hdr = document.querySelector("header");
        if (hdr && !document.getElementById("cert-link")) {{
            hdr.insertAdjacentHTML("beforeend", '<a id="cert-link" href="view_certificate.html" class="bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold px-4 py-2 rounded-xl ml-2">View Certificate</a>');
        }}
    }}

    if (path.includes("view_certificate.html") && currentExam) {{
        const exEl = document.getElementById("cert-exam");
        if (exEl) exEl.innerText = currentExam.title;
        const scEl = document.getElementById("cert-score");
        if (scEl) scEl.innerText = score;
    }}
}});
function startDemoExam(id) {{ localStorage.setItem("demo_exam_id", String(id)); }}
</script>
</body>'''

