function initialize_quiz(data) {
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').append(json_to_quiz(JSON.parse(data)));
    document.getElementById('content').innerHTML += "<input type='submit' class='quiz-submit' value='Submit' id='submitButton' />";

    document.getElementById('content').addEventListener('submit', function (event) {
        event.preventDefault();
        handleFormSubmit();
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
    for (let option of item.options) {
        let optionHtml = document.createElement('option');
        optionHtml.className = 'quiz-option';
        optionHtml.innerHTML = option;
        options.appendChild(optionHtml);
    }
    questionContainer.appendChild(options);

    return questionContainer;
}

function handleFormSubmit() {
    const formData = new FormData(document.getElementById('content'));
    const entries = Array.from(formData.entries());
    console.log(entries); // Process the form data as needed
    alert('Form submitted! Check the console for form data.');
}
