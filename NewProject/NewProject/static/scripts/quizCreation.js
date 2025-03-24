let questions = [];

class Question {
    constructor(question, options, answer) {
        this.question = question;
        this.options = options;
        this.answer = answer;
    }
}

function openQuestionForm() {
    console.log("openQuestionForm called");
    document.getElementById("question").value = "";
    document.getElementById("options").value = "";
    document.getElementById("questionForm").style.display = "block";
}

function closeQuestionForm(event) {
    event.preventDefault();
    questions.push(new Question(document.getElementById("question").value, document.getElementById("options").value.split("\n"), document.getElementById("answer").value));
    document.getElementById("questionForm").style.display = "none";
    updateQuestions();
}

function submitQuestions(event) {

    if (questions.length == 0) {
        return false;
    }

    event.preventDefault();
    const quizName = document.getElementById("quizName").value;
    const quizDescription = document.getElementById("quizDescription").value;
    const answer = document.getElementById("answer").value;
    const imageFile = document.getElementById("quizImage").files[0];
    const quizData = {
        name: quizName,
        description: quizDescription,
        questions: questions,
        answer: answer
    };

    const formData = new FormData();
    formData.append('quizData', JSON.stringify(quizData));
    if (imageFile) {
        formData.append('image', imageFile);
    }

    fetch('/create', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(`Error ${response.status}: ${errorData.message}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            alert('Quiz submitted successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error submitting quiz.');
        });
}

function updateQuestions() {
    let questionList = document.getElementById("questionList");
    questionList.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let listItem = document.createElement("li");
        listItem.innerHTML = questions[i].question;
        questionList.appendChild(listItem);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('quizForm').addEventListener('submit', submitQuestions);
    document.getElementById('questionForm').addEventListener('submit', closeQuestionForm);
});

function openQuestionForm() {
    console.log("openQuestionForm called");
    document.getElementById("question").value = "";
    document.getElementById("options").value = "";
    document.getElementById("questionForm").style.display = "block";
}

function closeQuestionForm(event) {
    event.preventDefault();
    const question = document.getElementById("question").value;
    const options = document.getElementById("options").value.split("\n");
    const answer = document.getElementById("answer").value;
    questions.push(new Question(question, options, answer));
    document.getElementById("questionForm").style.display = "none";
    updateQuestions();
}

function updateQuestions() {
    let questionList = document.getElementById("questionList");
    questionList.innerHTML = "";
    for (let i = 0; i < questions.length; i++) {
        let listItem = document.createElement("li");
        listItem.innerHTML = questions[i].question;
        questionList.appendChild(listItem);
    }
    updateAnswerOptions();
}

function updateAnswerOptions() {
    const options = document.getElementById("options").value.split("\n");
    const answerSelect = document.getElementById("answer");
    answerSelect.innerHTML = "";
    options.forEach(option => {
        let optionElement = document.createElement("option");
        optionElement.value = option;
        optionElement.text = option;
        answerSelect.appendChild(optionElement);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('quizForm').addEventListener('submit', submitQuestions);
    document.getElementById('questionForm').addEventListener('submit', closeQuestionForm);
    document.getElementById('options').addEventListener('input', updateAnswerOptions);
});