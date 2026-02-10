import json
import random

import pytest

from hangman import (
    Question,
    choose_hidden_indices,
    filter_questions_by_difficulty,
    read_json_file,
    render_word,
    select_random_questions,
)


def _write_questions(tmp_path, items):
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(items), encoding="utf-8")
    return path


def test_read_json_file_filters_invalid_entries(tmp_path):
    path = _write_questions(
        tmp_path,
        [
            {"question": "Q1", "answer": "Python", "difficulty": "easy"},
            {"question": "Q2", "answer": "List", "difficulty": "medium"},
            {"question": "", "answer": "Nope", "difficulty": "easy"},
            {"question": "Q3", "answer": "", "difficulty": "hard"},
            {"question": "Q4", "answer": "Test", "difficulty": "unknown"},
        ],
    )

    questions = read_json_file(str(path))

    assert len(questions) == 2
    assert questions[0] == Question(prompt="Q1", answer="python", difficulty="easy")
    assert questions[1] == Question(prompt="Q2", answer="list", difficulty="medium")


def test_read_json_file_raises_when_empty(tmp_path):
    path = _write_questions(tmp_path, [])
    with pytest.raises(ValueError):
        read_json_file(str(path))


def test_filter_questions_by_difficulty():
    questions = [
        Question(prompt="A", answer="x", difficulty="easy"),
        Question(prompt="B", answer="y", difficulty="medium"),
        Question(prompt="C", answer="z", difficulty="easy"),
    ]

    filtered = filter_questions_by_difficulty(questions, "easy")

    assert [q.prompt for q in filtered] == ["A", "C"]


def test_select_random_questions_returns_unique_subset():
    rng = random.Random(42)
    questions = [
        Question(prompt=f"Q{i}", answer="x", difficulty="easy") for i in range(6)
    ]

    selected = select_random_questions(questions, 4, rng)

    assert len(selected) == 4
    assert len({q.prompt for q in selected}) == 4


def test_choose_hidden_indices_size_and_bounds():
    rng = random.Random(0)
    indices_short = choose_hidden_indices("cat", rng)
    assert len(indices_short) == 1
    assert all(0 <= i < 3 for i in indices_short)

    indices_mid = choose_hidden_indices("snake", rng)
    assert len(indices_mid) == 2
    assert all(0 <= i < 5 for i in indices_mid)

    indices_long = choose_hidden_indices("developer", rng)
    assert len(indices_long) == 3
    assert all(0 <= i < 9 for i in indices_long)


def test_render_word():
    rendered = render_word("python", {0, 3, 5}, colorize_output=False)
    assert rendered == "p__h_n"
