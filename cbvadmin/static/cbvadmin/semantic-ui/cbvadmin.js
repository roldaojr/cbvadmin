var calendarFormatter = {
  datetime: function (datetime, settings) {
    if (!datetime) return '';
    var isTimeOnly = settings.type === 'time';
    var isDateOnly = settings.type.indexOf('time') < 0;
    if (isDateOnly) {
      return moment(datetime).format('L');
    }
    if (isTimeOnly) {
      return moment(datetime).format('LT');
    }
    return moment(datetime).format('L LT');
  }
}
$('.field > .dateinput').parent().addClass('ui calendar').calendar({
    type: 'date', formatter: calendarFormatter
})
$('.field > .datetimeinput').parent().addClass('ui calendar').calendar({
    formatter: calendarFormatter
})
$('.field > .timeinput').parent().addClass('ui calendar').calendar({
    type: 'time', formatter: calendarFormatter
})

$('#sidebar-toggle').click(function(){$('.ui.sidebar').sidebar('toggle')})
