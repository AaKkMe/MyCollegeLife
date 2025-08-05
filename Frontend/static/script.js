document.addEventListener('DOMContentLoaded', function() {
    const classSchedule = document.getElementById('class-schedule');
    const assignmentList = document.getElementById('assignment-list');

    // --- Fetch and Display Today's Schedule ---
    const fetchTodaysClasses = () => {
        fetch('/api/classes')
            .then(response => response.json())
            .then(data => {
                const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
                const todaysClasses = data.filter(c => c.day.toLowerCase() === today.toLowerCase());

                classSchedule.innerHTML = ''; // Clear existing content
                if (todaysClasses.length > 0) {
                    const list = document.createElement('ul');
                    todaysClasses.forEach(c => {
                        const item = document.createElement('li');
                        item.innerHTML = `<strong>${c.name}</strong> at ${c.time}`;
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
                today.setHours(0, 0, 0, 0); // Set to midnight to compare dates only

                const upcomingAssignments = data.filter(a => {
                    const dueDate = new Date(a.due_date);
                    return dueDate >= today;
                });

                // Sort by due date
                upcomingAssignments.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));

                assignmentList.innerHTML = ''; // Clear existing content
                if (upcomingAssignments.length > 0) {
                    const list = document.createElement('ul');
                    // Display only the next 5 assignments
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
