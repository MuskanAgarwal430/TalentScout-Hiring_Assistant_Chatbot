
class ConversationState:
    def __init__(self):
        self.stage = "greeting"
        self.data = {}
        self.tech_questions = []
        self.answers = []
        self.q_index = 0
        self.finished = False

        self.info_questions = [
            "What's your full name?",
            "Great! What’s your email address?",
            "What’s your phone number?",
            "Great! How many years of experience do you have?",
            "Which position are you applying for?",
            "Nice. What’s your current location?",
            "Please list your tech stack (e.g., programming languages, frameworks, libraries, tools, databases, etc.)"
        ]
        self.current_info_index = 0

    def record_info_answer(self, answer):
        keys = ['Full Name', 'Email', 'Phone', 'Experience', 'Position', 'Location', 'Tech Stack']
        if self.current_info_index < len(keys):
            self.data[keys[self.current_info_index]] = answer.strip()
            self.current_info_index += 1
            # Move to tech questions after last info question
            if self.current_info_index == len(self.info_questions):
                self.stage = "questions"

    def next_info_question(self):
        if self.current_info_index < len(self.info_questions):
            question = self.info_questions[self.current_info_index]
            # Insert name only when asking for phone number or tech stack
            if self.current_info_index in [2, 6]:
                name = self.data.get("Full Name", "")
                if name:
                    question = f"Thanks, {name}! {question}"
            return question
        else:
            self.stage = "questions"
            return "Awesome! I’ll now ask you a few technical questions based on your tech stack. Please answer them one by one."

    def add_tech_question(self, question):
        self.tech_questions.append(question)

    def add_tech_answer(self, answer):
        self.answers.append(answer)

    def get_tech_history(self):
        history = ""
        for i, (q, a) in enumerate(zip(self.tech_questions, self.answers)):
            history += f"{i+1}. Q: {q}\n   A: {a}\n"
        return history
