var grid = document.getElementById("puzzle_table");
var puzzle = [];
var grid_size = 3;

function createPuzzle() {
  var row, col;
  for (row = 0; row < grid_size**2; row++) {
    puzzle.push([]);
    for (col = 0; col < grid_size**2; col++) {
      puzzle[row].push([]);
    }
  }

  /* CLUES */
  puzzle[0][2] = 4
  puzzle[1][2] = 3; puzzle[1][3] = 5; puzzle[1][7] = 1; puzzle[1][8] = 6;
  puzzle[2][4] = 1; puzzle[2][7] = 9;
  puzzle[3][3] = 1; puzzle[3][5] = 6; puzzle[3][7] = 7;
  puzzle[4][2] = 2; puzzle[4][4] = 4; puzzle[4][6] = 3;
  puzzle[5][1] = 7; puzzle[5][3] = 3; puzzle[5][5] = 8;
  puzzle[6][1] = 4; puzzle[6][4] = 9;
  puzzle[7][0] = 9; puzzle[7][1] = 5; puzzle[7][5] = 2; puzzle[7][6] = 7;
  puzzle[8][6] = 2;
}

function displayPuzzle() {
  var row, col;
  var space = "&nbsp&nbsp&nbsp&nbsp";

  grid.innerHTML = "";
  for (row = 0; row < grid_size**2; row++) {
    if (row % 3 == 0 && row != 0) grid.innerHTML += "<br>";
    for (col = 0; col < grid_size**2; col++) {
      if (col % 3 == 0 && col != 0) grid.innerHTML += "&nbsp&nbsp";
      if (typeof(puzzle[row][col]) == "object") grid.innerHTML += ("<div class='boxes'>" + space + "</div>");
      else grid.innerHTML += ("<div class='boxes'>&nbsp" + puzzle[row][col] + "&nbsp</div>");
    }
    grid.innerHTML += "<br>";
  }
}

function checkFinish() {
  var row, col;
  for (row = 0; row < puzzle.length; row++) {
    for (col = 0; col < puzzle.length; col++) {
      if (typeof(puzzle[row][col]) == "object") return 0;
    }
  }
  return 1;
}

function checkRepeat(num, row, col) {
  var i, j;
  var row_index = Math.floor(row/grid_size)*grid_size;
  var col_index = Math.floor(col/grid_size)*grid_size;
  //check horizontally and vertically
  for (i = 0; i < puzzle.length; i++) {
    if (num === puzzle[row][i] || num === puzzle[i][col]) return 1;
  }
  //check box
  for (i = 0; i < grid_size; i++) {
    for (j = 0; j < grid_size; j++) {
      if (num === puzzle[i+row_index][j+col_index]) return 1;
    }
  }
  //if there is no repeat, return 0
  return 0;
}

function fill() {
  var number, row, column;
  for (row = 0; row < puzzle.length; row++) {
    for (column = 0; column < puzzle.length; column++) {
      //navigate through rows and columns
      if (typeof(puzzle[row][column]) == "number") continue;
      //insert candidates into empty spaces
      for (number = 1; number <= puzzle.length; number++) {
        if (checkRepeat(number, row, column) == 0) puzzle[row][column].push(number);
      }
      //remove singletons
      if (puzzle[row][column].length == 1) puzzle[row][column] = puzzle[row][column][0];
    }
  }
}

/* REMOVE UNWANTED CANDIDATES */
function removeCandidates() {
  var i, row, column;
  for (column = 0; column < puzzle.length; column++) {
    for (row = 0; row < puzzle.length; row++) {
      //navigate through rows and columns
      if (typeof(puzzle[row][column]) == "object") {
        //if cell consists of candidates, loop through candidates
        for (i = 0; i < puzzle[row][column].length; i++) {
          //remove candidates if repeated
          if (checkRepeat(puzzle[row][column][i], row, column) == 1) {
            puzzle[row][column].splice(i, 1);
          }
        }
        //remove singletons
        if (puzzle[row][column].length == 1) puzzle[row][column] = puzzle[row][column][0];
      }
    }
  }
}

function handleOverlap(number, box, line, status) {
  var i, j, k;
  var array = [];
  var line_multiple = Math.floor(line[0]/grid_size)*grid_size;

  switch(box.length) {
    case 1:
      var box_arr = [0, 1, 2];
      var line_arr = [0, 1, 2];
      box_arr.splice(Math.floor(box[0]/grid_size), 1);
      line_arr.splice((line[0] % grid_size), 1);
      for (i = 0; i < box_arr.length; i++) {
        box_arr[i] *= grid_size;
        line_arr[i] += line_multiple;
      }

      for (i = 0; i < box_arr.length; i++) {
        for (j = 0; j < line_arr.length; j++) {
          for (k = 0; k < grid_size; k++) {
            if (status == "across rows") {
              if (typeof(puzzle[line_arr[j]][k+box_arr[i]]) == "object") {
                if (checkRepeat(number, line_arr[j], k+box_arr[i]) == 0) array.push(line_arr[j], k+box_arr[i]);
              }
            } else if (status == "across columns") {
              if (typeof(puzzle[k+box_arr[i]][line_arr[j]]) == "object") {
                if (checkRepeat(number, k+box_arr[i], line_arr[j]) == 0) array.push(k+box_arr[i], line_arr[j]);
              }
            }
          }
        }
        if (array.length == 2) puzzle[array[0]][array[1]] = number;
      }
      break;
    case 2:
      var box_index = grid_size;
      var line_index = grid_size;

      for (i = 0; i < box.length; i++) {
        box_index -= Math.floor(box[i]/grid_size);
        line_index -= (line[i] % grid_size);
      }
      box_index *= grid_size;
      line_index += line_multiple;

      for (i = 0; i < grid_size; i++) {
        if (status == "across rows") {
          if (typeof(puzzle[line_index][i+box_index]) == "object") {
            if (checkRepeat(number, line_index, i+box_index) == 0) array.push(line_index, i+box_index);
          }
        } else if (status == "across columns") {
          if (typeof(puzzle[i+box_index][line_index]) == "object") {
            if (checkRepeat(number, i+box_index, line_index) == 0) array.push(i+box_index, line_index);
          }
        }
      }
      if (array.length == 2) puzzle[array[0]][array[1]] = number;
  }
}

function checkOverlap() {
  removeCandidates();
  var i, j, number, col, col_index, row, row_index, array;

  /* LOOP THROUGH NUMBERS */
  for (number = 1; number <= puzzle.length; number++) {
    /* NAVIGATE ACROSS ROW */
    for (row = 0; row < grid_size; row++) {
      row_index = row*grid_size;
      array = [[],[]];
      for (col = 0; col < grid_size; col++) {
        col_index = col*grid_size;
        //navigate within box
        for (i = 0; i < grid_size; i++) {
          for (j = 0; j < grid_size; j++) {
            if (number === puzzle[i+row_index][j+col_index]) {
              array[0].push(i+row_index);
              array[1].push(j+col_index);
            }
          }
        }
      }
      handleOverlap(number, array[1], array[0], "across rows");
    }

    /* NAVIGATE ACROSS COLUMN */
    for (col = 0; col < grid_size; col++) {
      col_index = col*grid_size;
      array = [[],[]];
      for (row = 0; row < grid_size; row++) {
        row_index = row*grid_size;
        //navigate within box
        for (i = 0; i < grid_size; i++) {
          for (j = 0; j < grid_size; j++) {
            if (number === puzzle[i+row_index][j+col_index]) {
              array[0].push(i+row_index);
              array[1].push(j+col_index);
            }
          }
        }
      }
      handleOverlap(number, array[0], array[1], "across columns");
    }
  }
}

function solve() {
  //fill();
  //while(checkFinish() == 0) {
    removeCandidates();
    checkOverlap();
  //}
  displayPuzzle();
}

/* INITIATION OF PUZZLE */
createPuzzle();
displayPuzzle();
fill();
