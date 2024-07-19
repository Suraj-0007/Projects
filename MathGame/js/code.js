var playing = false;
var action;
var timeremaining;
var correctAnswer;
// for start and reset button
document.getElementById('startreset').onclick=function(){
    if(playing ==true)
    {
        location.reload();//reload page
    }
    else{
        playing = true;//change mode
        score = 0;//set score
        document.getElementById('scorevalue').innerHTML=score;
        //to show countdown box
        show('timeremaining');
        timeremaining = 60;
        document.getElementById('trvalue').innerHTML = timeremaining;
        //hide game over box
        hide('gameover');
        //to change the button to reset game
        document.getElementById('startreset').innerHTML = "Reset Game";
        //shoe countdown box
        showcountdown();
        //to generate a new question and answer.
        generateQA();
    }
}

//if click on answer
for(i=1;i<5;i++)
{
    document.getElementById('box'+i).onclick = function(){
        //if we are playing
        if (playing==true)//yes
        {
            if(this.innerHTML == correctAnswer)
            {
                score++;
                document.getElementById('scorevalue').innerHTML = score;
                //show correct box and hide wrong box
                hide('wrong');
                show('correct');
                setTimeout(function(){
                    hide('correct');
                }, 1000);
                //generate new question answer
                generateQA();
            }
            else{
                hide('correct');
                show('wrong');
                setTimeout(function(){
                    hide('wrong');
                }, 1000);
            }
        }
    }
}


function showcountdown()
{
    action = setInterval(function(){
        timeremaining--;
        document.getElementById('trvalue').innerHTML = timeremaining;
        if(timeremaining==0){
            stopcountdown();//game over
            show('gameover');
            document.getElementById('gameover').innerHTML = "<p>Game Over</p><p>Your Score is "+ score + ". </p>";
            hide('timeremaining');
            hide('correct');
            hide('wrong');
            playing = false;
            document.getElementById('startreset').innerHTML = "Start Game";
        }
    },1000);
}
function stopcountdown()
{
    clearInterval(action);
}
function hide(id)
{
    document.getElementById(id).style.display="none";
}
function show(id)
{
    document.getElementById(id).style.display="block";
}


function generateQA()
{
    var x = 1+Math.round(9*Math.random());
    var y = 1+Math.round(9*Math.random());
    correctAnswer = x*y;
    document.getElementById('question').innerHTML = x + "x" + y;
    var correctPosition = 1+Math.round(3*Math.random());
    //fill correct box
    document.getElementById('box'+correctPosition).innerHTML = correctAnswer;
    //fill the wrong box
    var answers = [correctAnswer];
    for(i=1;i<5;i++){
        if(i!=correctPosition){
            var wrongAnswer;
            do
            {
                wrongAnswer = (1+Math.round(9*Math.random())) * (1+Math.round(9*Math.random()));
            }
            while(answers.indexOf(wrongAnswer)>-1)
            answers.push(wrongAnswer);
            document.getElementById('box'+i).innerHTML = wrongAnswer;
        }
    }
}
