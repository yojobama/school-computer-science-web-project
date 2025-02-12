function initialize_quiz(data) {
    document.getElementById('content').innerHTML = '';
    document.getElementById('content').appendChild(json_to_quiz(JSON.parse(data)));
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

    let options = document.createElement('div');
    options.className = 'quiz-options';
    for (let option of item.options) {
        let optionHtml = document.createElement('div');
        optionHtml.className = 'quiz-option';
        optionHtml.innerHTML = option;
        options.appendChild(optionHtml);
    }
    questionContainer.appendChild(options);

    return questionContainer;
}