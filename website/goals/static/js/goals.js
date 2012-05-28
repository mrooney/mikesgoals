goals = {}

goals.on_error = function() {
    alert('Alas, an error has occurred.');
}

goals.reload = function() {
    window.location.reload();
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
    var element = $(this).parent();
    var id = element.data('goal-id');
    var name = element.data('goal-name');

    var new_name = prompt("Goal name", name);
    if (new_name) {
        $.get('/api/goal_edit', {goal: id, name: new_name})
            .error(goals.on_error)
            .success(goals.reload);
    }
}

goals.new = function(event) {
    var name = prompt("Goal name");
    if (!name) { return; }
    var frequency = prompt("Frequency", 1);
    if (!frequency) { return; }
    $.get('/api/goal_new', {name: name, frequency: frequency})
        .error(goals.on_error)
        .success(goals.reload);
}

goals.delete = function(event) {
    var element = $(this).parent();
    if (confirm("Are you sure you want to delete this goal?")) {
        $.get('/api/goal_delete', {goal: element.data('goal-id')})
            .error(goals.on_error)
            .success(goals.reload);
    }
}


$(function() {
    $('td.trackBox').click(goals.increment);
    $('td.trackBox').on('click', '.checkbox', goals.decrement);
    $('td.goalTitle span.name').click(goals.edit);
    $('td.goalTitle span.delete').click(goals.delete);
    $('a.newGoal').click(goals.new);
});
