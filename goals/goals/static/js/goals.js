goals = {}

goals.api = function(action, element) {
    var id = element.data('goal-id');
    var date = element.data('goal-date');
    $.get('/api/check', {action: action, id: id, date: date})
        .success(function() {
        })
        .error(function() {
            alert('Alas, an error has occurred.');
        });
}

goals.increment = function() {
    var element = $(this);
    var img = $('<div class="checkbox"></div>');
    img.appendTo(element);
    goals.api('increment', element);
}

goals.decrement = function(event) {
    var element = $(this);
    event.stopPropagation();
    var parent = element.parent();
    element.remove();
    goals.api('decrement', parent);
}

$(function() {
    $('td.trackBox').click(goals.increment);
    $('td.trackBox').on('click', '.checkbox', goals.decrement);
});
