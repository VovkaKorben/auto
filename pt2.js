let ctx = document.getElementById('canv').getContext('2d')
let p[0], p[1], a[0], b[0], a[1], b[1] // координаты точки и концов отрезка соответственно
let x1, x2, x3, y1, y2, y3 // координаты векторов, построенных на сторонах треугольника
let out // расстояние между точкой и отрезком
let hx, hy, ax, ay // координаты тоски пересечения перпендикуляра с отрезком и 
let cnt = 0 // флаг, считающий номер нажатия на канвас

// функция обработки нажатия на канвас
function storeGuess(event) {
    // записываем координаты точки и рисуем ее
    if (cnt == 0) {
        p[0] = event.offsetX
        p[1] = event.offsetY
        ctx.beginPath()
        ctx.strokeStyle = "black"
        ctx.moveTo(p[0], p[1])
        ctx.lineTo(p[0] + 1, p[1] + 1)
        ctx.stroke()
    }
    // записываем координаты одного из концов отрезка и рисуем точку
    if (cnt == 1) {
        a[0] = event.offsetX
        a[1] = event.offsetY
        ctx.beginPath()
        ctx.moveTo(a[0], a[1])
        ctx.lineTo(a[0] + 1, a[1] + 1)
        ctx.stroke()
    }
    // записываем координаты другого конца отрезка рисуем точку и отрезок
    if (cnt == 2) {
        b[0] = event.offsetX
        b[1] = event.offsetY

        ctx.beginPath()
        ctx.moveTo(b[0], b[1])
        ctx.lineTo(b[0] + 1, b[1] + 1)
        ctx.stroke()
        ctx.beginPath()
        ctx.strokeStyle = "black"
        ctx.moveTo(a[0], a[1])
        ctx.lineTo(b[0], b[1])
        ctx.stroke()
        det()
    }
    cnt++
    cnt %= 3

}


// функция, проверяющая: тупоугольный ли треугольник (с помощью скалярного произведения векторов)
function IN() {
    if ((p[0] - b[0]) * (a[0] - b[0]) + (p[1] - b[1]) * (a[1] - b[1]) <= 0) {
        // console.log (2)
        return 0
    }
    else if ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1]) <= 0) {
        // console.log (3)
        return 0
    }
    else return 1
}
IN()

// функция считающая модуль вектора по его координатам
function md(x, y) {
    return Math.sqrt(x * x + y * y)
}

// функция определения расстояния и отрисовки отрезка
function det() {
    x1 = a[0] - p[0]
    y1 = a[1] - p[1]
    x2 = b[0] - p[0]
    y2 = b[1] - p[1]
    x3 = b[0] - a[0]
    y3 = b[1] - a[1]
    if (IN(x1, x2, x3, y1, y2, y3)) {
        ax = b[0] - a[0]
        ay = b[1] - a[1]
        if (ax == 0) {
            hx = a[0]
            hy = p[1]
        }
        else if (ay == 0) {
            hx = p[0]
            hy = a[1]
        }
        else {
            hy = (ax * (a[1] * (ax / ay) - a[0] + p[0]) + ay * p[1]) / ((ax * ax / ay) + ay)
            hx = (hy - a[1]) * (ax / ay) + a[0]
        }
        ctx.beginPath()
        ctx.strokeStyle = "red"
        ctx.moveTo(p[0], p[1])
        ctx.lineTo(hx, hy)
        ctx.stroke()
        let cs = (x1 * x2 + y1 * y2) / (md(x1, y1,) * md(x2, y2))
        let sn = Math.sqrt(1 - cs * cs)
        out = (sn * md(x1, y1,) * md(x2, y2)) / md(x3, y3)
    }

    else {
        out = Math.min(md(x1, y1), md(x2, y2))
        ctx.beginPath()
        ctx.strokeStyle = "red"
        ctx.moveTo(p[0], p[1])

        if (out == md(x1, y1)) {
            ctx.lineTo(a[0], a[1])
        }
        else {
            ctx.lineTo(b[0], b[1])
        }
        ctx.stroke()
    }
}