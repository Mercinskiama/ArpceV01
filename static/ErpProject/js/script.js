$(document).ready(function(){

	$("#btn-kanban").click(function(){
		$("#kanban-view").removeClass('erp-hidden');
		
		$("#tree-view").removeClass('erp-hidden');
		$("#tree-view").addClass('erp-hidden');		
	});

	$("#btn-tree").click(function(){
		$("#tree-view").removeClass('erp-hidden');
		
		$("#kanban-view").removeClass('erp-hidden');
		$("#kanban-view").addClass('erp-hidden');					
	});
});