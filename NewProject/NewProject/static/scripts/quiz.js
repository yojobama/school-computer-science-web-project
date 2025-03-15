function initialize_quiz(data) {
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').append(json_to_quiz(JSON.parse(data)));
    document.getElementById('content').innerHTML += "<input type='submit' class='quiz-submit' value='Submit' id='submitButton' />";

    document.getElementById('content').addEventListener('submit', function (event) {
        event.preventDefault();
        handleFormSubmit(JSON.parse(data));
    });
}

function json_to_quiz(json_input) {
    let container = document.createElement('div');
    container.className = 'quiz-container';

    let header = document.createElement('h3');
    header.className = 'quiz-header';
    header.innerHTML = json_input['header'];
    container.appendChild(header);

    let questions = document.createElement('div');
    for (let question of json_input['questions']) {
        questions.appendChild(create_item(question));
    }
    container.appendChild(questions);

    return container;
}

function create_item(item) {
    let questionContainer = document.createElement('div');
    questionContainer.className = 'quiz-question-container';

    let question = document.createElement('p');
    question.className = 'quiz-question';
    question.innerHTML = item['question'];
    questionContainer.appendChild(question);

    let options = document.createElement('select');
    options.className = 'quiz-options';
    options.name = item['question']; // Add name attribute to identify the question
    for (let option of item.options) {
        let optionHtml = document.createElement('option');
        optionHtml.className = 'quiz-option';
        optionHtml.value = option; // Set the value attribute to the option text
        optionHtml.innerHTML = option;
        options.appendChild(optionHtml);
    }
    questionContainer.appendChild(options);

    return questionContainer;
}

function handleFormSubmit(data) {
    const formData = new FormData(document.getElementById('content'));
    let correctAnswers = 0;

    data.questions.forEach((question) => {
        const selectedOption = formData.get(question.question);
        if (selectedOption === question.answer) {
            correctAnswers++;
        }
    });

    showResults(correctAnswers, data.questions.length);
}

function showResults(correct, total) {
    const percentage = (correct / total) * 100;
    const resultMessage = `You got ${percentage}% correct!`;
    document.getElementById('result-message').innerText = resultMessage;
    document.getElementById('result-popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('result-popup').style.display = 'none';
}
