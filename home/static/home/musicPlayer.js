var bar=document.getElementById('defaultbar');
		var aud=document.getElementById('audio1');
		function playPause(){
		if (aud.paused){
		   aud.play();
		   document.getElementById('play').innerHTML='Pause';}
		else{
		   aud.pause();
		   document.getElementById('play').innerHTML='Play';}

		var myVar=setInterval(durationInterval,1000);
		bar.addEventListener(click,clickedBar,false);
		
		}
		function durationInterval(){   
		f=getCurTime(aud.currentTime).toFixed(2);
		g=getCurTime(aud.duration).toFixed(2);
		w=document.getElementById('defaultbar').style.width;
		document.getElementById('dura').innerHTML= f + " " + "/" + " " + g;
		document.getElementById('pgb').style.width=f*650/g + 'px';
			}
	
		
		function getCurTime(a){
			
			if (a>58){
				c=a%60;
				d=a-c;
				b=d/60;
				return (b+c/100);
				}
			else
				return (a/100);
			
				
		}
		
		function fwdCurTime(){
		    aud.currentTime=aud.currentTime+5;
			durationInterval();
		    document.getElementById('aa').innerHTML=aud.currentTime;
		}
		
		function bwdCurTime(){
		    aud.currentTime=aud.currentTime-5;
			durationInterval();
		    document.getElementById('aa').innerHTML=aud.currentTime;
		}
		function oneVol(){
			aud.volume=0.1;
			document.getElementById('vol5').style.backgroundColor='black';
			document.getElementById('vol4').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol3').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol2').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol1').style.backgroundColor='rgba(204,0,0,1)';
		}
		function twoVol(){
			aud.volume=0.4;
			document.getElementById('vol5').style.backgroundColor='black';
			document.getElementById('vol4').style.backgroundColor='black';
			document.getElementById('vol3').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol2').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol1').style.backgroundColor='rgba(204,0,0,1)';
		}
		function threeVol(){
			aud.volume=0.6;
			document.getElementById('vol5').style.backgroundColor='black';
			document.getElementById('vol4').style.backgroundColor='black';
			document.getElementById('vol3').style.backgroundColor='black';
			document.getElementById('vol2').style.backgroundColor='rgba(204,0,0,1)';
			document.getElementById('vol1').style.backgroundColor='rgba(204,0,0,1)';
		}
		function fourVol(){
			aud.volume=0.8;
			document.getElementById('vol5').style.backgroundColor='black';
			document.getElementById('vol4').style.backgroundColor='black';
			document.getElementById('vol3').style.backgroundColor='black';
			document.getElementById('vol2').style.backgroundColor='black';
			document.getElementById('vol1').style.backgroundColor='rgba(204,0,0,1)';
		}
		function fiveVol(){
			aud.volume=1.0;
			document.getElementById('vol5').style.backgroundColor='black';
			document.getElementById('vol4').style.backgroundColor='black';
			document.getElementById('vol3').style.backgroundColor='black';
			document.getElementById('vol2').style.backgroundColor='black';
			document.getElementById('vol1').style.backgroundColor='black';
		}