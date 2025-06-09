
def greeting_prompt():
    return "Hello! 👋 Welcome to TalentScout’s virtual hiring assistant. I’ll ask you a few questions to help us understand your profile. Let’s begin!"

def fallback_prompt():
    return "Sorry, I didn't quite get that. Could you please rephrase?"

def build_first_tech_question_prompt(tech_stack):
    return f"Please ask the first technical interview question for a candidate skilled in {tech_stack}.Ask only question with no other description."

def build_next_tech_question_prompt(tech_stack, history):
    return (
        f"You are interviewing a candidate for {tech_stack} skills.\n\n"
        f"Previously asked questions and candidate answers:\n{history}\n\n"
        "Please ask the next most relevant and appropriately challenging technical question.\n"
        "Limit to a maximum of 3-5 technical questions for this interview.\n"
        "If enough questions have been asked already, respond with:'no more questions'\n"
        "Ask only one question at a time. Do not repeat anything."
        "Do not include any explanations, context, or follow-up text—just output the question clearly."
    )
