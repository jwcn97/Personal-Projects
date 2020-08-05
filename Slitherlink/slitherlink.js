var grid = document.getElementById('puzzle_table');
var states = [];
var hints = [];
var rows = 18;
var columns = 10;

function create() {
  var row, column;
  for (row = 0; row < rows; row++) {
    states.push([[],[]]);
    hints.push([]);
    for (column = 0; column < columns; column++) {
      states[row][0].push(-1);
      states[row][1].push(-1);
      hints[row].push(-1);
    }
    states[row][1].push(-1);
  }
  states.push([[]]);
  for (column = 0; column < columns; column++) states[row][0].push(-1);

  /* HINTS */
  hints[0][1] = 3; hints[0][2] = 1; hints[0][4] = 1; hints[0][5] = 1; hints[0][7] = 0; hints[0][8] = 2;
  hints[1][0] = 3; hints[1][3] = 3; hints[1][6] = 2; hints[1][9] = 1;
  hints[2][0] = 3; hints[2][3] = 3; hints[2][6] = 3; hints[2][9] = 1;
  hints[3][1] = 2; hints[3][2] = 2; hints[3][4] = 1; hints[3][5] = 3; hints[3][7] = 0; hints[3][8] = 3;
  hints[5][0] = 2; hints[5][1] = 3; hints[5][2] = 3; hints[5][3] = 1; hints[5][6] = 2; hints[5][7] = 3; hints[5][8] = 2; hints[5][9] = 3;
  hints[6][4] = 3; hints[6][5] = 1;
  hints[7][0] = 1; hints[7][1] = 0; hints[7][2] = 1; hints[7][7] = 0; hints[7][8] = 1; hints[7][9] = 2;
  hints[8][1] = 1; hints[8][4] = 1; hints[8][5] = 3; hints[8][8] = 2;
  hints[9][1] = 3; hints[9][4] = 1; hints[9][5] = 3; hints[9][8] = 0;
  hints[10][0] = 3; hints[10][1] = 1; hints[10][2] = 0; hints[10][7] = 2; hints[10][8] = 2; hints[10][9] = 1;
  hints[11][4] = 2; hints[11][5] = 0;
  hints[12][0] = 1; hints[12][1] = 2; hints[12][2] = 3; hints[12][3] = 3; hints[12][6] = 1; hints[12][7] = 0; hints[12][8] = 1; hints[12][9] = 1;
  hints[14][1] = 0; hints[14][2] = 3; hints[14][4] = 3; hints[14][5] = 1; hints[14][7] = 3; hints[14][8] = 1;
  hints[15][0] = 1; hints[15][3] = 2; hints[15][6] = 0; hints[15][9] = 3;
  hints[16][0] = 2; hints[16][3] = 1; hints[16][6] = 3; hints[16][9] = 1;
  hints[17][1] = 3; hints[17][2] = 3; hints[17][4] = 1; hints[17][5] = 1; hints[17][7] = 2; hints[17][8] = 3;
}

function display() {
  var row, col;
  var space = "&nbsp&nbsp&nbsp&nbsp";

  grid.innerHTML = "";
  for (row = 0; row < rows; row++) {
    for (col = 0; col < columns; col++) {
      //draw box
      if (hints[row][col] === -1) grid.innerHTML += ("<div class='boxes'>" + space + "</div>");
      else grid.innerHTML += ("<div class='boxes'>&nbsp" + hints[row][col] + "&nbsp</div>");

      //draw confirmed lines
      if (states[row][1][col] === 1) grid.lastChild.style.borderLeft = '0.5px solid blue';
      if (states[row][0][col] === 1) grid.lastChild.style.borderTop = '0.5px solid blue';
      if (states[row][1][col+1] === 1) grid.lastChild.style.borderRight = '0.5px solid blue';
      if (states[row+1][0][col] === 1) grid.lastChild.style.borderBottom = '0.5px solid blue';

      //draw unsure lines
      if (states[row][1][col] === -1) grid.lastChild.style.borderLeft = '0.5px solid red';
      if (states[row][0][col] === -1) grid.lastChild.style.borderTop = '0.5px solid red';
      if (states[row][1][col+1] === -1) grid.lastChild.style.borderRight = '0.5px solid red';
      if (states[row+1][0][col] === -1) grid.lastChild.style.borderBottom = '0.5px solid red';

      //draw non-existent lines
      if (states[row][1][col] === 0) grid.lastChild.style.borderLeft = '0.5px solid white';
      if (states[row][0][col] === 0) grid.lastChild.style.borderTop = '0.5px solid white';
      if (states[row][1][col+1] === 0) grid.lastChild.style.borderRight = '0.5px solid white';
      if (states[row+1][0][col] === 0) grid.lastChild.style.borderBottom = '0.5px solid white';
    }
    grid.innerHTML += "<br>";
  }
}

function check() {
  var row, col, counter;
  for (row = 0; row < rows; row++) {
    for (col = 0; col < columns; col++) {
      /* REMOVE UNCERTAINTY */
      counter = 0;
      if (states[row][1][col] === 1) counter++;
      if (states[row][0][col] === 1) counter++;
      if (states[row][1][col+1] === 1) counter++;
      if (states[row+1][0][col] === 1) counter++;
      if (counter === hints[row][col]) {
        if (states[row][1][col] === -1) states[row][1][col] = 0;
        if (states[row][0][col] === -1) states[row][0][col] = 0;
        if (states[row][1][col+1] === -1) states[row][1][col+1] = 0;
        if (states[row+1][0][col] === -1) states[row+1][0][col] = 0;
      }

      /* CONFIRM LINES */
      counter = 0;
      if (states[row][1][col] === 0) counter++;
      if (states[row][0][col] === 0) counter++;
      if (states[row][1][col+1] === 0) counter++;
      if (states[row+1][0][col] === 0) counter++;
      if (counter === (4-hints[row][col])) {
        if (states[row][1][col] === -1) states[row][1][col] = 1;
        if (states[row][0][col] === -1) states[row][0][col] = 1;
        if (states[row][1][col+1] === -1) states[row][1][col+1] = 1;
        if (states[row+1][0][col] === -1) states[row+1][0][col] = 1;
      }

      /* REMOVE STRAY HINT LINES */
      /* HORIZONTAL LINES */
      if (states[row][0][col] === -1) {
        //left side of horizontal line
        counter = 0;
        if (states[row][1][col] === 0) counter++;
        if (col != 0 && states[row][0][col-1] === 0) counter++;
        if (row != 0 && states[row-1][1][col] === 0) counter++;
        if ((row == 0 && counter == 2) || (row != 0 && counter == 3)) states[row][0][col] = 0;

        //right side of horizontal line
        counter = 0;
        if (states[row][1][col+1] === 0) counter++;
        if (col != 9 && states[row][0][col+1] === 0) counter++;
        if (row != 0 && states[row-1][1][col+1] === 0) counter++;
        if ((row == 0 && counter == 2) || (row != 0 && counter == 3)) states[row][0][col] = 0;
      }
      if (row == 17 && states[row+1][0][col] === -1) {
        //left side of horizontal line
        counter = 0;
        if (col != 0 && states[row+1][0][col-1] === 0) counter++;
        if (states[row][1][col] === 0) counter++;
        if (counter === 2) states[row+1][0][col] = 0;

        //right side of horizontal line
        counter = 0;
        if (col != 9 && states[row+1][0][col+1] === 0) counter++;
        if (states[row][1][col+1] === 0) counter++;
        if (counter === 2) states[row+1][0][col] = 0;
      }

      /* VERTICAL LINES */
      if (states[row][1][col+1] === -1) {
        //top side of vertical line
        counter = 0;
        if (states[row][0][col] === 0) counter++;
        if (row != 0 && states[row-1][1][col+1] === 0) counter++;
        if (col != 9 && states[row][0][col+1] === 0) counter++;
        if ((col == 9 && counter == 2) || (col != 9 && counter === 3)) states[row][1][col+1] = 0;

        //bottom side of vertical line
        counter = 0;
        if (states[row+1][0][col] === 0) counter++;
        if (row != 17 && states[row+1][1][col+1] === 0) counter++;
        if (col != 9 && states[row+1][0][col+1] === 0) counter++;
        if ((col == 9 && counter == 2) || (col != 9 && counter === 3)) states[row][1][col+1] = 0;
      }
      if (col == 0 && states[row][1][col] === -1) {
        //top side of vertical line
        counter = 0;
        if (row != 0 && states[row-1][1][col] === 0) counter++;
        if (states[row][0][col] === 0)counter++;
        if (counter === 2) states[row][1][col] = 0;

        //bottom side of vertical line
        counter = 0;
        if (row != 17 && states[row+1][1][col] === 0) counter++;
        if (states[row+1][0][col] === 0)counter++;
        if (counter === 2) states[row][1][col] = 0;
      }
    }
  }
}

function hint_zero_corner(row, col) {
  if (row != 0) {
    //top left
    if (col != 0) {
      switch(hints[row-1][col-1]) {
        case 1:
          states[row-1][1][col] = 0;
          states[row][0][col-1] = 0;
          break;
        case 2:
          if (states[row][0][col-1] === 0 || states[row-1][1][col] === 0) {
            states[row-1][0][col-1] = 1;
            states[row-1][1][col-1] = 1;
          }
          if (states[row-1][0][col-1] === 0 || states[row-1][1][col-1] === 0) {
            states[row][0][col-1] = 1;
            states[row-1][1][col] = 1;
          }
          break;
        case 3:
          states[row-1][1][col] = 1;
          states[row][0][col-1] = 1;
          break;
      }
    }
    //top right
    if (col != 9) {
      switch(hints[row-1][col+1]) {
        case 1:
          states[row-1][1][col+1] = 0;
          states[row][0][col+1] = 0;
          break;
        case 2:
          if (states[row][0][col+1] === 0 || states[row-1][1][col+1] === 0) {
            states[row-1][0][col+1] = 1;
            states[row-1][1][col+2] = 1;
          }
          if (states[row-1][0][col+1] === 0 || states[row-1][1][col+2] === 0) {
            states[row][0][col+1] = 1;
            states[row-1][1][col+1] = 1;
          }
          break;
        case 3:
          states[row-1][1][col+1] = 1;
          states[row][0][col+1] = 1;
          break;
      }
    }
  }
  if (row != 17) {
    //bottom left
    if (col != 0) {
      switch(hints[row+1][col-1]) {
        case 1:
          states[row+1][0][col-1] = 0;
          states[row+1][1][col] = 0;
          break;
        case 2:
          if (states[row+1][0][col-1] === 0 || states[row+1][1][col] === 0) {
            states[row+2][0][col-1] = 1;
            states[row+1][1][col-1] = 1;
          }
          if (states[row+2][0][col-1] === 0 || states[row+1][1][col-1] === 0) {
            states[row+1][0][col-1] = 1;
            states[row+1][1][col] = 1;
          }
          break;
        case 3:
          states[row+1][0][col-1] = 1;
          states[row+1][1][col] = 1;
          break;
      }
    }
    //bottom right
    if (col != 9) {
      switch(hints[row+1][col+1]) {
        case 1:
          states[row+1][0][col+1] = 0;
          states[row+1][1][col+1] = 0;
          break;
        case 2:
          if (states[row+1][0][col+1] === 0 || states[row+1][1][col+1] === 0) {
            states[row+2][0][col+1] = 1;
            states[row+1][1][col+2] = 1;
          }
          if (states[row+2][0][col+1] === 0 || states[row+1][1][col+2] === 0) {
            states[row+1][0][col+1] = 1;
            states[row+1][1][col+1] = 1;
          }
          break;
        case 3:
          states[row+1][0][col+1] = 1;
          states[row+1][1][col+1] = 1;
          break;
      }
    }
  }
}

function hint_zero_edge(row, col) {
  if (col != 0 && col != 9) {
    if (row == 0) {
      states[row][0][col-1] = 0;
      states[row][0][col+1] = 0;
    }
    if (row == 17) {
      states[row+1][0][col-1] = 0;
      states[row+1][0][col+1] = 0;
    }
  }
  if (row != 0 && row != 17) {
    if (col == 0) {
      states[row-1][1][col] = 0;
      states[row+1][1][col] = 0;
    }
    if (col == 9) {
      states[row-1][1][col+1] = 0;
      states[row+1][1][col+1] = 0;
    }
  }
}

function hint_pair_three(row, col) {
  if (col != 9) {
    //top right
    if (row != 0 && hints[row-1][col+1] === 3) {
      states[row][1][col] = 1;
      states[row+1][0][col] = 1;
      states[row-1][0][col+1] = 1;
      states[row-1][1][col+2] = 1;
      //special: top left corner pair
      if (row == 1 && col == 0) {
        states[row][0][col] = 1;
        states[row-1][1][col+1] = 1;
      }
      //special: bottom right corner pair
      if (row == 17 && col == 8) {
        states[row][1][col+1] = 1;
        states[row][0][col+1] = 0;
      }
    }
    //right
    if (hints[row][col+1] === 3) {
      states[row][1][col] = 1;
      states[row][1][col+1] = 1;
      states[row][1][col+2] = 1;
    }
    //bottom right
    if (row != 17 && hints[row+1][col+1] === 3) {
      states[row][1][col] = 1;
      states[row][0][col] = 1;
      states[ro+1][1][col+2] = 0;
      states[row+2][0][col+1] = 0;
      //special: top right corner pair
      if (row == 0 && col == 8) {
        states[row][1][col+1] = 1;
        states[row+1][0][col+1] = 1;
      }
      //special: bottom left corner pair
      if (row == 16 && col == 0) {
        states[row+1][0][col] = 0;
        states[row+1][1][col+1] = 0;
      }
    }
  }
  //bottom
  if (row != 17) {
    if (hints[row+1][col] === 3) {
      states[row][0][col] = 1;
      states[row+1][0][col] = 1;
      states[row+2][0][col] = 1;
    }
  }
}

function hint_three_corner(row, col) {
  //top left
  if ((row != 0 && states[row-1][1][col] === 1) || (col != 0 && states[row][0][col-1] === 1)) {
    states[row][1][col+1] = 1;
    states[row+1][0][col] = 1;
  }
  //top right
  if ((row != 0 && states[row-1][1][col+1] === 1) || (col != 9 && states[row][0][col+1] === 1)) {
    states[row][1][col] = 1;
    states[row+1][0][col] = 1;
  }

  //bottom left
  if ((col != 0 && states[row+1][0][col-1] === 1) || (row != 17 && states[row+1][1][col] === 1)) {
    states[row][0][col] = 1;
    states[row][1][col+1] = 1;
  }
  //bottom right
  if ((col != 9 && states[row+1][0][col+1] === 1) || (row != 17 && states[row+1][1][col+1] === 1)) {
    states[row][1][col] = 1;
    states[row][0][col] = 1;
  }
}

function preventIntersect(row, col) {
  /* CORNER LINES */
  //top left
  if (states[row][1][col] === 1 && states[row][0][col] === 1) {
    if (row != 0) states[row-1][1][col] = 0;
    if (col != 0) states[row][0][col-1] = 0;
  }
  //top right
  if (states[row][0][col] === 1 && states[row][1][col+1] === 1) {
    if (row != 0) states[row-1][1][col+1] = 0;
    if (col != 9) states[row][0][col+1] = 0;
  }
  //bottom left
  if (states[row][1][col] === 1 && states[row+1][0][col] === 1) {
    if (row != 17) states[row+1][1][col] = 0;
    if (col != 0) states[row+1][0][col-1] = 0;
  }
  //bottom right
  if (states[row][1][col+1] === 1 && states[row+1][0][col] === 1) {
    if (row != 17) states[row+1][1][col+1] = 0;
    if (col != 9) states[row+1][0][col+1] = 0;
  }

  /* STRAIGHT LINES */
  //horizontal lines
  if (col != 9 && states[row][0][col] === 1 && states[row][0][col+1] === 1) {
    if (row == 17) {
      if (states[row+1][0][col] === 1 && states[row+1][0][col+1] === 1) states[row][1][col+1] = 0;
    } else {
      if (row != 0) states[row-1][1][col+1] = 0;
      states[row][1][col+1] = 0;
    }
  }
  //vertical lines
  if (row != 17 && states[row][1][col] === 1 && states[row+1][1][col] === 1) {
    if (col == 9) {
      if (states[row][1][col+1] === 1 && states[row+1][1][col+1] === 1) states[row+1][0][col] = 0;
    } else {
      if (col != 0) states[row+1][0][col-1] = 0;
      states[row+1][0][col] = 0;
    }
  }
}

function handleDirection(row, col) {
  var array;

  /* HORIZONTAL LINES */
  if (states[row][0][col] === 1) {
    //left side of horizontal line
    array = [];
    if (states[row][1][col] === -1) array.push(row, 1, col);
    if (col != 0 && states[row][0][col-1] === -1) array.push(row, 0, col-1);
    if (row != 0 && states[row-1][1][col] === -1) array.push(row-1, 1, col);
    if (states[row][1][col] === 1 || (col != 0 && states[row][0][col-1] === 1) || (row != 0 && states[row-1][1][col] === 1)) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;

    //right side of horizontal line
    array = [];
    if (states[row][1][col+1] === -1) array.push(row, 1, col+1);
    if (col != 9 && states[row][0][col+1] === -1) array.push(row, 0, col+1);
    if (row != 0 && states[row-1][1][col+1] === -1) array.push(row-1, 1, col+1);
    if (states[row][1][col+1] === 1 || (col != 9 && states[row][0][col+1] === 1) || (row != 0 && states[row-1][1][col+1] === 1)) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;
  }
  if (row == 17 && states[row+1][0][col] === 1) {
    //left side of horizontal line
    array = [];
    if (col != 0 && states[row+1][0][col-1] === -1) array.push(row+1, 0, col-1);
    if (states[row][1][col] === -1) array.push(row, 1, col);
    if ((col != 0 && states[row+1][0][col-1] === 1) || states[row][1][col] === 1) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;

    //right side of horizontal line
    array = [];
    if (col != 9 && states[row+1][0][col+1] === -1) array.push(row+1, 0, col+1);
    if (states[row][1][col+1] === -1) array.push(row, 1, col+1);
    if ((col != 9 && states[row+1][0][col+1] === 1) || states[row][1][col+1] === 1) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;
  }

  /* VERTICAL LINES */
  if (states[row][1][col+1] === 1) {
    //top side of vertical line
    array = [];
    if (states[row][0][col] === -1) array.push(row, 0, col);
    if (row != 0 && states[row-1][1][col+1] === -1) array.push(row-1, 1, col+1);
    if (col != 9 && states[row][0][col+1] === -1) array.push(row, 0, col+1);
    if (states[row][0][col] === 1 || (row != 0 && states[row-1][1][col+1] === 1) || (col != 9 && states[row][0][col+1] === 1)) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;

    //bottom side of vertical line
    array = [];
    if (states[row+1][0][col] === -1) array.push(row+1, 0, col);
    if (row != 17 && states[row+1][1][col+1] === -1) array.push(row+1, 1, col+1);
    if (col != 9 && states[row+1][0][col+1] === -1) array.push(row+1, 0, col+1);
    if (states[row+1][0][col] === 1 || (row != 17 && states[row+1][1][col+1] === 1) || (col != 9 && states[row+1][0][col+1] === 1)) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;
  }
  if (col == 0 && states[row][1][col] === 1) {
    //top side of vertical line
    array = [];
    if (row != 0 && states[row-1][1][col] === -1) array.push(row-1, 1, col);
    if (states[row][0][col] === -1) array.push(row, 0, col);
    if ((row != 0 && states[row-1][1][col] === 1) || states[row][0][col] === 1) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;

    //bottom side of vertical line
    array = [];
    if (row != 17 && states[row+1][1][col] === -1) array.push(row+1, 1, col);
    if (states[row+1][0][col] === -1) array.push(row+1, 0, col);
    if ((row != 17 && states[row+1][1][col] === 1) || states[row+1][0][col] === 1) array = [];
    if (array.length === 3) states[array[0]][array[1]][array[2]] = 1;
  }
}

function navigate() {
  var row, col;
  for (row = 0; row < rows; row++) {
    for (col = 0; col < columns; col++) {
      if (hints[row][col] === 0) {
        states[row][1][col] = 0;
        states[row][0][col] = 0;
        states[row][1][col+1] = 0;
        states[row+1][0][col] = 0;
        hint_zero_corner(row, col);
        hint_zero_edge(row, col);
      }

      if (hints[row][col] === 3) {
        hint_pair_three(row, col);
        hint_three_corner(row, col);
      }

      preventIntersect(row, col);
      handleDirection(row, col);
    }
  }
}

function solve() {
  var i;
  for (i = 0; i < 15; i++) {
    check();
    navigate();
  }
  display();
}

create();display();
