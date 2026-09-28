const task = document.getElementById("task");
const level = document.getElementById("level");
const input = document.getElementById("input-text");
const inputLabel = document.getElementById("input-label");
const quizOptions = document.getElementById("quiz-options");
const goalBox = document.getElementById("goal-box");
const quizCount = document.getElementById("quiz-count");
const goal = document.getElementById("goal");
const button = document.getElementById("submit-btn");
const status = document.getElementById("status");
const result = document.getElementById("result-content");

const labels = {
  qa: ["Your question", "Example: Which is the largest ocean?"],
  explain: ["Topic to explain", "Example: Pythagoras theorem"],
  quiz: ["Topic or text for the quiz", "Example: Photosynthesis"],
  summarize: ["Educational passage", "Paste the passage you want summarized."],
  recommend: ["Topic", "Example: SQL"]
};

function updateForm() {
  const value = task.value;
  inputLabel.textContent = labels[value][0];
  input.placeholder = labels[value][1];
  quizOptions.classList.toggle("hidden", value !== "quiz");
  goalBox.classList.toggle("hidden", value !== "recommend");
}
task.addEventListener("change", updateForm);
updateForm();

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function render(data) {
  if (data.answer) {
    result.innerHTML = `<div>${escapeHtml(data.answer).replaceAll("\n", "<br>")}</div>`;
    return;
  }
  if (data.explanation) {
    result.innerHTML = `<div>${escapeHtml(data.explanation).replaceAll("\n", "<br>")}</div>`;
    return;
  }
  if (data.summary) {
    result.innerHTML = `<div>${escapeHtml(data.summary).replaceAll("\n", "<br>")}</div>`;
    return;
  }
  if (data.recommendations) {
    result.innerHTML = `<div>${escapeHtml(data.recommendations).replaceAll("\n", "<br>")}</div>`;
    return;
  }
  if (data.quiz) {
    const quiz = data.quiz;
    result.innerHTML = `<h3>${escapeHtml(quiz.topic)}</h3>` +
      quiz.questions.map((q, i) => `
        <article class="quiz-question">
          <strong>${i + 1}. ${escapeHtml(q.question)}</strong>
          ${q.options.map(o => `<div class="option">${escapeHtml(o)}</div>`).join("")}
          <div class="answer"><b>Answer:</b> ${escapeHtml(q.correct_answer)}<br>
          <b>Why:</b> ${escapeHtml(q.explanation)}</div>
        </article>`).join("");
  }
}

async function submit() {
  const value = input.value.trim();
  if (!value) {
    status.textContent = "Please enter some content first.";
    return;
  }

  let endpoint;
  let body;
  if (task.value === "qa") {
    endpoint = "/qa"; body = { question: value };
  } else if (task.value === "explain") {
    endpoint = "/explain"; body = { topic: value, level: level.value };
  } else if (task.value === "quiz") {
    endpoint = "/quiz"; body = { topic: value, level: level.value, count: Number(quizCount.value) };
  } else if (task.value === "summarize") {
    endpoint = "/summarize"; body = { text: value, level: level.value };
  } else {
    endpoint = "/learn/recommendations";
    body = { topic: value, level: level.value, goal: goal.value.trim() || "understand the topic well" };
  }

  button.disabled = true;
  status.textContent = "Generating...";
  result.textContent = "";
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    });
    const payload = await response.json();
    if (!response.ok || !payload.success) throw new Error(payload.detail || "Request failed.");
    render(payload.data);
    status.textContent = "Done.";
  } catch (err) {
    result.innerHTML = `<p class="error">${escapeHtml(err.message)}</p>`;
    status.textContent = "Something went wrong.";
  } finally {
    button.disabled = false;
  }
}
button.addEventListener("click", submit);
