# %%
import json
from difflib import get_close_matches


def load_json(file: str) -> dict:
    """Load json file

    Args:
        file (str): json file path

        Returns:
            dict: json file content
    """
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(file: str, data: dict) -> None:
    """Save data to json file

    Args:
        file (str): json file path
        data (dict): data to save
    """
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def new_input(input: str, inputs: list[str], answer: str) -> dict | None:
    """Create new input

    Args:
        input (str): input
        inputs (list): list of inputs
        answer (str): answer

    Returns:
        dict: new input
    """
    if input not in inputs:
        return {"input": input, "answer": answer}


def get_inputs(answers: list[dict]) -> list[str]:
    """Get inputs from answers

    Args:
        answers (list): list of answers

    Returns:
        list: list of inputs
    """
    return [answer['input'] for answer in answers]


def get_answer(input: str, answers: list[dict]) -> str:
    """Get answer from input

    Args:
        input (str): input
        answers (list): list of answers

    Returns:
        str: answer
    """
    return [answer['answer'] for answer in answers if answer['input'] == input][0]


def get_closest_match(input: str, inputs: list[str]) -> str:
    """Get closest match to input

    Args:
        input (str): user input
        inputs (list): list of inputs

    Returns:
        str: closest match
    """
    try:
        return get_close_matches(input, inputs, n=1, cutoff=0.7)[0]
    except IndexError:
        return ''
