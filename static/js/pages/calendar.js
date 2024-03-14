document.addEventListener('DOMContentLoaded', function () {
  if (window.myFullCalendar) {
    return;
  }
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
    },
    initialView: 'dayGridMonth',
    events: JSON.parse('{{ tasks_json | escapejs }}'),
    eventContent: function (arg) {
      // Create an element to display within the event with custom HTML
      var innerHtml = `<div class='fc-event-title'><span>${arg.event.title}</span></div>`;
      var arrayOfDomNodes = [document.createRange().createContextualFragment(innerHtml)];
      return { domNodes: arrayOfDomNodes };
    },
    eventDidMount: function (info) {
      // Dynamically set color based on progress
      var status = info.event.extendedProps.status; // Progress percentage
      var color = getStatusColor(status); // Function call to determine color
      info.el.style.backgroundColor = color;

      // Update tooltip content
      var tooltipContent = `${info.event.extendedProps.description}<br>Progress: ${status}%`;
      $(info.el).tooltip({
        title: tooltipContent,
        placement: 'top',
        trigger: 'hover',
        container: 'body',
        html: true
      });
    },
    windowResize: function (view) {
      if (window.innerWidth < 600) {
        calendar.changeView('listMonth'); // Using 'listMonth' view for very small screens
      } else if (window.innerWidth < 768) {
        calendar.changeView('timeGridDay'); // Using 'timeGridDay' view for medium-small screens
      } else {
        calendar.changeView('dayGridMonth'); // Default view for larger screens
      }
    }
  });
  window.myFullCalendar = calendar;
  calendar.render();
});

function getStatusColor(status) {
  // Returns color based on progress percentage
  if (status < 25) {
    return '#dc3545'; // Red for low progress
  } else if (status < 50) {
    return '#ffc107'; // Yellow for medium-low progress
  } else if (status < 75) {
    return '#17a2b8'; // Blue for medium-high progress
  }
  return '#28a745'; // Green for completed tasks or high progress
}