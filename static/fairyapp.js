const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");
const colors = document.getElementsByClassName("jsColor");
// const range = document.getElementById("jsRange");
const mode = document.getElementById("jsMode");
const mode2 = document.getElementById("jsMode2");
const saveBtn = document.getElementById("jsSave");
const saveBtn2 = document.getElementById("jsSave2");


ctx.strokeStyle = "#000000";
// ctx.lineWidth = 6.0; /* 라인 굵기 */
ctx.lineWidth = 10;

canvas.width = 800;
canvas.height = 350;

CANVAS_SIZEW =800;
CANVAS_SIZEH =350;

ctx.fillStyle = "#FFFFFF";
ctx.globalAlpha = "0.8"; 
ctx.fillRect(0,0,CANVAS_SIZEW,CANVAS_SIZEH);

let painting = false;
let filling = false;

function stopPainting() {
    painting = false;
}

function startPainting() {
    painting = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (!painting) {
        ctx.beginPath();
        ctx.moveTo(x, y);
    } else{
        ctx.lineTo(x, y);
        ctx.stroke();
    }
}

if (canvas) {
    canvas.addEventListener("mousemove", onMouseMove);
    canvas.addEventListener("mousedown", startPainting);
    canvas.addEventListener("mouseup", stopPainting);
    canvas.addEventListener("mouseleave", stopPainting);
}

function handleSaveClick(){
    const image = canvas.toDataURL("image/jpg");
    const link = document.createElement("a");
    link.href = image;
    link.download = "Paint.jpg";
    link.click();
}

function removeall(){
    ctx.clearRect(0, 0,CANVAS_SIZEW,CANVAS_SIZEH)
    ctx.fillStyle = "#FFFFFF";
    ctx.globalAlpha = "0.8"; 
    ctx.fillRect(0,0,CANVAS_SIZEW,CANVAS_SIZEH);
}
if (mode) {
    mode.addEventListener("click",removeall)
}
if(mode2){
    mode2.addEventListener("click",removeall)
}
if(saveBtn){
    saveBtn.addEventListener("click",handleSaveClick)
}
if(saveBtn2){
    saveBtn2.addEventListener("click",handleSaveClick)
}

