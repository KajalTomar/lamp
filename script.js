
// node.js module
var fs = require('fs');

// it's going to read this file completely before doing anything else
var todayResult = fs.readFileSync('streak.txt', 'utf8');
var totalStreak = fs.readFileSync('currentStreak.txt', 'utf8');

console.log(todayResult);

if(todayResult == 1)
{
	totalStreak++;
} 
else 
{
	totalStreak--;
	if(streak < 0)
	{
		streak = 0;
	}
}

console.log(totalStreak);
fs.writeFileSync("currentStreak.txt", totalStreak);
