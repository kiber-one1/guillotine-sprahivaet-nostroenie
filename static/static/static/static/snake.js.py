const canvas = document.getElementById("snake-bg");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const grid = 20;

let cols = Math.floor(canvas.width / grid);
let rows = Math.floor(canvas.height / grid);

let snake = [{ x: 10, y: 10 }];

let fruits = [];

// создать фрукты
function randPos() {
    return {
        x: Math.floor(Math.random() * cols),
        y: Math.floor(Math.random() * rows)
    };
}

for (let i = 0; i < 30; i++) {
    fruits.push(randPos());
}

// расстояние
function dist(a, b) {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}

// плотность фруктов
function density(f) {
    let c = 0;
    for (let o of fruits) {
        if (dist(f, o) < 5) c++;
    }
    return c;
}

// выбор цели
function targetFruit() {
    let best = fruits[0];
    let bestScore = -1;

    for (let f of fruits) {
        let s = density(f);
        if (s > bestScore) {
            bestScore = s;
            best = f;
        }
    }
    return best;
}

let target = targetFruit();

// движение
function move() {
    let head = snake[0];

    if (!target) target = targetFruit();

    if (head.x < target.x) head.x++;
    else if (head.x > target.x) head.x--;

    if (head.y < target.y) head.y++;
    else if (head.y > target.y) head.y--;

    snake.unshift(head);
    snake.pop();
}

// обновление
function update() {
    move();

    // съел фрукт
    for (let i = 0; i < fruits.length; i++) {
        if (snake[0].x === fruits[i].x && snake[0].y === fruits[i].y) {
            fruits.splice(i, 1);
            fruits.push(randPos());
            target = targetFruit();
            break;
        }
    }
}

// рисование
function drawCell(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * grid, y * grid, grid - 2, grid - 2);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let f of fruits) {
        drawCell(f.x, f.y, "lime");
    }

    snake.forEach((s, i) => {
        drawCell(s.x, s.y, i === 0 ? "red" : "white");
    });
}

function loop() {
    update();
    draw();
}

setInterval(loop, 120);