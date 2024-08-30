document.addEventListener('DOMContentLoaded', () => {

    // Get references to HTML elements
    const addTaskButton = document.getElementById('add-task');
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');

    addTaskButton.addEventListener('click', () => {
        const taskText = taskInput.value.trim(); // Trimming helps avoid spaces being added to the list
        if (taskText !== '') {
            // Send a POST request to the Flask server
            // fetch API
            // POST request made to the /classify route of flask server
            fetch('/classify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'task-input': taskText
                })
            })
            .then(response => response.json())
            .then(data => {
                const listItem = document.createElement('li');
                listItem.textContent = `${taskText} (${data.category})`; // Display task with its category

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'x';
                deleteBtn.className = 'delete-task';
                deleteBtn.addEventListener('click', function() {
                    listItem.remove();
                });

                listItem.addEventListener('click', function(event) {
                    event.stopPropagation(); // Prevents click from affecting the entire list item (delete button)
                    listItem.classList.toggle('strikethrough');
                });

                listItem.appendChild(deleteBtn);
                taskList.appendChild(listItem);

                taskInput.value = ''; // Clear input box after task is added
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
});
