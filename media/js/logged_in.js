$(document).ready(function(){

  // hide any messages that may have popped up
	$('.messages li').delay(15000).slideUp('slow');

  // hide completed tasks, toggle if title is clicked
	$('ul.tasklist.completed').hide();
  $('.completed_toggle').click(function(){
	  $('ul.tasklist.completed').slideToggle('slow');
  });
  
  
	$('.add_task_inline form').hide();
  $('.add_task_inline a.toggle').click(function(event){
    event.preventDefault();
    $('.add_task_inline a.toggle').hide();
	  $('.add_task_inline form').show();
	  $('.add_task_inline form input#id_title').focus();
	  return false;
	});
  	
});

jQuery(document).bind('keydown', 'Ctrl+c',function (evt){
  $('.add_task_inline a.toggle').hide();
  $('.add_task_inline form').show();
  $('.add_task_inline form input#id_title').focus();
  return false;
});
