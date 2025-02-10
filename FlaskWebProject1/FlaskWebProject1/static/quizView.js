// fetching a json containing the quizes from the server
function initialize_quizes() {
    fetch_json().then(json => {
        document.getElementById('content').appendChild(json_to_items(json));
    });
}

function fetch_json() {
    return fetch('/getQuizes')
        .then(response => response.json())
        .catch(error => console.error('Error fetching quizzes:', error));
}

// creating a quiz element from a json object
function create_item(json_input) {
    let division = document.createElement('div');
    division.className = 'quiz-container';

    let image = document.createElement('img');
    image.src = json_input['imageSrc'];
    division.appendChild(image);

    let quizName = document.createElement('p');
    quizName.className = 'quiz-title';
    quizName.innerHTML = json_input['name'];
    division.appendChild(quizName);

    return division;
}

function json_to_items(jsonInput) {
    let container = document.createElement('div');
    container.style.display = 'flex';
    container.style.flexWrap = 'wrap';
    container.style.gap = '20px';
    container.style.justifyContent = 'center';
    for (let item of jsonInput['items']) {
        container.appendChild(create_item(item));
    }
    return container;
}