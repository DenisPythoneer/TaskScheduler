document.addEventListener('DOMContentLoaded', function() {
    getTasks('all');
});


async function getTasks(filter) {
    try {
        const response = await fetch('/tasks');
        const tasks = await response.json();
        
        renderTasks(tasks, filter);
        updateStats(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}


function renderTasks(tasks, filter = 'all') {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    
    let filteredTasks = tasks;
    
    if (filter === 'active') {
        filteredTasks = tasks.filter(task => !task.isComplete);
    } else if (filter === 'completed') {
        filteredTasks = tasks.filter(task => task.isComplete);
    }
    
    if (filteredTasks.length === 0) {
        const emptyMessage = document.createElement('li');
        emptyMessage.textContent = 'Нет задач';
        emptyMessage.style.textAlign = 'center';
        emptyMessage.style.color = '#95a5a6';
        taskList.appendChild(emptyMessage);
        return;
    }
    
    filteredTasks.forEach(task => {
        const taskItem = document.createElement('li');
        taskItem.className = 'task-item';
        if (task.isComplete) {
            taskItem.classList.add('completed');
        }
        
        taskItem.innerHTML = `
            <input type="checkbox" ${task.isComplete ? 'checked' : ''} onclick="toggleTask(${task.id})">
            <span class="task-title">${task.title}</span>
            <div class="task-actions">
                <button class="complete-btn" onclick="toggleTask(${task.id})">
                    ${task.isComplete ? 'Активна' : 'Завершить'}
                </button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">Удалить</button>
            </div>
        `;
        
        taskList.appendChild(taskItem);
    });
}


async function addTask() {
    const taskInput = document.getElementById('taskInput');
    const title = taskInput.value.trim();
    
    if (!title) {
        alert('Пожалуйста, введите задачу!');
        return;
    }
    
    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                is_completed: false
            })
        });
        
        if (response.ok) {
            taskInput.value = '';
            getTasks('all');
        } else {
            console.error('Error adding task:', await response.text());
        }
    } catch (error) {
        console.error('Error adding task:', error);
    }
}


async function deleteTask(taskId) {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
        return;
    }
    
    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            getTasks('all');
        } else {
            console.error('Error deleting task:', await response.text());
        }
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}


async function toggleTask(taskId) {
    try {
        const response = await fetch(`/tasks/${taskId}`, {
            method: 'PATCH'
        });
        
        if (response.ok) {
            getTasks('all');
        } else {
            console.error('Error toggling task:', await response.text());
        }
    } catch (error) {
        console.error('Error toggling task:', error);
    }
}


function updateStats(tasks) {
    const statsElement = document.getElementById('stats');
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(task => task.isComplete).length;
    const activeTasks = totalTasks - completedTasks;
    
    statsElement.textContent = `Всего: ${totalTasks} | Активные: ${activeTasks} | Завершенные: ${completedTasks}`;
}

  const themeToggle = document.querySelector('.theme-toggle');
  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
    document.body.classList.add('dark-mode');
  }

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
  });
