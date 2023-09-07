from stackapi import StackAPI
from time import sleep


class StackOverflow:
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    def __init__(self):
        self.sent_questions = list()
        self.tags = ["python-3.x", "flask", "python-telegram-bot"]
        self.SITE = StackAPI('stackoverflow')

    def get_questions(self, tags):
        all_questions = list()
        for tag in tags:
            questions = self.SITE.fetch('questions', tagged=tag, sort='creation', order='desc', page=1, pagesize=5)
            for question in questions["items"]:
                if question["question_id"] not in self.sent_questions:
                    all_questions.append(question)
            sleep(2)
        return all_questions

    def send_question(self, question):
        question_text = question["title"]
        print(question_text)
        return True

    def send_questions(self, questions):
        for question in questions:
            if question["question_id"] not in self.sent_questions:
                if self.send_question(question):
                    self.sent_questions.append(question["question_id"])