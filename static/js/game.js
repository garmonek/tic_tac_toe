const url = '/ajax'

function post(json){
    $.ajax({
      url: url,
      type: 'POST',
      dataType:'json',
      contentType: 'application/json',
      data:JSON.stringify(json),
      success: function(result){
        renderGame(result);
    },
      error: function(err, s , exception){
          console.log(exception);
      }
  });
}

$(document).ready(function(){
    post({'cmd':'init'});
});

function renderGame(result) {
	renderBoards(result);
	renderErrors(result);
}

function renderErrors(result){
	const errors = result.violations.messages;
	$('#errors').empty();
	errors.forEach((error) => {
		$('#errors').append(`<p class='error'>${translate(error, pl)}</p>`);
	});
}

function renderBoards(result){
	const boards = result.boards.boards || null;
	const activeBoardId = result.activeBoardId;
	boards.forEach((board) => {
		selectActiveBoard(board, activeBoardId);
		renderFields(board);
	});
}

function selectActiveBoard(board, activeBoardId) {
	const id = createBoardId(board);
	$(id).removeClass('activeBoard');
	if (board.id === activeBoardId) {
		$(id).addClass('activeBoard');
	}
}

function renderFields(board) {
	board.fields.forEach((field) => {
		const id = createFieldId(board.id, field.x, field.y);
		$(id).empty();
		$(id).off('click');

		if (field.mark === 'X' || field.mark === 'O') {
			$(id).append(field.mark);
		}
		$(id).bind('click', () => post(createMove(board, field)));
	});
}

function createBoardId(board) {
	return `#board${board.id}`;
}

function createFieldId(boardId, x, y){
	return `#board${boardId}_X${x}_Y${y}`;
}

function createMove(board, field){
	return {'cmd':'move', 'move':{'boardId':board.id, 'x':field.x, 'y':field.y}};
}

function translate(key, object) {
	return object[key] || null;
}

const pl = {
	'cant_mark_inactive_board': 'Nie możesz zaznaczyć nieaktywnej planszy',
	'field_out_of_board': 'Zarządano zaznaczenia ruchu z poza planszy',
	'board_already_winned': 'Nie możesz zaznaczyć już wygranej planszy',
	'no_such_board': 'Nie planszy o tym id',
	'field_already_marked': 'Nie można zaznaczyć już zaznaczonego pola!'
};