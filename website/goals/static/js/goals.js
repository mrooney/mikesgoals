Date.prototype.getDOY = function() {
    var onejan = new Date(this.getFullYear(),0,1);
    return Math.ceil((this - onejan) / 86400000);
}

goals.on_error = function() {
    alert('Alas, an error has occurred. Please log out and back in again.');
    _gaq.push(['_trackEvent', 'api', 'error']);
}

goals.reload = function() {
    window.location.reload();
}

goals.api = function(action, element) {
    if (!goals.is_authenticated) { return; }
    var id = element.data('goal-id');
    var date = element.data('goal-date');
    $.get('/api/check', {action: action, id: id, date: date, breaker: Math.random()})
        .success(function() {
            _gaq.push(['_trackEvent', 'api', action]);
        })
        .error(goals.on_error);
}

goals.increment = function() {
    var box = $(this);
    var img = $('<div class="check"></div>');
    img.appendTo(box.find('.checkWrapper'));
    goals.api('increment', box);
    return false;
}

goals.decrement = function(event) {
    event.stopPropagation();
    var element = $(this);
    var box = element.parent().parent();
    element.remove();
    goals.api('decrement', box);
    return false;
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
    $('div#new_goal').slideDown();
    $('div#new_goal input[name=name]').focus();
    $("input[type='button']").click(function(){$('div#new_goal').slideUp();})
    $('form').submit(function(){
        var n = $("input[name='name']")
        if($.trim(n.val()).length == 0){ n.css({'border':'1px solid red'})}
        else {
            n.css({'border':'1px solid #DDDDDD'});
            $.get('/api/goal_new',$('form').serialize(), function(){$('div#new_goal').slideUp()})
                .error(goals.on_error)
                .success(function() {
                    _gaq.push(['_trackEvent', 'api', 'new']);
                    goals.reload();
                });
        }
 return false
 })
}
 

goals.delete = function(event) {
    var element = $(this).parent();
    if (confirm("Are you sure you want to delete this goal?")) {
        $.get('/api/goal_delete', {goal: element.data('goal-id')})
            .error(goals.on_error)
            .success(goals.reload);
    }
}

goals.reload_if_new_day = function() {
    if (new Date().getDOY() != goals.today) {
        goals.reload();
    }
}

$(function() {
    goals.today = new Date().getDOY();
    $('td.trackBox').on('click', goals.increment);
    $('td.trackBox').on('click', '.check', goals.decrement);
    $('td.goalTitle span.name').click(goals.edit);
    $('td.goalTitle span.delete').click(goals.delete);
    $('a.newGoal').click(goals.new);
    $(window).on('focus', goals.reload_if_new_day);
});
