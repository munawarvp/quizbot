
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id and current_question_id != 0:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["score"] = 0

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        bot_responses.append("Thank you for playing the game. Your result is: ")
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
        session["current_question_id"] = None
        session["answer_list"] = []

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id or current_question_id == 0:
        question = PYTHON_QUESTION_LIST[current_question_id]
        
        session["answer_list"].append({
            'question': question['question_text'],
            'answer': question['answer'],
            'user_answer': answer
        })

        if answer == question["answer"]:
            session["score"] += 1
        
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0
    
    if current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        return PYTHON_QUESTION_LIST[ current_question_id + 1 ], current_question_id + 1

    return False, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    final_result = {}
    score = session.get("score", 0)
    total_questions = len(PYTHON_QUESTION_LIST)
    answer_list = session.get("answer_list", [])

    if answer_list:
        final_result ={
            'score': score,
            'total_questions': total_questions,
            'answer_list': answer_list
        }

    return final_result
