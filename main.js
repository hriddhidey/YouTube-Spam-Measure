function checkSpam(){
	var url = document.getElementById('url').value;
	var output = document.getElementById('output');
	var v_id = url.substring(url.length-11,url.length);
	output.innerHTML=v_id;
}