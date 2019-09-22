
var canvas = document.getElementById("myCanvas");
var canvas2 = document.getElementById("myCanvas2");
var ctx = canvas.getContext("2d");
var ctx2 = canvas2.getContext("2d");
var imgAnt = document.getElementById("ant");
var imgFood = document.getElementById("food");
var imgHome = document.getElementById("home");

class CanvasObject {
	constructor(x, y) {
		this.x = getRandomInt(80, 800);
		this.y = getRandomInt(80, 650);
	}

	giveCoordinates(){
		console.log("Object is at: " + 
			this.x + " " + this.y)
	}
}


class Ameise extends CanvasObject {
	constructor(x, y) {
		super(x, y);
		this.hasFood = false;
		this.age = getRandomInt(1000, 2000);
		this.alive = true;
	}

	move() {
		ctx2.clearRect(this.x, this.y, 20, 20); //cleaning

		var stepX = getRandomInt(-5, 5);
		var stepY = getRandomInt(-5, 5);

		this.x = this.x + stepX;
		this.y = this.y + stepY;

		ctx2.drawImage(imgAnt, this.x, this.y);
	}

	seek(food, home){
		ctx2.clearRect(this.x, this.y, 20, 20); //cleaning
		if (this.hasFood == false) {
			let foodDistanceX = food.x - this.x;
			let foodDistanceY = food.y - this.y;

			if (foodDistanceX > 0) this.x += getRandomInt(0, 10);
			if (foodDistanceY > 0) this.y += getRandomInt(0, 10);
			if (foodDistanceX < 0) this.x -= getRandomInt(0, 10);
			if (foodDistanceY < 0) this.y -= getRandomInt(0, 10);
		}

		if (this.hasFood == true) {
			let homeDistanceX = home.x - this.x;
			let homeDistanceY = home.y - this.y;

			if (homeDistanceX > 0) this.x += getRandomInt(0, 10);
			if (homeDistanceY > 0) this.y += getRandomInt(0, 10);
			if (homeDistanceX < 0) this.x -= getRandomInt(0, 10);
			if (homeDistanceY < 0) this.y -= getRandomInt(0, 10);
		}

		if (this.y < food.y + 2 && this.y > food.y - 2) {
			if (this.x < food.x + 2 && this.x > food.x - 2){
				this.hasFood = true;
				food.amount -= 1;
				food.shrink();
			}
		}

		if (this.y < home.y + 5 && this.y > home.y - 5) {
			if (this.x < home.x + 5 && this.x > home.x - 5){
				this.hasFood = false;
				home.amount += 1;
				home.showFoodAmount();
			}
		}
		this.move();
		this.age -= 1;
		if (this.age <= 0) {
			this.isDead();
		}
	}

	isDead(){
		this.alive = false;
		ctx2.clearRect(this.x, this.y, 30, 30);
	}
}


class Food extends CanvasObject {
	constructor(amount, x, y) {
		super(x, y);
		this.amount = amount;
		this.currentWidth = imgFood.clientWidth;
		this.currentHeight = imgFood.clientHeight;
		ctx.drawImage(imgFood, this.x, this.y);
	}

	shrink() {
		ctx.clearRect(this.x, this.y, this.currentWidth, this.currentHeight)
		this.currentWidth -= 1;
		this.currentHeight -= 1;
		ctx.drawImage(imgFood, this.x, this.y, this.currentWidth, this.currentHeight);
	}
}


class Home extends CanvasObject {
	constructor(x, y) {
		super(x, y);
		this.amount = 0;
		ctx.drawImage(imgHome, this.x-40, this.y-40);
		ctx.font = "20px Arial";
 		ctx.fillText("Food collected: ", 20, 690);
	}

	showFoodAmount() {
		ctx.clearRect(165, 690, 25, -25)
 		ctx.fillText(home.amount, 165, 690);
	}
}


let ameisenAmount = 10;
let ameisen = [];

let foodAmount = 10
let food = new Food(foodAmount);
let home = new Home();

for (var i = 0; i < ameisenAmount; i++) {
	ameisen[i] = new Ameise();
	console.log("Ameise " + i + " lebt.")
}

console.log(ameisen.length)

async function update() {
	ctx.drawImage(imgHome, home.x-40, home.y-40);
	for (var i = 0; i < ameisen.length; i++) {
			if (ameisen[i].alive == true){
				ameisen[i].seek(food, home);
			}
	}
	ameisen = ameisen.filter(function(value, index, arr){
		return value.alive == true;
	});
	if (food.amount <= 0) {
		ctx.clearRect(food.x, food.y, 40, 40);
		food = new Food(foodAmount);
	}
	await sleep(100);
	update();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

