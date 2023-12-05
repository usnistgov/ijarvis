/*
* Full calender - Page
*/
$(function() {

  /* initialize the external events
  -----------------------------------------------------------------*/
  $('#external-events .fc-event').each(function() {

    // store data so the calendar knows to render an event upon drop
    $(this).data('event', {
      title: $.trim($(this).text()), // use the element's text as the event title
      stick: true, // maintain when user navigates (see docs on the renderEvent method)
      color: '#00bcd4'
    });

    // make the event draggable using jQuery UI
    $(this).draggable({
      zIndex: 999,
      revert: true, // will cause the event to go back to its
      revertDuration: 0 //  original position after the drag
    });

  });


  /* initialize the calendar
  -----------------------------------------------------------------*/
  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'basicDay,basicWeek,month'
    },
    defaultDate: '2018-08-07',
    editable: false,
    droppable: false, // this allows things to be dropped onto the calendar
    eventLimit: true, // allow "more" link when too many events
    events: [{
        title: 'Registration|badging',
        start: '2018-08-07T08:00:00',
        end: '2018-08-07T08:30:00',
        color: 'grey'
      },
      {
        title: 'Francesca Tavazza - Welcome note',
        start: '2018-08-07T08:30:00',
        end: '2018-08-07T08:40:00',
        color: 'blue'
      },
      {
        title: 'James Warren - NIST, [MGI and AI]',
        start: '2018-08-07T08:40:00',
        end: '2018-08-07T09:00:00',
        color: 'blue'
      },
      {
        title: 'Krishna Rajan - University at Buffalo, [AI for Discovering Materials Design Pathways]',
        start: '2018-08-07T09:00:00',
        end: '2018-08-07T09:30:00',
        color: 'green'
      },
      {
        title: 'Caleb Phillips - NREL, [Applications of Machine Learning for Materials Discovery using the NREL High Throughput Experimental Materials Database]',
        start: '2018-08-07T09:30:00',
        end: '2018-08-07T10:00:00',
        color: 'green'
      },
      {
        title: 'Break',
        start: '2018-08-07T10:00:00',
        end: '2018-08-07T10:30:00',
        color: 'grey'
      }
    ]
  });

});
