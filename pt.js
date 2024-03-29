let ctx = document.getElementById('canv').getContext('2d');
let dot_x, dot_y, sec_x1, sec_x2, sec_y1, sec_y2; // координаты точки и концов отрезка соответственно
let x1, x2, x3, y1, y2, y3; // координаты векторов, построенных на сторонах треугольника
let out; // расстояние между точкой и отрезком
let hx, hy, ax, ay; // координаты тоски пересечения перпендикуляра с отрезком и 
let cnt = 0; // флаг, считающий номер нажатия на канвас

// функция обработки нажатия на канвас
function storeGuess(event) {
    // записываем координаты точки и рисуем ее
    if (cnt == 0) {
        dot_x = event.offsetX;
        dot_y = event.offsetY;
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.moveTo(dot_x, dot_y);
        ctx.lineTo(dot_x + 1, dot_y + 1);
        ctx.stroke();
    }
    // записываем координаты одного из концов отрезка и рисуем точку
    if (cnt == 1) {
        sec_x1 = event.offsetX;
        sec_y1 = event.offsetY;
        ctx.beginPath();
        ctx.moveTo(sec_x1, sec_y1);
        ctx.lineTo(sec_x1 + 1, sec_y1 + 1);
        ctx.stroke();
    }
    // записываем координаты другого конца отрезка; рисуем точку и отрезок
    if (cnt == 2) {
        sec_x2 = event.offsetX;
        sec_y2 = event.offsetY;

        ctx.beginPath();
        ctx.moveTo(sec_x2, sec_y2);
        ctx.lineTo(sec_x2 + 1, sec_y2 + 1);
        ctx.stroke();
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.moveTo(sec_x1, sec_y1);
        ctx.lineTo(sec_x2, sec_y2);
        ctx.stroke();
        det();
    }
    cnt++;
    cnt %= 3;

}


// функция, проверяющая: тупоугольный ли треугольник (с помощью скалярного произведения векторов)
function IN() {
    if ((dot_x - sec_x2) * (sec_x1 - sec_x2) + (dot_y - sec_y2) * (sec_y1 - sec_y2) <= 0) {
        // console.log (2);
        return 0;
    }
    else if ((dot_x - sec_x1) * (sec_x2 - sec_x1) + (dot_y - sec_y1) * (sec_y2 - sec_y1) <= 0) {
        // console.log (3);
        return 0;
    }
    else return 1;
}
IN();

// функция считающая модуль вектора по его координатам
function md(x, y) {
    return Math.sqrt(x * x + y * y);
}

// функция определения расстояния и отрисовки отрезка
function det() {
    x1 = sec_x1 - dot_x;
    y1 = sec_y1 - dot_y;
    x2 = sec_x2 - dot_x;
    y2 = sec_y2 - dot_y;
    x3 = sec_x2 - sec_x1;
    y3 = sec_y2 - sec_y1;
    if (IN(x1, x2, x3, y1, y2, y3)) {
        ax = sec_x2 - sec_x1;
        ay = sec_y2 - sec_y1;
        if (ax == 0) {
            hx = sec_x1;
            hy = dot_y;
        }
        else if (ay == 0) {
            hx = dot_x;
            hy = sec_y1;
        }
        else {
            hy = (ax * (sec_y1 * (ax / ay) - sec_x1 + dot_x) + ay * dot_y) / ((ax * ax / ay) + ay);
            hx = (hy - sec_y1) * (ax / ay) + sec_x1;
        }
        ctx.beginPath();
        ctx.strokeStyle = "red";
        ctx.moveTo(dot_x, dot_y);
        ctx.lineTo(hx, hy);
        ctx.stroke();
        let cs = (x1 * x2 + y1 * y2) / (md(x1, y1,) * md(x2, y2));
        let sn = Math.sqrt(1 - cs * cs);
        out = (sn * md(x1, y1,) * md(x2, y2)) / md(x3, y3);
    }

    else {
        out = Math.min(md(x1, y1), md(x2, y2));
        ctx.beginPath();
        ctx.strokeStyle = "red";
        ctx.moveTo(dot_x, dot_y);

        if (out == md(x1, y1)) {
            ctx.lineTo(sec_x1, sec_y1);
        }
        else {
            ctx.lineTo(sec_x2, sec_y2);
        }
        ctx.stroke();
    }
}