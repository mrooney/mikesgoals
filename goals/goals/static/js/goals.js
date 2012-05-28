goals = {}

goals.on_error = function() {
    alert('Alas, an error has occurred.');
}

goals.api = function(action, element) {
    var id = element.data('goal-id');
    var date = element.data('goal-date');
    $.get('/api/check', {action: action, id: id, date: date})
        .success(function() {
        })
        .error(goals.on_error);
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

goals.edit = function(event) {
    var element = $(this);
    var id = element.data('goal-id');
    var name = element.data('goal-name');

    var new_name = prompt("Goal name", name);
    if (new_name) {
        $.get('/api/goal_edit', {goal: id, name: new_name})
            .success(function() {
                window.location.reload();
            })
            .error(goals.on_error);
    }
}


$(function() {
    $('td.trackBox').click(goals.increment);
    $('td.trackBox').on('click', '.checkbox', goals.decrement);
    $('td.goalTitle').click(goals.edit);
});
