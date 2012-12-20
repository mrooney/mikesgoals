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
    $.get('/api/check', {action: action, id: id, date: date, breaker: Math.random()})
        .success(function() {
        })
        .error(goals.on_error);
}

goals.increment = function() {
    var element = $(this);
    var img = $('<div class="check"></div>');
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
    //var name = prompt("Goal name");
    //if (!name) { return; }
    //var frequency = prompt("Frequency", 1);
    //if (!frequency) { return; }
    $('div#new_goal').slideDown();
    $("input[type='button']").click(function(){$('div#new_goal').slideUp();})
    $('form').submit(function(){
        var n = $("input[name='name']")
        if($.trim(n.val()).length == 0){ n.css({'border':'1px solid red'})}
        else{
          n.css({'border':'1px solid #DDDDDD'});
         $.get('/api/goal_new',$('form').serialize(), function(){$('div#new_goal').slideUp()})
         .error(goals.on_error)
         .success(goals.reload);
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


$(function() {
    $('td.trackBox').click(goals.increment);
    $('td.trackBox').on('click', '.check', goals.decrement);
    $('td.goalTitle span.name').click(goals.edit);
    $('td.goalTitle span.delete').click(goals.delete);
    $('a.newGoal').click(goals.new);

    // Figure out how many milliseconds until midnight, when we'll reload.
    var tomorrow = new Date();
    tomorrow.setTime(tomorrow.getTime() + 60*60*24*1000);
    tomorrow.setHours(0);
    tomorrow.setMinutes(0);
    tomorrow.setSeconds(0);
    var millisecondsToTomorrow = tomorrow - (new Date());
    // Set a timeout to reload at midnight, and at that point reload every 24h.
    setTimeout(function() {
        window.location.reload();
        setInterval(window.location.reload, 60*60*24*1000);
    }, millisecondsToTomorrow);
});
