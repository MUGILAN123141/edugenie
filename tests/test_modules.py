import qna
import summary_module
import learning_path

def test_qna_prompt(monkeypatch):
    monkeypatch.setattr(qna, "generate_text", lambda prompt: "Largest ocean: Pacific Ocean.")
    assert "Pacific" in qna.answer_question("Which is the largest ocean?")

def test_summary(monkeypatch):
    monkeypatch.setattr(summary_module, "generate_text", lambda prompt: "Short summary.")
    assert summary_module.summarize_text("This is a sufficiently long educational passage for testing.") == "Short summary."

def test_learning_path(monkeypatch):
    monkeypatch.setattr(learning_path, "generate_text", lambda prompt: "1. Basics\n2. Practice")
    assert "Basics" in learning_path.recommend_learning_path("SQL", "beginner", "learn SQL")
