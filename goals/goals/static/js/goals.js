$(function() {
    console.log('hello');
    $('td.trackBox').click(function() {
        var goal_name = $(this).data('name');
        var goal_date = $(this).data('date');
        console.log(goal_name, goal_date);
    });
});
