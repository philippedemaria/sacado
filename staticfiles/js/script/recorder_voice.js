


		//webkitURL is deprecated but nevertheless
		URL = window.URL || window.webkitURL;

		var gumStream; 						//stream from getUserMedia()
		var rec; 							//Recorder.js object
		var input; 							//MediaStreamAudioSourceNode we'll be recording

		// shim for AudioContext when it's not avb. 
		var AudioContext = window.AudioContext || window.webkitAudioContext;
		var audioContext //audio context to help us record

		var recordButton = document.getElementById("recordButton");
		var stopButton = document.getElementById("stopButton");
		var pauseButton = document.getElementById("pauseButton");

		 
		recordButton.addEventListener("click", startRecording);
		stopButton.addEventListener("click", stopRecording);
		pauseButton.addEventListener("click", pauseRecording);  

		function startRecording() {

			console.log("recordButton clicked");

			/*
				Simple constraints object, for more advanced audio features see
				https://addpipe.com/blog/audio-constraints-getusermedia/
			*/
		    
		    var constraints = { audio: true, video:false }

		 	/*
		    	Disable the record button until we get a success or fail from getUserMedia() 
			*/
			recordButton.disabled = true;
			stopButton.disabled = false;
			pauseButton.disabled = false

			/*
		    	We're using the standard promise based getUserMedia() 
		    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
			*/

			navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
				console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

				/*
					create an audio context after getUserMedia is called
					sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
					the sampleRate defaults to the one set in your OS for your playback device

				*/
				audioContext = new AudioContext();

				//update the format 
				document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

				/*  assign to gumStream for later use  */
				gumStream = stream;
				
				/* use the stream */
				input = audioContext.createMediaStreamSource(stream);

				/* 
					Create the Recorder object and configure to record mono sound (1 channel)
					Recording 2 channels  will double the file size
				*/ 
				rec = new Recorder(input,{numChannels:1})
		 
				//start the recording process
				rec.record()

				console.log("Recording started");

			}).catch(function(err) {

		    	 console.log( err);
			  	//enable the record button if getUserMedia() fails
		    	recordButton.disabled = false;
		    	stopButton.disabled = true;
		    	pauseButton.disabled = true;
			});
		}

		function pauseRecording(){
			console.log("pauseButton clicked rec.recording=",rec.recording );
			if (rec.recording){
				//pause
				rec.stop();
				pauseButton.innerHTML="Resume";
			}else{
				//resume
				rec.record()
				pauseButton.innerHTML="Pause";

			}
		}

		function stopRecording() {
			console.log("stopButton clicked");

			//disable the stop button, enable the record too allow for new recordings
			stopButton.disabled = true;
			recordButton.disabled = false;
			pauseButton.disabled = true;

			//reset button just in case the recording is stopped while paused
			pauseButton.innerHTML="Pause";
			
			//tell the recorder to stop the recording
			rec.stop();

			//stop microphone access
			gumStream.getAudioTracks()[0].stop();

			//create the wav blob and pass it on to createDownloadLink
			rec.exportWAV(createDownloadLink);
		}

		function createDownloadLink(blob) {
			
			var url = URL.createObjectURL(blob);
			var au = document.createElement('audio');
			var li = document.createElement('li');
			var link = document.createElement('a');

			//name of .wav file to use during upload and download (without extendion)
			var filename = new Date().getTime();

			//add controls to the <audio> element
			au.controls = true;
			au.src = url;

			//save to disk link
			link.href = url;
			link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
			link.innerHTML = "<br>";

			//add the new audio element to li
			li.appendChild(au);
			
			//add the filename to the li
			li.appendChild(document.createTextNode(filename+".wav "))

			//add the save to disk link to li
			li.appendChild(link);
			
			//upload link
			var upload = document.createElement('a');
			upload.href="#";
			upload.innerHTML = "<span class='btn btn-primary' data-dismiss='modal'>Téléverser ce commentaire</span>";
			upload.addEventListener("click", function(event){
				var xhr=new XMLHttpRequest();
				var fd=new FormData();

 

				if ( document.getElementById('custom') )
					{ 
						custom = document.getElementById('custom').value ;

						var id_student = document.getElementById('id_student').value ;
						var id_parcours = document.getElementById('id_parcours').value ;
						var id_relationship = document.getElementById('id_relationship').value ;						

						if (custom) {

							fd.append("custom",custom);						
							fd.append("id_parcours",id_parcours);
							fd.append("id_relationship",id_relationship);
							fd.append("id_student",id_student);
						}
						else 
						{
							fd.append("custom",custom);						
							fd.append("id_relationship",id_relationship);
							fd.append("id_student",id_student);
						}
						fd.append("id_mediation",blob, link.download);
						var url = "../../../ajax_audio_comment_all_exercise";


					}
				else 
					{  

						var id_title = document.getElementById('id_title').value ;
						var id_duration = document.getElementById('id_duration').value ;
						var id_relationship = document.getElementById('id_relationship').value ;
						var is_custom = document.getElementById('is_custom').value ;
						var id_parcours = document.getElementById('id_parcours').value ;

						document.getElementById('id_mediation').remove() ; 

						fd.append("id_title",id_title);
						fd.append("id_duration",id_duration);
						fd.append("id_audio",true);
						fd.append("id_video","");
						fd.append("id_mediation",blob, link.download);	
						fd.append("id_consigne",id_consigne);
						fd.append("id_relationship",id_relationship);
						fd.append("is_custom",is_custom);
						fd.append("id_parcours",id_parcours);

						var url = "../../audio_remediation";
					}
			  	xhr.onload = function() {
					   document.getElementById('response').innerHTML = "Votre commentaire audio est enregistré.";
					   document.getElementById('response_div').style.display = "block";
					   setTimeout(function() { document.getElementById('response').style.display = "none"; }, 3000);

					};
				xhr.open("POST",url);
				xhr.send(fd);
			})
			li.appendChild(document.createTextNode (" "))//add a space in between
			li.appendChild(upload)//add the upload link to li

			//add the li element to the ol
			recordingsList.appendChild(li);
		}


