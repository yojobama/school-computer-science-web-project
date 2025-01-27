
// Your function to fetch and display quizzes
async function fetchQuizzes() {
    try {
        const response = await fetch('/getQuizes');
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        const data = await response.json();
        let recived_quizes = data;
        console.log('Received quizzes:', recived_quizes);
        alert("Hello world!");

        const quizContainer = document.getElementById("quizContainer");
        // Clear the container before appending
        quizContainer.innerHTML = '';

        for (let quiz of recived_quizes.quizes) {
            let new_div = document.createElement("div");
            new_div.className = "question";

            let name_heading = document.createElement("h3");
            name_heading.innerText = "Name: " + quiz.name;
            new_div.appendChild(name_heading);

            let author_heading = document.createElement("h4");
            author_heading.innerText = "Author: " + quiz.author;
            new_div.appendChild(author_heading);

            quizContainer.appendChild(new_div);
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error.message);
    }
}

// Call the fetchQuizzes function when the page loads
window.onload = fetchQuizzes;