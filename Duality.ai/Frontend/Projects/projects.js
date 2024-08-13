document.addEventListener('DOMContentLoaded', function() {
    const projectsTable = document.getElementById('projectsTable');
    const tasksTable = document.getElementById('tasksTable');
    const tableTitle = document.getElementById('tableTitle');

    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength - 3) + '...';
    }

    // Function to switch to tasks table
    function showTasks(projectId, projectName) {
        projectsTable.style.display = 'none';
        tasksTable.style.display = 'table';
        tableTitle.textContent = projectName;
        tableTitle.dataset.projectId = projectId;
        tableTitle.classList.add('clickable-title');

        // Here you would typically fetch tasks for the project from a server
        // For this example, we'll just add some dummy data
        const taskData = [
            { 
                task: 'Codeverse form', 
                description: 'Submitting a codeverse form based on the query and client details from the database',
                steps: 'Step 1: Open Google.com\n Step 2: Type in Codeverse.uk.\n Step 3: Find and click Get in touch.\n Step 4: Fill in the form.\n Step 5: Submit',
                createdAt: '2023-08-16', 
                successRate: '75%' 
            },
            { 
                task: 'Github Completion', 
                description: 'Description for Task 2. This is also a long description that will be truncated initially.',
                steps: 'Step 1: Begin. Step 2: Continue. Step 3: End.',
                createdAt: '2023-08-17', 
                successRate: '90%' 
            },
            // Add more tasks as needed
        ];

        const tasksBody = tasksTable.querySelector('tbody');
        tasksBody.innerHTML = ''; // Clear existing rows

        taskData.forEach(task => {
            const row = tasksBody.insertRow();
            row.innerHTML = `
                <td>${task.task}</td>
                <td class="expandable-cell" data-full-text="${task.description}">${truncateText(task.description, 30)}</td>
                <td class="expandable-cell" data-full-text="${task.steps}">${truncateText(task.steps, 30)}</td>
                <td>${task.createdAt}</td>
                <td>${task.successRate}</td>
                <td>
                    <button class="edit-btn">Edit</button>
                    <button class="delete-btn">Delete</button>
                </td>
            `;
        });

        // Add click event for expandable cells
        tasksBody.querySelectorAll('.expandable-cell').forEach(cell => {
            cell.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent row from being selected
                this.classList.toggle('expanded');
                if (this.classList.contains('expanded')) {
                    this.textContent = this.getAttribute('data-full-text');
                } else {
                    this.textContent = truncateText(this.getAttribute('data-full-text'), 30);
                }
            });
        });
    }

    // Function to switch back to projects table
    function showProjects() {
        tasksTable.style.display = 'none';
        projectsTable.style.display = 'table';
        tableTitle.textContent = 'Projects';
        delete tableTitle.dataset.projectId;
        tableTitle.classList.remove('clickable-title');
    }

    // Event delegation for project name clicks
    projectsTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('project-name')) {
            e.preventDefault();
            const projectId = e.target.getAttribute('data-project-id');
            const projectName = e.target.textContent;
            showTasks(projectId, projectName);
        }
    });

    // Clickable title to return to projects view
    tableTitle.addEventListener('click', function() {
        if (this.classList.contains('clickable-title')) {
            showProjects();
        }
    });

    // Add edit and delete functionality for both projects and tasks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-btn')) {
            // Implement edit functionality
            console.log('Edit button clicked');
        } else if (e.target.classList.contains('delete-btn')) {
            // Implement delete functionality
            console.log('Delete button clicked');
        }
    });
});