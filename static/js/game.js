const url = '/ajax';
const MESSAGE_DIV_ID = '#messages';
const GAME_WINNED_KEY = 'game_winned';

function post(json){
    $.ajax({
      url: url,
      type: 'POST',
      dataType:'json',
      contentType: 'application/json',
      data:JSON.stringify(json),
      success: (result) => renderGame(result),
      error: (err, s , exception) => console.log(exception),
  });
}

$(document).ready(function(){
    post({'cmd':'init'});
});

function renderGame(result) {
	console.log(result);
	$(MESSAGE_DIV_ID).empty();
	renderWinner(result)
	renderBoards(result);
	renderErrors(result);
}

function renderWinner(result) {
	if (result.winner !== null) {
		const translatedError = `<p class='success'>${translate(GAME_WINNED_KEY, pl)}${result.winner._value_}</p>`;
		if (translatedError !== null) {
			$(MESSAGE_DIV_ID).append(translatedError);	
		}
	}
}

function renderErrors(result){
	const errors = result.violations.messages;
	errors.forEach((error) => {
		const translatedError = `<p class='error'>${translate(error, pl)}</p>`;
		if (translatedError !== null) {
			$(MESSAGE_DIV_ID).append(translatedError);
		}
	});
}

function renderBoards(result){
	const boards = result.boards.boards || null;
	const activeBoardId = result.activeBoardId;
	boards.forEach((board) => {
		markWinnedBoard(board);
		selectActiveBoard(board, activeBoardId);
		renderFields(board);
	});
}

function markWinnedBoard(board) {
	const htmlBoardId = createBoardId(board);
	const winner = board.winner ? board.winner._value_ : null;
	$(htmlBoardId).removeClass('X', 'Y');
	if (winner) {
		$(htmlBoardId).addClass(winner);
	}
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
		$(id).bind('click',() => post(createMove(board, field)));
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
	'cant_mark_inactive_board': 'Nie możesz zaznaczyć nieaktywnej planszy!',
	'field_already_marked': 'Nie możesz zaznaczyć już zaznaczonego pola!',
	'field_out_of_board': 'Zarządano zaznaczenia pola z poza planszy',
	'no_such_board': 'Nie ma planszy o tym id',
	'board_already_winned': 'Nie możesz zaznaczyć już wygranej planszy, zaznacz dowolną inną',
	'game_winned': 'Grę wygrywa '
};