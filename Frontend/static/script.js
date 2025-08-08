document.addEventListener('DOMContentLoaded', function() {
    const classSchedule = document.getElementById('class-schedule');
    const assignmentList = document.getElementById('assignment-list');

    // --- Fetch and Display Today's Schedule as an Interactive Checklist ---
    const fetchTodaysClasses = () => {
        fetch('/api/classes')
            .then(response => response.json())
            .then(data => {
                const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
                const todaysClasses = data.filter(c => c.day.toLowerCase() === today.toLowerCase());

                classSchedule.innerHTML = '';

                if (todaysClasses.length > 0) {
                    const list = document.createElement('ul');
                    list.className = 'checklist';

                    todaysClasses.forEach(c => {
                        const item = document.createElement('li');
                        const classId = `class-${c.id}`;
                        const isCompleted = localStorage.getItem(classId) === 'true';

                        // Set the inner HTML for the checklist item.
                        // The <label> is linked to the <input> by the `for` and `id` attributes.
                        // This is crucial for accessibility and for the browser's default behavior.
                        item.innerHTML = `
                            <input type="checkbox" id="${classId}" ${isCompleted ? 'checked' : ''}>
                            <label for="${classId}">${c.name} at ${c.time}</label>
                        `;

                        // Apply the 'completed' class if the item was already checked.
                        if (isCompleted) {
                            item.classList.add('completed');
                        }

                        // Find the checkbox we just created.
                        const checkbox = item.querySelector('input[type="checkbox"]');

                        // **FIXED LOGIC:**
                        // Listen for the 'change' event directly on the checkbox.
                        // This event fires after the browser has handled the click on the label and toggled the checkbox.
                        checkbox.addEventListener('change', function() {
                            // The checkbox's 'checked' state is now the source of truth.
                            // Toggle the visual 'completed' class on the parent list item.
                            item.classList.toggle('completed', checkbox.checked);

                            // Save the new state to localStorage.
                            localStorage.setItem(classId, checkbox.checked);
                        });

                        list.appendChild(item);
                    });

                    classSchedule.appendChild(list);
                } else {
                    classSchedule.innerHTML = '<p>No classes scheduled for today.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching classes:', error);
                classSchedule.innerHTML = '<p>Could not load schedule.</p>';
            });
    };

    // --- Fetch and Display Upcoming Assignments ---
    const fetchUpcomingAssignments = () => {
        fetch('/api/assignments')
            .then(response => response.json())
            .then(data => {
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                const upcomingAssignments = data.filter(a => {
                    const dueDate = new Date(a.due_date);
                    return dueDate >= today;
                });

                upcomingAssignments.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));

                assignmentList.innerHTML = '';
                if (upcomingAssignments.length > 0) {
                    const list = document.createElement('ul');
                    upcomingAssignments.slice(0, 5).forEach(a => {
                        const item = document.createElement('li');
                        item.innerHTML = `<strong>${a.title}</strong> (${a.subject}) - Due: ${a.due_date}`;
                        list.appendChild(item);
                    });
                    assignmentList.appendChild(list);
                } else {
                    assignmentList.innerHTML = '<p>No upcoming assignments.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching assignments:', error);
                assignmentList.innerHTML = '<p>Could not load assignments.</p>';
            });
    };

    // Initial data load
    fetchTodaysClasses();
    fetchUpcomingAssignments();
});
