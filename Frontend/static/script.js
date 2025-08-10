document.addEventListener('DOMContentLoaded', function() {
    const classSchedule = document.getElementById('class-schedule');
    const assignmentList = document.getElementById('assignment-list');
    const dashboardSummaryCard = document.getElementById('dashboard-summary-card');

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
                        // Use class id for unique key
                        const storageKey = `class_checked_${c.id}_${today}`;
                        const checked = localStorage.getItem(storageKey) === 'true';
                        item.innerHTML = `
                            <label>
                                <input type="checkbox" ${checked ? 'checked' : ''} data-class-id="${c.id}" data-class-day="${today}">
                                <strong>${c.name}</strong> at ${c.time}
                            </label>
                        `;
                        // Add event listener for checkbox
                        item.querySelector('input[type="checkbox"]').addEventListener('change', function(e) {
                            localStorage.setItem(storageKey, e.target.checked ? 'true' : 'false');
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

    // --- Fetch and Display Donut Chart in Summary Card ---
    fetch('/api/subject-donut-chart')
        .then(response => response.json())
        .then(data => {
            const dashboardSummaryCard = document.getElementById('dashboard-summary-card');
            dashboardSummaryCard.innerHTML = '';
            if (data.chart_url) {
                const img = document.createElement('img');
                img.src = data.chart_url;
                img.alt = 'Study Hours by Subject';
                img.style.maxWidth = '320px';
                img.style.borderRadius = '8px';
                dashboardSummaryCard.appendChild(img);

                // Add legend with color and subject
                if (data.legend && Array.isArray(data.legend)) {
                    const legendDiv = document.createElement('div');
                    legendDiv.className = 'donut-legend';
                    data.legend.forEach(item => {
                        const legendItem = document.createElement('div');
                        legendItem.className = 'donut-legend-item';
                        legendItem.innerHTML = `<span class="donut-legend-color" style="background:${item.color}"></span>${item.subject}`;
                        legendDiv.appendChild(legendItem);
                    });
                    dashboardSummaryCard.appendChild(legendDiv);
                }
            } else {
                dashboardSummaryCard.textContent = data.message || 'No chart data available.';
            }
        })
        .catch(() => {
            dashboardSummaryCard.textContent = 'Failed to load chart.';
        });

    // --- Fetch and Display Weekly Study Log Chart ---
    const weeklyStudylog = document.getElementById('weekly-studylog');
    fetch('/api/generate-study-chart')
        .then(response => response.json())
        .then(data => {
            weeklyStudylog.innerHTML = '';
            if (data.chart_url) {
                const img = document.createElement('img');
                img.src = data.chart_url;
                img.alt = 'Weekly Study Log Chart';
                img.style.maxWidth = '100%';
                img.style.borderRadius = '8px';
                weeklyStudylog.appendChild(img);
            } else {
                weeklyStudylog.textContent = data.message || 'No chart data available.';
            }
        })
        .catch(() => {
            weeklyStudylog.textContent = 'Failed to load chart.';
        });

    // Initial data load
    fetchTodaysClasses();
    fetchUpcomingAssignments();
});
