from django.core.management.base import BaseCommand
from Portal.models import Exam, Question

class Command(BaseCommand):
    help = 'Seeds 5 subject exams with preset questions'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        Exam.objects.all().delete()

        subjects_data = [
            {
                'title': 'Mathematics Advanced Test',
                'subject': 'Mathematics',
                'questions': [
                    {"q": "What is the derivative of x^2?", "a": "2x", "b": "x^2", "c": "x", "d": "2", "correct": "A"},
                    {"q": "Value of Pi (approx)?", "a": "3.14", "b": "2.71", "c": "1.41", "d": "1.73", "correct": "A"},
                    {"q": "Square root of 144?", "a": "10", "b": "11", "c": "12", "d": "14", "correct": "C"},
                    {"q": "If 2x = 10, what is x?", "a": "2", "b": "5", "c": "10", "d": "20", "correct": "B"},
                    {"q": "Sum of angles in a triangle?", "a": "90°", "b": "180°", "c": "360°", "d": "270°", "correct": "B"},
                ]
            },
            {
                'title': 'Physics Mechanics Test',
                'subject': 'Physics',
                'questions': [
                    {"q": "SI unit of Force?", "a": "Joule", "b": "Newton", "c": "Watt", "d": "Pascal", "correct": "B"},
                    {"q": "Speed of light in vacuum?", "a": "3x10^8 m/s", "b": "3x10^6 m/s", "c": "3x10^5 km/s", "d": "None", "correct": "A"},
                    {"q": "Newton's First Law is also known as?", "a": "Law of Inertia", "b": "Law of Momentum", "c": "Law of Gravity", "d": "Energy Law", "correct": "A"},
                    {"q": "Acceleration due to gravity (approx)?", "a": "8.9 m/s²", "b": "9.8 m/s²", "c": "10.5 m/s²", "d": "7.5 m/s²", "correct": "B"},
                    {"q": "Work done is product of force and?", "a": "Time", "b": "Velocity", "c": "Displacement", "d": "Mass", "correct": "C"},
                ]
            },
            {
                'title': 'Chemistry Basics Test',
                'subject': 'Chemistry',
                'questions': [
                    {"q": "Chemical symbol for Gold?", "a": "Ag", "b": "Au", "c": "Pb", "d": "Fe", "correct": "B"},
                    {"q": "What is the pH of pure water?", "a": "5", "b": "7", "c": "9", "d": "14", "correct": "B"},
                    {"q": "Gas most abundant in Earth's atmosphere?", "a": "Oxygen", "b": "Hydrogen", "c": "Nitrogen", "d": "Carbon Dioxide", "correct": "C"},
                    {"q": "Atomic number of Carbon?", "a": "6", "b": "8", "c": "12", "d": "14", "correct": "A"},
                    {"q": "H2O is commonly known as?", "a": "Salt", "b": "Water", "c": "Sugar", "d": "Acid", "correct": "B"},
                ]
            },
            {
                'title': 'Biology Life Science Test',
                'subject': 'Biology',
                'questions': [
                    {"q": "Powerhouse of the cell?", "a": "Nucleus", "b": "Ribosome", "c": "Mitochondria", "d": "Golgi body", "correct": "C"},
                    {"q": "Human body's largest organ?", "a": "Heart", "b": "Liver", "c": "Skin", "d": "Brain", "correct": "C"},
                    {"q": "Process plants use to make food?", "a": "Respiration", "b": "Photosynthesis", "c": "Transpiration", "d": "Digestion", "correct": "B"},
                    {"q": "Normal human body temperature?", "a": "37°C", "b": "98°C", "c": "35°C", "d": "40°C", "correct": "A"},
                    {"q": "Basic unit of life?", "a": "Tissue", "b": "Organ", "c": "Cell", "d": "Molecule", "correct": "C"},
                ]
            },
            {
                'title': 'Computer Science Python Test',
                'subject': 'Computer Science',
                'questions': [
                    {"q": "Which is a Python extension?", "a": ".pt", "b": ".py", "c": ".pn", "d": ".pi", "correct": "B"},
                    {"q": "Keyword used to define a function in Python?", "a": "func", "b": "define", "c": "def", "d": "lambda", "correct": "C"},
                    {"q": "Which data type is immutable?", "a": "List", "b": "Dictionary", "c": "Tuple", "d": "Set", "correct": "C"},
                    {"q": "HTML stands for?", "a": "Hyper Text Markup Language", "b": "High Tech Multi Language", "c": "Hyper Transfer Machine Language", "d": "None", "correct": "A"},
                    {"q": "Django is based on which architecture?", "a": "MVC", "b": "MVT", "c": "MVVM", "d": "Client-Server", "correct": "B"},
                ]
            }
        ]

        for s_data in subjects_data:
            exam = Exam.objects.create(
                title=s_data['title'],
                subject=s_data['subject'],
                description=f"Online evaluation test for {s_data['subject']}",
                duration_minutes=30,
                total_questions=len(s_data['questions']),
                start_date="2026-01-01",
                end_date="2026-12-31"
            )
            for q in s_data['questions']:
                Question.objects.create(
                    exam=exam,
                    question_text=q['q'],
                    option_a=q['a'],
                    option_b=q['b'],
                    option_c=q['c'],
                    option_d=q['d'],
                    correct_option=q['correct']
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 5 subject exams and questions!'))